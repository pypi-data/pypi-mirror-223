#!/usr/bin/python3
""" 翻译 """
import json
import sys
import re
from datetime import datetime
from pathlib import Path

import requests
import requests.utils

_save_d = dict()


def main():
    argv_len = len(sys.argv)
    if argv_len < 2:
        print("必须传输要翻译的单词")
        return

    get_mongo_db_connect()

    if argv_len == 2:
        kw = sys.argv[1]
        translate_sug(kw)
    elif argv_len == 3 and sys.argv[1] == 'v2':
        kw = sys.argv[2]
        translate_v2transapi(kw)

    close_mongo_db_connect()


def translate_sug(kw: str):
    query_result = query_kw_from_mongodb(kw, 'baidu sug')

    if query_result is None:
        baidu_fanyi_url = "https://fanyi.baidu.com/sug"
        session = requests.session()
        session.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1788.0"
        }

        param_d = {
            "kw": kw
        }

        result = session.post(url=baidu_fanyi_url, params=param_d)
        result_d = result.json()
    else:
        result_d = query_result['translate']

    if result_d['errno'] != 0:
        result_format = json.dumps(result_d, ensure_ascii=False, indent=2)
        print(result_format)
        return
    else:
        # 成功查询
        data: list = result_d['data']
        for kv in data:
            k = kv['k']
            v = kv['v']
            import colorama
            print(f"{colorama.Fore.GREEN}{k}{colorama.Fore.RESET}\t{v}")
            # print(f"\033[0;40;32m{k}\033[0m\t{v}")
        if query_result is None:
            save_query_result_to_mongodb(kw, 'baidu sug', result_d)


def translate_v2transapi(kw: str):
    v2 = BaiduFanYiV2Translate()
    result = v2.translate(kw)
    result_d = result.json()
    if result.status_code == 200:
        if 'errno' in result_d and result_d['errno'] != 0:
            result_format = json.dumps(result_d, ensure_ascii=False, indent=2)
            print(result_format)
            return
        else:
            # 成功查询
            result_format = json.dumps(result_d, ensure_ascii=False, indent=2)
            print(result_format)
            save_query_result_to_mongodb(kw, 'baidu v2transapi', result_d)
    else:
        print("翻译失败", file=sys.stderr)
        return


def query_kw_from_mongodb(kw: str, translator: str):
    try:
        mongodb_client = get_mongo_db_connect()
        logdb = mongodb_client['logdb']
        fy_coll = logdb['fy_coll']
        return fy_coll.find_one({"kw": kw, 'translator': translator})
    except Exception as e:
        print('*' * 30)
        print(f"mongodb query error: {e}", file=sys.stderr)


def save_query_result_to_mongodb(kw: str, translator: str, query_result: dict):
    try:
        mongodb_client = get_mongo_db_connect()
        logdb = mongodb_client['logdb']
        fy_coll = logdb['fy_coll']

        fy_find_one_result = fy_coll.find_one(
            {"kw": kw, 'translator': translator})
        if fy_find_one_result is not None:
            return

        mongo_doc = {
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),
            "kw": kw,
            "translator": translator,
            "translate": query_result
        }
        fy_coll.insert_one(mongo_doc)
    except Exception as e:
        print('*' * 30)
        print(f"mongodb save error: {e}", file=sys.stderr)


class BaiduFanYiV2Translate:
    def __init__(self):
        self.v2transapi_url = "https://fanyi.baidu.com/v2transapi"
        self._mongodb_client = get_mongo_db_connect()
        self._variable_db = self._mongodb_client['runtime-variable']
        self._cookies_coll = self._variable_db['cookies']
        self.session = requests.Session()
        # 初始化Javascript脚本执行上下文环境
        import js2py
        self.context = js2py.EvalJs()
        self._init_session()

    def _init_session(self):
        cookies_entity_d = self._cookies_coll.find_one(
            {"url": self.v2transapi_url})
        if True or cookies_entity_d is None or datetime.now().timestamp() - cookies_entity_d['timestamp'] > 60 * 60 * 6:
            # 已过期，重新获取gtk token cookies
            self._init_token_and_cookies()

            save_cookies_entity_d = {
                'url': self.v2transapi_url,
                'gtk': self.gtk,
                'token': self.token,
                'cookies': requests.utils.dict_from_cookiejar(self.session.cookies),
                'timestamp': datetime.now().timestamp()
            }
            if cookies_entity_d is None:
                self._cookies_coll.insert_one(save_cookies_entity_d)
            else:
                self._cookies_coll.update_one({'url': save_cookies_entity_d['url']}, {
                                              '$set': save_cookies_entity_d})
        else:
            # 未过期，使用保存的gtk token cookies
            self.gtk = cookies_entity_d['gtk']
            self.token = cookies_entity_d['token']
            self.session.cookies = requests.utils.cookiejar_from_dict(
                cookies_entity_d['cookies'])
            self.session.headers = {
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "Accept": "*/*",
                "Host": "fanyi.baidu.com",
                "Accept-Language": "zh-CN,zh;q=0.9",
                "Accept-Encoding": "gzip, deflate",
                "Origin": "https://fanyi.baidu.com",
                "Referer": "https://fanyi.baidu.com/",
                "Connection": "keep-alive",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
                "X-Requested-With": "XMLHttpRequest"
            }

    def _init_token_and_cookies(self):
        self.session.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Upgrade-Insecure-Requests": "1",
            "Host": "fanyi.baidu.com",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            "Accept-Language": "zh-cn",
            "Accept-Encoding": "gzip, deflate"
        }
        # 加载主页
        response = self.session.get("https://fanyi.baidu.com/")
        # 获取token
        token = re.findall("token: ('.*'),", response.text)[0]
        self.token = token[1:-1]
        # 获取gtk
        # 获取window.gtk的值。
        self.gtk = re.findall(';window.gtk = (".*?");', response.text)[0]

    def sign(self, word):
        # 从浏览器拷贝的签名生成函数脚本（r-raw表示原生字符串）
        js = r'''
        function a(r) {
            if (Array.isArray(r)) {
              for (var o = 0, t = Array(r.length); o < r.length; o++)
                t[o] = r[o];
              return t
            }
            return Array.from(r)
          }
          function n(r, o) {
            for (var t = 0; t < o.length - 2; t += 3) {
              var a = o.charAt(t + 2);
              a = a >= "a" ? a.charCodeAt(0) - 87 : Number(a),
                a = "+" === o.charAt(t + 1) ? r >>> a : r << a,
                r = "+" === o.charAt(t) ? r + a & 4294967295 : r ^ a
            }
            return r
          }
          function e(r) {
            var o = r.match(/[\uD800-\uDBFF][\uDC00-\uDFFF]/g);
            if (null === o) {
              var t = r.length;
              t > 30 && (r = "" + r.substr(0, 10) + r.substr(Math.floor(t / 2) - 5, 10) + r.substr(-10, 10))
            } else {
              for (var e = r.split(/[\uD800-\uDBFF][\uDC00-\uDFFF]/), C = 0, h = e.length, f = []; h > C; C++)
                "" !== e[C] && f.push.apply(f, a(e[C].split(""))),
                C !== h - 1 && f.push(o[C]);
              var g = f.length;
              g > 30 && (r = f.slice(0, 10).join("") + f.slice(Math.floor(g / 2) - 5, Math.floor(g / 2) + 5).join("") + f.slice(-10).join(""))
            }
            var u = void 0
              , l = "" + String.fromCharCode(103) + String.fromCharCode(116) + String.fromCharCode(107);
            u ='null !== i ? i : (i = window[l] || "") || ""';
            for (var d = u.split("."), m = Number(d[0]) || 0, s = Number(d[1]) || 0, S = [], c = 0, v = 0; v < r.length; v++) {
              var A = r.charCodeAt(v);
              128 > A ? S[c++] = A : (2048 > A ? S[c++] = A >> 6 | 192 : (55296 === (64512 & A) && v + 1 < r.length && 56320 === (64512 & r.charCodeAt(v + 1)) ? (A = 65536 + ((1023 & A) << 10) + (1023 & r.charCodeAt(++v)),
                S[c++] = A >> 18 | 240,
                S[c++] = A >> 12 & 63 | 128) : S[c++] = A >> 12 | 224,
                S[c++] = A >> 6 & 63 | 128),
                S[c++] = 63 & A | 128)
            }
            for (var p = m, F = "" + String.fromCharCode(43) + String.fromCharCode(45) + String.fromCharCode(97) + ("" + String.fromCharCode(94) + String.fromCharCode(43) + String.fromCharCode(54)), D = "" + String.fromCharCode(43) + String.fromCharCode(45) + String.fromCharCode(51) + ("" + String.fromCharCode(94) + String.fromCharCode(43) + String.fromCharCode(98)) + ("" + String.fromCharCode(43) + String.fromCharCode(45) + String.fromCharCode(102)), b = 0; b < S.length; b++)
              p += S[b],
                p = n(p, F);
            return p = n(p, D),
              p ^= s,
            0 > p && (p = (2147483647 & p) + 2147483648),
              p %= 1e6,
            p.toString() + "." + (p ^ m)
          }
        '''
        # 在javascript脚本中把u的值替换成window.gtk
        js = js.replace(
            '\'null !== i ? i : (i = window[l] || "") || ""\'', self.gtk)
        # 执行js
        self.context.execute(js)
        # 调用函数得到sign
        return self.context.e(word)

    def translate(self, word):
        # 构造请求数据
        data = {
            'from': 'en',
            'to': 'zh',
            'query': word,
            'transtype': 'realtime',
            'simple_means_flag': 3,
            'sign': self.sign(word),
            'token': self.token
        }
        response = self.session.post(self.v2transapi_url, data=data)
        return response


def get_mongo_db_connect():
    k = 'mongodb_connection'
    connection = _save_d.get(k, None)
    if connection is None:
        import pymongo
        connection = pymongo.MongoClient("mongodb://localhost:27017/")
        _save_d[k] = connection
    return connection


def close_mongo_db_connect():
    k = 'mongodb_connection'
    connection = _save_d.get(k, None)
    if connection is not None:
        _save_d[k] = None
        connection.close()


if __name__ == '__main__':
    print("he")
    main()

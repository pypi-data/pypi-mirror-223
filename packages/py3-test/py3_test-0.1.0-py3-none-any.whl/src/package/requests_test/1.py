"""
@Time   : 2019/3/27
@author : lijc210@163.com
@Desc:  : 功能描述。
"""
import json

import requests

with open("baidu_cookie.json") as f:
    cookies = json.loads(f.read())

cookie = [item["name"] + "=" + item["value"] for item in cookies]
COOKIE = "; ".join(item for item in cookie)
print(COOKIE)

headers = {
    "Cookie": COOKIE,
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
    "Referer": "https://www2.baidu.com",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}
url = """https://caiwu.baidu.com/fp-mgr/payment/user_page?relate=1&uid=5380819&castk=cdd44fy747a4020bbd578"""

r = requests.get(url, headers=headers)

print(r.status_code)
print(r.text)

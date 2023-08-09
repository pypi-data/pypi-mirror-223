"""
@author: lijc210@163.com
@file: process_url_path.py
@time: 2019/11/27
@desc: 功能描述。
"""
import urllib.parse

import requests

session = requests.Session()
host = "10.10.11.2:8082"
host = "127.0.0.1:8082"
# host = "bi-go.api.tg.local"

r = session.post(
    "http://{}/api/auth/".format(host),
    json={"email": "chenxianren@qeeka.com", "password": "@chenxianren12#"},
    headers={"Content-Type": "application/json"},
)

print(r.text)

print(session.get("http://{}/api/ad/kind/d/".format(host)).text)

a_ly_quote = urllib.parse.quote("短信", safe="/", encoding=None, errors=None)
a_lx_quote = urllib.parse.quote("内部数据", safe="/", encoding=None, errors=None)
data = "url=http://m.jia.com&site=JIA&kind=a&a_ly={a_ly}&a_lx={a_lx}".format(
    a_ly=a_ly_quote, a_lx=a_lx_quote
)

r = session.post(
    "http://{}/api/ad/".format(host),
    json={
        "url": "http://m.jia.com",
        "site": "JIA",
        "kind": "a",
        "a_ly": "短信",
        "a_lx": "内部数据",
    },
    headers={"Content-Type": "application/json"},
)
print(r.text)

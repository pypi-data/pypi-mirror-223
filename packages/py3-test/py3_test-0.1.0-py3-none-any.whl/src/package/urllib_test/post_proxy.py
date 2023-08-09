"""
@author: lijc210@163.com
@file: post.py
@time: 2019/10/08
@desc: 功能描述。
"""
import socket
from urllib.request import ProxyHandler, build_opener, Request, urlopen

if socket.gethostname() == "SHBGDZ05373":
    http, https = "http://172.17.15.93:7890", "http://172.17.15.93:7890"
else:
    http, https = "http://127.0.0.1:7890", "http://127.0.0.1:7890"

proxies = {"http": http, "https": https}

proxy_handler = ProxyHandler(proxies)

opener = build_opener(proxy_handler)
request = Request("https://www.google.com/")
r = opener.open(request, timeout=2)

print(r.code)
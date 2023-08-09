"""
@author: lijc210@163.com
@file: speed_test.py
@time: 2019/10/08
@desc: 功能描述。
"""
import timeit
import urllib.request

import requests

r1 = requests.get("https://www.baidu.com")
print(r1.text)

stmt1 = """requests.get("https://www.baidu.com")"""
print(timeit.timeit(stmt=stmt1, setup="import requests;", number=30))

r2 = urllib.request.urlopen("https://www.baidu.com")
print(r2.read())
stmt2 = """urllib.request.urlopen('https://www.baidu.com')"""
print(timeit.timeit(stmt=stmt2, setup="import urllib.request;", number=30))

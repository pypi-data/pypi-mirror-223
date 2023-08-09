"""
@author: lijc210@163.com
@file: url_process.py
@time: 2019/11/29
@desc: 功能描述。
"""
import urllib.parse

a = urllib.parse.quote("测试", safe="/", encoding=None, errors=None)
print(a)
b = urllib.parse.unquote(a, encoding="utf-8", errors="replace")
print(b)

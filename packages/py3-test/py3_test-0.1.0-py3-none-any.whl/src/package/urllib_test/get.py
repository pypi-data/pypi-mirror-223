"""
@author: lijc210@163.com
@file: get.py
@time: 2019/10/08
@desc: 功能描述。
"""
import urllib.request

rqs = urllib.request.urlopen("http://www.baidu.com")

html = rqs.read()

print(html)

"""
@author: lijc210@163.com
@file: wangke_sousuo.py
@time: 2019/12/01
@desc:
谷歌多站点搜索配置：
https://cse.google.com/cse/setup/basic?cx=018439907757911276332%3Aolvls7osv3v
公开搜索测试网址：
https://cse.google.com/cse?cx=018439907757911276332:olvls7osv3v
开发文档：
https://developers.google.com/custom-search/v1/cse/list
"""
import requests

cx = "018439907757911276332:olvls7osv3v"
key = "AIzaSyAmHwrm4BELiQ3yGGRMkJfj96QfWQ6HBqc"
q = "python教程"
start = 1
url = "https://www.googleapis.com/customsearch/v1?cx={cx}&key={key}&q={q}&start={start}".format(
    cx=cx, key=key, q=q, start=start
)

r = requests.get(url, timeout=5)

print(r.text)

"""
@author: lijc210@163.com
@file: groupby_test.py
@time: 2020/03/04
@desc: 功能描述。
"""
from itertools import groupby
from operator import itemgetter

alist = [
    {"type": "a", "data": "1"},
    {"type": "b", "data": "3"},
    {"type": "a", "data": "2"},
    {"type": "b", "data": "4"},
]

alist.sort(key=itemgetter("type"))
for _type, items in groupby(alist, key=itemgetter("type")):
    print(_type)
    for i in items:
        print(i)

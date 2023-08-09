"""
@author: lijc210@163.com
@file: sorted_test.py
@time: 2020/03/04
@desc: 功能描述。
"""

alist = [{"a": 1, "b": 3}, {"a": 2, "b": 1}, {"a": 2}]

a = sorted(alist, key=lambda asd: asd.get("b", 0), reverse=True)

for x in a:
    print(x)

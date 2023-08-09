"""
@author: lijc210@163.com
@file: 7.py
@time: 2020/06/22
@desc: 功能描述。
"""
l1 = [2, 2, 1, 1, 1, 2, 2]


def find_element(l1):
    adict = {}
    for x in l1:
        num = adict.get(x, 0)
        adict[x] = num + 1
    count = len(l1) / 2
    for k, v in adict.items():
        if v > count:
            return k
    return None


print(find_element(l1))

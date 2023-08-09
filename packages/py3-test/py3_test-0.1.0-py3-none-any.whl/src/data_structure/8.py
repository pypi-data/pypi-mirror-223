"""
@author: lijc210@163.com
@file: 7.py
@time: 2020/06/22
@desc: 功能描述。
"""
s1 = "leetcode"
s2 = "loveleetcode"


def first_uniq_char(s):
    adict = {}
    for x in s:
        num = adict.get(x, 0)
        adict[x] = num + 1
    for i, y in enumerate(s):
        num = adict.get(y, 0)
        if num == 1:
            return i


print(first_uniq_char(s1))
print(first_uniq_char(s2))

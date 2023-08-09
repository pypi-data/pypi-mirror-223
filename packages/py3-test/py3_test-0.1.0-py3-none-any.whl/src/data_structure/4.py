"""
@author: lijc210@163.com
@file: 3.py
@time: 2020/06/21
@desc: 功能描述。
"""
list1 = [2, 7, 11, 15]


def two_sum(list1, target):
    for i, num1 in enumerate(list1):
        for j, num2 in enumerate(list1):
            if i == j:
                continue
            if num1 + num2 == target:
                return [i, j]
    return []


print(two_sum(list1, 9))

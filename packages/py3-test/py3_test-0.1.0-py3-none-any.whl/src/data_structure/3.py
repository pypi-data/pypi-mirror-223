"""
@author: lijc210@163.com
@file: 3.py
@time: 2020/06/21
@desc: 功能描述。
"""
list1 = [3, 4, 7, 9, 11]
list2 = [1, 2, 5, 8, 13, 20]


def mergeTwoLists(list1, list2):
    result = []
    while list1 and list2:
        if list1[0] < list2[0]:
            result.append(list1[0])
            list1.pop(0)
        else:
            result.append(list2[0])
            list2.pop(0)
    if list1:
        result.extend(list1)
    if list2:
        result.extend(list2)
    return result


print(mergeTwoLists(list1, list2))

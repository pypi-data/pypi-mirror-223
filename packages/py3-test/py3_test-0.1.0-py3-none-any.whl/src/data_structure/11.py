"""
@author: lijc210@163.com
@file: 7.py
@time: 2020/06/22
@desc: 功能描述。
"""

alist = [1, 2, 3, 4, 5, 6, 7]


def find_element(alist, target):
    low, hight = 0, len(alist) - 1
    while low <= hight:
        mid = low + (hight - low) // 2
        print("aaaaaaa", mid)
        if alist[mid] > target:
            hight = mid - 1
        elif alist[mid] < target:
            low = mid + 1
        else:
            return mid
    return -1


print(find_element(alist, 2))

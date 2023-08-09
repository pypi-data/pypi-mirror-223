"""
@Time   : 2019/5/30
@author : lijc210@163.com
@Desc:  : 功能描述。
"""

import multiprocessing
from multiprocessing import Array

num = Array("i", [1, 2, 3, 4, 5])  # 主进程与子进程共享这个数组
print(num[:])


def func(num):
    num[2] = 9999  # 子进程改变数组，主进程跟着改变


if __name__ == "__main__":
    p = multiprocessing.Process(target=func, args=(num,))
    p.start()
    p.join()

    print(num[:])

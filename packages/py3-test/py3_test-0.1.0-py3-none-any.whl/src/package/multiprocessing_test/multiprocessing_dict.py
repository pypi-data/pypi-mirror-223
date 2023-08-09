"""
@Time   : 2019/5/30
@author : lijc210@163.com
@Desc:  : 功能描述。
"""

import multiprocessing
from multiprocessing import freeze_support


def func(mydict):
    mydict["c"] = "d"


if __name__ == "__main__":
    freeze_support()
    mydict = multiprocessing.Manager().dict()  # 主进程与子进程共享这个字典
    mydict["a"] = "b"
    p = multiprocessing.Process(target=func, args=(mydict,))
    p.start()
    p.join()

    print(mydict)

"""
Created on 2017/6/8 0008
@author: lijc210@163.com
Desc: 多进程,顺序保留
"""
import os
import time
from multiprocessing import Pool

alist = list(range(5))


def get(x):
    time.sleep(1)
    print(x, os.getpid())
    return x


if __name__ == "__main__":
    pool = Pool(3)
    res = [pool.apply_async(get, "a")]
    thread_res_list = [r.get() for r in res]
    x = thread_res_list[0]
    print(x)

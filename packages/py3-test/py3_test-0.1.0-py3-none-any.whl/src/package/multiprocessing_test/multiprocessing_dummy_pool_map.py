"""
Created on 2017/6/8 0008
@author: lijc210@163.com
Desc: 多进程,linux可运行。结果保留顺序，只支持一个参数
"""
import time
from multiprocessing.dummy import Pool as ThreadPool

alist = [1, 2, 3, 4, 5, 6, 7, 8]


def get(x):
    time.sleep(1)
    print(x)
    return x


pool = ThreadPool(6)
res = pool.map(get, alist)
print(res)
pool.close()
pool.join()
print("bbbbb")

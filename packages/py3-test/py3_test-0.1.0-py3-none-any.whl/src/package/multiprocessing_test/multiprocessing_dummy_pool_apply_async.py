"""
Created on 2017/6/8 0008
@author: lijc210@163.com
Desc: 多进程,linux可运行，随机执行，返回结果顺序保持
"""
import os
import threading
import time
from multiprocessing.dummy import Pool as ThreadPool

alist = [(1, 2), (3, 4), (5, 6), (7, 8)]


# adict = {"a":"b","c":"d"}
def get2(x, y):
    time.sleep(2)
    print((x, y), os.getpid(), threading.currentThread().name)
    return x, y


pool = ThreadPool(6)
res = [pool.apply_async(get2, args) for args in alist]
pool.close()
pool.join()
for r in res:
    print(r.get(), "bbbbbbbbb", os.getpid(), threading.currentThread().name)
print("bbbbb")

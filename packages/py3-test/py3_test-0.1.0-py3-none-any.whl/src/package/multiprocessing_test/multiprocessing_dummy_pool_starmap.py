"""
Created on 2017/6/8 0008
@author: lijc210@163.com
Desc: 多进程,linux可运行。随机执行（阻塞），顺序保留，支持多个参数
"""
import time
from multiprocessing.dummy import Pool as ThreadPool

# alist = [(1,2),(3,4),(5,6),(7,8)]
alist = [(1, 2), (3, 4), (5, 6), (7, 8)]
adict = {"a": "b", "c": "d"}


def get2(x, y):
    time.sleep(2)
    print((x, y))
    return x, y


pool = ThreadPool(6)
res1 = pool.starmap(get2, alist)
print(res1)
pool.close()
pool.join()
print("bbbbb")

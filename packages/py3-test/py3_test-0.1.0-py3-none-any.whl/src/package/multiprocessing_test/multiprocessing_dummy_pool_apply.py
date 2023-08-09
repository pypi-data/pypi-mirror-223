"""
Created on 2017/6/8 0008
@author: lijc210@163.com
Desc: 多进程,linux可运行。顺序执行（阻塞），返回结果保留顺序
"""
import time
from multiprocessing.dummy import Pool as ThreadPool

alist = [(1, 2), (3, 4), (5, 6), (7, 8)]


# adict = {"a":"b","c":"d"}
def get2(x, y):
    time.sleep(2)
    print((x, y))
    return x, y


pool = ThreadPool(6)
res = [pool.apply(get2, args) for args in alist]
pool.close()
pool.join()
for r in res:
    print(r)
print("bbbbb")

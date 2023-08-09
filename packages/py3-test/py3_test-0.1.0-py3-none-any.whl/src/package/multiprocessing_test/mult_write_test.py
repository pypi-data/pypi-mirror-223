"""
Created on 2017/6/8 0008
@author: lijc210@163.com
Desc: 多进程。
"""
from multiprocessing import Pool

alist = list(range(20))

f = open("test.txt", "a")


def get(x):
    f.write(str(x) + "\n")


if __name__ == "__main__":
    pool = Pool(5)
    res = pool.map(get, alist)
    print(res)
    pool.close()
    pool.join()

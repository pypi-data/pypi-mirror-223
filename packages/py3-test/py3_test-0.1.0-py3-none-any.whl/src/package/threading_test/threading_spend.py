"""
@Time   : 2018/8/13
@author : lijc210@163.com
@Desc:  : 功能描述。
"""
import threading
import time

t = time.time()


def a(n):
    return n


alist = []
for _x in range(10):
    t1 = threading.Thread(target=a, args=(5,))
    t1.start()
    alist.append(t1)

for t2 in alist:
    t2.join()

print(time.time() - t)

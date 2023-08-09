"""
@Time   : 2018/8/13
@author : lijc210@163.com
@Desc:  : 功能描述。
"""
import threading
import time

t = time.time()


def a(n):
    time.sleep(2)
    return n


def b(n):
    time.sleep(4)
    return n


t1 = threading.Thread(target=a, args=(5,))
t2 = threading.Thread(target=b, args=(8,))
t1.start()
t2.start()
t1.join()
t2.join()

print(time.time() - t)
print(dir(t1))
print(t1.get_result(), t2.get_result())

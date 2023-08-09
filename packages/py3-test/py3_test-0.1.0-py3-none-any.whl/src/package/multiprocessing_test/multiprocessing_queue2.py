"""
@Time   : 2019/5/30
@author : lijc210@163.com
@Desc:  : 功能描述。
"""
from multiprocessing import Process, Queue


def put(q):
    q.put(1)


def get(q):
    print(q.get())


if __name__ == "__main__":
    q = Queue()
    proc_write1 = Process(target=put, args=(q,))
    proc_write2 = Process(target=get, args=(q,))
    proc_write1.start()
    proc_write2.start()

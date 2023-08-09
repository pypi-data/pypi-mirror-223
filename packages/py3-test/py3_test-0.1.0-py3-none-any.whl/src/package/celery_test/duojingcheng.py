"""
Created on 2017/4/10 0010
@author: lijc210@163.com
Desc: 功能描述。
"""
import os
import random
import time
from multiprocessing import Pool


def long_time_task(name):
    print("Run task {} ({})...".format(name, os.getpid()))
    start = time.time()
    time.sleep(random.random() * 3)
    end = time.time()
    print("Task {} runs {:0.2f} seconds.".format(name, (end - start)))


if __name__ == "__main__":
    print("Parent process %s." % os.getpid())
    p = Pool()
    for i in range(5):
        p.apply_async(long_time_task, args=(i,))
    print("Waiting for all subprocesses done...")
    p.close()
    p.join()
    print("All subprocesses done.")

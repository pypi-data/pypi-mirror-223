"""
@Time   : 2018/8/13
@author : lijc210@163.com
@Desc:  : 功能描述。
python 多线程的管理机制
"""

import threading
import time

__author__ = "sallency"


# 封装一个线程包的类
class MyThread(threading.Thread):
    def __init__(self, name, count, interval):
        threading.Thread.__init__(self)
        self.name = name
        self.count = count
        self.interval = interval
        self.stop = False

    def run(self):
        while not self.stop:
            print("thread: %s count %d time %s" % (self.name, self.count, time.ctime()))
            time.sleep(self.interval)
            self.count += 1

    def stop(self):
        self.stop = True


# 任务
def task():
    thr_1 = MyThread("thread_1", 10, 3)
    thr_2 = MyThread("thread_2", 5, 3)
    # 如果这里设为true的话 则主线程执行完毕后会将子线程回收掉
    # 默认是 false 则主进程执行结束时不会回收子线程
    thr_1.setDaemon(True)
    thr_2.setDaemon(True)
    thr_1.start()
    thr_2.start()
    # join则是阻塞主线程 让其在子线程执行完毕后方可继续执行
    # 这就保证了当主线程执行完毕前，所有的子线程一定执行完毕了
    # thr_1.join()
    # thr_2.join()
    return True


if __name__ == "__main__":
    print("main threading start: %s" % (time.ctime()))
    task()
    print("main threading end: %s" % (time.ctime()))

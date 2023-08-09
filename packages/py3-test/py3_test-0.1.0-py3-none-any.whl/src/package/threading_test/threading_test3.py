"""
@Time   : 2018/8/13
@author : lijc210@163.com
@Desc:  : 功能描述。
"""

import threading
import time


class TestThread(threading.Thread):
    def __init__(self, thread_num=0, timeout=1.0):
        super().__init__()
        self.thread_num = thread_num

        self.stopped = False
        self.timeout = timeout

    def run(self):
        def target_func():
            inp = input("Thread %d: " % self.thread_num)
            print("Thread {} input {}".format(self.thread_num, inp))

        subthread = threading.Thread(target=target_func, args=())
        subthread.setDaemon(True)
        subthread.start()

        while not self.stopped:
            subthread.join(self.timeout)

        print("Thread stopped")

    def stop(self):
        self.stopped = True

    def isStopped(self):
        return self.stopped


thread1 = TestThread(timeout=5)
thread2 = TestThread(timeout=10)
thread1.start()
thread2.start()

print("Main thread Wainting")
time.sleep(2)

thread1.stop()
thread1.join()
thread2.join()

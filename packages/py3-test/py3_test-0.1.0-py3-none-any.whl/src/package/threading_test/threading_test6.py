"""
@Time   : 2018/8/13
@author : lijc210@163.com
@Desc:  : 功能描述。
"""
import threading
import time
import traceback


def a():
    n = 0
    while 1:
        print("a")
        if n >= 5:
            raise ValueError("aaaaa")
        n += 1
        time.sleep(1)


def b():
    n = 0
    while 1:
        print("b")
        if n >= 10:
            raise ValueError("bbbbbbb")
        n += 1
        time.sleep(1)


def c():
    print("c")
    time.sleep(1)


class MyThread(threading.Thread):
    def __init__(self, target, **args):
        threading.Thread.__init__(self)
        self.target = target
        self.args = args

    def run(self):
        try:
            self.target(**self.args)
        except Exception:
            traceback.print_exc()


for target in [a, b]:
    t = MyThread(target)
    t.start()

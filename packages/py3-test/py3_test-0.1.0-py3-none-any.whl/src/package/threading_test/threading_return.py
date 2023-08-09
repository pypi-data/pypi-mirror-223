"""
@author: lijc210@163.com
@file: tool_threading.py
@time: 2020/03/11
@desc: 多线程类
"""

from threading import Thread, active_count


class MyThread(Thread):
    def __init__(self, func, args):
        super().__init__()
        self.func = func
        self.args = args

    def run(self):
        self.result = self.func(*self.args)

    def get_result(self, defult_value=None):
        try:
            return self.result
        except Exception:
            return defult_value


if __name__ == "__main__":
    import time

    def a(n):
        time.sleep(n)
        return n

    t1 = MyThread(a, args=(4,))
    t2 = MyThread(a, args=(6,))
    t3 = MyThread(a, args=(8,))
    t1.start()
    t2.start()
    t3.start()

    print("aaaaaa", active_count())

    start = time.time()
    t1.join(2)
    t2.join(2)
    t3.join(2)
    res1 = t1.get_result()
    res2 = t2.get_result("a")
    res3 = t3.get_result("a")
    print(res1)
    print(res2)
    print(res3)

    print(time.time() - start)

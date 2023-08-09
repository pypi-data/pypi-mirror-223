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
            raise ValueError
        n += 1
        time.sleep(1)


def b():
    while 1:
        print("b")
        time.sleep(1)


# a()
# b()

# for target in [a,b]:
#     t = threading.Thread(target=target).start()
# t.start()


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


thread_list = []
for target in [a, b]:
    t = MyThread(target)
    thread_list.append(t)
    t.start()

print("bbbbbbbbbb")

for t in thread_list:
    print(t)
    t.stop()

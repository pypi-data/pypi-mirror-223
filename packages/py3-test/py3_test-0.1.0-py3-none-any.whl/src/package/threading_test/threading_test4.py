"""
@Time   : 2018/8/13
@author : lijc210@163.com
@Desc:  : 功能描述。
"""

import sys
import time
import traceback
from threading import Thread


class CountDown(Thread):
    def __init__(self):
        super().__init__()
        self.exitcode = 0
        self.exception = None
        self.exc_traceback = ""

    def run(self):
        try:
            # self._run()
            pass
        except Exception as e:
            self.exitcode = 1
            self.exception = e
            self.exc_traceback = "".join(traceback.format_exception(*sys.exc_info()))


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


if __name__ == "__main__":
    print("main start")
    td = CountDown()
    td.start()
    td.join()
    if td.exitcode != 0:
        print("Exception in " + td.getName() + " (catch by main)")
        print(td.exc_traceback)
    print("main end")

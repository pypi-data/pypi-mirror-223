"""
@Time   : 2018/9/13
@author : lijc210@163.com
@Desc:  : 功能描述。
"""

# -*- coding:utf-8 -*-
import datetime
import logging
import threading
import time
from logging.handlers import TimedRotatingFileHandler

logging.basicConfig()

myapp = logging.getLogger("test")
myapp.setLevel(logging.INFO)


class MyTimedRotatingFileHandler(TimedRotatingFileHandler):
    def shouldRollover(self, record):
        rel = super().shouldRollover(record)
        if rel:
            with threading.RLock():
                rel = super().shouldRollover(record)
        return rel

    def check_rollover(self):
        if self.shouldRollover(None):
            with threading.RLock():
                if self.shouldRollover(None):
                    self.doRollover()


handler = MyTimedRotatingFileHandler("test.log", when="S", interval=3, backupCount=3)
myapp.addHandler(handler)

t = time.time()

for i in range(10):
    handler.check_rollover()
    if time.time() - t >= 7:
        t = time.time()
        myapp.info("%d --> %s", i, datetime.datetime.now().strftime("%F %X"))
    time.sleep(1)

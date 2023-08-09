"""
@author: lijc210@163.com
@file: 1.py
@time: 2019/12/27
@desc: 功能描述。
"""
import time

from func_timeout import func_set_timeout


@func_set_timeout(1)
def task():
    print("hello world")
    time.sleep(2)


if __name__ == "__main__":
    task()

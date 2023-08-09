"""
@author: lijc210@163.com
@file: 2.py
@time: 2019/12/27
@desc: 功能描述。
"""
import time

from func_timeout import FunctionTimedOut, func_timeout


def task(a, b, c=0):
    print(a, b, c)
    print("hello world")
    time.sleep(2)


def t(*args, **kwargs):
    try:
        func_timeout(1, task, args=args, kwargs=kwargs)
    except FunctionTimedOut:
        print(
            "doit('arg1', 'arg2') could not complete within 5 seconds and was terminated.\n"
        )
    except Exception:
        # Handle any exceptions that doit might raise here
        pass


t("arg1", "arg2", c=1)

"""
@Time   : 2018/8/22
@author : lijc210@163.com
@Desc:  : 功能描述。
"""
import time
from functools import wraps

from line_profiler import LineProfiler


# 查询接口中每行代码执行的时间
def func_line_time(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        func_return = f(*args, **kwargs)
        lp = LineProfiler()
        lp_wrap = lp(f)
        lp_wrap(*args, **kwargs)
        lp.print_stats()
        return func_return

    return decorator


@func_line_time
def aaa(x):
    print("haha")
    print(x)
    time.sleep(1)
    time.sleep(2)


aaa("aaa")

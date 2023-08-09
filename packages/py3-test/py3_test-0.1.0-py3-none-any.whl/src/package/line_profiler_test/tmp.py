"""
@Time   : 2018/8/22
@author : lijc210@163.com
@Desc:  : 功能描述。
"""
import sys
import time

import line_profiler


def aaa():
    print("haha")
    time.sleep(1)
    time.sleep(2)


prof = line_profiler.LineProfiler(aaa)
prof.enable()  # 开始性能分析
aaa()
prof.disable()  # 停止性能分析
prof.print_stats(sys.stdout)

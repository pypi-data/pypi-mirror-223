"""
@author: lijc210@163.com
@file: search_tool.py
@time: 2020/04/30
@desc: 功能描述。
"""
import time

import search_tool

adict = {str(i): i * 0.12345678 for i in range(10000, 20000)}
bdict = {str(i): i * 0.12345678 for i in range(20000, 30000)}
cdict = {str(i): i * 0.12345678 for i in range(40000, 50000)}
ddict = {str(i): i * 0.12345678 for i in range(40000, 50000)}
edict = {str(i): i * 0.12345678 for i in range(50000, 60000)}
fdict = {str(i): i * 0.12345678 for i in range(50000, 70000)}

alist = [adict, bdict, cdict, ddict, edict, fdict]
start = time.time()
all_counter = search_tool.search_tool(alist)
print(all_counter.most_common(100))
print(time.time() - start)

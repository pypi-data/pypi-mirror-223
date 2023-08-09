"""
@author: lijc210@163.com
@file: 3.py.py
@time: 2020/03/26
@desc: 功能描述。
"""

with open("test2.pdf", encoding="GB18030") as f:
    for line in f.readlines():
        print(line)

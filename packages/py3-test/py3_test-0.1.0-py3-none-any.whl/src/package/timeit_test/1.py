"""
@author: lijc210@163.com
@file: 1.py
@time: 2019/10/08
@desc: 功能描述。
"""
import timeit

foooo = """
sum = []
for i in range(1000):
    sum.append(i)
"""

print(timeit.timeit(stmt="[i for i in range(1000)]", number=100000))
print(timeit.timeit(stmt=foooo, number=100000))

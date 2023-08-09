"""
@author: lijc210@163.com
@file: 3.py
@time: 2020/09/18
@desc: 功能描述。
"""

import numpy as np

a = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
b = np.array([1, 2, 3])

c = np.column_stack((a, b))

print(c)

print(type(a.tolist()))

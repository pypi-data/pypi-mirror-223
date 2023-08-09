"""
@author: lijc210@163.com
@file: 2.py
@time: 2019/10/28
@desc: 功能描述。
"""
import math

import pandas as pd

data_list = [
    [1, 1, 1, 1],
    [2, 2, 2, 2],
    [3, 3, 3, 3],
    [4, 4, 4, 4],
    [5, 5, 5, 5],
    [6, 6, 6, 6],
    [7, 7, 7, 7],
]

df = pd.DataFrame(data_list, columns=["a", "b", "c", "d"])

size = 4
num = math.ceil(len(df) / size)

for i in range(num):
    print(df.loc[i * size : (i + 1) * size - 1])

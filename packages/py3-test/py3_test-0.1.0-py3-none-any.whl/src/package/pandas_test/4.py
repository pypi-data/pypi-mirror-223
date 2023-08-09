"""
@author: lijc210@163.com
@file: 2.py
@time: 2019/10/28
@desc: 功能描述。
"""
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

print(df.columns)
print(list(df.columns))

for index, row in df.iterrows():
    print(index, row["a"])

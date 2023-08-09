"""
@author: lijc210@163.com
@file: 2.py
@time: 2019/10/28
@desc: 功能描述。
"""

import pandas as pd

data_list = [[1, 1, 1, 1], [2, 2, 2, 2]]

df = pd.DataFrame(data_list, columns=["a", "b", "c", "d"])


def get_top(row):
    row[["b", "c"]] = 0
    return row


print(df.apply(get_top, axis=1))

print(df)

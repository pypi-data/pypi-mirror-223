"""
@author: lijc210@163.com
@file: 1.py
@time: 2019/10/12
@desc: 功能描述。
"""
import pandas as pd

df = pd.DataFrame(index=[0, 1, 2], columns=["uid", "name"])

print(df)

df.loc[0]["uid"] = "aaaaa"
#
print(df)

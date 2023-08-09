"""
@File    :   celue.py
@Time    :   2021/08/17 17:36:05
@Author  :   lijc210@163.com
@Desc    :   累计收益 = 持仓金额 - 所有投入本金 + 所有赎回金额
"""

import os
import pickle

import pandas as pd
import tushare as ts

pd.set_option("display.max_rows", 1000)

BASE_DIR = "D:\\gupiao"
pro = ts.pro_api("5eecd230c3f70af5695ba92d92aa006a5f5f4e712a27de6175adbf0d")


def pickleFile(file, item):
    with open(file, "wb") as dbFile:
        pickle.dump(item, dbFile)


def unpickeFile(file):
    with open(file, "rb") as dbFile:
        return pickle.load(dbFile)


hs_list_path = os.path.join(BASE_DIR, "hs_list.pick")
if os.path.exists(hs_list_path) is False:
    hs_list = pro.stock_basic(exchange="", list_status="L", fields="")
    pickleFile(hs_list_path, hs_list)
else:
    hs_list = unpickeFile(hs_list_path)


def jisuan(daily):
    print(daily.head(10))
    print(
        "index".ljust(20, " "),
        "行".ljust(20, " "),
        "初".ljust(20, " "),
        "关".ljust(20, " "),
        "金".ljust(20, " "),
        "赎".ljust(20, " "),
        "投".ljust(20, " "),
        "幅".ljust(20, " "),
        "上幅".ljust(20, " "),
    )

    a = 0  # 初
    b = 0  # 金
    c = 0  # 赎
    d = 0  # 投
    e = 0  # 幅
    f = 0  # 上幅
    for index, row in daily.iterrows():
        close = row["close"]
        if index == 0:
            a = row["pre_close"]
            f = (close - a) / a

        e = (close - a) / a
        if e - f >= 0.1 and abs(e) >= 0.1:
            b = b if b != 0 else row["close"]
            c += b * float(format(abs(e), ".1f"))
            b = b - b * float(format(abs(e), ".1f"))
            f = e
            print(
                str(index).ljust(20, " "),
                "+".ljust(20, " "),
                str(a).ljust(20, " "),
                str(close).ljust(20, " "),
                str(b).ljust(20, " "),
                str(c).ljust(20, " "),
                str(d).ljust(20, " "),
                str(e).ljust(20, " "),
                str(f).ljust(20, " "),
            )
        elif f - e >= 0.1 and abs(e) >= 0.1:
            b = b if b != 0 else row["close"]
            d += b * float(format(abs(e), ".1f"))
            b = b + b * float(format(abs(e), ".1f"))
            f = e
            print(
                str(index).ljust(20, " "),
                "-".ljust(20, " "),
                str(a).ljust(20, " "),
                str(close).ljust(20, " "),
                str(b).ljust(20, " "),
                str(c).ljust(20, " "),
                str(d).ljust(20, " "),
                str(e).ljust(20, " "),
                str(f).ljust(20, " "),
            )
        else:
            pass

        if index >= 10000:
            break


for _index, row in hs_list.iterrows():
    print(row["ts_code"], row["symbol"])
    ts_code = row["ts_code"]
    daily_path = os.path.join(BASE_DIR, f"{ts_code}.pick")
    if os.path.exists(daily_path) is False:
        daily = pro.daily(ts_code=ts_code, start_date="20010816", end_date="20210816")
        pickleFile(daily_path, daily)
    else:
        daily = unpickeFile(daily_path)
    jisuan(daily)
    break

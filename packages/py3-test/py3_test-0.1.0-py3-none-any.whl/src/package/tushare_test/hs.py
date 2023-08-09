import os
import pickle

import tushare as ts

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

for _index, row in hs_list.iterrows():
    print(row["ts_code"], row["symbol"])
    ts_code = row["ts_code"]
    daily_path = os.path.join(BASE_DIR, f"{ts_code}.pick")
    if os.path.exists(daily_path) is False:
        daily = pro.daily(ts_code=ts_code, start_date="20010816", end_date="20210816")
        pickleFile(daily_path, hs_list)
    else:
        daily = unpickeFile(daily_path)

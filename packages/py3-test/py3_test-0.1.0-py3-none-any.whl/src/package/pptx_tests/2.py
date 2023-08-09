"""
@author: lijc210@163.com
@file: 2.py
@time: 2020/03/26
@desc: 功能描述。
"""
import json

data_dict = json.load(open("data.json", encoding="utf-8"))

l2 = data_dict["锁单接单结构-订单区域分布"]["天怡美装饰-215227980"]

print(json.dumps(l2, ensure_ascii=False))

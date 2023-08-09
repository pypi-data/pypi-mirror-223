"""
@author: lijc210@163.com
@file: 1.py
@time: 2020/08/17
@desc: 功能描述。
"""
import pickledb

db = pickledb.load("test.db", True)

db.set("test", "value")
print(db.get("key"))

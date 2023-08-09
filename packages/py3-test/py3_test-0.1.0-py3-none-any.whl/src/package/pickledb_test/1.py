"""
@author: lijc210@163.com
@file: 1.py
@time: 2020/08/17
@desc: 功能描述。
"""
import time

import pickledb

db = pickledb.load("test.db", True)

db.set("key", "value")
print(db.get("key"))

# l = [["key" + str(x), "value" + str(x)] for x in range(1000)]

# start = time.time()
# for k, v in l:
#     db.set(k, v)
# print(time.time()-start)

# l2 = [k for k, v in l]
# print(l2)
#
# start = time.time()
# for k, v in l:
#     print(db.get(k))
# print(time.time()-start)

while 1:
    print(db.get("test"))
    time.sleep(1)

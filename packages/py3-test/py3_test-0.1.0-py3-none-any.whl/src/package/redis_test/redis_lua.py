"""
Created on 2015/12/13
@author: lijc210@163.com

"""
import json
import time

import redis

r = redis.StrictRedis(host="10.10.20.165", port=6379, db=11)

# lua1 = """
#    redis.call("select", ARGV[1])
#    return redis.call("get",KEYS[1])
# """

lua1 = """
   redis.call("select", 11)
   return redis.call("ZREVRANGEBYSCORE",KEYS[1],"+INF", "-INF",'LIMIT',0,5000, 'withscores')
"""

script1 = r.register_script(lua1)

key_list = [
    ["客厅", "9e459dfacbd96cd5507896988f6ac92c"],
    ["设计", "7c018f05007126f2601eed9b59d99f4a"],
    ["效果图", "d93a402895f7aa66303278a795ab2c6d"],
    ["卧室", "2d33fbe8c279d5bb73962b18dc03bb09"],
]

start = time.time()
a = r.get("teststr")
print(time.time() - start)
print(json.loads(a))

# for keyword, key in key_list:
#     start = time.time()
#     res = r.zrevrangebyscore(key, 'inf', 0, 0, 5000, withscores=True)
#     print time.time() - start, res[0:10]
#
#     start = time.time()
#     res = script1(keys=[key])
#     print time.time() - start, res[0:10]

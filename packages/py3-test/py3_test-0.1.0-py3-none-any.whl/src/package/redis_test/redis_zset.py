"""
@author: lijc210@163.com
@file: redis_zset.py
@time: 2019/10/14
@desc: 功能描述。
"""
import time

import redis

r = redis.StrictRedis(host="10.10.20.165", port=6379, db=0, decode_responses=True)

udid = "11676CCE-9230-4D1B-B733-0F9B7883A011"
s = r.zrangebyscore(
    "r_v9_news" + udid, int(time.time()) - 604800, int(time.time())
)  # 7天已经推荐过资讯，视频

print(s)

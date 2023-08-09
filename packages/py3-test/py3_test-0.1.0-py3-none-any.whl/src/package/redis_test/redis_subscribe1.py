"""
@author: lijc210@163.com
@file: redis_subscribe2.py
@time: 2019/11/13
@desc: 功能描述。
"""

import redis

r = redis.StrictRedis(host="10.10.20.165", port=6379, db=0, decode_responses=True)
ps = r.pubsub()
ps.subscribe("invalid_id")  # 从liao订阅消息
for item in ps.listen():  # 监听状态：有消息发布了就拿过来
    if item["type"] == "message":
        print(item["channel"])
        print(item["data"])

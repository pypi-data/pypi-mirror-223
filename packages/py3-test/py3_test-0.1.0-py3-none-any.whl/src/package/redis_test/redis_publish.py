"""
@author: lijc210@163.com
@file: redis_subscribe2.py
@time: 2019/11/13
@desc: 功能描述。
"""

import json

import redis

r = redis.StrictRedis(host="10.10.20.165", port=6379, db=0, decode_responses=True)

# r.publish("liao", "1")  #发布消息到liao
#
# r.publish("liao", "2")  #发布消息到liao
#
# r.publish("liao", "3")  #发布消息到liao

r.publish("invalid_id", json.dumps({"zxtt_note_new_only_wx_id": 456}))  # 发布消息到liao
r.publish("invalid_id", json.dumps({"zxtt_note_new_only_wx_id": 789}))  # 发布消息到liao

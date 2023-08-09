"""
Created on 2015/12/13
@author: lijc210@163.com

"""

import json
import time

import redis

from .pg_client import PostgreSQL

pg = PostgreSQL()


class Getredis:
    rdb3 = redis.StrictRedis(host="10.10.23.16", port=6379, db=3)
    rdb2 = redis.StrictRedis(host="10.10.23.16", port=6379, db=2)

    def get_cookie(self):
        cookie = "15pubp4xt3va6si9"
        print(self.rdb3.get(cookie))

    def get_tagdetail(self, start_timeStamp, end_timeStamp):
        alist = self.rdb2.zrangebyscore("tagdetail", start_timeStamp, end_timeStamp)  #
        visitor_id_list = []
        for detail in alist:
            detail_json = json.loads(detail)
            if "visitor_id" in detail_json:
                visitor_id_list.append(detail_json["visitor_id"])
        pv = len(visitor_id_list)
        uv = len(set(visitor_id_list))
        return pv, uv

    def insertPG(self):
        end_timeStamp = time.time()  # 当前时间戳
        start_timeStamp = end_timeStamp - 600  # 10分钟前时间戳
        start_date = time.strftime("%Y%m%d", time.localtime(start_timeStamp))  # 当前日期
        start_datetime = time.strftime(
            "%Y%m%d%H%M", time.localtime(start_timeStamp)
        )  # 当前日期+时分
        pv, uv = data.get_tagdetail(start_timeStamp, end_timeStamp)
        sql = "INSERT INTO public.ol_traf_real_minute_detail VALUES({},{},{},{},CURRENT_TIMESTAMP)".format(
            start_date, start_datetime, pv, uv
        )
        pg.sqlcommit(sql)


if __name__ == "__main__":
    data = Getredis()
    data.insertPG()

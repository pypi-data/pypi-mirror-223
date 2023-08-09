"""
@Time   : 2020/12/03
@author : lijc210@163.com
@Desc:  : 功能描述。
"""
import time

import itchat
from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()

itchat.auto_login(True)


def my_job():
    r = itchat.search_chatrooms(name="练车通知群")
    # print(json.dumps(r))
    if r:
        room = r[0]
        room.send("刘教练，预约我明天练车")
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())))


print("start")
sched.add_job(my_job, "cron", year=2021, month=2, day=20, hour=0o6, minute=30, second=0)
sched.start()

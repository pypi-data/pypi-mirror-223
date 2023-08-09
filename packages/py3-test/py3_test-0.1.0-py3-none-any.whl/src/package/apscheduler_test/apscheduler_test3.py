import time

from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()


def my_job1():
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())))


def my_job2():
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())), "my_job2")


# 表示2017年3月22日17时19分07秒执行该程序
sched.add_job(my_job1, "cron", day_of_week=3, hour=15, minute=0o5, second=00)
sched.add_job(my_job2, "cron", day_of_week=2, hour=15, minute=0o5, second=00)

sched.start()

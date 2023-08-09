import time

from apscheduler.schedulers.blocking import BlockingScheduler


def my_job1():
    time.sleep(2)
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())), "my_job1")


def my_job2():
    time.sleep(2)
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())), "my_job2")


sched = BlockingScheduler()
sched.add_job(my_job1, "interval", seconds=5)
sched.add_job(my_job2, "interval", seconds=5)
sched.start()

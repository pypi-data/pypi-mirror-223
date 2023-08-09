import time

from apscheduler.executors.pool import ProcessPoolExecutor, ThreadPoolExecutor
from apscheduler.schedulers.background import BackgroundScheduler

executors = {"default": ThreadPoolExecutor(2), "processpool": ProcessPoolExecutor(2)}
job_defaults = {"coalesce": False, "max_instances": 3}
sched = BackgroundScheduler(executors=executors, job_defaults=job_defaults)

dateMap = {
    "d": "*",
    "mm": "*/1",
    "m": "*",
    "ss": "0",
    "hh": "*",
    "w": "*",
    "y": "2017-2022",
}

dateMap = {
    "d": "*",
    "mm": "*",
    "m": "*",
    "ss": "*/1",
    "hh": "*",
    "w": "*",
    "y": "2017-2022",
}


def getDataByLabelRuleCondition(requestData):
    time.sleep(5)
    print(requestData)


for i in range(5):
    sched.add_job(
        getDataByLabelRuleCondition,
        "cron",
        year=dateMap.get("y"),
        month=dateMap.get("m"),
        day_of_week=dateMap.get("w"),
        day=dateMap.get("d"),
        hour=dateMap.get("hh"),
        minute=dateMap.get("mm"),
        second=dateMap.get("ss"),
        kwargs={"requestData": i},
        id=str(i),
        name=str(i),
        misfire_grace_time=None,
    )

sched.start()
time.sleep(1)

# for job in sched.get_jobs():
#     sched.add_job(job.func, kwargs=job.kwargs)
#
# print("bbbbbbbbbbbbbbbbbbbbb")
#
# for i in range(12):
#     time.sleep(1)
#
# sched.print_jobs()

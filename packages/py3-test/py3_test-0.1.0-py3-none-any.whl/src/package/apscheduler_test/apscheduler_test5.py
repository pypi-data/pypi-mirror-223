from apscheduler.schedulers.background import BackgroundScheduler

sched = BackgroundScheduler()

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
    print(requestData)
    print("aaaaaaaaaaaa")


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
    kwargs={"requestData": "requestData"},
    id="12345678",
    name="720171018000035",
    misfire_grace_time=None,
)

sched.start()

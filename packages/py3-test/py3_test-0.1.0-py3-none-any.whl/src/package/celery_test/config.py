#!/usr/bin/env python

from datetime import timedelta

from celery.schedules import crontab

CELERY_RESULT_BACKEND = "redis://10.10.20.35:6379/10"
BROKER_URL = "redis://10.10.20.35:6379/10"

CELERY_TIMEZONE = "Asia/Shanghai"

# schedules
CELERYBEAT_SCHEDULE = {
    "add-every-5-seconds": {
        "task": "tasks.add",
        "schedule": timedelta(seconds=5),  # 每 5 秒执行一次
        "args": (5, 8),  # 任务函数参数
    },
    "a-at-some-time": {
        "task": "tasks.add",
        "schedule": crontab(hour=9, minute=50),  # 每天早上 9 点 50 分执行一次
        "args": (3, 7),  # 任务函数参数
    },
}

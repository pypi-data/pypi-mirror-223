"""
Created on 2017/2/14
@author: lijc210@163.com
Desc: 功能描述。
"""

from celery import Celery

app = Celery("tasks", include=["tasks"])
app.config_from_object("config")

if __name__ == "__main__":
    app.start()

"""
@author: lijc210@163.com
@file: aaa.py
@time: 2019/11/04
@desc: 功能描述。
"""
import requests

body = {
    "key": "简约,水电,二房",
    "pagesize": 10,
    "uuid": "5008C251-F4BB-42BB-82C6-A7DAF9E031BE",
    "city": "上海",
    "level": "debug",
    "api": "qijia_recommend",
    "v9_news_column": ["id", "title", "create_time"],
    "note_new_column": ["id", "title", "create_time"],
    "design_case_column": ["id", "title", "create_time"],
    "design_case_pics_column": ["id", "title", "create_time"],
    "show_home_column": ["id", "title", "create_time"],
    "v9_special_column": ["id", "title", "create_time"],
    "question_column": ["id", "city", "case_count"],
    "v9_design_column": ["id", "city", "case_count"],
}

r = requests.post(
    "http://bi-python.api.tg.local/rt/qijia/recommend/v2/",
    json=body,
    headers={"cookie": "cccccccccccc", "udid": "dddddddddd"},
)

print(r.json())

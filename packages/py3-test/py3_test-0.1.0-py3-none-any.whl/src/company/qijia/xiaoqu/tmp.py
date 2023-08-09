"""
@author: lijc210@163.com
@file: tmp.py
@time: 2019/12/19
@desc: 功能描述。
"""
import time

import requests

for _i in range(1000):
    body = {
        "page_index": 0,
        "page_size": 10,
        "api": "qijia_recommend",
        "uuid": "56CF337E-A547-45A1-82DB-D61B57A11D73",
        "key": "准备,三房,简约,中式,准备,三房,简约,中式",
        "pagesize": 10,
        "city": "zhumadian",
        "url": "rt/qijia/recommend/v1/",
        "v9_news_column": [
            "id",
            "title",
            "thumb",
            "thumb_bak",
            "thumb_mp4",
            "views",
            "account_name",
            "video_time",
            "target_url",
            "comment_count",
            "userid",
            "small_face_url",
            "width_int",
            "height_int",
        ],
        "v9_design_column": [
            "id",
            "design_name",
            "thumb",
            "space",
            "layout",
            "genre",
            "url",
            "views",
            "design_id",
        ],
        "design_case_column": [
            "id",
            "title",
            "cover_image_url",
            "user_name",
            "page_view",
            "comment_count",
            "image_count",
            "label_str",
            "label_list",
            "image_list",
            "house_type",
            "decorate_style",
            "designer_id",
            "designer_name",
            "small_face_url",
        ],
        "note_new_column": [
            "id",
            "title",
            "cover_url",
            "user_name",
            "browse_count",
            "comment_count",
            "image_list",
            "video_id",
        ],
        "v9_special_column": ["id", "title", "banner", "cover_url", "article_list"],
        "question_column": [
            "id",
            "title",
            "browse_count",
            "answer_count",
            "answer_content",
            "answer_user_name",
        ],
    }
    start = time.time()
    r = requests.post("http://10.10.20.165:19035/rt/qijia/recommend/v1/", json=body)
    print(r.status_code, time.time() - start)

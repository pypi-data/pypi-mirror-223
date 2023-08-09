"""
@Time   : 2019/2/26
@author : lijc210@163.com
@Desc:  : 功能描述。
"""
import random
import time

from elasticsearch import Elasticsearch
from sanic import Sanic
from sanic.response import json

ES_HOST = ["http://120.27.14.16:9200"]

es_client = Elasticsearch(
    ES_HOST,
    retry_on_timeout=True,
    timeout=100,
    max_retries=3,
    sniff_on_start=True,
    sniff_on_connection_fail=True,
    sniffer_timeout=60,
)

app = Sanic()

all_tag_list = []
with open("tag_data.txt", encoding="utf-8") as f:
    for line in f.readlines():
        all_tag_list.append(line.strip().split("\t")[1])


@app.route("/api/1.0/more_like_this", methods=["GET"])
async def more_like_this_get(request):
    res_dict = {
        "参数": {
            "id": "http://schools.idp.cn/rank/major/2019-timesuk-Nursing/Leeds-Beckett-University",
            "title": "2019年TIMES英国大学专业排名_护理学专业排名_护理学专业排行榜",
            "category": ["排名", "院校首页", "院校问答", "院校专业", "顾问首页", "案例", "成功故事", "文章"],
            "column": ["url", "title", "keywords"],
            "page": 1,
            "page_size": 10,
        },
        "返回结果": {
            "statusCode": "0000",
            "msg": "请求成功",
            "result": {
                "date_list": [
                    {
                        "keywords": "QS世界大学专业排名,QS世界大学学科排名,QS世界大学专业排行榜",
                        "title": "2016年QS世界大学专业排名_护理学专业排名_护理学专业排行榜",
                        "url": "http://schools.idp.cn/rank/major/2016-qs-Nursing/Queensland-University-of-Technology",
                    }
                ],
                "total": 14164,
            },
            "costTime": "8.30388",
        },
        "备注": "相关阅读接口，接口类型POST,category可以指定返回的类型",
    }
    return json(res_dict)


@app.route("/api/1.0/more_like_this", methods=["POST"])
async def more_like_this(request):
    start = time.time()
    _id = request.json.get("id", "")
    title = request.json.get("title", "")
    category = request.json.get("category", [])
    column_list = request.json.get("column", ["url", "title", "keywords"])
    page = request.json.get("page", 1)
    page_size = request.json.get("page_size", 10)

    body = {
        "query": {
            "bool": {
                "must": [
                    {"terms": {"category.keyword": category}},
                    {
                        "more_like_this": {
                            "fields": ["title", "text"],
                            "like": [{"_index": "idp", "_id": _id}, title],
                            "minimum_should_match": "30%",
                            "min_doc_freq": 1,
                        }
                    },
                ]
            }
        },
        "_source": column_list,
        "size": page_size,
        "from": (page - 1) * page_size,
    }
    es_res = es_client.search(index="idp", doc_type="doc", body=body)

    result = {
        "date_list": [adict["_source"] for adict in es_res["hits"]["hits"]],
        "total": es_res["hits"]["total"],
    }
    res_dict = {
        "statusCode": "0000",
        "msg": "请求成功",
        "result": result,
        "costTime": format((time.time() - start) * 1000, ".6"),
    }

    return json(res_dict)


@app.route("/api/1.0/mget", methods=["GET"])
async def mget(request):
    res_dict = {
        "参数": {
            "ids": [
                "http://schools.idp.cn/rank/major/2019-timesuk-Nursing/Leeds-Beckett-University",
                "http://schools.idp.cn/rank/major/2019-timesuk-Psychology/Nottingham-Trent-University",
            ],
            "column": ["tag_list"],
            "page_size": 3,
        },
        "返回结果": {
            "statusCode": "0000",
            "msg": "请求成功",
            "result": {
                "http://schools.idp.cn/rank/major/2019-timesuk-Nursing/Leeds-Beckett-University": {
                    "tag_list": ["times排名", "英国大学排行榜", "英国大学专业"]
                },
                "http://schools.idp.cn/rank/major/2019-timesuk-Psychology/Nottingham-Trent-University": {
                    "tag_list": [
                        "年世界大学排名",
                        "世界大学排名",
                        "大学排名",
                        "世界大学排名前200",
                        "世界大学排名前500",
                        "2019世界大学排名榜",
                        "世界大学2019排名榜",
                        "2019世界大学综合排名",
                        "世界大学排名榜",
                        "世界大学综合排名",
                    ]
                },
            },
            "costTime": "23.0002",
        },
        "备注": "批量获取接口",
    }
    return json(res_dict)


@app.route("/api/1.0/mget", methods=["POST"])
async def more_like_this_post(request):
    start = time.time()
    ids = request.json.get("ids", [])
    column_list = request.json.get("column", ["tag_list"])
    page_size = request.json.get("page_size", 10)

    body = {"docs": [{"_id": _id, "_source": column_list} for _id in ids]}
    es_res = es_client.mget(index="idp", doc_type="doc", body=body)
    docs_tmp = es_res["docs"]
    res_dict = {}
    for doc in docs_tmp:
        _id = doc.get("_id")
        _source = doc.get("_source")
        tag_list = _source.get("tag_list", [])
        add_num = page_size - len(tag_list)
        if add_num > 0:
            selected_list = random.sample(all_tag_list, add_num)
            tag_list.extend(selected_list)
            _source["tag_list"] = tag_list
        res_dict[_id] = _source
    res_dict = {
        "statusCode": "0000",
        "msg": "请求成功",
        "result": res_dict,
        "costTime": format((time.time() - start) * 1000, ".6"),
    }

    return json(res_dict)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9001)

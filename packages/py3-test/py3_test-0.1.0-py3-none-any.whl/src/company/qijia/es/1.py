"""
@author: lijc210@163.com
@file: 1.py
@time: 2020/08/04
@desc: 功能描述。
"""

data_dict = {
    "建筑形式": "buildingform",
    "装修风格": "contstyle",
    "人群": "crowd",
    "装修预算": "decobudget",
    "装修档次": "decograde",
    "装修方式": "decomode",
    "装修阶段": "decophase",
    "装修色调": "zx_tone",
    "装修类型": "decotype",
    "装修感觉": "feeling",
    "房屋面积": "houarea",
    "房屋户型": "houunit",
    "用户年龄阶段": "user_age_group",
}

for k, v in data_dict.items():
    body = {"aggs": {"aggs": {"terms": {"field": v}}}}

    from utils.es_client import EsClient

    es_client = EsClient(
        [
            "http://10.10.20.248:9200",
            "http://10.10.20.231:9200",
            "http://10.10.20.143:9200",
        ]
    )

    res = es_client.search("kn2_es", "user_base_info_new", body)

    buckets = res["aggregations"]["aggs"]["buckets"]
    # print(json.dumps(buckets,ensure_ascii=False))
    for adict in buckets:
        print(k, adict["key"], adict["doc_count"])

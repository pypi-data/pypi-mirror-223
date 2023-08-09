"""
@author: lijc210@163.com
@file: add.py
@time: 2019/08/27
@desc: 功能描述。
"""
from elasticsearch import Elasticsearch

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

es_all_url_set = set()
with open("all.txt", encoding="utf-8") as f:
    for line in f.readlines():
        url = line.strip()
        es_all_url_set.add(url)

for url in es_all_url_set:
    if "_r-" in url:
        print(url)
        res = es_client.get("idp", "doc", id=url)
        _id = res["_id"]
        _source = res["_source"]
        url = _source["url"]
        print(url)
        print(res)
        es_client.delete("idp", "doc", _id)
        es_client.index("idp", "doc", _source, id=url)
        # break

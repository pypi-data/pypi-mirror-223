"""
@author: lijc210@163.com
@file: scan_url.py
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

with open("del.txt", encoding="utf-8") as f:
    for line in f.readlines():
        url = line.strip()
        res = es_client.delete("idp", "doc", id=url)
        print(res)

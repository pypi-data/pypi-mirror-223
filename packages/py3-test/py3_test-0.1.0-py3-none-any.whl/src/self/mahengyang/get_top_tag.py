"""
@Time   : 2019-09-01
@author : lijc210@163.com
@Desc:  : 功能描述。
"""
import json

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

docs = []
for _id in [
    "http://blog.idp.cn/beijing/ksyusha-guan/index.html",
    "http://blog.idp.cn/wuhan/raymond%20lei/index_6.html",
]:
    doc = {
        "filter": {"min_term_freq": 1, "min_doc_freq": 1, "min_word_length": 2},
        "fields": [
            "title",
            "keywords",
            "content",
            "description",
            "complement",
            "topic_title",
        ],
        "offsets": False,
        "payloads": True,
        "positions": False,
        "term_statistics": True,
        "field_statistics": True,
        "_id": _id,
    }
    docs.append(doc)

response = es_client.mtermvectors("idp", "doc", body={"docs": docs})
if "docs" in response:
    for adoc in response["docs"]:
        print(adoc)
        print(json.dumps(adoc))

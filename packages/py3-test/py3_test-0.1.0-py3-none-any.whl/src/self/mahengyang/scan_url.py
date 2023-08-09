"""
@author: lijc210@163.com
@file: scan_url.py
@time: 2019/08/27
@desc: 功能描述。
"""

from elasticsearch import Elasticsearch, helpers

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

body = {"query": {}, "_source": ["title", "keywords", "category"]}
# res = es_client.search(index="idp", doc_type="doc", body=None)
# print(res)

response = helpers.scan(
    es_client,
    query=None,
    index="idp",
    doc_type="doc",
    scroll="5m",
    raise_on_error=True,
    preserve_order=False,
    size=1000,
    request_timeout=None,
    clear_scroll=True,
    scroll_kwargs=None,
)

with open("all.txt", "w", encoding="utf-8") as f:
    for resp in response:
        # print(resp)
        _id = resp["_id"]
        _source = resp["_source"]
        if _source:
            print(_id)
            keywords = _source.get("keywords", "")
            if keywords is None:
                keywords = ""
            category = _source.get("category", "")
            if category is None:
                category = ""
            title = _source.get("title", "")
            if title is None:
                title = ""
            keywords = keywords.replace("\n", "")
            category = category.replace("\n", "")
            title = title.replace("\n", "")
            f.write(category + "\t" + keywords + "\t" + _id + "\t" + title + "\n")

"""
@Time   : 2019-08-07
@author : lijc210@163.com
@Desc:  : 功能描述。
"""
import jieba
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

# 清空
with open("tag.txt", "w", encoding="utf-8") as f:
    f.write("")

with open("tag_data.txt", encoding="utf-8") as f:
    for line in f.readlines():
        line_list = line.strip().split("\t")
        country = line_list[0]
        tag = line_list[1]
        tag_list = list(jieba.cut_for_search(tag))
        if len(tag_list) - len(set(tag_list)) != 0:  # 跳过有重复的词
            continue
        print(tag)
        body = {
            "query": {
                "bool": {
                    "must": [
                        {
                            "multi_match": {
                                "query": tag,
                                "fields": ["keywords", "title", "description"],
                                "minimum_should_match": "100%",
                            }
                        }
                    ]
                }
            },
            "_source": ["title", "keywords"],
        }

        # res = es_client.search(index="idp", doc_type="doc", body=None)
        # print(res)

        response = helpers.scan(
            es_client,
            query=body,
            index="idp",
            doc_type="doc",
            scroll="5m",
            raise_on_error=True,
            preserve_order=False,
            size=1000,
            request_timeout=None,
            clear_scroll=True,
            scroll_kwargs=None,
            track_scores=True,
        )

        with open("tag.txt", "a", encoding="utf-8") as f:
            for resp in response:
                # print(resp)
                _id = resp["_id"]
                _source = resp["_source"]
                _score = resp["_score"]
                print(_id)
                if _source:
                    title = _source.get("title", "").replace("\n", "")
                    f.write(tag + "\t" + _id + "\t" + str(_score) + "\t" + title + "\n")
        # break

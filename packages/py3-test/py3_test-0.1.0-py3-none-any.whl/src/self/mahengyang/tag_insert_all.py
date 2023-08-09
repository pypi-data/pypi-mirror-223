"""
@Time   : 2019-08-07
@author : lijc210@163.com
@Desc:  : 功能描述。
"""
from collections import Counter, defaultdict

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

default_dict = defaultdict(dict)
url_title_dict = {}

with open("tag.txt", encoding="utf-8") as f:
    for _i, line in enumerate(f.readlines()):
        # print(i)
        line_list = line.strip().split("\t")
        tag = line_list[0]
        url = line_list[1]
        score = line_list[2]
        title = line_list[3]
        default_dict[url][tag] = score
        # break

i = 0
actions = []
for url, adict in default_dict.items():
    new_dict = {tag: float(score) for tag, score in adict.items()}
    tmp_counter = Counter(new_dict)
    tmp_list = [tag for tag, score in tmp_counter.most_common(10)]
    print(url, tmp_list)
    i += 1
    actions.append(
        {
            "_op_type": "update",
            "_index": "idp",
            "_type": "doc",
            "_id": url,
            "doc": {"tag_list": tmp_list},
        }
    )
    if i % 5000 == 0:
        print(len(actions))
        success, errors = helpers.bulk(es_client, actions=actions)
        actions = []

print(len(actions))
success, errors = helpers.bulk(es_client, actions=actions)
actions = []

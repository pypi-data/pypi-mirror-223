"""
@Time   : 2019-08-07
@author : lijc210@163.com
@Desc:  : 功能描述。
"""
import logging
from collections import Counter, defaultdict
from datetime import datetime, timedelta

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

logger = logging.getLogger("tag_cron")  # 创建logger
logger.setLevel(logging.INFO)  # DEBUG输出调试日志，INFO则不输出日志
hdr = logging.StreamHandler()  # 用于输出到控制台
fh = logging.FileHandler("tag_cron.log", mode="a")  # 用于输出到文件
formatter = logging.Formatter("[%(asctime)s] %(name)s:%(levelname)s: %(message)s")
hdr.setFormatter(formatter)
fh.setFormatter(formatter)
logger.addHandler(hdr)  # 用于输出到控制台，上线注释此项
logger.addHandler(fh)  # 用于输出到文件

date_ago = "2019-11-21T00:19:25.000Z"
date_ago = (datetime.now() + timedelta(seconds=60 * 40)).strftime(
    "%Y-%m-%dT%H:%M:%S.000Z"
)

with open("tag_cron.txt", "w", encoding="utf-8") as fw:
    with open("tag_data.txt", encoding="utf-8") as f:
        for i, line in enumerate(f.readlines(), 1):
            if i % 2000 == 0:
                logger.info(i)
            line_list = line.strip().split("\t")
            country = line_list[0]
            tag = line_list[1]
            tag_list = list(jieba.cut_for_search(tag))
            if len(tag_list) - len(set(tag_list)) != 0:  # 跳过有重复的词
                continue
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
                            },
                            {"range": {"date": {"gte": date_ago}}},
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

            for resp in response:
                # print(resp)
                _id = resp["_id"]
                _source = resp["_source"]
                _score = resp["_score"]
                if _source:
                    title = _source.get("title", "").replace("\n", "")
                    fw.write(
                        tag + "\t" + _id + "\t" + str(_score) + "\t" + title + "\n"
                    )
            # break

# tag_list写入es

default_dict = defaultdict(dict)
url_title_dict = {}

with open("tag_cron.txt", encoding="utf-8") as f:
    for i1, line in enumerate(f.readlines()):
        print(i1)
        line_list = line.strip().split("\t")
        tag = line_list[0]
        url = line_list[1]
        score = line_list[2]
        title = line_list[3]
        default_dict[url][tag] = score
        # break

logger.info("default_dict长度{}".format(len(default_dict)))

i = 0
actions = []
for url, adict in default_dict.items():
    new_dict = {tag: float(score) for tag, score in adict.items()}
    tmp_counter = Counter(new_dict)
    tmp_list = [tag for tag, score in tmp_counter.most_common(10)]
    logger.info("{}    {}".format(url, tmp_list))
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
        success, errors = helpers.bulk(es_client, actions=actions)
        logger.info("写入{}".format(len(actions)))
        actions = []

success, errors = helpers.bulk(es_client, actions=actions)
logger.info("写入{}".format(len(actions)))

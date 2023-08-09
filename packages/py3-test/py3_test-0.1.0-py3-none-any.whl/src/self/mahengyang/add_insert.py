"""
@author: lijc210@163.com
@file: add.py
@time: 2019/08/27
@desc: 功能描述。
"""
import time
import traceback
from urllib.parse import urlparse

import requests
from elasticsearch import Elasticsearch
from pyquery import PyQuery as pq

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


def get_domain(url):
    parse_result = urlparse(url)
    return parse_result.netloc


with open("add.txt", encoding="utf-8") as f:
    for line in f.readlines():
        url = line.strip()
        try:
            r = requests.get(url, timeout=5)
            r.encoding = "utf-8"
            doc = pq(r.text)
            title = doc("title").text()
            statusCode = r.status_code
            print("正确", statusCode, url)
            keywords = doc("meta[name='keywords']").attr("content")
            description = doc("meta[name='description']").attr("content")
            date = doc(
                "body > div.whole > div.list.left > div.new_article > p > span:nth-child(1)"
            ).text()
            # date = "2017-02-17T08:51:00.000Z"
            print(date)
            date = time.strftime(
                "%Y-%m-%dT%H:%M:%S.000Z", time.strptime(date, "%Y-%m-%d %H:%M")
            )
            suggestion = keywords
            suggest = title
            rawTitle = title
            host = get_domain(url)
            text = (
                doc("body > div.whole > div.list.left > div.new_article > div")
                .text()
                .replace("\n", "")
            )
            body = {
                "date": date,
                "keywords": keywords,
                "suggestion": suggestion,
                "description": description,
                "suggest": suggest,
                "title": title,
                "url": url,
                "statusMessage": "OK",
                "rawTitle": rawTitle,
                "host": host,
                "text": text,
                "statusCode": statusCode,
                "status": 1,
            }
            # print(json.dumps(body,ensure_ascii=False))
            res = es_client.index("idp", "doc", body, id=url)
            print(res)
            print("正确", statusCode, url)
            # break
        except Exception:
            traceback.print_exc()
            print("错误", url)

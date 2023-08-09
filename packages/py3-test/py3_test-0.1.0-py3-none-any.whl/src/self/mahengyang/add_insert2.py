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


del_url_set = set()
with open("add2.txt", encoding="utf-8") as f:
    for line in f.readlines():
        url = line.strip()
        try:
            r = requests.get(url, timeout=5, allow_redirects=False)
            if r.status_code != 200:
                del_url_set.add(url)
                print("xxxxxxxxxxxx", url)
            else:
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
                if not date and "ask" in url:
                    date = (
                        doc(
                            "body > div.wrapper.box.clearfix > div.left.box_left > div.yx_rz.clearfix > span:nth-child(2)"
                        )
                        .text()
                        .replace("更新", "")
                        + " 00:00"
                    )
                try:
                    date = time.strftime(
                        "%Y-%m-%dT%H:%M:%S.000Z", time.strptime(date, "%Y-%m-%d %H:%M")
                    )
                except Exception:
                    print("时间错误", url)
                    date = "1970-01-01T00:00:00.000Z"
                suggestion = keywords
                suggest = title
                rawTitle = title
                host = get_domain(url)
                text = (
                    doc("body > div.whole > div.list.left > div.new_article > div")
                    .text()
                    .replace("\n", "")
                )
                if not text and "ask" in url:
                    text = (
                        doc(
                            "body > div.wrapper.box.clearfix > div.left.box_left > div:nth-child(6) > div > h3"
                        )
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
        except Exception:
            traceback.print_exc()
            print("错误", url)

with open("del.txt", "w", encoding="utf-8") as fw:
    for url in del_url_set:
        fw.write(url + "\n")

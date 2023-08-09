"""
@Time   : 2019/3/21
@author : lijc210@163.com
@Desc:  : 功能描述。
"""

from es_client import EsClient

es_client = EsClient(hosts=["http://10.10.20.165:9200"])

body = {
    "query": {"bool": {"must": [{"term": {"project": {"value": "lianjia_newfang"}}}]}}
}
response = es_client.scan(index="pyspider", doc_type="result", body=body, size=1000)

for resp in response:
    _source = resp.get("_source")
    if _source:
        print(_source)
        break

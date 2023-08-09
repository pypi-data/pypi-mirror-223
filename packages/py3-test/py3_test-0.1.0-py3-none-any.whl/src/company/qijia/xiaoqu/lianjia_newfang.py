"""
@Time   : 2019/3/21
@author : lijc210@163.com
@Desc:  : 功能描述。
"""

from es_client import EsClient

es_client = EsClient(hosts=["http://10.10.20.165:9200"])

# body = {
#     "query": {
#         "bool": {
#             "must": [
#                 {
#                     "term": {
#                         "project": {
#                             "value": "lianjia_newfang"
#                         }
#                     }
#                 }
#             ]
#         }
#     },
#     "aggs": {
#         "city_name": {
#             "terms": {
#                 "field": "result.city_name",
#                 "size": 100
#             }
#         }
#     }
# }
# response = es_client.search(index="pyspider", doc_type="result", body=body)
#
# buckets = response["aggregations"]["city_name"]["buckets"]
# print(len(buckets))

body = {
    "query": {"bool": {"must": [{"term": {"project": {"value": "lianjia_newfang"}}}]}}
}
response = es_client.scan(index="pyspider", doc_type="result", body=body, size=1000)

with open("lianjia.json", "w") as f:
    lianjia_dict = {}
    for resp in response:
        _source = resp.get("_source")
        if _source:
            # print(_source)
            city_name = _source.get("city_name", "")
            house_type = _source.get("house_type", "")

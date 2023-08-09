"""
@Time   : 2019-08-07
@author : lijc210@163.com
@Desc:  : 功能描述。
"""
import copy

from elasticsearch import Elasticsearch, helpers

ES_HOST = ["http://127.0.0.1:9200"]

es_client = Elasticsearch(
    ES_HOST,
    retry_on_timeout=True,
    timeout=100,
    max_retries=3,
    sniff_on_start=True,
    sniff_on_connection_fail=True,
    sniffer_timeout=60,
)

data = [
    ("1", "案例", ["成功", "案例", "故事"]),
    ("2", "择校", ["中学推荐", "大学推荐", "研究生推荐", "本科推荐", "预科推荐", "tafa推荐"]),
    # (2,"择校",[]),
    ("3", "行前", ["行李", "体检", "登机", "接机", "机票", "汇学率", "汇率", "行前", "日用品", "药品"]),
    ("4", "申请条件", ["申请", "条件", "方案"]),
    (
        "4",
        "费用",
        [
            "费用",
            "花费",
            "多少钱",
            "贵",
            "性价比",
            "学费",
            "生活费",
            "交通费",
            "澳元",
            "美元",
            "英镑",
            "欧元",
            "港币",
            "新西兰元",
        ],
    ),
    ("5", "排名", ["排名", "QS", "THE", "USNEWS", "CUG", "软科", "ranking", "rank"]),
    ("6", "申请条件", ["奖学金", "奖金"]),
    ("6", "专业", ["专业", "课程"]),
    ("6", "签证", ["签证", "visa", "资金担保", "存款证明"]),
    ("7", "申请条件", ["文书", "套磁", "背景提升", "面试", "个人简介", "PS"]),
    ("8", "实习就业", ["实习", "就业"]),
    (
        "9",
        "生活",
        [
            "生活",
            "安全",
            "住宿",
            "假日",
            "节日",
            "文化",
            "暑假",
            "寒假",
            "放假",
            "假期",
            "风景",
            "美食",
            "食堂",
            "交通",
            "购物",
        ],
    ),
    ("10", "申请条件", ["难", "简单", "易"]),
    # ("11","政策",[]),
]

# res = es_client.get("idp",1, doc_type="doc")
# print res
# res = es_client.search(index="idp", doc_type="doc", body=body)
# print res
school_set = set()
with open("合并.txt") as f:
    for line in f.readlines():
        school_set.add(line.strip())

id_set = set()

with open("1.txt", "w") as f:
    # 最后
    data_list = []
    body = {}
    # body = {
    #     "query": {
    #         "term": {
    #             "_id": {
    #                 "value": "http://www.idp.cn/meiguo/shenghuojiuye-WY1006/87068.html"
    #             }
    #         }
    #     },
    #     "_source": [
    #         "id",
    #         "title"
    #     ]
    # }
    response = helpers.scan(
        es_client,
        index="idp",
        doc_type="doc",
        query=body,
        scroll="5m",
        raise_on_error=True,
        preserve_order=False,
        size=5000,
        request_timeout=None,
        clear_scroll=True,
    )
    for resp in response:
        if "_source" in resp:
            _id = resp["_id"]
            title = resp["_source"]["title"].replace("\n", "").replace("\r", "")
            data_list.append((_id, title))

    print("数量", len(data_list))

    for _id, title in data_list:
        print(_id)
        is_match = False
        for school1 in school_set:
            if school1 in title:
                two_school = False
                tmp_school_set = copy.copy(school_set)
                tmp_school_set.remove(school1)
                for school2 in tmp_school_set:
                    if school2 in school1 or school1 in school2:
                        continue
                    if school2 in title:
                        two_school = True
                        is_match = True
                        tmp = ["2", "择校", school1 + "," + school2, _id, title]
                        f.write("\t".join(tmp) + "\n")
                        break
                if two_school is False:
                    if "简介" in title:
                        is_match = True
                        tmp = ["2", "择校", school1 + "," + "简介", _id, title]
                        f.write("\t".join(tmp) + "\n")
                    elif "介绍" in title:
                        is_match = True
                        tmp = ["2", "择校", school1 + "," + "介绍", _id, title]
                        f.write("\t".join(tmp) + "\n")
        if is_match is False:
            is_in2 = False
            for alist in data:
                is_in = False
                for keywords in alist[2]:
                    if keywords in title:
                        tmp = [alist[0], alist[1], keywords, _id, title]
                        f.write("\t".join(tmp) + "\n")
                        is_in = True
                        break
                if is_in:
                    is_in2 = True
                    break
            if is_in2 is False:
                tmp = ["11", "政策", "", _id, title]
                f.write("\t".join(tmp) + "\n")

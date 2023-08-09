import requests

id_list = []
for i in range(1, 100):
    body = {
        "api": "pic_page_tuijian",
        "pagesize": 1,
        "pt": "wap",
        "column": ["id"],
        "table": "aabb.v9_picture_page",
        "sortby": "attr",
        "id": 1058019,
        "page": i,
        "must": [{"terms": {"catid": ["360", "525"]}}],
        "should": [{"range": {"height_int": {"gte": 10000}}}],
    }

    r = requests.post("http://bi-python.api.tg.local/tuijian/", json=body)
    # r = requests.post("http://127.0.0.1:9033/tuijian/",json=body)
    # r = requests.post("http://10.10.11.2:9033/tuijian/",json=body)
    res_dict = r.json()
    print(res_dict)
    id_list.append(res_dict["result"]["list"]["0"]["id"])

print(id_list)
print(len(id_list))
print(len(set(id_list)))

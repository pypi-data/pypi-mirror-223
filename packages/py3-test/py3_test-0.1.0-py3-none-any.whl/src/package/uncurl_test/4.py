"""
@Time   : 2019/4/1
@author : lijc210@163.com
@Desc:  : 功能描述。
"""
import json
import re
import time

import requests

for x in range(30):
    rn = 50  # 每页50
    pn = x * rn

    r = requests.get(
        "https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php?resource_id=6899&query=%E5%A4%B1%E4%BF%A1&pn={pn}&rn={rn}&ie=utf-8&oe=utf-8&format=json&t=1557111304004&cb=jQuery1102005364097566514636_1557107899680&_=1557107899762".format(
            pn=pn, rn=rn
        ),
        headers={
            "Referer": "https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&rsv_idx=1&tn=baidu&wd=%E5%A4%B1%E4%BF%A1&oq=%25E4%25BF%25A1%25E7%2594%25A8%25E4%25B8%25AD%25E5%259B%25BD&rsv_pq=8486ec850000099d&rsv_t=e90bQj6L8XZNWTB328LlCbrqYDdUe7TuhRtfY5fqACDi76B75Ow9ZS%2F9UsA&rqlang=cn&rsv_enter=0&inputT=1250&rsv_sug3=30&rsv_sug1=37&rsv_sug7=100&rsv_n=2&rsv_sug4=1250&rsv_sug=1",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36",
        },
        cookies={},
    )

    tmp_text = (
        re.search("\\({.*}\\)", r.text).group(0).replace("(", "").replace(")", "")
    )

    tmp_dict = json.loads(tmp_text)

    data_list = tmp_dict["data"][0]["result"]

    for adict in data_list:
        print(adict["iname"], adict["cardNum"])
    time.sleep(2)

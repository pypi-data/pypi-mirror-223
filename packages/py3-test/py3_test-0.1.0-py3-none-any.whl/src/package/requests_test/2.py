"""
@author: lijc210@163.com
@file: 2.py
@time: 2019/10/08
@desc: 功能描述。
"""
import requests

url = "http://10.10.11.24:10005/user/getUserAvatar"
params = {
    "app_id": "500",
    "user_ids": [110889494, 109303300, 109303300, 116637892, 116637892],
}
print(requests.post(url, json=params).text)

# import json
# import urllib.request
#
#
#
#
# params = json.dumps(params)
# headers = {'Accept-Charset': 'utf-8', 'Content-Type': 'application/json'}
# params = bytes(params, 'utf8')
#
# req = urllib.request.Request(url=url, data=params, headers=headers, method='POST')
# response = urllib.request.urlopen(req).read()
# print(response)

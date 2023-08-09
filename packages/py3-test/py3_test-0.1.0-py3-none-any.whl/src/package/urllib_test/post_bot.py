"""
@author: lijc210@163.com
@file: post.py
@time: 2019/10/08
@desc: 功能描述。
"""
import json
import urllib.request

url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=a4ade9f2-068a-4837-8d68-07d405838fe7"
data = {
    "msgtype": "text",
    "text": {
        "content": "test",
        "mentioned_list": [],
    },
}
params = json.dumps(data)
headers = {"Accept-Charset": "utf-8", "Content-Type": "application/json"}
params = bytes(params, "utf8")

req = urllib.request.Request(url=url, data=params, headers=headers, method="POST")
response = urllib.request.urlopen(req).read()
print(response)

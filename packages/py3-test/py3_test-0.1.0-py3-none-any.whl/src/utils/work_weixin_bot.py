# Created on: 2021/3/11 11:11
# Email: lijicong@163.com
# desc
import requests
from retry import retry


@retry(tries=2, delay=60)
def send_text(key, content, mentioned_list=None):
    if mentioned_list is None:
        mentioned_list = []
    data = {
        "msgtype": "text",
        "text": {
            "content": content,
            "mentioned_list": mentioned_list,
        },
    }
    url = f"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={key}"
    res = requests.post(url, json=data, headers={"Content-Type": "application/json"})
    if res.json().get("errcode") == 45009:  # 接口调用超过限制
        raise ValueError(res.text)
    elif res.json().get("errcode") != 0:
        data = {
            "msgtype": "text",
            "text": {
                "content": res.json().get("errmsg", ""),
                "mentioned_list": mentioned_list,
            },
        }
        requests.post(url, json=data, headers={"Content-Type": "application/json"})
    else:
        print(res.text)
    return res.json()


@retry(tries=2, delay=60)
def send_img(key, md5, base64_data):
    data = {"msgtype": "image", "image": {"base64": base64_data, "md5": md5}}
    url = f"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={key}"
    res = requests.post(url, json=data, headers={"Content-Type": "text/plain"})
    if res.json().get("errcode") == 45009:  # 接口调用超过限制
        raise ValueError(res.text)
    elif res.json().get("errcode") != 0:
        data = {
            "msgtype": "text",
            "text": {
                "content": res.json().get("errmsg", ""),
                "mentioned_list": ["@all"],
            },
        }
        requests.post(url, json=data, headers={"Content-Type": "application/json"})
    else:
        print(res.text)
    return res.json()


@retry(tries=2, delay=60)
def upload_media(key, file_name, data):
    url = (
        f"https://qyapi.weixin.qq.com/cgi-bin/webhook/upload_media?key={key}&type=file"
    )
    res = requests.post(url, files={"image": (file_name, data)})
    if res.json().get("errcode") == 45009:  # 接口调用超过限制
        raise ValueError(res.text)
    elif res.json().get("errcode") != 0:
        data = {
            "msgtype": "text",
            "text": {
                "content": res.json().get("errmsg", ""),
                "mentioned_list": ["@all"],
            },
        }
        requests.post(url, json=data, headers={"Content-Type": "application/json"})
    else:
        print(res.text)
    return res.json()


@retry(tries=2, delay=60)
def send_file(key, media_id):
    data = {"msgtype": "file", "file": {"media_id": media_id}}
    url = f"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={key}"
    res = requests.post(url, json=data, headers={"Content-Type": "application/json"})
    if res.json().get("errcode") == 45009:  # 接口调用超过限制
        raise ValueError(res.text)
    elif res.json().get("errcode") != 0:
        data = {
            "msgtype": "text",
            "text": {
                "content": res.json().get("errmsg", ""),
                "mentioned_list": ["@all"],
            },
        }
        requests.post(url, json=data, headers={"Content-Type": "application/json"})
    else:
        print(res.text)
    return res.json()


if __name__ == "__main__":
    send_text("a4ade9f2-068a-4837-8d68-07d405838fe7", "test", ["@all"])

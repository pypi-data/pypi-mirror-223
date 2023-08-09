"""
Created on 2017/6/15 0015
@author: lijc210@163.com
Desc: 功能描述。
"""
import json
import os
import sys
import time
import traceback
import warnings

import requests

warnings.filterwarnings("ignore")


class Weixin:
    """
    save corp_id, secret
    save token and refresh every 7200 Seconds

    #企业号开发者平台，发送消息文档
    http://qydev.weixin.qq.com/wiki/index.php?title=%E6%B6%88%E6%81%AF%E7%B1%BB%E5%9E%8B%E5%8F%8A%E6%95%B0%E6%8D%AE%E6%A0%BC%E5%BC%8F
    """

    URL_GET_TOKEN = "https://qyapi.weixin.qq.com/cgi-bin/gettoken"  # get method, 1)corpid,2)corpsecret
    URL_SEND_MSG = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token="  # access_token=ACCESS_TOKEN, post method
    TOKEN_COTENT = ".TOKEN_CONTENT"
    TOKEN_TIMESTAMP = ".TOKEN_TIMESTAMP"

    def __init__(self):
        # 1000012: 企业应用: BI_python脚本报警
        # 1000013: 企业应用: BI_数据统计通知
        self.send_list_dict = {
            1000012: {
                "corp_id": "wx12e5bb9ec21908f5",
                "secret": "hOkvyG-XOS2fv0wUnqzKeWIoRnkBW9yHHIrhHhobluI",
                "touser": "@all",
                "toparty": "29",
                "agentid": 1000012,
            },
            1000013: {
                "corp_id": "wx12e5bb9ec21908f5",
                "secret": "tuhKyZcdSK-lscf6leCgxfZhW1OnrIpiTWUdWoMNBIk",
                "touser": "@all",
                "toparty": "29",
                "agentid": 1000013,
            },
        }

        self.diff = 7000

    def send(self, agentid=None, text=None):
        send_dict = self.send_list_dict[agentid]
        _corp_id = send_dict["corp_id"]
        _secret = send_dict["secret"]
        _touser = send_dict["touser"]
        _toparty = send_dict["toparty"]
        _agentid = send_dict["agentid"]

        try:
            self.TOKEN_COTENT = self.TOKEN_COTENT + str(_agentid)
            self.TOKEN_TIMESTAMP = self.TOKEN_TIMESTAMP + str(_agentid)
            token = self.refresh_token(_corp_id, _secret)
            payload = {
                "touser": _touser,
                "toparty": _agentid,
                "msgtype": "text",
                "agentid": _agentid,
                "text": {"content": str(text)},
                "safe": "0",
            }
            response = requests.post(
                self.URL_SEND_MSG + token,
                data=json.dumps(payload, ensure_ascii=False),
                verify=False,
            )
            response_json = response.json()
            if response_json["errcode"] == 0:
                print("success")
            else:
                print("fail")
        except Exception:
            traceback.print_exc()

    def refresh_token(self, _corp_id, _secret):
        last_time = 0
        need_refresh = False
        if os.path.exists(self.TOKEN_TIMESTAMP):
            f_time = open(self.TOKEN_TIMESTAMP)
            last_time = float(f_time.read())

        current_time = time.time()
        if current_time - last_time > self.diff:  # need refresh
            need_refresh = True

        if not os.path.exists(self.TOKEN_COTENT):
            need_refresh = True

        if need_refresh:
            f_time = open(self.TOKEN_TIMESTAMP, "w")
            f_time.write(str(time.time()))
            f_time.close()

            payload = {"corpid": _corp_id, "corpsecret": _secret}
            response = requests.get(self.URL_GET_TOKEN, params=payload, verify=False)
            response_json = response.json()
            # print response_json

            token = response_json["access_token"]
            f_content = open(self.TOKEN_COTENT, "w")
            f_content.write(token)
            f_content.close()
        else:
            f_content = open(self.TOKEN_COTENT)
            token = f_content.read()
            f_content.close()
        return token


if __name__ == "__main__":
    if len(sys.argv) == 2:
        content = sys.argv[1]
    else:
        content = "测试"
    weixin = Weixin()
    weixin.send(agentid=1000012, text=content)

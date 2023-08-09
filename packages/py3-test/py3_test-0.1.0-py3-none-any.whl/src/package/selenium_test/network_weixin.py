"""
@Time   : 2019/3/28
@author : lijc210@163.com
@Desc:  : 功能描述。
"""
import json
import re
import time

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from utils.utils import process_login_info, s

caps = DesiredCapabilities.CHROME
caps["loggingPrefs"] = {"performance": "ALL"}
# driver = webdriver.Chrome(desired_capabilities=caps, executable_path="./chromedriver")
driver = webdriver.Chrome(desired_capabilities=caps)

driver.get("https://wx.qq.com/")

print(driver.log_types)
logs = [json.loads(log["message"])["message"] for log in driver.get_log("performance")]
logs1 = [json.loads(log["message"])["message"] for log in driver.get_log("browser")]
logs2 = [json.loads(log["message"])["message"] for log in driver.get_log("driver")]

global loginInfo

i = 0
while 1:
    i += 1
    if i % 10 == 0:  # 每10轮打印
        print("-" * 20)
    for log in driver.get_log("performance"):
        message = json.loads(log["message"])["message"]
        method = message["method"]
        if method == "Network.requestWillBeSent":
            request = message["params"]["request"]
            # print(request)
            postDataJson = request.get("postData")
            url = request.get("url")
            headers = request.get("headers")
            loginInfo = {}
            if "mmwebwx-bin/login" in url:  # 获取登录信息
                r = s.get(url, headers=headers)
                print(r.text)
                regx = r"window.code=(\d+)"
                data = re.search(regx, r.text)
                if data and data.group(1) == "200":
                    print("登录成功")
                    process_status, loginInfo = process_login_info(r.text)
                    if process_status:
                        print("loginInfo正常")
                        regx = r'window.redirect_uri="(\S+)";'
                        redirect_uri = re.search(regx, r.text).group(1)
                        driver.get(redirect_uri)  # 跳转到微信页面

                        # r = s.get(url, headers=headers)
                        # print(r.text)
                        # process_status, loginInfo = process_login_info(r.text)
                        # print(loginInfo)
                        # get_contact(loginInfo)
                    else:
                        break
            if "mmwebwx-bin/webwxgetcontact" in url:  # 获取联系信息
                pass

            # if postDataJson:
            #     if "mmwebwx-bin/webwxsendmsg" in url:  # 发送消息
            #         postData = json.loads(postDataJson)
            #         Msg = postData.get("Msg")
            #         if Msg:
            #             Content = ["Content"]
            #             ToUserName = postData["Msg"]["ToUserName"]
            #             print("发送消息", ToUserName, Content)
            #     elif "mmwebwx-bin/webwxsync" in url and loginInfo:  # 接收消息
            #         postData = json.loads(postDataJson)
            #         loginInfo.update(postData)
            #         print("收到消息", get_msg(loginInfo))
    time.sleep(2)

# driver.close()

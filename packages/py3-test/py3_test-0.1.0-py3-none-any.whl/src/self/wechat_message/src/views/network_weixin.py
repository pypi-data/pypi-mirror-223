"""
@Time   : 2019/3/28
@author : lijc210@163.com
@Desc:  : 功能描述。
msg_type 1代表发送消息，2代表接消息
msg_source 1代表普通消息，2代表群消息
"""
import json
import os
import re
import time
import traceback

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from utils.utils import (
    get_contact,
    get_msg,
    process_login_info,
    s,
    show_mobile_login,
    sqlite3_client,
    update_chatrooms,
    update_friends,
    web_init,
)

optons = webdriver.ChromeOptions()
optons.add_argument("--disk-cache-dir=./cache")

optons.add_argument("disable-infobars")  # 隐藏‘Chrome正在受到自动软件的控制’
caps = DesiredCapabilities.CHROME
caps["loggingPrefs"] = {"performance": "ALL"}

chromedriver_path = os.path.join(os.path.abspath(".."), "chromedriver")

try:
    driver = webdriver.Chrome(
        desired_capabilities=caps,
        chrome_options=optons,
        executable_path="c:\\chromedriver",
    )
    # driver = webdriver.Chrome(desired_capabilities=caps)
except Exception:
    traceback.print_exc()

# print(driver.log_types)
loginInfo, UserName_info_dict = {}, {}


def network_weixin():
    global loginInfo, UserName_info_dict
    driver.get("https://wx.qq.com/")
    i = 0
    isLoggedIn = False
    while 1:
        i += 1
        if i % 100 == 0:  # 每100轮打印
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
                if "mmwebwx-bin" in url:
                    if "mmwebwx-bin/login" in url and isLoggedIn is False:  # 获取登录信息
                        print("获取登录信息")
                        r = s.get(url, headers=headers)
                        print(url)
                        print(r.text)
                        regx = r"window.code=(\d+)"
                        data = re.search(regx, r.text)
                        if data and data.group(1) == "200":
                            print("登录成功")
                            isLoggedIn = True
                            process_status, loginInfo = process_login_info(r.text)
                            if process_status:
                                print("loginInfo正常")
                                regx = r'window.redirect_uri="(\S+)";'
                                redirect_uri = re.search(regx, r.text).group(1)
                                print("redirect_uri", redirect_uri)
                                # driver.get(redirect_uri)  # 跳转到微信页面

                                UserName_info_dict1 = web_init(loginInfo)
                                UserName_info_dict.update(UserName_info_dict1)

                                show_mobile_login(loginInfo)

                                UserName_info_dict2 = get_contact(loginInfo)
                                UserName_info_dict.update(UserName_info_dict2)
                                print("总人数", len(UserName_info_dict))

                                driver.get(redirect_uri)  # 跳转到微信页面
                            else:
                                print("loginInfo异常")
                                break
                    if not loginInfo or not UserName_info_dict:
                        print("失败，尝试重新登录")

                    if postDataJson:
                        if "mmwebwx-bin/webwxsendmsg" in url:  # 发送消息
                            postData = json.loads(postDataJson)
                            Msg = postData.get("Msg")
                            if Msg:
                                # print("Msg",Msg)
                                FromUserName = Msg["FromUserName"]
                                ToUserName = Msg["ToUserName"]
                                Content = Msg["Content"]
                                if Content:
                                    print(
                                        "收到消息",
                                        FromUserName,
                                        UserName_info_dict.get(
                                            FromUserName, "FromUserName未找到"
                                        ),
                                        ToUserName,
                                        UserName_info_dict.get(
                                            FromUserName, "ToUserName未找到"
                                        ),
                                        Content,
                                    )
                                    if "@@" in FromUserName:
                                        msg_source = 2
                                    else:
                                        msg_source = 1
                                    sql = (
                                        "INSERT INTO message (from_username,to_username,content,msg_type,msg_source,create_time) "
                                        "VALUES ('{from_username}','{to_username}' , '{content}',{msg_type},{msg_source}, {create_time})".format(
                                            from_username=FromUserName,
                                            to_username=ToUserName,
                                            content=Content,
                                            msg_type=1,
                                            msg_source=msg_source,
                                            create_time=int(time.time()),
                                        )
                                    )
                                    sqlite3_client.insert(sql)
                        elif "mmwebwx-bin/webwxsync" in url and loginInfo:  # 接收消息
                            postData = json.loads(postDataJson)
                            loginInfo.update(postData)
                            AddMsgList, ModContactList = get_msg(loginInfo)
                            if not AddMsgList:
                                continue
                            for Msg in AddMsgList:
                                # print("Msg", Msg)
                                StatusNotifyUserName = Msg["StatusNotifyUserName"]
                                FromUserName = Msg["FromUserName"]
                                ToUserName = Msg["ToUserName"]
                                Content = Msg["Content"]
                                usernames = StatusNotifyUserName.split(",")
                                if usernames:
                                    user_name_list = []
                                    chatroom_list = []
                                    for username in usernames:
                                        if "@@" in username:
                                            chatroom_list.append(username)
                                        elif "@" in username:
                                            user_name_list.append(username)
                                    if chatroom_list:
                                        UserName_info_dict3 = update_chatrooms(
                                            loginInfo, chatroom_list
                                        )
                                        UserName_info_dict.update(UserName_info_dict3)
                                        # UserName_info_dict4=update_chatrooms_all(loginInfo, chatroom_list)
                                        # UserName_info_dict.update(UserName_info_dict4)
                                    if user_name_list:
                                        UserName_info_dict4 = update_friends(
                                            loginInfo, user_name_list
                                        )
                                        UserName_info_dict.update(UserName_info_dict4)

                                if Content:
                                    print(
                                        "收到消息",
                                        FromUserName,
                                        UserName_info_dict.get(
                                            FromUserName, "FromUserName未找到"
                                        ),
                                        ToUserName,
                                        UserName_info_dict.get(
                                            FromUserName, "ToUserName未找到"
                                        ),
                                        Content,
                                    )
                                    if "@@" in FromUserName:
                                        msg_source = 2
                                    else:
                                        msg_source = 1
                                    sql = (
                                        "INSERT INTO message (from_username,to_username,content,msg_type,msg_source,create_time) "
                                        "VALUES ('{from_username}','{to_username}' , '{content}',{msg_type},{msg_source}, {create_time})".format(
                                            from_username=FromUserName,
                                            to_username=ToUserName,
                                            content=Content,
                                            msg_type=2,
                                            msg_source=msg_source,
                                            create_time=int(time.time()),
                                        )
                                    )
                                    sqlite3_client.insert(sql)
        time.sleep(1)


if __name__ == "__main__":
    try:
        network_weixin()
    except Exception:
        traceback.print_exc()
        driver.close()

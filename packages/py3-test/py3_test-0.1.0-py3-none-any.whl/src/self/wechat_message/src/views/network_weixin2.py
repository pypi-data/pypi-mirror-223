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
from src.views.html_js import get_add_script, get_menu_script, get_script, quick_reply

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

optons.add_argument("disable-infobars")  # 隐藏‘Chrome正在受到自动软件的控制’
optons.add_argument("--window-size=1960,1080")
caps = DesiredCapabilities.CHROME
caps["loggingPrefs"] = {"performance": "ALL"}

# chromedriver_path = os.path.join(os.path.abspath(".."), "chromedriver")

# print(driver.log_types)
loginInfo, UserName_info_dict = {}, {}


def network_login():
    if not os.path.exists("wechat.db"):
        print("重新生成wechat.db")
        sqlite3_client.execute(
            """
                CREATE TABLE user
               (user_name   PRIMARY KEY   NOT NULL ,
                nick_name   CHAR(50)                ,
                remark_name   CHAR(50)                ,
                head_img_url      CHAR(50)               )
        """
        )
        sqlite3_client.execute(
            """
                CREATE TABLE message
               (from_username   CHAR(50)                ,
               to_username   CHAR(50)                ,
               content   TEXT                ,
               msg_type      TINYINT                 ,
               msg_source      TINYINT                 ,
               create_time   INT                )
        """
        )
    redirect_uri = ""
    global loginInfo, UserName_info_dict
    try:
        driver = webdriver.Chrome(
            desired_capabilities=caps,
            chrome_options=optons,
            executable_path="c:\\chromedriver",
        )
        # driver = webdriver.Chrome(desired_capabilities=caps)
    except Exception:
        traceback.print_exc()
    else:
        driver.get("https://wx.qq.com/")
        i = 0
        isLoggedIn = False
        while isLoggedIn is False:
            i += 1
            if i % 100 == 0:  # 每100轮打印
                print("-" * 20)
            for log in driver.get_log("performance"):
                message = json.loads(log["message"])["message"]
                method = message["method"]
                if method == "Network.requestWillBeSent":
                    request = message["params"]["request"]
                    # print(request)
                    request.get("postData")
                    url = request.get("url")
                    headers = request.get("headers")
                    if "mmwebwx-bin" in url:
                        if "mmwebwx-bin/login" in url and isLoggedIn is False:  # 获取登录信息
                            print("获取登录信息")
                            r = s.get(url, headers=headers)
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

                                    driver.close()
                                else:
                                    print("loginInfo异常")
                                    break
    return redirect_uri


def network_weixin(redirect_uri):
    time.sleep(10)
    try:
        driver = webdriver.Chrome(
            desired_capabilities=caps,
            chrome_options=optons,
            executable_path="c:\\chromedriver",
        )
        # driver = webdriver.Chrome(desired_capabilities=caps)
    except Exception:
        traceback.print_exc()
    else:
        driver.get(redirect_uri)
        js1 = """$("body > div.main").css("float","left");
                $("body > div.main").css("margin-left","10%");
                var html="{html}";
                var script="{script}";
                var add_script='{add_script}';
                $('body > div.main').after(html);
                $('body > div.main').after(script);
                $('body > div.main').after(add_script);
        """.format(
            html=quick_reply(), script=get_script(), add_script=get_add_script()
        )
        js2 = """
                var menu_script="{menu_script}";
                $('body > div.main').after(menu_script);
        """.format(
            menu_script=get_menu_script()
        )
        driver.execute_script(js1)
        time.sleep(5)
        driver.execute_script(js2)
        i = 0
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
                    request.get("headers")
                    if "mmwebwx-bin" in url:
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
                                            "发送消息",
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
                                            UserName_info_dict.update(
                                                UserName_info_dict3
                                            )
                                        if user_name_list:
                                            UserName_info_dict4 = update_friends(
                                                loginInfo, user_name_list
                                            )
                                            UserName_info_dict.update(
                                                UserName_info_dict4
                                            )

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
            # try:
            #     driver.find_element_by_class_name("quick_reply")
            # except Exception:
            #     driver.execute_script(js1)
            #     time.sleep(1)
            #     driver.execute_script(js2)


def main():
    try:
        redirect_uri = network_login()
        network_weixin(redirect_uri)
    except Exception:
        traceback.print_exc()


if __name__ == "__main__":
    main()

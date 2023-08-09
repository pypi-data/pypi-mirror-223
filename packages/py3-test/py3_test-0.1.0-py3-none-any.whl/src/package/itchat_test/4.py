"""
@Time   : 2019/5/20
@author : lijc210@163.com
@Desc:  : 功能描述。
"""
import json

import itchat
from itchat.content import FRIENDS

itchat.auto_login(hotReload=True)

itchat.send("Hello, filehelper", toUserName="filehelper")


@itchat.msg_register(itchat.content.TEXT)
def text_reply(msg):
    print(msg.text)
    print(msg.user)
    # return msg.text


@itchat.msg_register(FRIENDS)
def add_friend(msg):
    msg.user.verify()
    msg.user.send("Nice to meet you!")


print(itchat.search_friends(wechatAccount="lijc210"))
print(itchat.search_friends(name="lijc210"))
print(itchat.search_friends(name="李继聪"))
print(itchat.search_friends(nickName="李继聪"))
Chatroom = itchat.search_chatrooms(name="相亲相爱一家人")
print(json.dumps(Chatroom))

# 获取群及成员
chatroomList = itchat.get_chatrooms(True)
for i in range(len(chatroomList)):
    print(
        "序号：%s   NickName：%s   key: %s"
        % (i + 1, chatroomList[i]["NickName"], chatroomList[i]["UserName"])
    )

chatrooms_key = input("请输入要获取群号成员的的key:\n")
itchat.update_chatroom(chatrooms_key, detailedMember=True)
chatroomList = itchat.get_chatrooms(True)
for i in range(len(chatroomList)):
    if chatroomList[i]["UserName"] == chatrooms_key:
        for adict in chatroomList[i]["MemberList"]:
            print(adict["NickName"], adict["UserName"])
            r = itchat.add_friend(userName=adict["UserName"], status=2)
            print("添加结果", r)
itchat.get_chatrooms(True)

itchat.run()

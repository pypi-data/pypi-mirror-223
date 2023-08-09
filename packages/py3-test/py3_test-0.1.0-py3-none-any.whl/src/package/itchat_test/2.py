"""
@Time   : 2019/5/20
@author : lijc210@163.com
@Desc:  : 功能描述。
"""
import itchat
from itchat.content import (
    ATTACHMENT,
    CARD,
    FRIENDS,
    MAP,
    NOTE,
    PICTURE,
    RECORDING,
    SHARING,
    TEXT,
    VIDEO,
)


@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING])
def text_reply(msg):
    print(msg)
    if msg.user.RemarkName in ["陈城", "谢彦彬"] or msg.user.NickName in ["陈城", "谢彦彬"]:
        print("aaaaaa")
        msg.user.send("{}: {}".format(msg.type, msg.text))


@itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO])
def download_files(msg):
    print(msg)
    msg.download(msg.fileName)
    if msg.user.RemarkName in ["陈城", "谢彦彬"] or msg.user.NickName in ["陈城", "谢彦彬"]:
        typeSymbol = {
            PICTURE: "img",
            VIDEO: "vid",
        }.get(msg.type, "fil")
        return "@{}@{}".format(typeSymbol, msg.fileName)


@itchat.msg_register(FRIENDS)
def add_friend(msg):
    msg.user.verify()
    msg.user.send("Nice to meet you!")


@itchat.msg_register(TEXT, isGroupChat=True)
def text_reply1(msg):
    print(msg)
    print(msg.user.NickName)
    if msg.user.NickName == "群消息测试":
        # if msg.isAt:
        msg.user.send("@{}\u2005I received: {}".format(msg.actualNickName, msg.text))


itchat.auto_login(True)
itchat.run(True)

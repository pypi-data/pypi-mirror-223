"""
@File    :   wechat_everyday.py
@Time    :   2022/01/20 19:14:02
@Author  :   lijc210@163.com
@Desc    :
"""
import random
import time

import itchat
import requests
from apscheduler.schedulers.blocking import BlockingScheduler

key = "9efde80421f85748192c9b2e76c356ac"
city = "阳江市"
url = "http://api.tianapi.com"

headers = {"Content-type": "application/x-www-form-urlencoded"}


def day_now(outfmt="%Y-%m-%d %H:%M:%S"):
    """
    当前时间格式化
    :param days:
    :param outfmt:
    :return:
    """
    return time.strftime(outfmt, time.localtime(time.time()))


def send_tianqi(toUserName="filehelper"):
    # 天气
    res1 = requests.post(
        f"http://api.tianapi.com/tianqi/index?key={key}&city={city}", headers=headers
    )
    newslist1 = res1.json().get("newslist", [])

    # 质量
    res2 = requests.post(
        f"http://api.tianapi.com/aqi/index?key={key}&area={city}", headers=headers
    )
    newslist2 = res2.json().get("newslist", [])
    # print(res2.text)

    if newslist1:
        data = newslist1[0]
        area = data["area"]
        weather = data["weather"]
        lowest = data["lowest"]
        highest = data["highest"]
        wind = data["wind"]
        windsc = data["windsc"]
        tips = data["tips"]

        if newslist2:
            data2 = newslist2[0]
            pm2_5 = data2["pm2_5"]
            quality = data2["quality"]

            text = (
                f"{area}天气预报\n"
                + f"【今日天气】{weather}\n"
                + f"【今日温度】低温 {lowest},高温 {highest}\n"
                + f"【今日风速】{wind}{windsc}\n"
                + f"【空气质量】{quality} pm2.5:{pm2_5}\n"
                + f"【出行提示】{tips}\n"
            )
            print(text)
            itchat.send(text, toUserName=toUserName)


def send_one(toUserName="filehelper"):
    # one
    dt = day_now("%Y-%m-%d")
    res1 = requests.post(
        f"http://api.tianapi.com/one/index?key={key}&date={dt}", headers=headers
    )
    newslist1 = res1.json().get("newslist", [])
    if newslist1:
        data = newslist1[0]
        word = data["word"]
        imgurl = data["imgurl"]
        img = requests.get(imgurl, headers=headers)
        file_name = "one_" + str(int(time.time())) + ".png"
        with open(file_name, "wb") as f:
            f.write(img.content)
        text = f"每日一句\n『 {word} 』"
        print(text)
        itchat.send(text, toUserName=toUserName)
        itchat.send_image(file_name, toUserName=toUserName)


def send_caihongpi(toUserName="filehelper"):
    # 彩虹屁
    res1 = requests.post(
        f"http://api.tianapi.com/caihongpi/index?key={key}", headers=headers
    )
    newslist1 = res1.json().get("newslist", [])
    if newslist1:
        data = newslist1[0]
        content = data["content"]
        text = f"每日一句\n『 {content} 』"
        print(text)
        itchat.send(text, toUserName=toUserName)


def send_saylove(toUserName="filehelper"):
    # 土味情话
    res1 = requests.post(
        f"http://api.tianapi.com/saylove/index?key={key}", headers=headers
    )
    newslist1 = res1.json().get("newslist", [])
    if newslist1:
        data = newslist1[0]
        text = data["content"]
        print(text)
        itchat.send(text, toUserName=toUserName)


def send_sentence(toUserName="filehelper"):
    # 精美句子
    res1 = requests.post(
        f"http://api.tianapi.com/sentence/index?key={key}", headers=headers
    )
    newslist1 = res1.json().get("newslist", [])
    if newslist1:
        data = newslist1[0]
        text = data["content"]
        print(text)
        itchat.send(text, toUserName=toUserName)


def send_dialogue(toUserName="filehelper"):
    # 经典台词
    res1 = requests.post(
        f"http://api.tianapi.com/dialogue/index?key={key}", headers=headers
    )
    newslist1 = res1.json().get("newslist", [])
    if newslist1:
        data = newslist1[0]
        dialogue = data["dialogue"]
        source = data["source"]
        english = data["english"]
        text = f"《{source}》\n" + f"{english}\n" + f"{dialogue}"

        print(text)
        itchat.send(text, toUserName=toUserName)


def send_pyqwenan(toUserName="filehelper"):
    # 经典台词
    res1 = requests.post(
        f"http://api.tianapi.com/pyqwenan/index?key={key}", headers=headers
    )
    newslist1 = res1.json().get("newslist", [])
    if newslist1:
        data = newslist1[0]
        text = data["content"]
        print(text)
        itchat.send(text, toUserName=toUserName)


def send_mingyan(toUserName="filehelper"):
    # 经典台词
    res1 = requests.post(
        f"http://api.tianapi.com/mingyan/index?key={key}", headers=headers
    )
    newslist1 = res1.json().get("newslist", [])
    if newslist1:
        data = newslist1[0]
        author = data["author"]
        content = data["content"]
        text = f"{content}——{author}"
        print(text)
        itchat.send(text, toUserName=toUserName)


def send_everyday(toUserName="filehelper"):
    # 每日一句
    dt = day_now("%Y-%m-%d")
    res1 = requests.post(
        f"http://api.tianapi.com/everyday/index?key={key}&date={dt}", headers=headers
    )
    newslist1 = res1.json().get("newslist", [])
    if newslist1:
        data = newslist1[0]
        imgurl = data["imgurl"]
        img = requests.get(imgurl, headers=headers)
        file_name = "everyday_" + str(int(time.time())) + ".png"
        with open(file_name, "wb") as f:
            f.write(img.content)
        itchat.send_image(file_name, toUserName=toUserName)


def send_mgjuzi(toUserName="filehelper"):
    # 民国句子
    res1 = requests.post(
        f"http://api.tianapi.com/mgjuzi/index?key={key}", headers=headers
    )
    newslist1 = res1.json().get("newslist", [])
    if newslist1:
        data = newslist1[0]
        author = data["author"]
        content = data["content"]
        text = f"{content}——{author}"
        print(text)
        itchat.send(text, toUserName=toUserName)


def send_qingshi(toUserName="filehelper"):
    # 民国句子
    res1 = requests.post(
        f"http://api.tianapi.com/mgjuzi/index?key={key}", headers=headers
    )
    newslist1 = res1.json().get("newslist", [])
    if newslist1:
        data = newslist1[0]
        author = data["author"]
        content = data["content"]
        text = f"{content}——{author}"
        print(text)
        itchat.send(text, toUserName=toUserName)


def send_qingshi2(toUserName="filehelper"):
    # 古代情诗
    res1 = requests.post(
        f"http://api.tianapi.com/qingshi/index?key={key}", headers=headers
    )
    newslist1 = res1.json().get("newslist", [])
    if newslist1:
        data = newslist1[0]
        source = data["source"]
        author = data["author"]
        content = data["content"]
        text = f"《{source}》\n{content}——{author}"
        print(text)
        itchat.send(text, toUserName=toUserName)


def send_ensentence(toUserName="filehelper"):
    # 英语一句话
    res1 = requests.post(
        f"http://api.tianapi.com/ensentence/index?key={key}", headers=headers
    )
    newslist1 = res1.json().get("newslist", [])
    if newslist1:
        data = newslist1[0]
        en = data["en"]
        zh = data["zh"]
        text = f"{en}\n{zh}"
        print(text)
        itchat.send(text, toUserName=toUserName)


def send_qinghua(toUserName="filehelper"):
    # 本地情话
    text_set = set()
    with open("qinghua.txt", encoding="utf-8") as f:
        for line in f.readlines():
            # print(line)
            text_set.add(line.strip())
    text = random.choice(list(text_set))
    text = f"每日一句\n『 {text} 』"
    print(text)
    itchat.send(text, toUserName=toUserName)


def send_check():
    friends = itchat.search_friends(remarkName="阿里小号")
    print(friends)
    if friends:
        toUserName = friends[0]["UserName"]
        print(toUserName)
        text = "itchat检测"
        print(text)
        itchat.send(text, toUserName=toUserName)
        send_tianqi(toUserName=toUserName)
        send_qinghua(toUserName=toUserName)


def send():
    friends = itchat.search_friends(remarkName="李金鞠")
    print(friends)
    if friends:
        toUserName = friends[0]["UserName"]
        print(toUserName)
        send_tianqi(toUserName=toUserName)
        # send_one(toUserName=toUserName)
        # send_caihongpi(toUserName=toUserName)
        # send_saylove(toUserName=toUserName)
        # send_sentence(toUserName=toUserName)
        # send_dialogue(toUserName=toUserName)
        # send_pyqwenan(toUserName=toUserName)
        # send_mingyan(toUserName=toUserName)
        # send_everyday(toUserName=toUserName)
        # send_mgjuzi(toUserName=toUserName)
        # send_qingshi(toUserName=toUserName)
        # send_ensentence(toUserName=toUserName)
        send_qinghua(toUserName=toUserName)


def test():
    # itchat.auto_login(hotReload=True)
    # itchat.run()
    send_check()


def main(send_now=False):
    itchat.auto_login(hotReload=True)
    send_check()
    if send_now:
        send()
    else:
        sched = BlockingScheduler()
        print("start")
        # sched.add_job(send, 'cron', year=2021, month=2, day=20, hour=0o6, minute=30, second=0)
        sched.add_job(test, "cron", hour="22")
        sched.add_job(test, "cron", hour="23")
        sched.add_job(send, "cron", hour="6")
        sched.start()


if __name__ == "__main__":
    # test()
    main(send_now=False)
    # main(send_now=True)

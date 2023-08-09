"""
@File    :   domain.py
@Time    :   2022/11/22 10:53:35
@Author  :   lijc210@163.com
@Desc    :   None
"""
import json
import os

import pinyin
import requests


def search(domain):
    url = f"https://checkapi.aliyun.com/check/search?domainName={domain}"
    r = requests.post(url)
    res_dict = r.json()
    success = res_dict["success"]
    if success:
        universalList = res_dict["module"]["universalList"]
        for universal in universalList:
            domainName = universal["domainName"]
            if domainName == domain + ".com":
                break
    print(r.json())


def check(domain):
    url = f"https://checkapi.aliyun.com/check/domaincheck?domain={domain}&token=Y7f88c2e11099cf225343732a53298b5e"
    r = requests.post(url)
    res_dict = r.json()
    success = res_dict["success"]
    if success:
        avail = res_dict["module"]["domainDetail"]["avail"]
    else:
        avail = -1
        print(res_dict)
    return avail


def words():
    word_finish_set = set()
    if os.path.exists("word_finish.txt"):
        with open("word_finish.txt", encoding="utf-8") as f:
            for line in f.readlines():
                word_finish_set.add(line.strip())

    with open("word_result.txt", "a", encoding="utf-8") as f1:
        with open("word_finish.txt", "a", encoding="utf-8") as fw:
            with open("D:\\word.json", encoding="utf-8") as f:
                ajson = json.loads(f.read())
                text = ""
                word_str = ""
                for i, adict in enumerate(ajson, 1):
                    word = adict["word"]
                    if word not in word_finish_set:
                        word_py = pinyin.get(word, format="strip")
                        domain = word_py + ".com"
                        avail = check(domain)
                        print(i, word, domain, avail)
                        text += word + "\t" + domain + "\t" + str(avail) + "\n"
                        word_str += word + "\n"
                    if i % 100 == 0:
                        f1.write(text)
                        fw.write(word_str)
                        text = ""
                        word_str = ""


if __name__ == "__main__":
    # search("baidu")
    # check("baidu.com")
    words()

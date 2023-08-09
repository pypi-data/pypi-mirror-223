"""
@author: lijc210@163.com
@file: add.py
@time: 2019/08/27
@desc: 功能描述。
"""
all_url_set = set()
with open("文章1.txt", encoding="utf-8") as f:
    for line in f.readlines():
        url = line.strip()
        all_url_set.add(url)

with open("文章2.txt", encoding="utf-8") as f:
    for line in f.readlines():
        url = line.strip()
        all_url_set.add(url)

print("all_url_set", len(all_url_set))

es_all_url_set = set()
with open("all.txt", encoding="utf-8") as f:
    for line in f.readlines():
        url = line.strip()
        es_all_url_set.add(url)

print("es_all_url_set", len(es_all_url_set))

add_url_set = all_url_set - es_all_url_set

print("add_url_set", len(add_url_set))

with open("add.txt", "w", encoding="utf-8") as f:
    for url in add_url_set:
        if "http" in url:
            f.write(url + "\n")

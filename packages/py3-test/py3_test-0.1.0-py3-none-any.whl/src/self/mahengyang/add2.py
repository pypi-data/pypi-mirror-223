"""
@author: lijc210@163.com
@file: add.py
@time: 2019/08/27
@desc: 功能描述。
"""
add_url_set = set()
with open("all.txt", encoding="utf-8") as f:
    for line in f.readlines():
        if line.strip():
            line_list = line.replace("\n", "").split("\t")
            category = line_list[0]
            keywords = line_list[1]
            url = line_list[2]
            title = line_list[3]
            if (
                "Redirecting" in title
                or "Not Found" in title
                or title == ""
                or "301" in title
                or "404" in title
                or "502" in title
                or "error" in title
            ):
                add_url_set.add(url)

with open("add2.txt", "w", encoding="utf-8") as f:
    for url in add_url_set:
        if "http" in url:
            f.write(url + "\n")

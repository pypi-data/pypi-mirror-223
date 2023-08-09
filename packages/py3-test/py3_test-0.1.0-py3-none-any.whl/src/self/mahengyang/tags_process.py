"""
@author: lijc210@163.com
@file: tags_process.py
@time: 2019/10/24
@desc: 功能描述。
"""
import jieba

with open("tag_data.txt", encoding="utf-8") as f:
    for line in f.readlines():
        line_list = line.strip().split("\t")
        country = line_list[0]
        tag = line_list[1]
        tag_list = list(jieba.cut_for_search(tag))
        if len(tag_list) - len(set(tag_list)) != 0:
            print(tag)

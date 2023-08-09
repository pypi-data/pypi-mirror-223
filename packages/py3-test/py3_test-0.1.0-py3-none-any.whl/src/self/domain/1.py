"""
@author: lijc210@163.com
@file: 1.py
@time: 2019/11/09
@desc: 功能描述。
"""
word_finish_set = set()
with open("word_finish.txt", encoding="utf-8") as f:
    for line in f.readlines():
        word_finish_set.add(line.strip())

with open("word_finish.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(word_finish_set))

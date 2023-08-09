"""
@File    :   text_process.py
@Time    :   2022/01/24 18:41:08
@Author  :   lijc210@163.com
@Desc    :   None
"""
import random

text_set = set()
with open("qinghua.txt", encoding="utf-8") as f:
    for line in f.readlines():
        # print(line)
        text_set.add(line.strip())

text = random.choice(list(text_set))

print(text)

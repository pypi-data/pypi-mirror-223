"""
Created on 2016/1/13
@author: lijc210@163.com

"""
import random

# 意图分成2份

with open("cnews.train.txt", "wb") as fw1:
    with open("cnews.test.txt", "wb") as fw:
        with open("train.txt", "rb") as f:
            line_list = [line.strip() for line in f.readlines()]
            slice = set(random.sample(list(range(len(line_list))), 400))
            for i, aline in enumerate(line_list):
                if i in slice:
                    fw.write(aline + "\n")
                else:
                    fw1.write(aline + "\n")

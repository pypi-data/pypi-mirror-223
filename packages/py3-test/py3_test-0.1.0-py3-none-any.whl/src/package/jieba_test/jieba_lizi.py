"""
Created on 2015/12/28
@author: lijc210@163.com

"""

# encoding=utf-8
import jieba

# jieba.enable_parallel(4)

all_the_text = open("test.txt").read()

test_sent = all_the_text
words = jieba.cut(test_sent)
print("/".join(words))

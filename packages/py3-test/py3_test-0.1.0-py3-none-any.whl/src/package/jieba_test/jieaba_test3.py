"""
Created on 2016/8/2
@author: lijc210@163.com
Desc: 功能描述。
"""
import jieba
import jieba.analyse
import jieba.posseg as pseg

jieba.load_userdict("userdict.txt")

content = """我来到北京清华大学"""

jieba.analyse.set_stop_words("stop_words.txt")

# tags = jieba.analyse.extract_tags(content, topK=200)

# print(",".join(tags))

words = pseg.cut(content)

for word, flag in words:
    print("{} {}".format(word, flag))

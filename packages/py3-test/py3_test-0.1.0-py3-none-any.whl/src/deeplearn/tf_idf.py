"""
@author: lijc210@163.com
@file: 2.py
@time: 2019/12/20
@desc: 功能描述。
"""

import jieba
from gensim import corpora, models, similarities

l1 = ["你的名字是什么", "你今年几岁了", "你有多高你胸多大", "你胸多大"]


def load_data():
    all_doc_list = []
    for doc in l1:
        doc_list = list(jieba.cut(doc))
        all_doc_list.append(doc_list)
    return all_doc_list


def train(all_doc_list):
    # 制作语料库
    dictionary = corpora.Dictionary(all_doc_list)  # 制作词袋
    corpus = [dictionary.doc2bow(doc) for doc in all_doc_list]
    # 将corpus语料库(初识语料库) 使用Lsi模型进行训练
    lsi = models.LsiModel(corpus)
    # 稀疏矩阵相似度 将 主 语料库corpus的训练结果 作为初始值
    index = similarities.SparseMatrixSimilarity(
        lsi[corpus], num_features=len(dictionary.keys())
    )
    return dictionary, index, lsi


def search(dictionary, index, lsi, key, num):
    doc_test_list = list(jieba.cut(key))
    # 将需要寻找相似度的分词列表 做成 语料库 doc_test_vec
    doc_test_vec = dictionary.doc2bow(doc_test_list)
    # 将 语料库doc_test_vec 在 语料库corpus的训练结果 中的 向量表示 与 语料库corpus的 向量表示 做矩阵相似度计算
    sim = index[lsi[doc_test_vec]]
    # 对下标和相似度结果进行一个排序,拿出相似度最高的结果
    cc = sorted(enumerate(sim), key=lambda item: -item[1])[0:num]
    for i, score in cc:
        print(l1[i], score)


if __name__ == "__main__":
    key = "你今年多大了"
    all_doc_list = load_data()
    dictionary, index, lsi = train(all_doc_list)
    search(dictionary, index, lsi, key, 2)

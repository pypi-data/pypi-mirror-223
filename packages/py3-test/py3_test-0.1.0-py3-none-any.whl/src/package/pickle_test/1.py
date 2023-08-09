"""
@author: lijc210@163.com
@file: 1.py
@time: 2020/02/19
@desc: 功能描述。
"""
import pickle


def pickleFile(file, item):
    with open(file, "wb") as dbFile:
        pickle.dump(item, dbFile)


def unpickeFile(file):
    with open(file, "rb") as dbFile:
        return pickle.load(dbFile)

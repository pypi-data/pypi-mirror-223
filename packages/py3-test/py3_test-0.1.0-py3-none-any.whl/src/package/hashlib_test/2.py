"""
@author: lijc210@163.com
@file: 2.py
@time: 2020/02/19
@desc: 小文件md5。
"""
import hashlib


def md5sum(filename):
    with open(filename) as f:
        fmd5 = hashlib.md5(f.read().encode()).hexdigest()
    return fmd5


if __name__ == "__main__":
    fmd5 = md5sum("2.py")
    print(fmd5)

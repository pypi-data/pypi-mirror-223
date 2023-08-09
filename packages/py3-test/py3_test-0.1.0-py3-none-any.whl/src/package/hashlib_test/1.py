"""
@author: lijc210@163.com
@file: 1.py
@time: 2020/02/19
@desc: 功能描述。
"""
import hashlib


def get_md5(key):
    """
    字符串转md5
    :param key:
    :return:
    """
    return hashlib.md5(key.encode()).hexdigest()


if __name__ == "__main__":
    print(get_md5("aaaa"))
    print(get_md5("的"))

"""
@File    :   crypto_test.py
@Time    :   2022/05/09 13:36:05
@Author  :   lijc210@163.com
@Desc    :   None
"""

import base64

from Crypto.Cipher import AES


def aesEncrypt(data, key="放入你的密钥", BLOCK_SIZE=16):
    """
    AES的ECB模式加密方法
    :param key: 密钥
    :param data:被加密字符串（明文）
    :return:密文
    """

    def pad(s):
        return s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(
            BLOCK_SIZE - len(s) % BLOCK_SIZE
        )

    key = key.encode("utf8")
    # 字符串补位
    data = pad(str(data))
    cipher = AES.new(key, AES.MODE_ECB)
    # 加密后得到的是bytes类型的数据，使用Base64进行编码,返回byte字符串
    result = cipher.encrypt(data.encode())
    print(data.encode())
    encodestrs = base64.b64encode(result)
    enctext = encodestrs.decode("utf8")
    # print(enctext)
    return enctext


def aesDecrypt(data, key="放入你的密钥", BLOCK_SIZE=16):
    """
    AES的ECB模式解密方法
    :param key: 密钥
    :param data: 加密后的数据（密文）
    :return:明文
    """

    def unpad(s):
        return s[: -ord(s[len(s) - 1 :])]

    key = key.encode("utf8")
    data = base64.b64decode(data)
    cipher = AES.new(key, AES.MODE_ECB)

    # 去补位
    text_decrypted = unpad(cipher.decrypt(data))
    text_decrypted = text_decrypted.decode("utf8")
    # print(text_decrypted)
    return text_decrypted


if __name__ == "__main__":
    key = "L4JVXd79WstjQiGn9C340chTLJC69Ljf"
    s = "15724567895"
    ss = aesEncrypt(s, key=key)
    print(ss)
    print(aesDecrypt(ss, key=key))

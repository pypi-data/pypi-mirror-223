"""
@Time   : 2019/4/11
@author : lijc210@163.com
@Desc:  : 功能描述。
"""
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 建立连接:
s.connect(("127.0.0.1", 19999))
# 接收欢迎消息:
print(s.recv(1024).decode("utf-8"))
for data in [b"Michael", b"Tracy", b"Sarah"]:
    # 发送数据:
    s.send(data)
    print(s.recv(1024).decode("utf-8"))
s.send(b"exit")
s.close()

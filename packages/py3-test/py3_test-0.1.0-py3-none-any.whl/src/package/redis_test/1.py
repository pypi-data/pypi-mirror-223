"""
@Time   : 2019/5/23
@author : lijc210@163.com
@Desc:  : 功能描述。
"""
import time
from multiprocessing import Pipe, Process, freeze_support

# 创建管道对象
# False fd1只能recv fd2只能send
fd1, fd2 = Pipe(False)


def read():
    while True:
        data = fd1.recv()  # 从管道获取消息
        print(data)


def write():
    while True:
        time.sleep(2)
        fd2.send({"name": "Lily"})  # 向管道发送内容


if __name__ == "__main__":
    freeze_support()
    r = Process(target=read)
    w = Process(target=write)
    r.start()
    w.start()
    r.join()
    w.join()

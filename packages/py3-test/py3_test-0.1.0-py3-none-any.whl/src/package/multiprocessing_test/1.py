"""
@author: lijc210@163.com
@file: 1.py
@time: 2019/11/13
@desc: 功能描述。
"""

import time
from multiprocessing import Process, get_context, set_start_method


def read():
    while True:
        data = fd1.recv()  # 从管道获取消息
        print(data)


def write():
    while True:
        time.sleep(2)
        fd2.send({"name": "Lily"})  # 向管道发送内容


if __name__ == "__main__":
    # windows 启动方式
    set_start_method("spawn")
    # 获取上下文
    ctx = get_context("spawn")
    # 创建管道对象
    # False fd1只能recv fd2只能send

    fd1, fd2 = ctx.Pipe(False)
    r = ctx.Process(target=read)
    w = Process(target=write)

    r.start()
    w.start()
    r.join()
    w.join()

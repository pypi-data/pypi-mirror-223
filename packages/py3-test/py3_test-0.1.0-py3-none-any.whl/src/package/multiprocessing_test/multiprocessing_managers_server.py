"""
@Time   : 2019/5/30
@author : lijc210@163.com
@Desc:  : 功能描述。
"""

import queue
import random
import time
from multiprocessing.managers import BaseManager

# 发送任务的队列:
task_queue = queue.Queue()
# 接收结果的队列:
result_queue = queue.Queue()


def get_task_queue():
    global task_queue
    return task_queue


def get_result_queue():
    global result_queue
    return result_queue


def startManager(host, port, authkey):
    # 把两个Queue都注册到网络上，callable参数关联了Queue对象，注意回调函数不能使用括号
    BaseManager.register("get_task_queue", callable=get_task_queue)
    BaseManager.register("get_result_queue", callable=get_result_queue)
    # 设置host,绑定端口port，设置验证码为authkey
    manager = BaseManager(address=(host, port), authkey=authkey)
    # 启动manager服务器
    manager.start()
    return manager


def put_queue(manager):
    # 通过网络访问
    queueu_task = manager.get_task_queue()
    while 1:
        n = random.randint(0, 1000)
        print("Put task %d" % n)
        queueu_task.put(n)
        time.sleep(0.5)


if __name__ == "__main__":
    host = "127.0.0.1"
    port = 5000
    authkey = b"abc"
    # 启动manager服务器
    manager = startManager(host, port, authkey)
    # 给task队列添加数据
    put_queue(manager)
    # 关闭服务器
    manager.shutdown()

"""
@Time   : 2018/9/19
@author : lijc210@163.com
@Desc:  : 功能描述。
"""
import time
from concurrent.futures import ThreadPoolExecutor
from queue import Queue

queue = Queue(maxsize=5)


def ProducerThread():
    for i in range(10):
        time.sleep(1)
        queue.put(i)


def ConsumerThread():
    while 1:
        data = queue.get()
        time.sleep(1)

        print(data)
        queue.task_done()


def return_future_result(message):
    time.sleep(2)
    return message


pool = ThreadPoolExecutor(max_workers=2)  # 创建一个最大可容纳2个task的线程池
future1 = pool.submit(ProducerThread)  # 往线程池里面加入一个task
future2 = pool.submit(ConsumerThread)  # 往线程池里面加入一个task
future2 = pool.submit(ConsumerThread)  # 往线程池里面加入一个task

queue.put(1)
queue.put(2)
queue.put(3)
queue.put(4)
queue.put(5)
# queue.put(["a","b"])
print(queue.get())
print(queue.get())
print(queue.get())

"""
@Time   : 2018/9/19
@author : lijc210@163.com
@Desc:  : 功能描述。
"""

import time
from concurrent.futures import ThreadPoolExecutor


def return_future_result(message):
    time.sleep(2)
    return message


pool = ThreadPoolExecutor(max_workers=1)  # 创建一个最大可容纳2个task的线程池
future1 = pool.submit(return_future_result, ("hello"))  # 往线程池里面加入一个task
future2 = pool.submit(return_future_result, ("world"))  # 往线程池里面加入一个task

start = time.time()
print(future1.result())  # 查看task1返回的结果
print(future2.result())  # 查看task2返回的结果
print(time.time() - start)

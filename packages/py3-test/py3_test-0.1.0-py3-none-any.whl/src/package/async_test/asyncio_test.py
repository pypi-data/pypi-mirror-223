"""
@author: lijc210@163.com
@file: asyncio_test.py
@time: 2020/04/22
@desc: 功能描述。
"""
import asyncio
import threading
import time


async def world():
    time.sleep(2)
    return 2


@asyncio.coroutine
def hello():
    print("Hello world! (%s)" % threading.currentThread())
    yield from world()
    print("Hello again! (%s)" % threading.currentThread())


loop = asyncio.get_event_loop()
tasks = [hello(), hello()]
start = time.time()
loop.run_until_complete(asyncio.wait(tasks))
print(time.time() - start)
loop.close()

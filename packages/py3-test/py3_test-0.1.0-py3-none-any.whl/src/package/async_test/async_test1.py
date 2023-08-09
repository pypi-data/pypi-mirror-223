"""
@author: lijc210@163.com
@file: asyncio_test.py
@time: 2020/04/22
@desc: 功能描述。
"""
import asyncio
import time


def aaa(i):
    time.sleep(i)
    return i


# 定义异步函数
async def hello(i):
    print("Hello World:%s" % time.time())
    # 必须使用await，不能使用yield from；如果是使用yield from ，需要采用@asyncio.coroutine相对应
    response = await loop.run_in_executor(None, aaa, i)
    print("Hello wow World:%s" % time.time())
    return response


def run():
    tasks = []
    for i in range(1, 6):
        print(i)
        tasks.append(hello(i))
    done, _ = loop.run_until_complete(asyncio.wait(tasks, timeout=3))

    for fut in done:
        print(fut)
        print("return value is {}".format(fut.result()))

    # loop.close()


loop = asyncio.get_event_loop()
if __name__ == "__main__":
    t = time.time()
    run()
    print(time.time() - t)
    print("aaaaaaaaaaaaaaaa")

    while 1:
        print("aaaa")
        time.sleep(1)

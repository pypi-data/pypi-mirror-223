"""
@Time   : 2019/5/30
@author : lijc210@163.com
@Desc:  : 功能描述。
"""
import time
from multiprocessing import Process

data_list = []


def test1():
    for i in range(1, 5):
        print("---%d---" % i)
        time.sleep(1)


def test2():
    for i in range(5, 10):
        print("---%d---" % i)
        time.sleep(1)


if __name__ == "__main__":
    p1 = Process(target=test1)
    p2 = Process(target=test2)
    p1.start()  # 让这个进程开始执行test函数里面的代码
    p2.start()  # 让这个进程开始执行test函数里面的代码
    p1.join()  # 等进程p结束之后，才会继续向下走
    p2.join()  # 等进程p结束之后，才会继续向下走
    print("---main----")
    print(data_list)

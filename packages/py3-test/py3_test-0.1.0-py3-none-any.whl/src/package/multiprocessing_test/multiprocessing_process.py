"""
@Time   : 2019/5/30
@author : lijc210@163.com
@Desc:  : 功能描述。
"""
import time
from multiprocessing import Process


def test():
    for i in range(1, 5):
        print("---%d---" % i)
        time.sleep(1)


if __name__ == "__main__":
    p = Process(target=test)
    p.start()  # 让这个进程开始执行test函数里面的代码
    p.join()  # 等进程p结束之后，才会继续向下走
    print("---main----")

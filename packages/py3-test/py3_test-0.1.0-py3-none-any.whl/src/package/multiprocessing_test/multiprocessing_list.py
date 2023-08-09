"""
@Time   : 2019/5/30
@author : lijc210@163.com
@Desc:  : 功能描述。
"""

from multiprocessing import Manager, Process


def f(l2):
    l2.append(1)


if __name__ == "__main__":
    lists = Manager().list()  # Manager类实例化代码只能写在main()函数里面
    p = Process(target=f, args=(lists,))
    p.start()
    p.join()

    print(lists)

    print(set(lists))

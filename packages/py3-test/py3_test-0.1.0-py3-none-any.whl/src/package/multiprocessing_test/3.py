"""
@author: lijc210@163.com
@file: 3.py
@time: 2019/11/14
@desc: 功能描述。
"""
import multiprocessing

p1, p2 = multiprocessing.Pipe()


def ProcessCreator(pipe):
    pipe.send("hello from other process")


if __name__ == "__main__":
    multiprocessing.freeze_support()
    proc = multiprocessing.Process(target=ProcessCreator, args=(p2,))
    proc.start()
    print(p1.recv())

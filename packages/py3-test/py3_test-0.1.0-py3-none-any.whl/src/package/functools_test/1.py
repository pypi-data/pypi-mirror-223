"""
@author: lijc210@163.com
@file: 1.py
@time: 2020/08/21
@desc: 功能描述。
"""

import time
from functools import lru_cache


@lru_cache(maxsize=10)
class Model:
    def calculate(self, number):
        print(f"calculate({number}) is  running,", end=" ")
        print("sleep  3s  ")
        time.sleep(3)

        return number * 3


if __name__ == "__main__":
    model = Model()

    for i in range(5):
        print(model.calculate(i))

    for i in range(5):
        print(model.calculate(i))

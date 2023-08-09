"""
@Time   : 2019/1/7
@author : lijc210@163.com
@Desc:  : 功能描述。
"""


class a:
    def __init__(self):
        print("aa")

    @staticmethod
    def b():
        print("bb")


if __name__ == "__main__":
    a().b()
    a.b()

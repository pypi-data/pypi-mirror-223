"""
@Time   : 2019/1/7
@author : lijc210@163.com
@Desc:  : 功能描述。
"""


class a:
    def a(self):
        print("bb")


class b(a):
    def b(self):
        print("bb")


class c(b):
    def b(self):
        print("bb")


if __name__ == "__main__":
    c().a()

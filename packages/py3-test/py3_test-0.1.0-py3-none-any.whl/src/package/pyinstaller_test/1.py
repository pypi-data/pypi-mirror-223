"""
@Time   : 2019/5/22
@author : lijc210@163.com
@Desc:  : 功能描述。
"""
import os
import sys

print("hello world")
dir_name = os.path.basename(os.getcwd())
print(os.path.dirname(__file__))
print(dir_name)
print(sys.executable)


# 生成资源文件目录访问路径
def resource_path(relative_path):
    if getattr(sys, "frozen", False):  # 是否Bundle Resource
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


# 访问res文件夹下a.txt的内容
filename = resource_path(os.path.join("res", "a.txt"))
print(filename)

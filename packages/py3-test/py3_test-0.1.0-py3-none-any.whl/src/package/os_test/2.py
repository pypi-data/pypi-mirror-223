"""
@Time   : 2019-06-07
@author : lijc210@163.com
@Desc:  : 功能描述。
"""
import os
import time

rootdir = "."
alist = os.listdir(rootdir)  # 列出文件夹下所有的目录与文件
for _i, tmp in enumerate(alist):
    path = os.path.join(rootdir, tmp)
    if os.path.isfile(path):
        print(path)
        ts = os.path.getctime(path)
        # t = time.mktime(time.strptime(str(int(ts)), "%Y-%m-%d %H:%M:%S"))
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ts))
        print(t)

"""
@Time   : 2019/5/15
@author : lijc210@163.com
@Desc:  : 功能描述。
"""

import zipfile

# 压缩
with zipfile.ZipFile("test.zip", mode="w") as zipf:
    zipf.write("1.py")
    zipf.write("__init__.py")

# zipf = zipfile.ZipFile('test.zip')
# print (zipf.namelist())

# #解压缩
# zipf = zipfile.ZipFile('test.zip')
# zipf.extractall('channel1/')#将所有文件解压到channel1目录下

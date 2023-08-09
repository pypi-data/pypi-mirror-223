"""
Created on 2017/4/6 0006
@author: lijc210@163.com
Desc: 功能描述。
"""
import hashlib

md5key = hashlib.md5(b"15002107795").hexdigest()
print(md5key)

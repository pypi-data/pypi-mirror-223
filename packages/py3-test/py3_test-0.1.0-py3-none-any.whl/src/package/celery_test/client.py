"""
Created on 2017/2/14
@author: lijc210@163.com
Desc: 功能描述。
"""
from .tasks import add

result = add.delay(2, 2)
print(result)
print("hello world")
print(result.get())  # 此方法会把异步调用变成同步调用

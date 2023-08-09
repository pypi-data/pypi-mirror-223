"""
Created on 2017/2/14
@author: lijc210@163.com
Desc: 功能描述。
"""

from .works import app


@app.task
def add(x, y):
    return x + y

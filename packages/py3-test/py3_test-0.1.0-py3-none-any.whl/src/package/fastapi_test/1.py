"""
@author: lijc210@163.com
@file: 1.py
@time: 2020/09/03
@desc: 功能描述。
"""

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

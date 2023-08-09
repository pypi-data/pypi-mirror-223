"""
@Time   : 2019/5/22
@author : lijc210@163.com
@Desc:  : 功能描述。
"""
from sanic import Sanic
from sanic.response import json

app = Sanic()


@app.route("/")
async def test(request):
    return json({"hello": "world"})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000)

"""
@Time   : 2019/2/26
@author : lijc210@163.com
@Desc:  : 功能描述。
"""
import multiprocessing
from multiprocessing import Pool

from sanic import Sanic
from sanic.response import json

pool = Pool()
mydict = multiprocessing.Manager().dict()
mydict["m_pool"] = "aaaaaa"

app = Sanic()


@app.route("/")
async def test(request):
    mydict["c"] = "d"
    print(mydict)
    return json({"hello": "world"})


if __name__ == "__main__":
    # app.run(host="0.0.0.0", port=8002)
    app.run(host="0.0.0.0", port=8002, workers=2)

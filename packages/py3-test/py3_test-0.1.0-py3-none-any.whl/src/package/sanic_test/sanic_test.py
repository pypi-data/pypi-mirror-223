"""
@Time   : 2019/2/26
@author : lijc210@163.com
@Desc:  : 功能描述。
"""
import json as in_json

from sanic import Sanic
from sanic.response import json
from sanic_openapi import swagger_blueprint

app = Sanic()
app.blueprint(swagger_blueprint)


@app.route("/", methods=["POST"])
async def test(request):
    print(dir(request))
    print("form", request.form)
    print(request.body)
    print(in_json.dumps(request.json))
    print(in_json.dumps(request.raw_args))
    apiid = request.args.get("apiid", "1")
    print(apiid)
    return json({"hello": "world"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)

"""
@author: lijc210@163.com
@file: sanic_bp.py
@time: 2020/03/18
@desc: 功能描述。
"""
import sys

from jinja2 import Environment, PackageLoader, select_autoescape
from sanic import Blueprint, Sanic
from sanic.response import html

index_bp1 = Blueprint("index1", url_prefix="index1")
# index_bp.static('/static/douban', '/static/douban')

index_bp2 = Blueprint("index2", url_prefix="index2")
# index_bp2.static('/static/douban', '/static/douban')

# https://github.com/channelcat/sanic/blob/5bb640ca1706a42a012109dc3d811925d7453217/examples/jinja_example/jinja_example.py
# 开启异步特性  要求3.6+
enable_async = sys.version_info >= (3, 6)

# jinjia2 config
env = Environment(
    loader=PackageLoader("sanic_bp", "templates"),
    autoescape=select_autoescape(["html", "xml", "tpl"]),
    enable_async=enable_async,
)


async def template(tpl, **kwargs):
    template = env.get_template(tpl)
    rendered_template = await template.render_async(**kwargs)
    return html(rendered_template)


@index_bp1.route("/index1")
async def index(request):
    print("aaaaa")
    return await template("index.html")


@index_bp2.route("/index2")
async def index2(request):
    print("aaaaa")
    return await template("index2.html")


app = Sanic(__name__)

app.blueprint(index_bp1)
app.blueprint(index_bp2)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)

#!/usr/bin/env python
import sys

import itchat
from jinja2 import Environment, PackageLoader, select_autoescape
from sanic import Blueprint
from sanic.response import html, json, redirect

from src.config import CONFIG

# https://github.com/channelcat/sanic/blob/5bb640ca1706a42a012109dc3d811925d7453217/examples/jinja_example/jinja_example.py
# 开启异步特性  要求3.6+
enable_async = sys.version_info >= (3, 6)

wechat_bp = Blueprint("wechat", url_prefix="")
wechat_bp.static("/statics/", CONFIG.BASE_DIR + "/statics/")

# jinjia2 config
env = Environment(
    loader=PackageLoader("views.wechat", "../templates"),
    autoescape=select_autoescape(["html", "xml", "tpl"]),
    enable_async=enable_async,
)


async def template(tpl, **kwargs):
    template = env.get_template(tpl)
    rendered_template = await template.render_async(**kwargs)
    return html(rendered_template)


@wechat_bp.route("/")
async def index(request):
    status = itchat.check_login()
    if status == 200:
        print("登陆成功", status)
        return redirect("wechat")
    else:
        print("登陆失败", status)
        return redirect("login")


@wechat_bp.route("/login")
async def login(request):
    print("aaaaa")
    # picDir = CONFIG.BASE_DIR + '/statics/img/QR.png'
    # if os.path.exists(picDir):
    #     os.remove(picDir)
    #
    # while not itchat.get_QRuuid():
    #     time.sleep(1)
    # uuid = itchat.originInstance.uuid
    #
    # qrStorage = io.BytesIO()
    # qrCode = QRCode('https://login.weixin.qq.com/l/' + uuid)
    # qrCode.png(qrStorage, scale=10)
    #
    # with open(picDir, 'wb') as f:
    #     f.write(qrStorage.getvalue())
    # # itchat.get_QR(enableCmdQR=False, picDir=picDir, qrCallback=None)
    itchat.auto_login(True)
    return await template("login.htm")


@wechat_bp.route("/check_login")
async def check_login(request):
    data = {"status": itchat.check_login()}
    return json(data)


# @wechat_bp.route("/wechat")
# async def wechat(request):
#     status = itchat.check_login()
#     if status == 200:
#         print("登陆成功", status)
#         return redirect('wechat')
#     else:
#         print("登陆失败", status)
#         return redirect('login')


@wechat_bp.route("/wechat")
async def wechat(request):
    return await template("wechat.htm")


@wechat_bp.route("/web_init", methods=["POST"])
async def web_init(request):
    return json(itchat.web_init1())

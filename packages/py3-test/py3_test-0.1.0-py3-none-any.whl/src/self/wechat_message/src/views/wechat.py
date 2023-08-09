#!/usr/bin/env python
import json as in_json
import sys
import time

from jinja2 import Environment, PackageLoader, select_autoescape
from sanic import Blueprint
from sanic.response import html, json

from src.config import CONFIG
from utils.utils import sqlite3_client

# https://github.com/channelcat/sanic/blob/5bb640ca1706a42a012109dc3d811925d7453217/examples/jinja_example/jinja_example.py
# 开启异步特性  要求3.6+
enable_async = sys.version_info >= (3, 6)

index_bp = Blueprint("index", url_prefix="")
wechat_bp = Blueprint("wechat", url_prefix="wechat")
index_bp.static("/statics/", CONFIG.BASE_DIR + "/statics/")
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


@index_bp.route("a.html", methods=["GET", "POST"])
async def a(request):
    """
    :param request:
    :return:
    """
    return await template("a.html")


@index_bp.route("b.html", methods=["GET", "POST"])
async def b(request):
    """
    :param request:
    :return:
    """
    return await template("b.html")


@index_bp.route("")
async def index(request):
    """
     快速回复
    :param request:
    :return:
    """
    sql = "select id,content from quick_reply"
    data_list = sqlite3_client.query(sql)
    return await template("quick_reply.html", data_list=data_list)


@index_bp.route("/remove", methods=["GET", "POST", "OPTIONS"])
async def remove(request):
    """
     删除
    :param request:
    :return:
    """
    _id = request.args.get("id", "")
    sql = "delete from quick_reply where id={_id}".format(_id=_id)
    print(sql)
    sqlite3_client.execute(sql)
    data = {"msg": "删除成功"}
    return json(
        data,
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "*",
        },
    )


@index_bp.route("/save", methods=["GET", "POST", "OPTIONS"])
async def save(request):
    """
     保存
    :param request:
    :return:
    """
    post_data = {}
    for k, _v in request.form.items():
        post_data[k] = request.form.get(k)
    try:
        post_body = in_json.loads(request.body)
        post_data.update(post_body)
    except Exception:
        pass

    _id = post_data.get("id", None)
    content = post_data.get("content", "")
    if _id:  # 存在id是更新，不存在是插入
        sql = "update quick_reply set content='{content}' where id={_id}".format(
            content=content, _id=_id
        )
        sqlite3_client.execute(sql)
    else:
        sql = "INSERT INTO quick_reply (content) \
            VALUES ('{content}')".format(
            content=content
        )
        print(sql)
        _id = sqlite3_client.insert(sql)

    data = {"msg": "保存成功", "id": _id}
    return json(
        data,
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "*",
        },
    )


@wechat_bp.route("/search.html")
async def search(request):
    """
    搜索页面
    :param request:
    :return:
    """
    return await template("search.html")


@wechat_bp.route("/result")
async def result(request):
    """
    搜索结果页面
    :param request:
    :return:
    """
    sql = "select * from user "
    UserName_info_dict = {}
    for adict in sqlite3_client.query(sql):
        UserName_info_dict[adict["user_name"]] = adict

    query = request.args.get("query")
    sql = "select * from message where content like '%{query}%' order by  create_time desc ".format(
        query=query
    )
    data_list = []
    for bdict in sqlite3_client.query(sql):
        from_username = bdict["from_username"]
        to_username = bdict["to_username"]
        content = bdict["content"]
        msg_type = bdict["msg_type"]
        msg_source = bdict["msg_source"]
        create_time = bdict["create_time"]

        info_dict1 = UserName_info_dict.get(from_username, {})
        info_dict2 = UserName_info_dict.get(to_username, {})
        from_username = (
            info_dict1.get("remark_name")
            if info_dict1.get("remark_name")
            else info_dict1.get("nick_name")
        )
        to_username = (
            info_dict2.get("remark_name")
            if info_dict2.get("remark_name")
            else info_dict2.get("nick_name")
        )
        msg_type = "发送" if msg_type == 1 else "接收"
        msg_source = "普通消息" if msg_source == 1 else "群消息"
        create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(create_time))

        data_list.append(
            {
                "from_username": from_username,
                "to_username": to_username,
                "content": content,
                "msg_type": msg_type,
                "msg_source": msg_source,
                "create_time": create_time,
            }
        )
    return await template("result.html", data_list=data_list)


@wechat_bp.route("/statistics.html")
async def statistics(request):
    """
    统计页面
    :param request:
    :return:
    """

    sql = (
        "select t2.head_img_url,case when remark_name='' then nick_name else nick_name end as name,sum(1) as num "
        "from message t1 left join user t2 on t1.from_username=t2.user_name where msg_type=1 group by name,head_img_url order by num desc "
    )
    send_list = sqlite3_client.query(sql)

    sql = (
        "select head_img_url,case when remark_name='' then nick_name else nick_name end as name,sum(1) as num "
        "from message t1 left join user t2 on t1.from_username=t2.user_name where msg_type=2 group by name order by num desc "
    )
    receive_list = sqlite3_client.query(sql)
    return await template(
        "statistics.html", send_list=send_list, receive_list=receive_list
    )

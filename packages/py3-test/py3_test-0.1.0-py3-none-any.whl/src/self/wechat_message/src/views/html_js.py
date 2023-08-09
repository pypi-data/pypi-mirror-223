"""
@Time   : 2019/5/20
@author : lijc210@163.com
@Desc:  : 功能描述。
"""
from utils.utils import sqlite3_client


def quick_reply():
    sql = "select id,content from quick_reply"
    data_list = sqlite3_client.query(sql)

    all_tr = ""
    for adict in data_list:
        _id = adict["id"]
        content = adict["content"]
        tr = """
                <tr>
                <td style='white-space: pre-line' id={_id} class='contextMenu2' onfocusout='save(this)' contentEditable='true' ondblclick='send(this)'>{content}</td>
            </tr>
        """.format(
            _id=_id, content=content
        )
        all_tr += tr

    html = (
        """
<link href='https://netdna.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css' rel='stylesheet'>
<link href='https://cdn.bootcss.com/jquery-contextmenu/2.6.3/jquery.contextMenu.min.css' rel='stylesheet'>
<script src='https://cdn.bootcss.com/jquery-contextmenu/2.6.3/jquery.contextMenu.min.js'></script>
<style type='text/css'>
    table.gridtable {
        font-family: verdana, arial, sans-serif;
        font-size: 11px;
        color: #333333;
        border-width: 1px;
        border-color: #666666;
        border-collapse: collapse;
    }

    table.gridtable th {
        border-width: 1px;
        padding: 8px;
        border-style: solid;
        border-color: #666666;
        background-color: #dedede;
    }

    table.gridtable td {
        word-break: break-all;
        border-width: 1px;
        padding: 8px;
        border-style: solid;
        border-color: #666666;
        background-color: #ffffff;
    }

    table.gridtable td a {
        display: inline;
    }
</style>
<body>

<div class='quick_reply' style='width:30%%;height:80%%;overflow-y:scroll;float: left;margin-top: 100px;margin-left: 10px;'>
    <!-- CSS goes in the document HEAD or added to your external stylesheet -->


    <!-- Table goes in the document BODY -->
    <table class='gridtable'>
        <tr>
            <th>单击编辑，双击发送，右键菜单（<a href='http://127.0.0.1:8000/wechat/statistics.html' target='_blank'>统计</a>
                &nbsp;<a href='http://127.0.0.1:8000/wechat/search.html' target='_blank'>搜索</a>）
            </th>
        </tr>

        %s

        <tr>
            <td><a onclick='add(this)' class='btn btn-danger' href='#'><i class='fa fa-plus fa-lg'></i> </a></td>
        </tr>
    </table>
</div>
"""
        % all_tr
    )
    return html.replace("\n", "")


def get_script():
    script = """
    <script>
    function send(obj) {
        document.querySelector('#editArea').innerText=obj.innerText;
    }

    function save(obj) {
        var data = {
            'id': obj.id,
            'content': obj.innerText
        };
        var httpRequest = new XMLHttpRequest();
        httpRequest.open('POST', 'http://127.0.0.1:8000/save', true);
        httpRequest.setRequestHeader('Content-type', 'application/json');
        httpRequest.send(JSON.stringify(data));
        httpRequest.onreadystatechange = function () {
            if (httpRequest.readyState == 4 && httpRequest.status == 200) {
                var json=JSON.parse(httpRequest.responseText);
                console.log(json);
                obj.setAttribute('id',json.id)
            }
        };
    }
    </script>
    """
    return script.replace("\n", "")


def get_add_script():
    script = """
<script>
        function add(obj) {
            var tr = "<tr>                <td style=\\'white-space: pre-line\\' class=\\'contextMenu2\\' onfocusout=\\'save(this)\\' contentEditable=\\'true\\'                    ondblclick=\\'send(this)\\'></td>            </tr>";
            $(obj).parent().parent().before(tr);
        }
    </script>
    """
    return script.replace("\n", "")


def get_menu_script():
    script = """
    <script>
    $.contextMenu({
        selector: '.contextMenu2',
        callback: function (key, options) {

            if (key == 'level_down') {
                var len = options.$trigger.length;
                var $tr = options.$trigger.parents('tr');
                if ($tr.index() != len - 2) {
                    $tr.fadeOut().fadeIn();
                    $tr.next().after($tr);
                }
            }
            if (key == 'level_up') {
                var $tr = options.$trigger.parents('tr');
                if ($tr.index() != 0) {
                    $tr.fadeOut().fadeIn();
                    $tr.prev().before($tr);
                }
            }
            if (key == 'delete') {
                var id = options.$trigger.attr('id');
                var httpRequest = new XMLHttpRequest();
                httpRequest.open('GET', 'http://127.0.0.1:8000/remove?id=' + id, true);
                httpRequest.send();
                httpRequest.onreadystatechange = function () {
                    if (httpRequest.readyState == 4 && httpRequest.status == 200) {
                        var json = httpRequest.responseText;
                        console.log(json);
                        options.$trigger.parent().remove();
                    }
                };
            }
        },
        items: {
            'level_down': {name: '下移'},
            'level_up': {name: '上移'},
            'delete': {name: '删除'}
        }
    });
</script>
    """
    return script.replace("\n", "")


if __name__ == "__main__":
    print(quick_reply())
    print(get_script())
    print(get_add_script())
    print(get_menu_script())

"""
@author: lijc210@163.com
@file: 1.py
@time: 2019/12/25
@desc: 功能描述。
"""
from pyecharts import options as opts
from pyecharts.charts import Bar

bar = Bar(init_opts=opts.InitOpts(width="620px", height="420px"))
bar.add_xaxis(["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"])
bar.add_yaxis("商家A", [5, 20, 36, 10, 75, 90])
# render 会生成本地 HTML 文件，默认会在当前目录生成 render.html 文件
# 也可以传入路径参数，如 bar.render("mycharts.html")
bar.render()

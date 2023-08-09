"""
@author: lijc210@163.com
@file: 1.py
@time: 2019/12/25
@desc: 功能描述。
"""
import pyecharts.options as opts
from pyecharts.charts import Line
from pyecharts.faker import Faker

print(Faker.choose())
print(Faker.values())

c = (
    Line()
    .add_xaxis(Faker.choose())
    .add_yaxis("商家A", Faker.values(), is_smooth=True)
    .add_yaxis("商家B", Faker.values(), is_smooth=True)
    .set_global_opts(title_opts=opts.TitleOpts(title="Line-smooth"))
    .render("line_smooth.html")
)

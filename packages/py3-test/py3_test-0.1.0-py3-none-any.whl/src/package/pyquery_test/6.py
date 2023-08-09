"""
@author: lijc210@163.com
@file: 6.py
@time: 2020/06/14
@desc: 功能描述。
"""

from pyquery import PyQuery as pq

with open("git clone一个仓库下的单个文件.html", encoding="utf-8") as f:
    doc = pq(f.read())
    with open("2.html", "w", encoding="utf-8") as f:
        f.write(doc.outer_html())

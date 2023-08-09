"""
@author: lijc210@163.com
@file: 1.py
@time: 2020/04/01
@desc: 功能描述。
"""
import re

text = "教育部认证罗素集团世界大学联盟2018-12-26更新"

search = re.search("\\d\\d\\d\\d-\\d\\d-\\d\\d", text)

print(search.group(0))

raise ValueError

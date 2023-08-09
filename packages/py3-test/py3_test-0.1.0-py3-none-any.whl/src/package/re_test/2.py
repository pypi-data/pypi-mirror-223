"""
@Time   : 2019-06-07
@author : lijc210@163.com
@Desc:  : 功能描述。
"""
# 判断一段文本中是否包含简体中文
import re

zhmodel = re.compile("[\u4e00-\u9fa5]+")  # 检查中文
# zhmodel = re.compile(u'[^\u4e00-\u9fa5]')   #检查非中文


def hanzi(content):
    match = zhmodel.search(content)
    if match:
        return len(match.group())
    else:
        return 0


content1 = "（2014）深南法民二初字第280号"
content2 = "（2014）asfsfsgs"
print(hanzi(content1))
print(hanzi(content2))

"""
@Time   : 2019/3/26
@author : lijc210@163.com
@Desc:  : 功能描述。
"""
from requests_html import HTMLSession

session = HTMLSession()
r = session.get("http://www.e658.cn/jg/show-htm-itemid-165839.html")
# r.html.render()
print(r.html.xpath('//*[@id="content"]/div/div[2]/text()'))

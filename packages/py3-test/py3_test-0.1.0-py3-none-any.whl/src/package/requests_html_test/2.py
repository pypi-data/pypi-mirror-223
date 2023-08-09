"""
@Time   : 2019/3/26
@author : lijc210@163.com
@Desc:  : 功能描述。
"""
from requests_html import HTMLSession

session = HTMLSession()
r = session.get("https://www.cnhnb.com/supply/search/?k=鸭胸")
# r.html.render()
divs = r.html.xpath('//*[@class="supply-list"]')
for doc in divs:
    print("#########################")
    print(doc.html)
    print("#########################")
    for doc1 in doc.xpath("//div/a"):
        print("aaaaaa")
        print(doc1.html)
        print("bbbbbb")
    print("************************")
    # print(doc.xpath('div[0]').html)
    # print(doc.xpath('div/a'))
    # print(doc('/div[1]/a'))

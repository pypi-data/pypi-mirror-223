"""
@Time   : 2018/11/14
@author : lijc210@163.com
@Desc:  : 功能描述。
"""

import requests
from retry import retry

# from pyquery import PyQuery as pq

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.8",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    # "Cookie":"did_close_tag=; _lxsdk_cuid=15ff423ef4946-0d509442727fe3-474a0521-1fa400-15ff423ef4ac8; _lxsdk=15ff423ef4946-0d509442727fe3-474a0521-1fa400-15ff423ef4ac8; _hc.v=62c3a87a-3d33-8d18-d{0}-4e5d4c6d09af.1511629517; __mta=209001133.1511629517946.1511629517946.1511629517946.1; _lxsdk_s=15ff423ef4d-99-849-1d7%7C%7C24".format(choice(l)),
    "Host": "www.dianping.com",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
    "Referer": "http://www.dianping.com/shanghai/home",
}


@retry(tries=3, delay=2)  # 报错重试
def retry_get(url):
    print(url)
    res = requests.get(url, timeout=5)
    print((url, res.status_code))
    return res


@retry(tries=3, delay=2)  # 报错重试
def retry_post(url, data=None, json=None):
    res = requests.post(url, data=data, json=json, timeout=5)
    print((url, res.status_code))
    return res


if __name__ == "__main__":
    html = retry_get("httpss://movie.douban.com/top250").text
    print(html)
    # doc = pq(html)
    #
    # # content > div > div.article > ol > li:nth-child(1) > div > div.info > div.hd > a > span:nth-child(1)
    #
    # # first_title = doc('#content > div > div.article > ol > li:nth-child(1) > div > div.info > div.hd > a > span:nth-child(1)')
    # # print(first_title.text())
    #
    # all_title = doc('#content > div > div.article > ol > li > div > div.info > div.hd > a')
    # for each in all_title.items():
    #     # print(each.html())
    #     # print(each.text())
    #     print(each.attr.href)
    #     first_span = each('span:nth-child(1)')
    #     print(first_span.text())
    #     # print(first_span.attr("class"))
    #     # break

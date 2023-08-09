"""
@File    :   google_search.py
@Time    :   2022/11/24 15:35:01
@Author  :   lijc210@163.com
@Desc    :   None
"""

import requests

proxies = {"http": "socks5://127.0.0.1:4455", "https": "socks5://127.0.0.1:4455"}


def search():
    url = "https://www.googleapis.com/customsearch/v1"  # 每日100
    url = "https://www.googleapis.com/customsearch/v1/siterestrict"  # 此接口没有每日查询限制，但只能搜10个网站，
    parameters = "?key=AIzaSyCprHubqUwrJ6zPuKOrd17dhojnyF7MT8g&q=%E4%BD%99%E5%8D%8E&cx=059193d9c5740450f&start=0&num=10"
    r = requests.get(url + parameters, timeout=2, proxies=proxies)
    res_dict = r.json()
    print(r.text)
    print(res_dict["searchInformation"]["formattedTotalResults"])


if __name__ == "__main__":
    for _i in range(0, 200):
        search()

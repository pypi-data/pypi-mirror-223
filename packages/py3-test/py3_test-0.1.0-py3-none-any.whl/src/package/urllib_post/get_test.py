import requests

uri = "http://192.168.25.39:8011/tplink"
adict = [
    {
        "bill_code": 123,
        "disp_site_id": "2652",
        "rec_site_id": "3729",
        "scan_center_id": "",
        "scan_date": "2018-02-06 20:00:28",
        "scan_site_id": 2435,
        "scan_type": "daojian",
        "maxWeight": 1.3,
    }
]


def get(url):
    res = requests.get(url)
    return res.elapsed.microseconds / 1000


print(get("https://api.douban.com/v2/book/2129650"))

import json
import urllib.error
import urllib.parse
import urllib.request

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


def post(post_data):
    ret = urllib.request.urlopen(uri, data=post_data)
    ret_data = ret.read()
    return ret_data


print(post(json.dumps(adict)))

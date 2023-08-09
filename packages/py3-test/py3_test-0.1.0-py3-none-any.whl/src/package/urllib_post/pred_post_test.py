import json
import time
import urllib.error
import urllib.parse
import urllib.request
from multiprocessing.dummy import Pool

rowkey_list = []
with open("rowkey.json") as f:
    rowkey_list = json.loads(f.read())
uri = "http://192.168.25.39:8011/tplink"
alist = rowkey_list[:5]

task_num = 1
post_data = []
for rowkey in alist:
    rec_site_id = rowkey.split("##")[0]
    disp_site_id = rowkey.split("##")[1]
    adict = {
        "bill_code": "10101201",
        "disp_site_id": disp_site_id,
        "rec_site_id": rec_site_id,
        "scan_center_id": "",
        "scan_date": "2017-12-14 14:38:32",
        "scan_site_id": rec_site_id,
        "scan_type": "xiadan",
    }
    post_data.append(adict)
post_data = json.dumps(post_data)
data = [post_data] * task_num


def post(post_data):
    ret = urllib.request.urlopen(uri, data=post_data)
    ret_data = ret.read()
    return ret_data


start = time.time()
pool = Pool(task_num)
resultlist = pool.map(post, data)
pool.close()
pool.join()

# print(json.loads(result[0]))

for bdict in json.loads(resultlist[0]):
    routelist = bdict["result"]
    for result in routelist:
        print(result)
        rate = result["rate"]
        rank_id = result["rank_id"]
        billcode = result["bill_code"]
        history_route_list = result["rolu"]
        for sitedict in history_route_list:
            site_id = sitedict.get("id", "")
            name = sitedict.get("name", "")
            scan_time = sitedict.get("scan_time", "")
            scan_type = sitedict.get("scan_type", "")
            zx_wd = sitedict.get("zx_wd", "")
            alist = (
                billcode,
                rank_id,
                rate,
                site_id,
                name,
                zx_wd,
                scan_time,
                scan_type,
            )
            print(alist)

print(task_num, (time.time() - start), "seconds")

import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

sys.setdefaultencoding("utf-8")


class Mapreduce:
    def __init__(self):
        self.timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    def read_input(self, file):
        for line in file:
            if line and line.strip():  # 略过空行
                yield line.split("\t")

    def main(self):
        data = self.read_input(sys.stdin)
        for line in data:
            try:
                zx_need_id = line[0]
                need_time = line[1]
                house_address = line[2].strip().replace(" ", "").decode()  # 去空格
            except Exception:
                continue
            timestamp = self.timestamp
            res_json = self.get(house_address)
            status = res_json["status"]
            if status == "1":
                try:
                    district = res_json["data"]["tip_list"][0]["tip"]["district"]
                except Exception:
                    district = ""
            elif status == "7":
                res_json = self.get(house_address[0:8])  # 取前8个汉字去搜索
                status = res_json["status"]
                if status == "1":
                    try:
                        district = res_json["data"]["tip_list"][0]["tip"]["district"]
                    except Exception:
                        district = ""
                elif status == "7":
                    res_json = self.get(house_address[0:5])  # 取前5个汉字去搜索
                    status = res_json["status"]
                    if status == "1":
                        try:
                            district = res_json["data"]["tip_list"][0]["tip"][
                                "district"
                            ]
                        except Exception:
                            district = ""
                    elif status == "7":
                        res_json = self.get(house_address[0:3])  # 取前3个汉字去搜索
                        status = res_json["status"]
                        if status == "1":
                            try:
                                district = res_json["data"]["tip_list"][0]["tip"][
                                    "district"
                                ]
                            except Exception:
                                district = ""
                        else:
                            district = ""
                    else:
                        district = ""
                else:
                    district = ""
            else:
                district = ""
            if "省" in district:
                alist = district.split("省", 1)
                province = alist[0] + "省"
                if "自治州" in alist[1]:
                    blist = alist[1].split("自治州", 1)
                    city = blist[0] + "自治州"
                    area = blist[1]
                elif "市" in alist[1]:
                    blist = alist[1].split("市", 1)
                    city = blist[0] + "市"
                    area = blist[1]
                else:
                    city, area = "Null", "Null"
            else:
                if "自治区" in district:
                    alist = district.split("自治区", 1)
                    province = alist[0] + "自治区"
                    if "自治州" in alist[1]:
                        blist = alist[1].split("自治州", 1)
                        city = blist[0] + "自治州"
                        area = blist[1]
                    elif "市" in alist[1]:
                        blist = alist[1].split("市", 1)
                        city = blist[0] + "市"
                        area = blist[1]
                    else:
                        city, area = "Null", "Null"
                elif "市" in district:
                    province = "Null"
                    alist = district.split("市", 1)
                    city = alist[0] + "市"
                    area = alist[1]
                else:
                    province, city, area = "Null", "Null", "Null"
            if province == "":
                province = "Null"
            if city == "":
                city = "Null"
            if area == "":
                area = "Null"
            print(
                zx_need_id
                + "\t"
                + need_time
                + "\t"
                + house_address
                + "\t"
                + province
                + "\t"
                + city
                + "\t"
                + area
                + "\t"
                + timestamp
            )

    def get(self, key):
        words = urllib.parse.quote(key.encode())
        url = "http://ditu.amap.com/service/poiTipslite?&words={}".format(words)
        req = urllib.request.Request(url)
        try:
            res_data = urllib.request.urlopen(req)
            res = res_data.read()
        except Exception:
            time.sleep(120)
            res_data = urllib.request.urlopen(req)
            res = res_data.read()
        try:
            res_json = json.loads(res)
        except Exception:
            time.sleep(10)
            res_json = {"status": "0"}
        return res_json


if __name__ == "__main__":
    mapreduce = Mapreduce()
    mapreduce.main()

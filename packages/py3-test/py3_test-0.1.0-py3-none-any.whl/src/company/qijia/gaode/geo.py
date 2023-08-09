# Created on: 2018/3/2 16:03
# Email: lijicong@163.com
# desc   根据地址获取省市区，坐标
# -*- coding:utf-8 -*-

from platform import python_version

import requests

if python_version().startswith("2"):
    import sys

georegeo_url = "https://restapi.amap.com/v3/geocode/geo?parameters"

key = "ec67ff42f93e2088681011e54edf688d"


def geo(address, city=None):
    try:
        resp = requests.get(
            georegeo_url, params={"key": key, "address": address, "city": city}
        )
        rel_json = resp.json()
        rel_array = rel_json["geocodes"]
        if len(rel_array) > 0:
            rel = rel_array[0]
            location = rel.get("location")
            lng, lat = (
                location
                and len(location.split(",")) == 2
                and [float(it) for it in location.split(",")]
                or [-1, -1]
            )
            formatted_address = rel.get("formatted_address", "Null")
            country = rel.get("country", "Null")
            province = rel.get("province", "Null")
            city = rel.get("city", "Null")
            district = rel.get("district", "Null")
            if isinstance(city, list):
                city = ""
            if isinstance(district, list):
                district = ""
            line_list = [
                address,
                formatted_address,
                country,
                province,
                city,
                district,
                str(lng),
                str(lat),
            ]
        else:
            line_list = [address, "Null", "Null", "Null", "Null", "Null", "-1", "-1"]
    except Exception:
        # traceback.print_exc()
        line_list = [address, "Null", "Null", "Null", "Null", "Null", "-1", "-1"]
    return "\t".join(line_list)


def read_input(file):
    for line in file:
        if line and line.strip():  # 略过空行
            yield line.rstrip().split("\t")


def main():
    data = read_input(sys.stdin)
    for line in data:
        address = line[0]
        print("\001".join(geo(address)))


if __name__ == "__main__":
    # main()
    print(geo("东营市垦利区石化工业园区"))

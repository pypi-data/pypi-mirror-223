"""
@Time   : 2019/3/14
@author : lijc210@163.com
@Desc:  : 功能描述。
"""
from geo import geo

with open("res.txt", "w", encoding="utf-8") as fw:
    with open("test.txt", encoding="utf-8") as f:
        for line in f.readlines():
            line = line.replace("\n", "")
            company, province1, address1 = line.split("\t")
            res = geo(address1)
            (
                address,
                formatted_address,
                country,
                province,
                city,
                district,
                lng,
                lat,
            ) = res.split("\t")
            new_list = [
                company,
                province1,
                address1,
                province,
                city,
                district,
                lng,
                lat,
            ]
            print(new_list)
            fw.write("\001".join(new_list) + "\n")

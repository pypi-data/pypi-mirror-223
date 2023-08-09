"""
Created on 2016/1/13
@author: lijc210@163.com

"""
import json
import re

msg_set = set()

zhPattern = re.compile("[\u4e00-\u9fa5]+")

with open("msg.txt", "wb") as fw:
    with open("6-80000.csv", "rb") as f:
        for line in f.readlines():
            data_str = '["' + line.replace(" , ", '", ').strip() + "]"
            try:
                adict = json.loads(data_str)
                tmp_dict = adict[1]["bodies"][0]
            except Exception:
                print(1)
                tmp_dict = {}
            if "msg" in tmp_dict:
                msg = tmp_dict["msg"].strip()
                if len(msg) < 4:
                    print(msg)
                elif zhPattern.search(msg):  # 有中文:
                    msg_set.add(msg)
                else:
                    print(msg)
        fw.write("\n".join(msg_set))

# coding: utf-8
"""
@File    :   1.py
@Time    :   2023/08/01 15:19:10
@Author  :   lijc210@163.com
@Desc    :   None
"""
from collections import defaultdict

d1 = defaultdict(list)
d2 = defaultdict(list)

with open("src/company/guoquan/1.txt", "r") as f:
    for line in f.readlines():
        print(line.strip())
        alist = line.strip().split()
        if len(alist) == 2:
            k, v = alist
            d1[k].append(v)


with open("src/company/guoquan/2.txt", "r") as f:
    for line in f.readlines():
        # print(line.strip())
        k, v = line.strip().split(",", 1)
        k = k.replace("yunpu", "")
        v = v.replace('"', "")
        v = v.split(",")
        d2[k] = v

print(len(d1))
print(len(d2))


with open("src/company/guoquan/不存在bi账号的用户.txt", "w") as f:
    i = 0
    for k, v in d1.items():
        v2 = d2.get(k)
        if v2 is None:
            f.write(k + "\n")
            # print(k, v)
            i += 1
    # print(i)

with open("src/company/guoquan/门店不一致的用户.txt", "w") as f:
    i = 0
    for k, v in d1.items():
        v2 = d2.get(k)
        if v2 is None:
            continue
        else:
            if set(v) != set(v2):
                f.write(
                    k + "\t\t\t\t\t" + ",".join(v) + "\t\t\t\t\t" + ",".join(v2) + "\n"
                )
                print(k, v, v2)
                i += 1
    print(i)

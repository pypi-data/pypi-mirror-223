"""
@Time   : 2019/5/24
@author : lijc210@163.com
@Desc:  : 功能描述。

"""

from urllib import parse

url = "_from=R40&LH_BIN=1&_sop=13&LH_Complete=1&LH_Sold=1&_udlo=24&_udhi=48&_ipg=200&_pgn=1&_skc=0"
res = dict(parse.parse_qsl(url))
print(res)

# 或
res = {k.split("=")[0]: k.split("=")[1] for k in url.split("&") if k}
print(res)

# 或
res = dict(k.split("=") for k in url.split("&") if k)
print(res)

# 反过来
res = {
    "_from": "R40",
    "LH_BIN": "1",
    "_sop": "13",
    "LH_Complete": "1",
    "LH_Sold": "1",
    "_udlo": "24",
    "_udhi": "48",
    "_ipg": "200",
    "_pgn": "1",
    "_skc": "0",
}
parameters = parse.urlencode(res)
print(parameters)

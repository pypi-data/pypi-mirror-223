"""
@Time   : 2019/4/1
@author : lijc210@163.com
@Desc:  : 功能描述。
"""

import requests

# curl = '''
# print(uncurl.parse(curl))

r = requests.post(
    "http://fengchao.baidu.com/mcc/request.ajax?path=GET/mcc/user/report",
    data="superUcId=5380819&optId=5380819&path=GET%2Fmcc%2Fuser%2Freport&token=&params=%7B%22appId%22%3A%22422%22%2C%22type%22%3A2%2C%22mccType%22%3A%220%22%2C%22startDate%22%3A%222019-04-01%22%2C%22endDate%22%3A%222019-04-30%22%2C%22index%22%3A1%7D",
    headers={
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "http://fengchao.baidu.com",
        "Referer": "http://fengchao.baidu.com/mcc/main.html?optId=5380819&superUcId=5380819&userid=5380819&castk=4c7e2dx70221faaf9d812",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
    },
    cookies={
        "BAIDUID": "3DF010A6D7FE57972A51538834A9A778:FG=1",
        "BIDUPSID": "3DF010A6D7FE57972A51538834A9A778",
        "CPID_3": "5380819",
        "CPTK_3": "191373783",
        "H_PS_PSSID": "1421_28939_21113_28774_28722_28964_28837_28584_26350_28604_20718",
        "MCITY": "-%3A",
        "PSINO": "5",
        "PSTM": "1548036101",
        "SAMPLING_OPT_ID": "5380819",
        "SIGNIN_UC": "70a2711cf1d3d9b1a82d2f87d633bd8a03073814399",
        "ZD_ENTRY": "baidu",
        "__cas__id__3": "5380819",
        "__cas__rn__": "307381439",
        "__cas__st__3": "7aa4b7f1bd48af76ca1b1252e57b6ca4dc98e93c28305ea84a8d80a336cd217a74fc4edc830ac7609c27d1bf",
        "delPer": "0",
        "td_cookie": "18446744073183879594",
        "yjs_js_security_passport": "f79e4787b0559af45f407a922d820932781730ce_1557374305_js",
    },
)

print(r.text)

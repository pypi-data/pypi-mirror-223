"""
@Time   : 2019/1/15
@author : lijc210@163.com
@Desc:  : 功能描述。
"""
import re

from pyquery import PyQuery as pq

doc = pq("https://www.pdflibr.com/SMSContent/68")
for tr in doc("table > tbody > tr").items():
    tmp = re.search("登录百度推广，验证码为：\\d{6}", tr.text())
    if tmp:
        phone_Verif_code = tmp.group(0).replace("登录百度推广，验证码为：", "")
        print(phone_Verif_code)

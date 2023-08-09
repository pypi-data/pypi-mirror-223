"""
@Time   : 2019/4/23
@author : lijc210@163.com
@Desc:  : 功能描述。
"""
import requests

session = requests.Session()

r = session.post(
    "http://bi-go.api.tg.local/api/auth/",
    data="email=chenxianren@qeeka.com&password=@chenxianren12#",
    headers={"Content-Type": "application/x-www-form-urlencoded"},
    cookies={},
)

# print(r.text)

p = "?apply_id=12548110&code=&apply_source=m-toutiao&type=5&apply_url=http://zixun.m.jia.com/zixun/article/712608.html?wxsharetype=1&from=timeline&isappinstalled=0?m_toutiao_detail_xrhb&areaflag=other"
p = """?apply_id=12684025&code=dvzxu4UO&apply_source=wap-zaixianyusuan-baojia&type=7&apply_url=https://m.jia.com/cms/yusuan/gdtq4.html?qz_gdt=qb3zwa5wewlh201&areaflag=jiangmen"""
p = "?apply_id=12685605&code=dTQzYV6w&apply_source=wap-zaixianyusuan-baojia&type=7&apply_url=https://m.jia.com/cms/yusuan/gdtq2.html?qz_gdt=y2d44xfiaiap5fhxigja&areaflag=chongqing"
print("go版：")
print(session.get("http://bi-go.api.tg.local/api/channel/{}".format(p)).text)
print("python版：")
print(requests.get("http://bi-python.api.tg.local/tool/channel{}".format(p)).text)
print("合并版：")
print(requests.get("http://127.0.0.1:8005/tool/channel{}".format(p)).text)
print("测试环境：")
print(requests.get("http://10.10.20.165:8005/tool/channel{}".format(p)).text)

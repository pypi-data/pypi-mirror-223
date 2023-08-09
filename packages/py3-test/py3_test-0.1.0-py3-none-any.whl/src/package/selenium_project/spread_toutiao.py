"""
Created on 2016/10/8
@author: lijc210@163.com
Desc: 功能描述。
"""
import datetime
import json
import os
import sys
import time

from selenium import webdriver

driver = webdriver.PhantomJS()


class ToutiaoApi:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.driver = self.login()

    def login(self):
        # 登陆首页
        driver.get("https://ad.toutiao.com/login/")
        # time.sleep(2)
        # print driver.title
        # 登陆，会自动跳转到https://ad.toutiao.com/overture/data/
        driver.find_element_by_xpath(
            '//*[@id="login_form"]/table/tbody/tr[2]/td/input'
        ).send_keys(self.username)
        driver.find_element_by_xpath(
            '//*[@id="login_form"]/table/tbody/tr[3]/td/input'
        ).send_keys(self.password)
        driver.find_element_by_xpath('//*[@id="login_form"]').submit()
        # 等待登陆
        time.sleep(3)
        # print driver.title
        # print driver.current_url
        # print driver.page_source
        return driver

    def getData(self, fileName, startDate, endDate):
        # 第一页数据
        page = 1
        self.driver.get(
            "https://ad.toutiao.com/overture/data/creative_stat/?page={}&st={} 00:00:00&et={} 00:00:00&status=&landing_type=0&image_mode=0&pricing=0&search_type=2&keyword=".format(
                page, startDate, endDate
            )
        )
        dataJson = driver.find_element_by_xpath("/html/body/pre").text
        # print dataJson
        dataDict = json.loads(dataJson)
        # 解析字典存到文件
        with open(fileName, "ab") as f:
            table = self.dict2file(dataDict)
            f.write(table)
        # 第二页到最后一页数据
        total_count = dataDict["data"]["table"]["pagination"]["total_count"]
        limit = dataDict["data"]["table"]["pagination"]["limit"]
        page_count = total_count / limit + 1  # 总页数
        # print total_count,limit,page_count
        for page in range(2, page_count + 1):
            print(page)
            self.driver.get(
                "https://ad.toutiao.com/overture/data/creative_stat/?page={}&st={} 00:00:00&et={} 00:00:00&status=&landing_type=0&image_mode=0&pricing=0&search_type=2&keyword=".format(
                    page, startDate, endDate
                )
            )
            print(self.driver.current_url)
            dataJson = driver.find_element_by_xpath("/html/body/pre").text
            dataDict = json.loads(dataJson)
            # 解析字典存到文件
            with open(fileName, "ab") as f:
                table = self.dict2file(dataDict)
                f.write(table)
        self.driver.get("https://ad.toutiao.com/overture/data/")  # 调到首页
        self.driver.find_element_by_xpath(
            '//*[@id="pagelet-header"]/div/div[2]/span[4]/a'
        ).click()  # 退出登陆

    def dict2file(self, dataDict):
        creative_data_list = dataDict["data"]["table"]["creative_data"]
        table = ""
        for creative_data in creative_data_list:
            creative_id = creative_data["creative_id"]  # 创意ID
            title = creative_data["title"]  # 创意
            status = creative_data["status"]  # 状态
            ad_inventory_types = creative_data["ad_inventory_types"][0]  # 已选流量
            ad_name = creative_data["ad_name"]  # 广告计划
            campaign_name = creative_data["campaign_name"]  # 广告组
            stat_cost = creative_data["stat_data"]["stat_cost"]  # 总花费(元)
            show = creative_data["stat_data"]["show"]  # 展示数
            click = creative_data["stat_data"]["click"]  # 点击数
            ctr = creative_data["stat_data"]["ctr"] + "%"  # 点击率
            click_cost = creative_data["stat_data"]["click_cost"]  # 平均点击单价(元)
            ecpm = creative_data["stat_data"]["ecpm"]  # 平均千次展现费用(元)
            vlist = [
                startDate,
                self.username,
                str(creative_id),
                title,
                status,
                ad_inventory_types,
                ad_name,
                campaign_name,
                stat_cost,
                str(show),
                str(click),
                ctr,
                click_cost,
                ecpm,
            ]
            # print vlist
            line = "\001".join(vlist) + "\n"
            # print line
            table += line
        return table


if __name__ == "__main__":
    toutiaoAccount = {
        "fenzhanwuxian@163.com": "Mark520520",
        "shqijiashanghai@126.com": "Mark520520",
    }
    startDate = (datetime.datetime.now() + datetime.timedelta(days=-1)).strftime(
        "%Y-%m-%d"
    )  # 默认昨天
    endDate = (datetime.datetime.now()).strftime("%Y-%m-%d")  # 今天
    dt = (datetime.datetime.now() + datetime.timedelta(days=-1)).strftime(
        "%Y%m%d"
    )  # 文件名日期格式
    if len(sys.argv) == 2 and len(sys.argv[1]) == 8:
        dt = sys.argv[1]
        startDate = datetime.datetime.strptime(dt, "%Y%m%d").strftime("%Y-%m-%d")
        endDate = startDate
        print("获取{}数据".format(startDate))
    elif len(sys.argv) == 1:
        print("获取{}数据".format(startDate))
    else:
        print("[ERROR]只接收一个日期参数，格式YYYYMMDD")
    # fileName = "/data/file/search/ods_traf_toutiao_search_%s.txt" %dt#最终结果保存的文件名
    fileName = "ods_traf_toutiao_search_%s.txt" % dt  # 本地测试用
    if os.path.exists(fileName):
        os.remove(fileName)
    for username, password in toutiaoAccount.items():
        toutiaoApi = ToutiaoApi(username, password)
        toutiaoApi.getData(fileName, startDate, endDate)

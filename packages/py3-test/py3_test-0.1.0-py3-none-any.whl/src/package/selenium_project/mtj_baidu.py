"""
Created on 2016/10/8
@author: lijc210@163.com
Desc: 功能描述。
"""
import datetime
import os
import time
import urllib.error
import urllib.parse
import urllib.request

from selenium import webdriver

driver = webdriver.PhantomJS()


class MtjBaiduApi:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.driver = self.login()

    def login(self):
        # 登陆
        driver.get("https://mtj.baidu.com/web/welcome/login")
        time.sleep(2)
        # print driver.title
        driver.find_element_by_xpath('//*[@id="btn-login"]').click()
        time.sleep(1)
        driver.find_element_by_xpath('//*[@id="TANGRAM__PSP_15__userName"]').send_keys(
            self.username
        )
        driver.find_element_by_xpath('//*[@id="TANGRAM__PSP_15__password"]').send_keys(
            self.password
        )
        driver.find_element_by_xpath('//*[@id="TANGRAM__PSP_15__submit"]').submit()
        img = driver.find_element_by_xpath(
            '//*[@id="TANGRAM__PSP_15__verifyCodeImg"]'
        ).get_attribute("src")
        urllib.request.urlretrieve(img, "genimage.png")

        # 等待登陆
        # time.sleep(10)
        # print driver.title
        # print driver.current_url
        # print driver.page_source
        return driver

    def getData(self, fileName):
        self.driver.get("https://mtj.baidu.com/web/dashboard")
        time.sleep(3)
        # print driver.page_source
        all_td = driver.find_elements_by_xpath(
            '//*[@id="detail-wrapper"]/table[2]/tbody/tr/td'
        )
        for td in all_td:
            print(td.find_element_by_xpath("/div/span[1]"))
        # # print dataJson
        # dataDict = json.loads(dataJson)
        # #解析字典存到文件
        # with open(fileName,'ab') as f:
        #     table = self.dict2file(dataDict)
        #     f.write(table)
        # #第二页到最后一页数据
        # total_count = dataDict['data']['table']['pagination']['total_count']
        # limit = dataDict['data']['table']['pagination']['limit']
        # page_count = total_count/limit+1#总页数
        # # print total_count,limit,page_count
        # for page in range(2,page_count+1):
        #     print page
        #     self.driver.get('https://ad.toutiao.com/overture/data/creative_stat/?page={0}&st={1} 00:00:00&et={2} 00:00:00&status=&landing_type=0&image_mode=0&pricing=0&search_type=2&keyword='.format(page,startDate,endDate))
        #     print self.driver.current_url
        #     dataJson = driver.find_element_by_xpath('/html/body/pre').text
        #     dataDict = json.loads(dataJson)
        #     #解析字典存到文件
        #     with open(fileName,'ab') as f:
        #         table = self.dict2file(dataDict)
        #         f.write(table)

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
            ctr = creative_data["stat_data"]["ctr"]  # 点击率
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
    ###不支持自定义时间，只支持获取昨天的数据###
    # MtjBaiduAccount = {"15665659760":"wangdan1025","13636046460":"licong210"}
    MtjBaiduAccount = {"15665659760": "wangdan1025"}
    # MtjBaiduAccount = {"13636046460":"licong2100000"}
    dt = (datetime.datetime.now() + datetime.timedelta(days=-1)).strftime(
        "%Y%m%d"
    )  # 文件名日期格式
    startDate = (datetime.datetime.now() + datetime.timedelta(days=-1)).strftime(
        "%Y-%m-%d"
    )  # 默认昨天
    # endDate = (datetime.datetime.now()).strftime('%Y-%m-%d') #今天
    # fileName = "/data/file/search/ods_traf_qq_search_%s.txt" %dt#最终结果保存的文件名
    fileName = "ods_conf_wireless_promotion_%s.txt" % dt  # 本地测试用
    if os.path.exists(fileName):
        os.remove(fileName)
    for username, password in MtjBaiduAccount.items():
        guangdiantongApi = MtjBaiduApi(username, password)
        guangdiantongApi.getData(fileName)

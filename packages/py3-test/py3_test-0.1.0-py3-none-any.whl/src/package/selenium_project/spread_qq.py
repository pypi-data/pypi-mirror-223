"""
Created on 2016/10/8
@author: lijc210@163.com
Desc: 功能描述。
"""
import datetime
import os
import time

from selenium import webdriver

driver = webdriver.PhantomJS()


class GuangdiantongApi:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def getData(self, fileName):
        # 登陆首页
        driver.get(
            "http://xui.ptlogin2.qq.com/cgi-bin/xlogin?appid=15000103&s_url=http%3A%2F%2Fe.qq.com%2Fads&style=20&border_radius=1&target=top&maskOpacity=60&"
        )
        time.sleep(1)
        driver.find_element_by_xpath('//*[@id="switcher_plogin"]').click()
        driver.find_element_by_xpath('//*[@id="u"]').send_keys(self.username)
        driver.find_element_by_xpath('//*[@id="p"]').send_keys(self.password)
        driver.find_element_by_xpath('//*[@id="login_button"]').click()
        # 等待登陆
        time.sleep(3)
        # print driver.current_url
        # 广告页
        driver.get("http://e.qq.com/atlas/268350/report/order")
        # print driver.current_url
        time.sleep(5)
        # 选择日期
        span = driver.find_element_by_xpath('//*[@id="_queryForm"]/div[2]/div/span')
        driver.execute_script("$(arguments[0]).click()", span)
        driver.find_element_by_xpath(
            "/html/body/div[2]/div[3]/ul/li[2]"
        ).click()  # 点击昨天
        time.sleep(5)
        # 过滤无数据的广告
        driver.find_element_by_xpath('//*[@id="reportonly"]').click()  #
        time.sleep(5)
        # 获取第一页数据
        with open(fileName, "ab") as f:
            table = self.getTable()
            f.write(table)
        if driver.find_elements_by_xpath('//*[@id="_pager"]/div/a').is_displayed():
            # 获取分页a标签长度
            all_a = driver.find_elements_by_xpath('//*[@id="_pager"]/div/a')
            a_len = len(all_a)
            # 从第二页开始点击，到最后一页
            for i in range(2, a_len + 1):
                driver.find_element_by_xpath(
                    '//*[@id="_pager"]/div/a[{}]'.format(i)
                ).click()
                time.sleep(10)
                with open(fileName, "ab") as f:
                    table = self.getTable()
                    f.write(table)

    def getTable(self):
        table = ""
        all_tr = driver.find_elements_by_xpath(
            '//*[@id="_list"]/div/div[1]/div[1]/table/tbody/tr'
        )
        for tr in all_tr:
            # print tr.get_attribute("innerHTML")
            if tr.get_attribute("class") == "_todetail ":
                v1 = tr.find_element_by_xpath("td[2]").text  # 广告名称
                v2 = tr.find_element_by_xpath("td[3]").get_attribute(
                    "innerHTML"
                )  # 广告ID
                v3 = (
                    tr.find_element_by_xpath("td[4]").get_attribute("innerHTML").strip()
                )  # 所属推广计划
                v4 = tr.find_element_by_xpath("td[5]").get_attribute(
                    "innerHTML"
                )  # 计划ID
                v5 = tr.find_element_by_xpath("td[6]").get_attribute(
                    "innerHTML"
                )  # 标的物类型
                v6 = tr.find_element_by_xpath("td[7]").get_attribute(
                    "innerHTML"
                )  # 标的物名称
                v7 = tr.find_element_by_xpath("td[9]").get_attribute("innerHTML")  # 曝光量
                v8 = tr.find_element_by_xpath("td[10]").get_attribute(
                    "innerHTML"
                )  # 点击量
                v9 = tr.find_element_by_xpath("td[11]").get_attribute(
                    "innerHTML"
                )  # 点击率
                v10 = tr.find_element_by_xpath("td[15]").get_attribute(
                    "innerHTML"
                )  # 点击均价(元)
                v11 = tr.find_element_by_xpath("td[42]").get_attribute(
                    "innerHTML"
                )  # 花费(元)
                v12 = tr.find_element_by_xpath("td[51]/span").get_attribute(
                    "innerHTML"
                )  # 状态
                v13 = (
                    tr.find_element_by_xpath("td[52]/div/span")
                    .get_attribute("innerHTML")
                    .strip()
                )  # 出价(元)
                vlist = [
                    startDate,
                    self.username,
                    v1,
                    v2,
                    v3,
                    v4,
                    v5,
                    v6,
                    v7,
                    v8,
                    v9,
                    v10,
                    v11,
                    v12,
                    v13,
                ]
                line = "\001".join(vlist) + "\n"
                # print line
                table += line
        return table


if __name__ == "__main__":
    ###不支持自定义时间，只支持获取昨天的数据###
    qqAccount = {"553444391": "Mark520520"}
    dt = (datetime.datetime.now() + datetime.timedelta(days=-1)).strftime(
        "%Y%m%d"
    )  # 文件名日期格式
    startDate = (datetime.datetime.now() + datetime.timedelta(days=-1)).strftime(
        "%Y-%m-%d"
    )  # 默认昨天
    endDate = (datetime.datetime.now()).strftime("%Y-%m-%d")  # 今天
    # fileName = "/data/file/search/ods_traf_qq_search_%s.txt" %dt#最终结果保存的文件名
    fileName = "ods_traf_qq_search_%s.txt" % dt  # 本地测试用
    if os.path.exists(fileName):
        os.remove(fileName)
    for username, password in qqAccount.items():
        guangdiantongApi = GuangdiantongApi(username, password)
        guangdiantongApi.getData(fileName)

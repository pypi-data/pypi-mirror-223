"""
@Time   : 2018/11/14
@author : lijc210@163.com
@Desc:  : 功能描述。
"""

from selenium import webdriver

driver = webdriver.PhantomJS()  # 无界面，更快，节省资源
# driver = webdriver.Chrome() #有界面
driver.get("https://movie.douban.com/")
print(driver.current_url)
print(driver.title)
print(driver.page_source)

driver.close()

"""
@Time   : 2019/3/28
@author : lijc210@163.com
@Desc:  : 功能描述。
"""
import os

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

os.makedirs("cache", exist_ok=True)
caps = DesiredCapabilities.CHROME
caps["loggingPrefs"] = {"performance": "ALL"}
options = webdriver.ChromeOptions()

# driver = webdriver.Chrome(desired_capabilities=caps, executable_path="./chromedriver")
driver = webdriver.Chrome(desired_capabilities=caps, chrome_options=options)

driver.get("https://www.baidu.com")

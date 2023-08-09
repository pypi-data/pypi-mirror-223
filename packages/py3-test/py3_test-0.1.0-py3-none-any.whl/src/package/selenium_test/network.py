"""
@Time   : 2019/3/28
@author : lijc210@163.com
@Desc:  : 功能描述。
"""
import json

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

caps = DesiredCapabilities.CHROME
caps["loggingPrefs"] = {"performance": "ALL"}
driver = webdriver.Chrome(desired_capabilities=caps)

driver.get("https://www.baidu.com")

logs = [json.loads(log["message"])["message"] for log in driver.get_log("performance")]

for tmp_dict in logs:
    print(json.dumps(tmp_dict))

with open("devtools.json", "w") as f:
    json.dump(logs, f)

driver.close()

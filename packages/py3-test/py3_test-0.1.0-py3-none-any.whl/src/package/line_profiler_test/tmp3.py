"""
@Time   : 2018/8/22
@author : lijc210@163.com
@Desc:  : 功能描述。
"""
import traceback

try:
    raise ValueError
except Exception:
    traceback.print_exc()

print("aaaaaa")

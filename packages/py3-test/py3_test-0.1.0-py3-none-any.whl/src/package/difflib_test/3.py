"""
@author: lijc210@163.com
@file: 2.py
@time: 2020/05/19
@desc: 功能描述。
"""
import difflib


def diff_text(a, b):
    return difflib.SequenceMatcher(a=a, b=b).quick_ratio()


print(diff_text(a="陈嘉映", b="24_《浮士德》:陈嘉映"))
print(diff_text(a="陈嘉映", b="【陈嘉映】为什么现在成功那么难？"))
print(diff_text(a="陈嘉映", b="周廉和陈嘉映对话"))
print(diff_text(a="陈嘉映", b="映嘉陈"))
print(diff_text(a="陈嘉映", b="小狐狸卖空气"))
print(diff_text(a="鱿鱼", b="真鱿"))

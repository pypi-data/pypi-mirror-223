"""
@author: lijc210@163.com
@file: 2.py
@time: 2020/05/19
@desc: 功能描述。
"""
import difflib

print(difflib.SequenceMatcher(a="饰全饰美装饰", b="饰全室美").quick_ratio())
print(difflib.SequenceMatcher(a="饰全饰美装饰", b="饰全饰美装饰工程有限公司").quick_ratio())
print(difflib.SequenceMatcher(a="饰全饰美装饰", b="饰之美装饰").quick_ratio())


def replace_text(text):
    text = (
        text.replace("有限公司", "")
        .replace("有限责任公司", "")
        .replace("股份", "")
        .replace("集团", "")
        .replace("工程", "")
        .replace("装饰", "")
        .replace("装修", "")
        .replace("装潢", "")
        .replace("装璜", "")
        .replace("建筑", "")
        .replace("设计", "")
        .replace("家居", "")
        .replace("（", "")
        .replace("）", "")
        .replace("(", "")
        .replace(")", "")
    )
    return text


def diff_text(a, b):
    return difflib.SequenceMatcher(a=a, b=b).quick_ratio()


print(replace_text("青田县艺品轩装饰工程有限公司"))
print(diff_text(a="饰全饰美装饰", b="饰全室美"))
print(diff_text(a="饰全饰美装饰", b="饰全饰美装饰工程有限公司"))
print(diff_text(a="饰全饰美装饰", b="饰之美装饰"))

print(diff_text(a=replace_text("饰全饰美装饰"), b=replace_text("饰之美装饰")))
print(diff_text(a=replace_text("饰全饰美装饰"), b=replace_text("饰全饰美装饰工程有限公司")))
print(diff_text(a=replace_text("饰全饰美装饰"), b=replace_text("饰之美装饰")))
print(diff_text(a=replace_text("测试公司的"), b=replace_text("测试公司")))

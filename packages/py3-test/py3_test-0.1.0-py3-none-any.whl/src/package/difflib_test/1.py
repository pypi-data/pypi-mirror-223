"""
@Time   : 2018/12/13
@author : lijc210@163.com
@Desc:  : 功能描述。
"""
import difflib

print(difflib.SequenceMatcher(a="进程池使用有四种方式", b="进程池使用有四种方式").quick_ratio())
print(difflib.SequenceMatcher(a="饰全饰美装饰", b="饰全室美").quick_ratio())
print(difflib.SequenceMatcher(a="饰全饰美装饰", b="饰全饰美装饰工程有限公司").quick_ratio())
print(difflib.SequenceMatcher(a="饰全饰美装饰", b="饰之美装饰").quick_ratio())
print(difflib.SequenceMatcher(a="进程池使用有四种方式", b="使用进程池有四种方式").quick_ratio())
print(
    difflib.SequenceMatcher(a="留学英国法律专业", b="英国留学,法律,专业,特点,介绍,法律,专业,是,").quick_ratio()
)
print(difflib.SequenceMatcher(a="青田县艺品轩", b="上海青田县艺品轩").quick_ratio())


print(
    "青田县艺品轩装饰工程有限公司".replace("有限公司", "")
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

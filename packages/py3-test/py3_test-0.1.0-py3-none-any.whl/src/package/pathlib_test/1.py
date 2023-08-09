"""
@Time   : 2019/3/25
@author : lijc210@163.com
@Desc:  : 功能描述。
"""
from pathlib import Path

print(Path(Path.cwd()).parent)

# p = Path(Path.cwd())
# print(p.resolve())                 # 获取当前绝对路径
# print(p.parent)
#
# p = Path('C:/Users/Administrator/Desktop/')
# print(p.resolve())
# print(p.parent)

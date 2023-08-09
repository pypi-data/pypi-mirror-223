"""
@Time   : 2018/10/8
@author : lijc210@163.com
@Desc:  : 功能描述。
"""

from pytrie import Trie

t = Trie(an=0, ant=1, all=2, allot=3, alloy=4, aloe=5, are=6, be=7)
t = Trie({["a", "n"]: 0})

print(t.keys(prefix="al"))
print(t.items(prefix="al"))

"""
@Time   : 2018/9/30
@author : lijc210@163.com
@Desc:  : 功能描述。
https://github.com/pytries/marisa-trie
https://marisa-trie.readthedocs.io/en/latest/tutorial.html
"""

import marisa_trie

# l = [u'key1', u'key2', u'key12', u'key13']

l1 = ["some.long.name", "some.short.name"]

t = marisa_trie.Trie(["some.long.name", "some.short.name"])

print(t.longest_unique_prefixes())

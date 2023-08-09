"""
@Time   : 2018/9/30
@author : lijc210@163.com
@Desc:  : 功能描述。
https://github.com/pytries/marisa-trie
https://marisa-trie.readthedocs.io/en/latest/tutorial.html
"""

import marisa_trie

l1 = ["key1", "key2", "key12", "key13"]

l_reversed = [x[::-1] for x in l1]

trie = marisa_trie.Trie(l1)

print("key1" in trie)

print(trie["key12"])

print(trie.restore_key(2))

print(trie.prefixes("key125"))

print(trie.keys("key1"))

print()

print("#" * 20)

trie = marisa_trie.Trie(l_reversed)

print(trie.prefixes("key125"))

print(trie.save("l.marisa"))

print(trie.load("l.marisa").keys("31"))

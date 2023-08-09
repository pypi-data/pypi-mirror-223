"""
@author: lijc210@163.com
@file: 7.py
@time: 2020/06/22
@desc: 功能描述。
"""


class Tree:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


t = Tree(1)
t.left = Tree(1)
t.right = Tree(1)
t.left.left = Tree(1)
t.left.right = Tree(1)
t.right.left = Tree(1)
t.right.right = Tree(1)


def PreOrder(root):
    if root is None:
        return
    PreOrder(root.left)
    PreOrder(root.right)


def is_one_val(t):
    if t is None:
        return True
    if t.left is not None and t.val != t.left.val:
        return False
    if t.right is not None and t.val != t.right.val:
        return False
    return is_one_val(t.left) & is_one_val(t.right)


print(is_one_val(t))

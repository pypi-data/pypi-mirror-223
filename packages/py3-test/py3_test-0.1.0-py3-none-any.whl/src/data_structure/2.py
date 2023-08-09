"""
@author: lijc210@163.com
@file: 1.py
@time: 2020/06/21
@desc: 功能描述。
"""


class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


def isSameTree(p, q):
    if p == q is None:
        return True
    if p.val != q.val:
        return False
    left_same = isSameTree(p.left, q.left)
    right_same = isSameTree(p.right, q.right)
    return left_same & right_same


def PreOrder(root):
    if root is None:
        return
    print(root.val)
    PreOrder(root.left)
    PreOrder(root.right)


if __name__ == "__main__":
    p = TreeNode(1)
    p.left = TreeNode(2)
    p.right = TreeNode(3)

    # print(p.val, p.left.val, p.right.val)
    #
    # q = TreeNode(1)
    # q.left = TreeNode(None)
    # q.right = TreeNode(3)
    #
    # print(q.val, q.left.val, q.right.val)
    #
    # print(isSameTree(p, q))

    print(PreOrder(p))

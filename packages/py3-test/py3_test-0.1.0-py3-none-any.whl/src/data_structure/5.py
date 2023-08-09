"""
@author: lijc210@163.com
@file: 3.py
@time: 2020/06/21
@desc: 功能描述。
"""


class Node:
    def __init__(self, val=None):
        self.val = val
        self.next = None


class LinkList:
    def __init__(self):
        pass

    def init_node(self, alist):
        link_list = Node(alist[0])
        p = link_list
        for i in alist[1:]:
            node = Node(i)
            p.next = node
            p = p.next
        return link_list


def deleteDuplicates(link_list):
    LinkList()
    curr = link_list
    head = curr  # 点前比较节点
    while curr and curr.next:
        print(curr.val)
        if curr.val != head.val:
            head = head.next
        else:
            curr.next = head.next


if __name__ == "__main__":
    alist = [1, 1, 2, 2, 3]
    link_list = LinkList().init_node(alist)
    # print(link_list.data)
    print(deleteDuplicates(link_list))

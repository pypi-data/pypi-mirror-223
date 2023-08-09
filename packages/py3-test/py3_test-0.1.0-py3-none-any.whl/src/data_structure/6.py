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
    def init_link_list(self, data_list):
        if not data_list:
            link_list = Node()
        else:
            link_list = Node(data_list[0])
            p = link_list
            for x in data_list[1:]:
                node = Node(x)
                p.next = node
                p = p.next
        return link_list


def has_cycle(link_list):
    aset = set()
    p = link_list
    while p:
        print(p.val)
        if p in aset:
            return True
        else:
            aset.add(p)
            p = p.next
    return False


alist = [1, 2, 3, 4, 5, 6, 5, 6]
link_list = LinkList().init_link_list(alist)
# print(link_list.next.val)
link_list.next.next.next = link_list.next.next
print(has_cycle(link_list))

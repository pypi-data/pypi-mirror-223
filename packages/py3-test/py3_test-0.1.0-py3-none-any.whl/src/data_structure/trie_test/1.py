"""
@Time   : 2018/9/30
@author : lijc210@163.com
@Desc:  : 功能描述。
"""


class ListNode:
    def __init__(self, val):
        self.val = val
        self.next = None


# 借助辅助空间
# class Solution:
#     def hasCycle(self, head: ListNode) -> bool:
#         a = set()
#         while head:
#             if head in a:
#                 return True
#             a.add(head)
#             head = head.next
#         return False


# 快慢指针法
class Solution:
    def hasCycle(self, head: ListNode) -> bool:
        slow = fast = head
        while fast and fast.next:  ##保证fast和fast.next有值 不然fast.next.next会报错
            slow = slow.next
            fast = fast.next.next
            if slow is fast:
                return True
        return False


if __name__ == "__main__":
    ln1 = ListNode(1)
    ln2 = ListNode(2)
    ln1.next = ln2
    ln2.next = ln1

    r = Solution().hasCycle(ln1)
    print(r)

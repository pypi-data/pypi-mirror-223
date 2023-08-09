"""
@author: lijc210@163.com
@file: 5.py
@time: 2020/01/29
@desc:   两个数组的交集 II。
"""
nums1 = [4, 9, 5]
nums2 = [9, 4, 9, 8, 4]


class Solution:
    def intersect(self, nums1, nums2):
        return [x for x in nums1 if x in set(nums2)]


print(Solution().intersect(nums1, nums2))

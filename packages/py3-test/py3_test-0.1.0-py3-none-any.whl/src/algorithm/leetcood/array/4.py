"""
@author: lijc210@163.com
@file: 4.py
@time: 2020/01/29
@desc:   只出现一次的数字。
"""
a = [4, 1, 2, 1, 2, 5, 5]


class Solution:
    def singleNumber(self, nums) -> int:
        nums.sort()
        nums.append("x")
        for i, x in enumerate(nums):
            if (i + 1) % 2 != 0:
                if x != nums[i + 1]:
                    return x


print(Solution().singleNumber(a))

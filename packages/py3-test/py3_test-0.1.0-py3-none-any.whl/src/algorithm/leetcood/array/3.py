"""
@author: lijc210@163.com
@file: 3.py
@time: 2020/01/29
@desc: 旋转数组。
"""

a = [1, 2, 3, 4, 5, 6, 7]


class Solution:
    def rotate(self, nums, k: int) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        for _i, x in enumerate(nums[: len(nums) - k]):
            nums.pop(0)
            nums.append(x)
        return nums


print(Solution().rotate(nums=a, k=3))

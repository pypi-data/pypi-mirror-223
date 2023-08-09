"""
@author: lijc210@163.com
@file: 6.py
@time: 2020/01/29
@desc: 移动零。
"""

# [0,1,0,3,12]


class Solution:
    def moveZeroes(self, nums) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        n = 0  # 第一个0索引
        for i in range(len(nums)):
            if nums[i] != 0:
                nums[n], nums[i] = nums[i], nums[n]  # 位置互换
                n += 1
        return nums


# class Solution:
#     def moveZeroes(self, nums) -> None:
#         """
#         Do not return anything, modify nums in-place instead.
#         """
#         i = 0  ## i是第一个指针，代表第i个非零数
#         for j in range(len(nums)):  ## j是第二个指针，代表第j个数
#             if nums[j]:  ## 如果第j个数非0，那么把第j个数放到第i个位置上，并且i += 1
#                 nums[i], nums[j] = nums[j], nums[i]
#                 i += 1
#         return nums  ## 完成后，最够若干位（i+1以及后面的位置）自动都交换变成0
print(Solution().moveZeroes([0, 0, 1]))
print(Solution().moveZeroes([0, 1, 0, 3, 12]))

"""
@Time   : 2018/12/19
@author : lijc210@163.com
@Desc:  : 删除排序数组中的重复项。
"""

a = [0, 0, 1, 1, 1, 2, 2, 3, 3, 4]


class Solution:
    def removeDuplicates(self, nums) -> int:
        n = 0
        for _i, x in enumerate(nums[1:]):
            if nums[n] == x:
                pass
            else:
                nums[n + 1] = x
                n += 1
        return n + 1


print(Solution().removeDuplicates(a))

"""
@author: lijc210@163.com
@file: 2.py
@time: 2020/01/29
@desc: 买卖股票的最佳时机。
"""
a = [7, 1, 5, 3, 6, 4]


class Solution:
    def maxProfit(self, prices) -> int:
        n = 0
        for i, x in enumerate(prices[1:], 1):
            if x > prices[i - 1]:
                n += x - prices[i - 1]
        return n


print(Solution().maxProfit(a))

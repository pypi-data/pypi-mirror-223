"""
@author: lijc210@163.com
@file: 7.py
@time: 2020/06/22
@desc: 功能描述。
"""
# alist = [2, 5, 1, 2, 3, 4, 7, 7, 6]
alist = [2, 1, 1, 3, 1, 2, 1, 2]


def trap1(height):
    """
    双指针写法
    :param height:
    :return:
    """
    rst = 0
    if not height:
        return rst
    # 左边及右边“桶壁” ---- 起挡水作用的柱子
    max_left, max_right = height[0], height[-1]
    # 内部柱子
    left, right = 1, len(height) - 2
    # 处理完内部所有柱子
    while right >= left:
        # 左边为短板
        if max_left < max_right:
            if max_left > height[left]:
                rst += max_left - height[left]
            else:
                max_left = height[left]
            left += 1
        # 右边是短板
        else:
            if max_right > height[right]:
                rst += max_right - height[right]
            else:
                max_right = height[right]
            right -= 1
    return rst


def trap2(height):
    """
    遍历
    :param height:
    :return:
    """
    left, right = [0] * len(height), [0] * len(height)
    cur_max = 0

    for i, h in enumerate(height):
        left[i] = max(0, cur_max - h)  # 如果左边长度大于右边长度，取差值，否则置为0
        cur_max = max(cur_max, h)  # 保存左边最大值

    cur_max = 0
    for i, h in enumerate(height[::-1]):  # 从右往左遍历
        right[len(right) - 1 - i] = max(
            0, cur_max - h
        )  # 如果右边长度大于左边长度，取差值，否则置为0 (把最先算的放最后面)
        cur_max = max(cur_max, h)  # 保存右边最大值

    return sum(
        [min(l2, r) for l2, r in zip(left, right, strict=True)]
    )  # 从左往右蓄水值和从右往左蓄水值比较，取较小值，短的那边决定实际蓄水值


def trap3(alist):
    alist_len = len(alist)
    left = [0] * alist_len
    right = [0] * alist_len
    cur1_max = 0
    cur2_max = 0

    for i, x in enumerate(alist):
        left[i] = max(0, cur1_max - x)
        cur1_max = max(cur1_max, x)

    for j, y in enumerate(alist[::-1]):
        right[alist_len - j - 1] = max(0, cur2_max - y)
        cur2_max = max(cur2_max, y)

    return sum([min(l1, r) for l1, r in zip(left, right, strict=True)])


print(trap3(alist))

"""
@author: lijc210@163.com
@file: wilson_score.py
@time: 2019/09/09
@desc: 功能描述。
"""

import numpy as np


def wilson_score(pos, total, p_z=2.0):
    """
    威尔逊得分计算函数
    参考：https://en.wikipedia.org/wiki/Binomial_proportion_confidence_interval
    :param pos: 正例数
    :param total: 总数
    :param p_z: 正太分布的分位数
    :return: 威尔逊得分
    """
    pos_rat = pos * 1.0 / total * 1.0  # 正例比率
    score = (
        pos_rat
        + (np.square(p_z) / (2.0 * total))
        - (
            (p_z / (2.0 * total))
            * np.sqrt(4.0 * total * (1.0 - pos_rat) * pos_rat + np.square(p_z))
        )
    ) / (1.0 + np.square(p_z) / total)
    return score


def wilson_score_norm(mean, var, total, p_z=2.0):
    """
    威尔逊得分计算函数 正态分布版 支持如5星评价，或百分制评价
    :param mean: 均值
    :param var: 方差
    :param total: 总数
    :param p_z: 正太分布的分位数
    :return:
    """
    # 归一化，符合正太分布的分位数
    score = (
        mean
        + (np.square(p_z) / (2.0 * total))
        - ((p_z / (2.0 * total)) * np.sqrt(4.0 * total * var + np.square(p_z)))
    ) / (1 + np.square(p_z) / total)
    return score


def of_values():
    """
    五星评价的归一化实例，百分制类似
    :return: 总数，均值，方差
    """
    max = 5.0  # 五星评价的最大值
    min = 1.0  # 五星评价的最小值
    values = np.array([1.0, 2.0, 3.0, 4.0, 5.0])  # 示例

    norm_values = (values - min) / (max - min)  # 归一化
    total = norm_values.size  # 总数
    mean = np.mean(norm_values)  # 归一化后的均值
    var = np.var(norm_values)  # 归一化后的方差
    return total, mean, var


# total, mean, var = of_values()
# print ("total: %s, mean: %s, var: %s" % (total, mean, var))

# print ('score: %s' % wilson_score_norm(mean=mean, var=var, total=total))
# print ('score: %s' % wilson_score(90, 90 + 10, p_z=2.))
# print ('score: %s' % wilson_score(90, 90 + 10, p_z=6.))
# print ('score: %s' % wilson_score(900, 900 + 100, p_z=6.))

if __name__ == "__main__":
    print("score: %s" % wilson_score(1, 2, p_z=2.0))
    print("score: %s" % wilson_score(4, 10, p_z=2.0))

    print("*" * 20)

    print("score: %s" % wilson_score(1, 2, p_z=6.0))
    print("score: %s" % wilson_score(4, 10, p_z=6.0))

    print("*" * 20)

    print("score: %s" % wilson_score(4, 36, p_z=2.0))

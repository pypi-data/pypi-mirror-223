"""
@Time   : 2019/3/25
@author : lijc210@163.com
@Desc:  : 功能描述。
"""
import os
import sys

import pytest


def inc(x):
    return x + 1


def test_answer():
    assert inc(4) == 5


if __name__ == "__main__":
    filename = os.path.basename(sys.argv[0])
    pytest.main(args=[filename])

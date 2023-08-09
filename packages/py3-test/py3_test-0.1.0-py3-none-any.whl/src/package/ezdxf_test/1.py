"""
@File    :   1.py
@Time    :   2021/03/19 16:12:01
@Author  :   lijc210@163.com
@Desc    :   None
"""

import ezdxf

rect_points_outer = [(1.0, 1.0), (8.0, 1.0), (8.0, 8.0), (1.0, 8.0)]
rect_points_inner = [(2.0, 2.0), (7.0, 2.0), (7.0, 7.0), (2.0, 7.0)]

# 函数不支持自动闭环，为了形成封闭区域，把第一个点增加到点集的尾部
rect_points_outer.append(rect_points_outer[0])
rect_points_inner.append(rect_points_inner[0])

dwg = ezdxf.new("R2010")
modespace = dwg.modelspace()
modespace.add_lwpolyline(rect_points_outer)
modespace.add_lwpolyline(rect_points_inner)
dwg.saveas("rectangle.dxf")

"""
@Time   : 2018/9/11
@author : lijc210@163.com
@Desc:  : 功能描述。
"""

import os

import cv2

fn = "v0200fdc0000bcboatnvrnhmsq8f2l70.mp4"

print(os.path.getsize(fn) / 1024, "kb")
cap = cv2.VideoCapture(fn)
print(cap.get(cv2.CAP_PROP_POS_MSEC))
print(cap.get(cv2.CAP_PROP_POS_AVI_RATIO))
print(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
print(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
print(cap.get(cv2.CAP_PROP_FPS))
print(cap.get(cv2.CAP_PROP_FRAME_COUNT))

print(cap.get(cv2.CAP_PROP_FRAME_COUNT) / cap.get(cv2.CAP_PROP_FPS))

print("*" * 20)

fn = "v0200fc00000bcf385elg9jno07b3ncg.mp4"

print(os.path.getsize(fn) / 1024, "kb")
cap = cv2.VideoCapture(fn)
print(cap.get(cv2.CAP_PROP_POS_MSEC))
print(cap.get(cv2.CAP_PROP_POS_AVI_RATIO))
print(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
print(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
print(cap.get(cv2.CAP_PROP_FPS))
print(cap.get(cv2.CAP_PROP_FRAME_COUNT))

print(cap.get(cv2.CAP_PROP_FRAME_COUNT) / cap.get(cv2.CAP_PROP_FPS))

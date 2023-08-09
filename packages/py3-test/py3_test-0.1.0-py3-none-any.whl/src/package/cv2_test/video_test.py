"""
@Time   : 2018/9/11
@author : lijc210@163.com
@Desc:  : 功能描述。
"""

import os

import cv2


def video(fn):
    size = os.path.getsize(fn) / 1024  # 视频大小kb
    cap = cv2.VideoCapture(fn)
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)  # 宽
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)  # 高
    fps = cap.get(cv2.CAP_PROP_FPS)  # FPS
    count = cap.get(cv2.CAP_PROP_FRAME_COUNT)  # 总帧数
    time_long = count / fps  # 时长
    print(size)
    print(width, height)
    print(time_long)
    print(size / time_long)

    if 320 * 568 <= width * height < 540.0 * 960.0:
        if size / time_long < 35:
            print("轮播")
    elif 540.0 * 960.0 <= width * height < 576.0 * 1024.0:
        if size / time_long < 120:
            print("轮播")
    elif 576.0 * 1024.0 <= width * height:
        if size / time_long < 150:
            print("轮播")
    print("*" * 20)


if __name__ == "__main__":
    for filename in os.listdir(r"video4"):
        print(filename)
        video("video4/" + filename)

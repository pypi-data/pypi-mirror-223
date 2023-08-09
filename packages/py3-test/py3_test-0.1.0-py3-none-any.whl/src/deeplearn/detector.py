"""
detector.py
-------
文字定位器，
定位身份证中的文字区块.
@author: Heng Ding
@e-mail: hengding@whu.edu.cn
"""
import cv2
import numpy as np


class TextDetector:
    """文字定位器类"""

    def __init__(self, img_path):
        self.img = cv2.imread(img_path)
        self.resize_img = self.transform()

    def transform(self):
        """归一化尺寸，将图片缩放到统一尺寸"""
        h, w, c = np.shape(self.img)
        f_h = 1920
        f_y = float(h) / 1920
        f_w = int(float(w) / f_y)
        resize_img = cv2.resize(self.img, (f_w, f_h), interpolation=cv2.INTER_AREA)
        # cv2.imwrite("resize_img.jpg", resize_img)
        return resize_img

    def hyp_parameters(self):
        """计算经验参数"""
        h, w, c = np.shape(self.resize_img)
        # 文字区块最小最大面积
        min_area, max_area = 27 * 2700, 0.05 * h * w
        # min_area, max_area = 27*27, 400 * 150
        # 文字区块最小最大高度
        min_h, max_h = 100, 1000
        return min_area, max_area, min_h, max_h

    def find_candidates(self):
        """返回候选文字区块坐标"""
        # 灰度化
        gray = cv2.cvtColor(self.resize_img, cv2.COLOR_BGR2GRAY)
        # cv2.imwrite("gray.jpg", gray)
        # 二值化
        _threshold = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)[1]
        # cv2.imwrite("_threshold.jpg", _threshold)
        # 腐蚀
        kernel = np.ones((27, 27), np.uint8)
        erosion = cv2.erode(_threshold, kernel, iterations=2)
        # cv2.imwrite("erosion.jpg", erosion)
        # 轮廓检测
        _, contours, hierarchy = cv2.findContours(
            erosion, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
        )
        # 根据经验参数选取区域
        candidate_boxes = []
        min_area, max_area, min_h, max_h = self.hyp_parameters()
        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)

            if min_area < cv2.contourArea(cnt) < max_area and min_h < h < max_h:
                candidate_boxes.append((x, y, x + w, y + h))
        return candidate_boxes

    def split_candidates(self, box, i):
        """候选区块切割"""
        # 灰度化
        gray = cv2.cvtColor(self.resize_img, cv2.COLOR_BGR2GRAY)
        # 二值化
        _threshold = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)[1]
        # 腐蚀
        kernel = np.ones((3, 5), np.uint8)
        erosion = cv2.erode(_threshold, kernel, iterations=2)
        # 获取区块对应腐蚀图像
        x1, y1, x2, y2 = box
        box_erosion = erosion[y1:y2, x1:x2]
        cv2.imwrite("box_erosion{}.jpg".format(i), box_erosion)
        # 依据连续空白区域进行列切割
        his = np.mean(box_erosion, axis=0)
        split_indexes, flag = [0], True
        for i in range(len(his)):
            c = his[i]
            if c != 255 and flag is True:
                split_indexes.append(i)
                flag = False
            elif c == 255 and flag is False:
                split_indexes.append(i)
                flag = True
        split_indexes.append(len(his))
        # assert len(split_indexes) % 2 == 0
        t = [
            int((i + j) / 2)
            for i, j in zip(split_indexes[::2], split_indexes[1::2], strict=True)
        ]
        boxes = [
            (x1 + t[i], y1, x1 + t[i + 1], y2)
            for i in range(len(t) - 1)
            if t[i + 1] - t[i]
        ]
        return boxes

    def is_noisy(self, box):
        """基于坐标规则判断是否属于人脸噪声区块"""
        h, w, c = np.shape(self.resize_img)
        x1, y1, x2, y2 = box
        if (x1 + x2) / 2 > 0.65 * w and (y1 + y2) / 2 < 0.7 * h:
            return True
        return False

    # def detect(self):
    #     # 初步查找候选区域
    #     candidate_boxes = self.find_candidates()
    #     # 初步候选区域切割
    #     split_boxes = []
    #     for candidate in candidate_boxes:
    #         if candidate[2]-candidate[0] > 100:
    #             split_boxes += self.split_candidates(candidate)
    #         else:
    #             split_boxes += [candidate]
    #     # 屏蔽人脸区域噪音
    #     final_boxes = []
    #     for box in split_boxes:
    #         if not self.is_noisy(box):
    #             final_boxes.append(box)
    #     return final_boxes

    def detect(self):
        # 初步查找候选区域
        candidate_boxes = self.find_candidates()
        # 初步候选区域切割

        x, y, x_w, y_h = [], [], [], []
        for _i, candidate in enumerate(candidate_boxes):
            x.append(candidate[0])
            y.append(candidate[1])
            x_w.append(candidate[2])
            y_h.append(candidate[3])
        candidate = (min(x), min(y), max(x_w), max(y_h))
        d = self.resize_img
        # cv2.imwrite("test.jpg", d[candidate[1]:candidate[3],candidate[0]:candidate[2]])
        print(candidate[0], candidate[1], candidate[2], candidate[3])
        img_dict = {}
        # d[y1:y2, x1:x2]
        big_w = candidate[2] - candidate[0]
        big_h = candidate[3] - candidate[1]
        img_dict["name"] = {
            "image": d[
                candidate[1] : candidate[1] + int(big_h * 0.12),
                candidate[0] : candidate[0] + int(big_w * 0.3),
            ],
            "w": int(big_w * 0.3),
            "h": int(big_h * 0.12),
        }
        img_dict["sex"] = {
            "image": d[
                candidate[1] + int(big_h * 0.17) : candidate[1] + int(big_h * 0.28),
                candidate[0] : candidate[0] + int(big_w * 0.06),
            ],
            "w": int(big_w * 0.06),
            "h": int(big_h * 0.28) - int(big_h * 0.17),
        }
        img_dict["ethnicity"] = {
            "image": d[
                candidate[1] + int(big_h * 0.17) : candidate[1] + int(big_h * 0.28),
                candidate[0] + int(big_w * 0.26) : candidate[0] + int(big_w * 0.32),
            ],
            "w": int(big_w * 0.32) - int(big_w * 0.26),
            "h": int(big_h * 0.28) - int(big_h * 0.17),
        }
        img_dict["bd"] = {
            "image": d[
                candidate[1] + int(big_h * 0.32) : candidate[1] + int(big_h * 0.42),
                candidate[0] : candidate[0] + int(big_w * 0.45),
            ],
            "w": int(big_w * 0.45),
            "h": int(big_h * 0.42) - int(big_h * 0.3),
        }
        img_dict["addr"] = {
            "image": d[
                candidate[1] + int(big_h * 0.43) : candidate[1] + int(big_h * 0.88),
                candidate[0] : candidate[0] + int(big_w * 0.58),
            ],
            "w": int(big_w * 0.58),
            "h": int(big_h * 0.88) - int(big_h * 0.43),
        }
        img_dict["id"] = {
            "image": d[
                candidate[1] + int(big_h * 0.88) : candidate[1] + int(big_h * 0.99),
                candidate[0] + int(big_w * 0.2) : candidate[0] + int(big_w * 0.95),
            ],
            "w": int(big_w * 0.95) - int(big_w * 0.2),
            "h": int(big_h * 0.99) - int(big_h * 0.88),
        }

        cv2.imwrite("name.jpg", img_dict["name"]["image"])
        cv2.imwrite("sex.jpg", img_dict["sex"]["image"])
        cv2.imwrite("ethnicity.jpg", img_dict["ethnicity"]["image"])
        cv2.imwrite("bd.jpg", img_dict["bd"]["image"])
        cv2.imwrite("addr.jpg", img_dict["addr"]["image"])
        cv2.imwrite("id.jpg", img_dict["id"]["image"])

        return img_dict

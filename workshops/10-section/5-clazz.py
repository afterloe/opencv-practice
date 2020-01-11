#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv

"""
    描述子匹配
        图像特征检测首先会获取凸显关键点，然后根据关键点周围像素的ROI区域的大小，生成描述子，完整的描述子自向量就表示了一张图的特征，是
    图像特征数据，这种方式也被称为图像特征工程，即通过先验证模型模型与合理计算得到图像特征数据的过程。opencv提供了两种图像特征匹配算法分
    别是暴力匹配、FLANN匹配。FLANN是一种高效的数值或字符串匹配算法，SIFT/SURF是基于浮点数的匹配，ORB是二值匹配，速度更快。
"""


def main():
    meter = cv.imread("../../../raspberry-auto/pic/Meter.jpg")
    meter_find = cv.imread("../../../raspberry-auto/pic/Meter_in_word.png")
    meter = cv.medianBlur(meter, 9)
    meter_find = cv.medianBlur(meter_find, 9)
    orb = cv.ORB_create()
    kp1, des1 = orb.detectAndCompute(meter, None)
    kp2, des2 = orb.detectAndCompute(meter_find, None)
    bf = cv.BFMatcher(cv.NORM_HAMMING, crossCheck=True)
    matches = bf.match(des1, des2)
    matches = sorted(matches, key=lambda x: x.distance)
    result = cv.drawMatches(meter, kp1, meter_find, kp2, matches[:10], None)
    cv.namedWindow("orb-match", cv.WINDOW_NORMAL)
    cv.imshow("orb-match", result)
    cv.waitKey(0)
    cv.destroyAllWindows()


if "__main__" == __name__:
    main()

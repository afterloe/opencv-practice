#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv

"""
    BRIEF特征描述子
        通过BRIEF特征点数据后，根据BRIEF算法建立描述子，选择特征点周围SxS大小的像素块，随机选择n对像素点，其中p(x)是图像模糊处理后的
    像素值，通常使用均值滤波代替高斯滤波以便利用积分图方式加速计算获得更好的性能表现，常见的滤波卷积核在(3, 3)~ (9,9)之间。
"""


def main():
    tmp = cv.imread("../../../raspberry-auto/pic/IMG_20191204_151145.jpg")
    src = cv.imread("../../../raspberry-auto/pic/money.jpg")

    src = cv.medianBlur(src, 3)
    tmp = cv.medianBlur(tmp, 3)

    orb = cv.ORB_create()
    kp1, des1 = orb.detectAndCompute(tmp, None)
    kp2, des2 = orb.detectAndCompute(src, None)

    bf = cv.BFMatcher(cv.NORM_HAMMING, crossCheck=True)
    matches = bf.match(des1, des2)

    result = cv.drawMatches(tmp, kp1, src, kp2, matches, None)
    cv.namedWindow("result", cv.WINDOW_NORMAL)
    cv.imshow("result", result)
    cv.waitKey(0)
    cv.destroyAllWindows()


if "__main__" == __name__:
    main()

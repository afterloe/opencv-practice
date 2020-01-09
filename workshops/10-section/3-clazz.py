#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv
import numpy as np

"""
    ORB FAST特征关键点提取
        ORB - (Oriented Fast and Rotated BRIEF)算法是基于FAST特征检测与BRIEF特征描述子匹配实现，相比BRIEF算法中依靠随机方式获取
    而值点对，ORB通过FAST方法，FAST方式寻找候选特征点方式是假设灰度图像像素点A周围的像素存在连续大于或者小于A的灰度值。至少其中三个点
    满足上述不等式条件，即可将P视为候选点，然后通过阈值进行最终的筛选即可得到ORB特征点。相关API描述如下：
    
    cv.ORB::create()
"""


def main():
    src = cv.imread("../../../raspberry-auto/pic/ele_panel.jpg")
    blur = cv.medianBlur(src, 3)
    cv.imshow("src", src)
    orb = cv.ORB.create()
    kps = orb.detect(blur)
    i = 0
    color = np.random.randint(0, 255, (len(kps), 3))
    for kp in kps:
        x, y = kp.pt
        cv.circle(src, (np.int32(x), np.int32(y)), 5, color[i].tolist(), 2)
        i += 1
    # result = cv.drawKeypoints(src, kps, None, (0, 255, 0), cv.DrawMatchesFlags_DEFAULT)  # opencv 中的用的 kp绘制方法
    cv.imshow("dst", src)
    cv.waitKey(0)
    cv.destroyAllWindows()


if "__main__" == __name__:
    main()

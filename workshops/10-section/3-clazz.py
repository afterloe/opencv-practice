#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv
import numpy as np

"""
    ORB FAST特征关键点提取
        ORB - (Oriented Fast and Rotated BRIEF)算法是基于FAST特征检测与BRIEF特征描述子匹配实现，相比BRIEF算法中依靠随机方式获取
    而值点对，ORB通过FAST方法，FAST方式寻找候选特征点方式是假设灰度图像像素点A周围的像素存在连续大于或者小于A的灰度值。至少其中三个点
    满足上述不等式条件，即可将P视为候选点，然后通过阈值进行最终的筛选即可得到ORB特征点。相关API描述如下：
    
    cv.ORB::create(nfeatures, scaleFactor, nlevels, edgeThreshold, firstLevel, WTA_K, scoreType, patchSize,
                    fastThreshold)
        - nfeatures: 最终输出最大特征点数目
        - scaleFactor: 金字塔上采样比率
        - nlevels: 金字塔层数
        - edgeThreshold: 边缘阈值
        - firstLevel:  从第几层级开始，默认为0，即第一层
        - WTA_K: BRIEF描述算子所用的
        - scoreType: 对所有的特征点进行排民用的方法
        - patchSize: 定向修复的大小，越大修复比率越高
        - fastThreshold: fast算法阈值 
"""

MAX_POINTS = 500
orb_param = dict(nfeatures=MAX_POINTS, scaleFactor=1.2, nlevels=8, edgeThreshold=31, firstLevel=0)
color = np.random.randint(0, 255, (MAX_POINTS, 3))


def main():
    src = cv.imread("../../../raspberry-auto/pic/ele_panel.jpg")
    blur = cv.medianBlur(src, 3)
    cv.imshow("src", src)
    orb = cv.ORB.create(**orb_param)
    kps = orb.detect(blur)
    i = 0
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

#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv

"""
    使用Hu矩实现轮廓匹配：
        对二值图的各个轮廓进行几何矩计算，根据几何矩获取图像的中心位置，再根据中心位置计算中心矩与hu矩。opencv中通过一个api就可以计算出
    上述三种矩。
    
        cv.moments(contours, binaryImage)
            - contours: 轮廓
            - binaryImage: 二值图返回
        
        cv.HuMoments(&Moments, hu)
            - &Moments: moments计算后的图像矩
            - hu: 输出的hu矩七个值
            
        cv.matchShapes(contour1, contour2, method)
            - contour1, contour2: 轮库点集合或灰度图像
            - method: 匹配算法
                      CONTOURS_MATCH_I1  常用
                      CONTOURS_MATCH_I2
                      CONTOURS_MATCH_I3
"""


T = 80


# 轮廓提取
def contours_extract(image):
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    # 由于输入的图像为白底黑字的内容，所以在二值图上进行取反操作
    _, binary = cv.threshold(gray, 0, 255, cv.THRESH_BINARY_INV | cv.THRESH_TRIANGLE)  # 单峰图像
    contours, _ = cv.findContours(binary, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    return contours


def main():
    src = cv.imread("../../pic/fonts.png")
    target = cv.imread("../../pic/one.png")

    # 轮廓发现
    contours_src = contours_extract(src)
    contours_target = contours_extract(target)

    # 几何矩计算与hu矩计算
    mm_target = cv.moments(contours_target[0])  # 计算几何矩
    hum_target = cv.HuMoments(mm_target)  # 计算hu矩

    # 轮廓匹配
    for index in range(len(contours_src)):
        mm = cv.moments(contours_src[index])
        hum = cv.HuMoments(mm)
        dist = cv.matchShapes(hum, hum_target, cv.CONTOURS_MATCH_I1, 0)
        if 0.5 > dist:
            cv.drawContours(src, contours_src, index, (255, 0, 0), 2, cv.LINE_8)
        print("dist %f " % dist)

    cv.namedWindow("dist", cv.WINDOW_KEEPRATIO)
    cv.imshow("dist", src)
    cv.waitKey(0)
    cv.destroyAllWindows()


if "__main__" == __name__:
    main()

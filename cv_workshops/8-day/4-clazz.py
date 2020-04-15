#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv

"""
    图像去水印/修复
        opencv中有时候需要批量去水印，其本质上是一中图像修复，该api如下：
            cv.inpaint(src, inpaintMask, dst, napaintRaduis, fags)
                - src: 需要修复的图像
                - inpaintMask: 图形遮罩(水印)
                - inpaintRadius: 图像修复半径，半径越小印象越小
                - fags: cv::INPAINT_NS or cv::INPAINT_TELEA
        去水印的关键是图形遮罩的寻找，最好的方式是找美工将水印抠出来作证模板，然后进行处理即可
"""


def main():
    src = cv.imread("../../pic/master2.jpg")
    cv.imshow("src", src)
    # 通过颜色 搜寻水印
    hsv = cv.cvtColor(src, cv.COLOR_BGR2HSV)
    # 蓝色hsv色系
    lower = (100, 43, 46)
    upper = (124, 255, 255)
    mask = cv.inRange(hsv, lower, upper)
    cv.imshow("mask", mask)
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (3, 3))
    mask = cv.morphologyEx(mask, cv.MORPH_DILATE, kernel)
    result = cv.inpaint(src, mask, 3, cv.INPAINT_TELEA)
    cv.imshow("result", result)
    cv.waitKey(0)
    cv.destroyAllWindows()


if "__main__" == __name__:
    main()

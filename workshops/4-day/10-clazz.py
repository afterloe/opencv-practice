#!/usr/bi/env python
# -*- coding=utf-8 -*-

import cv2 as cv
import numpy as np

"""
    二值图像:
        将图像像素点按照一定阈值进行切分，大于该阀值时像素点值为1，小于阀值时像素点值为0。二值图像处理与分析在机器视觉与
    机器自动化中非常重要，主要用于解决该领域内的轮廓分析、对象测量、轮廓匹配、识别、形态学处理与分割、各种形状检测、拟
    合、投影与逻辑操作、轮廓特征提取与编码等。
    
    主要流程1) 输入图像； 2）转换为灰度图像； 3）计算图像均值；4）按均值对图像进行二值化操作
"""


def binary_pic(mean, gray):
    h, w = gray.shape
    binary = np.zeros((h, w), dtype=np.uint8)
    for row in range(h):
        for col in range(w):
            binary[row, col] = 0 if mean > gray[row, col] else 255
    cv.imshow("binary", binary)


def main():
    src = cv.imread("../../pic/luoxiaohei.jpg")
    cv.imshow("src", src)
    gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
    mean = cv.mean(gray)[0]  
    print(mean)
    binary_pic(mean, gray)
    cv.waitKey(0)
    cv.destroyAllWindows()


if "__main__" == __name__:
    main()

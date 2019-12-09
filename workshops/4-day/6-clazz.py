#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv

"""
    canny边缘检测算法，该算法是一种经典的图像边缘检测与提取算法，该算法的主要具备以下几个特点:
        1. 有效的噪声抑制
        2. 更强的完整边缘提取
    主要用于机器视觉、内容标注、目标识别等领域。
    
    canny算法的实现步骤如下:
        - 对采集图像进行高斯模糊，抑制并去除噪声
        - 对x、y两个方向使用二阶偏导数进行像素梯度运算，获得候选边缘
        - 角度计算与非最大型号抑制，避免过度曝光与过度黑暗
        - 候选边缘过滤，进行高低阀值连接，获取完整边缘。高于高阀值的全部保留，低于低阀值的全部舍弃，在两个阀值之间的按照
    8领域方式进行中心像素连接，不能连接的舍弃；
        - 输出边缘    
        
    cv.Canny(src, threshold1, threshold2, apertureSize, L2gradient)
        - threshold1 -> 低阀值 (高阀值的一半 或 三分之一，即低高阀值之比为1:2 或 1:3)
        - threshold2 -> 高阀值 (尽量不超过400)
        - apertureSize -> Sobel算子(一阶求导算子，梯度计算)的卷积核大小，默认3即 3 * 3
        - L2gradient -> 连接算法选取 False， 采用L1算法即绝对值计算； false ， 采用L2算法，平方和开根号进行向量计算
        
    canny 输入可以是三通道彩色图片，也可以使单通道灰度图像，输出为单通道二值图像
"""


def main():
    src = cv.imread("../../pic/luoxiaohe.jpg")
    cv.imshow("src", src)
    # 使用Sobel 3*3 算子获取像素梯度，并采用L1方式连接边缘
    canny = cv.Canny(src, 100, 300, apertureSize=3, L2gradient=False)
    cv.imshow("canny", canny)
    dst = cv.bitwise_and(src, src, mask=canny)  # 原色边框
    cv.imshow("dst", dst)
    cv.waitKey(0)
    cv.destroyAllWindows()


if "__main__" == __name__:
    main()

#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv

"""
    图像梯度 - 拉普拉斯算子（二阶导数算子）
        二阶导数算子可快速检测图像边缘，其原理同一阶导数算子类似，只不过在x，y方向的二阶偏导数。一般来说是4领域增强，也
    可以进一步扩展增强为8领域。由于二阶偏导数的关系，图像在处理过程易受到噪声的影响， 一般先使用高斯进行降噪，在进行
    计算。
    
    cv.Laplacian(src, ddepth, ksize, scale, delta, borderType)
        ddepth - 图像深度，默认为-1， 表示输入输出图像相同
        kszie - 卷积核， 默认是1 （4领域）， 必须为奇数， 大于1则表示为 8领域算子
        scale - 缩放比率， 1表示不变
        delta - 对输出图像加上常量值(即第三通道RGB + delta)
        borderType - 边缘处理方法
"""


def main():
    src = cv.imread("../../pic/IMG_20191204_151110.jpg")
    cv.imshow("src", src)
    gaussian = cv.GaussianBlur(src, (0, 0), 1)  # 使用高斯模糊 对 src进行降噪处理
    # 对降噪处理后的图像进行 8领域求导， 求导后颜色接近于0，使用delta增加亮度
    dst = cv.Laplacian(gaussian, cv.CV_32F, ksize=3, delta=127)  # ksize - 1 4领域 3 - 8领域
    dst = cv.convertScaleAbs(dst)
    cv.imshow("dst", dst)
    cv.waitKey(0)
    cv.destroyAllWindows()


if "__main__" == __name__:
    main()

#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv

"""
    拉普拉斯金字塔：
        拉普拉斯金字塔基于图像金字塔进行处理，对不同分辨率的结果进行反向扩充，举例如下：
            - 输入图像G0
            - 图像金字塔 reduce生成 G1 G2 G3
            - 拉普拉斯金字塔 L0 = G0 - expand(G1)
                             L1 = G1 - expand(G2)
                             L2 = G2 - expand(G3)
        G0减去expand(G1)得到的结果就是两次高斯模糊输出的不同，所以L0称为DOG（高斯不同）
"""


# 生成图像金字塔 -> 金字塔向上，逐步缩小
def generator_pyramid_up(image, level=3):
    temp = image.copy()
    pyramid = []
    for i in range(level):
        dst = cv.pyrDown(temp)
        pyramid.append(dst)
        temp = dst.copy()
    return pyramid


def generator_laplacian_pyramid(image, pyramid_pic):
    level = len(pyramid_pic)
    # range(start, stop[, step])
    for i in range(level - 1, -1, -1):
        if 0 > i - 1:
            expand = cv.pyrUp(pyramid_pic[i])
            # 亮度增加127 方便演示，前往不要在非演示环境添加该阀值，防止后续操作错处
            lpls = cv.subtract(image, expand) + 127
            cv.imshow("lpls_" + str(i), lpls)
        else:
            h, w = pyramid_pic[i - 1].shape[:2]
            lpls = cv.subtract(pyramid_pic[i - 1], expand) + 127
            cv.imshow("lpls_" + str(i), lpls)
    cv.waitKey(0)
    cv.destroyAllWindows()


def main():
    src = cv.imread("../../pic/3.png")
    pyramid = generator_pyramid_up(src)
    generator_laplacian_pyramid(src, pyramid)


if "__main__" == __name__:
    main()

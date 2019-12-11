#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv

"""
    单峰直方图二值寻找算法 - TRIANGLE:
        单峰直方图的波峰与直方图顶部连线，并绘制直接三角形，在三角形上算出高，并将高的位置平移已确定阀值。opencv实现过
    程中将单峰直方图进行取反操作（即不用担心波峰离0或255过于接近而导致阈值不准确的问题）,使用时在threshold中将type指定
    为THRESH_TRIANGLE即可。 该方法对双峰直方图效果表示并不是很好
"""


def main():
    src = cv.imread("../../pic/luoxiaohei.jpg")
    cv.imshow("src", src)
    gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
    ret, binary = cv.threshold(gray, 0, 255, cv.THRESH_BINARY | cv.THRESH_TRIANGLE)
    print("ret: ", ret)
    cv.imshow("binary", binary)
    cv.waitKey(0)
    cv.destroyAllWindows()


if "__main__" == __name__:
    main()

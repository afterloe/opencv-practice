#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv

"""
    二值阈值寻找算法 - OTSU
        OTSU算法适合对直方图具有两个峰的图像，对于只有一个峰的图像，该算法的阈值获取并不是十分理想。
        在cv.threshold中使用将type指定为 THRESH_OTSU即可
"""


def main():
    src = cv.imread("../../pic/money.jpg")
    cv.imshow("src", src)
    gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
    ret, binary = cv.threshold(gray, 0, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)
    print("ret: ", ret)
    cv.imshow("binary", binary)
    _, binary = cv.threshold(gray, cv.mean(gray)[0], 255, cv.THRESH_BINARY)
    cv.imshow("mean binary", binary)  # 均值的效果比 OTSU的要差
    cv.waitKey(0)
    cv.destroyAllWindows()


if "__main__" == __name__:
    main()

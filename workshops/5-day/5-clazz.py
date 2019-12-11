#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv

"""
    图像降噪与二值化对比， 快速降噪即 blur的方式效果较好
"""


def with_gaussian(src):
    blur = cv.bilateralFilter(src, 0, 130, 15)
    gray = cv.cvtColor(blur, cv.COLOR_BGR2GRAY)
    ret, binary = cv.threshold(gray, 0, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)
    print("with gaussian blur (bilateralFilter) ret is ", ret)
    return binary


def with_mean_blur(src):
    blur = cv.pyrMeanShiftFiltering(src, 10, 100)
    gray = cv.cvtColor(blur, cv.COLOR_BGR2GRAY)
    ret, binary = cv.threshold(gray, 0, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)
    print("with mean blur (pyrMeanShiftFiltering) ret is ", ret)
    return binary


def with_blur(src):
    blur = cv.blur(src, (15, 15))
    gray = cv.cvtColor(blur, cv.COLOR_BGR2GRAY)
    ret, binary = cv.threshold(gray, 0, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)
    print("with quick blur ret is ", ret)
    return binary


def without_blur(src):
    gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
    ret, binary = cv.threshold(gray, 0, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)
    print("without blur ret is ", ret)
    return binary


def main():
    src = cv.imread("../../pic/money.jpg")
    cv.imshow("src", src)
    binary = without_blur(src)
    cv.imshow("without blur", binary)
    binary = with_blur(src)
    cv.imshow("quick blur", binary)
    binary = with_mean_blur(src)
    cv.imshow("pyrMeanShiftFiltering", binary)
    binary = with_gaussian(src)
    cv.imshow("bilateralFilter", binary)
    cv.waitKey(0)
    cv.destroyAllWindows()


if "__main__" == __name__:
    main()

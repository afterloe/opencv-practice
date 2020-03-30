#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv
import imutils
import math
import numpy as np
import time

"""

"""


def get_point_line_distance(point, line):
    point_x = point[0]
    point_y = point[1]
    line_s_x = line[0][0]
    line_s_y = line[0][1]
    line_e_x = line[1][0]
    line_e_y = line[1][1]
    #若直线与y轴平行，则距离为点的x坐标与直线上任意一点的x坐标差值的绝对值
    if line_e_x - line_s_x == 0:
        return math.fabs(point_x - line_s_x)
    #若直线与x轴平行，则距离为点的y坐标与直线上任意一点的y坐标差值的绝对值
    if line_e_y - line_s_y == 0:
        return math.fabs(point_y - line_s_y)
    #斜率
    k = (line_e_y - line_s_y) / (line_e_x - line_s_x)
    #截距
    b = line_s_y - k * line_s_x
    #带入公式得到距离dis
    dis = math.fabs(k * point_x - point_y + b) / math.pow(k * k + 1, 0.5)
    return dis


def t(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def main():
    image = cv.imread("G:\\Project\\opencv-ascs-resources\\meter_pointer_roi\\2020-03-05_22-18-25.jpeg")
    # image = cv.imread("/Users/afterloe/Project/opencv-ascs-resources/meter_pointer_roi/2020-03-05_22-18-30.jpeg")
    start = time.time()
    image = imutils.resize(image, width=500)
    h, w = image.shape[: 2]
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    gray = cv.bilateralFilter(gray, 11, 17, 17)
    blurred = cv.GaussianBlur(gray, (5, 5), 0)
    threshed = cv.adaptiveThreshold(blurred, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY_INV, 25, 10)
    lines = cv.HoughLinesP(threshed, 1, np.pi / 180, 180, None, 100, 10)

    # 绘制图像中心点
    # cv.circle(image, (np.int32(w // 2), np.int32(h // 2)), 2, (255, 0, 0), 2, cv.LINE_8)

    if None is lines:
        print("未检测到直线")
        return
    pointer = None
    dist = h
    # 找出指针
    for index in range(len(lines)):
        line = lines[index][0]  # 检测到的直线信息
        d = t(line[2], line[3], w, h)
        if d < dist:
            dist = d
            pointer = line[:4]
    # 绘制指针
    cv.line(image, (pointer[0], pointer[1]), (pointer[2], pointer[3]), (0, 255, 255), 1, cv.LINE_AA)

    cnts = cv.findContours(threshed, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    dig_cnts = []

    for cnt in cnts:
        x, y, w, h = cv.boundingRect(cnt)
        if 25 < h < 35 and 8 < w < 25:
            rect = cv.minAreaRect(cnt)
            cx, cy = rect[0]  # 中心点
            # box = cv.boxPoints(rect)
            # box = np.int32(box)
            # cv.drawContours(image, [box], 0, (0, 0, 255), 2, cv.LINE_8)
            # cv.circle(image, (np.int32(cx), np.int32(cy)), 2, (255, 0, 0), 2, cv.LINE_8)
            dig_cnts.append((x, y, w, h, cx, cy))  # 提取数字
            # cv.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
    for i in range(len(dig_cnts)):
        img = image.copy()
        i_x, i_y, i_w, i_h, i_c_x, i_c_y = dig_cnts[i]
    #     cv.circle(img, (np.int32(i_c_x), np.int32(i_c_y)), 2, (255, 0, 0), 2, cv.LINE_8)
    #     cv.line(img, (i_x, i_y), (i_x + i_w, i_y + i_h), (0, 255, 255), 1, cv.LINE_AA)
        cv.rectangle(img, (i_x, i_y), (i_x + i_w, i_y + i_h), (255, 255, 0), 2, cv.LINE_8)
        # cv.imshow("target", img)
        # cv.waitKey(0)
        for j in range(i, len(dig_cnts) - 1):
            j_x, j_y, j_w, j_h, j_c_x, j_c_y = dig_cnts[j]
            cv.circle(img, (np.int32(j_c_x), np.int32(j_c_y)), 2, (255, 0, 0), 2, cv.LINE_8)
            d = t(j_c_x, j_c_y, i_c_x, i_c_y)
            print(d)
            # cv.imshow("target", img)

            # cv.waitKey(0)
            if 25 > d:
                print(d)
                cv.line(img, (i_x, i_y), (j_x + j_w, j_y + j_h), (0, 255, 255), 1, cv.LINE_AA)
                # cv.imshow("target", img)
                # cv.waitKey(0)
    #             i_c_x, i_c_y = j_c_x, j_c_y
    #             cv.rectangle(image, (i_x, i_y), (i_x + j_w, i_y + j_h), (0, 0, 255), 2, cv.LINE_8)

    print(time.time() - start)
    cv.imshow("threshed", threshed)
    cv.imshow("target", image)

    cv.waitKey(0)


if "__main__" == __name__:
    main()
    cv.destroyAllWindows()

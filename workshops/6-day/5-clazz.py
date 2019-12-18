#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv

"""
    凸包检测
        对二值图获取轮廓之后，对获取的轮廓进行排序并链接，并对其进行过滤，将最外侧的定点链接形成一个凸形的区域。
        
        cv.convexHull(contours, closkwise, returnPoints)
            - contours: 轮廓集
            - clockwis: 顺时针或逆时针链接，bool, default False 顺时针
            - returnPoints: 返回类型, bool, default True 默认返回凸包的点集
"""


def main():
    src = cv.imread("../../pic/hand.jpg")
    cv.namedWindow("dst", cv.WINDOW_KEEPRATIO)
    blur = cv.medianBlur(src, 17)
    gray = cv.cvtColor(blur, cv.COLOR_BGR2GRAY)
    _, binary = cv.threshold(gray, 0, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)
    contours, _ = cv.findContours(binary, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    for index in range(len(contours)):
        contour = contours[index]
        ret = cv.isContourConvex(contour)  # 判断轮廓是否是凸包
        points = cv.convexHull(contour)  # 凸包计算
        total = len(points)  # 获取凸包的外接点数
        for i in range(total):
            x1, y1 = points[i % total][0]
            x2, y2 = points[(i + 1) % total][0]
            cv.circle(src, (x1, y1), 4, (255, 0, 0), 2, cv.LINE_8)
            cv.line(src, (x1, y1), (x2, y2), (0, 255, 0), 2, cv.LINE_8)
        print(points)
        print("convex: ", ret)
    cv.imshow("dst", src)
    cv.waitKey(0)
    cv.destroyAllWindows()


if "__main__" == __name__:
    main()

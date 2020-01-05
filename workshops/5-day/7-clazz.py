#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv
import numpy as np

"""
    连通组件状态统计:
        opencv中有关联通组件还有一个是携带其状态的api，`cv.connectedComponentsWithStats`， 使用该函数能够输出联通组件的统计情况。
        
        cv.connectedComponentsWithStats(binary, labels, status, centroids, connectivity, ltype, ccltype)
            - binary: 输入的二值图
            - labels: 输出的组件
            - status: 组件状态
            - centroids: 各组件的中心坐标
            - ltype: 组件类型
            - ccltype: 
            
        CC_STAT_LEFT:   连通组件外接矩形左上角坐标的X位置
        CC_STAT_TOP:    连通组件外接左上角坐标的Y位置
        CC_STAT_WIDTH:  连通组件外接矩形的宽度
        CC_STAT_HEIGHT: 连通组件外接矩形的高度
        CC_STAT_AREA:   连通组件的面积大小
"""


def main():
    src = cv.imread("../../pic/sw/sw_game_duiduipen.png")
    blur = cv.medianBlur(src, 41)
    gray = cv.cvtColor(blur, cv.COLOR_BGR2GRAY)
    _, binary = cv.threshold(gray, 0, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)
    num_labels, labels, stats, centers = cv.connectedComponentsWithStats(binary, connectivity=8, ltype=cv.CV_32S)
    colors = [(0, 0, 0)]
    for i in range(num_labels):
        r = np.random.randint(0, 256)
        g = np.random.randint(0, 256)
        b = np.random.randint(0, 256)
        colors.append((b, g, r))
    image = src.copy()
    for t in range(1, num_labels, 1):
        x, y, w, h, area = stats[t]
        cx, cy = centers[t]  # float 类型
        # 绘制组件 中心坐标点
        cv.circle(image, (np.int32(cx), np.int32(cy)), 2, (0, 255, 0), 2, cv.LINE_8, 0)
        # 绘制组件连接框
        cv.rectangle(image, (x, y), (x + w, y + h), colors[t], 1, cv.LINE_8, 0)
        cv.putText(image, "num: " + str(t), (x, y), cv.FONT_HERSHEY_SIMPLEX, .5, (0, 0, 255), 1)
        print("label index %d, area of the label: %d " % (t, area))
    cv.imshow("src", src)
    cv.imshow("dst", image)
    cv.waitKey(0)
    cv.destroyAllWindows()


if "__main__" == __name__:
    main()

#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv
import numpy as np

"""
    图像透视变换
        图像透视变换用于修正文本扫描图片时ROI区域倾斜，通过图像透视变换能够获取较好剪切效果。通过图像透视变化的好处如下：
            1 透视变换不会涉及到集合变换角度旋转
            2 透视变换对畸变图像有一定的展开效果（对于鱼眼摄像头，需要获的其摄像头的某些参数才行，否则需要自行编写算法）
            3 透视变换可以完成对图像的ROI区域提取
        关于图像透视变换的api描述如下：
            
            图像矫正及剪切获取变换矩阵
            cv.findHomography(srcPoints, dstPoints)
                - srcPoints: 原图像
                - dstPoints: 需要剪切的图像
            return mat, status -> 剪切的图像，状态
            
            透视变换
            cv.warpPerspective(srcPoints, mat, dsize)
                - srcPoints: 原图像
                - mat: 变换矩阵，由findHomography操作后的图像
                - dsize: 矩阵的大小
"""


def main():
    src = cv.imread("../../pic/FiRWhzOKMHfoUtDn50TMvbQhbBKl.png")
    gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
    blur = cv.GaussianBlur(gray, (15, 15), 0)    # 根据图像的特质， 进行高度模糊。 这样可避免进行最大轮库求取
    _, binary = cv.threshold(blur, 0, 255, cv.THRESH_BINARY_INV | cv.THRESH_OTSU)
    contours, _ = cv.findContours(binary, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    if 1 != len(contours):
        print("未寻找到轮廓或寻找到多个轮廓")
        return
    rect = cv.minAreaRect(contours[0])  # 最小外接矩形, 返回三个值 最小矩形的旋转角度、中心点坐标及大小
    height, width = rect[1]  # 获取中心点坐标
    box = cv.boxPoints(rect)  # 获取旋转矩形的的坐标信息
    src_pts = np.int0(box)  # 旋转矩形的坐标点
    # 重置mask的四个点的坐标信息，按照顺时针进行排序，ps 左上角为0,0
    dst_pts = [[width, height], [0, height], [0, 0], [width, 0]]
    # 通过图像单一矩阵计算实现图像矫正及剪切
    mat, status = cv.findHomography(src_pts, np.array(dst_pts))
    # 透视变换
    # src 输入图像； mat 变换矩阵； dsize 被变换图像的大小
    result = cv.warpPerspective(src, mat, (np.int32(width), np.int32(height)))
    if height < width:
        result = cv.rotate(result, cv.ROTATE_90_CLOCKWISE)
    cv.imshow("binary", binary)
    cv.imshow("result", result)
    cv.waitKey(0)
    cv.destroyAllWindows()


if "__main__" == __name__:
    main()

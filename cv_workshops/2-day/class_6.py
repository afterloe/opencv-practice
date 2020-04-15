#!/usr/bin/env python
# -*- coding=utf-8 -*-

"""
    ROI - region of interest 图像中感兴趣区域，用于降低图像处理的难度
"""

import cv2 as cv
import numpy as np
import imutils


# 规则图形的ROI提取 - 矩形
def ruleROIExtract(img):
    h, w = img.shape[:2]
    cv.imshow("input", img)
    cy = h // 2 - 50  # 获取ROI区域的起始位置
    cx = w // 2 - 80
    roi = img[cy - 2 * 100: cy + 2 * 100, cx - 2 * 100: cx + 2 * 100, :]  # 截取roi区域
    cv.imshow("roi", roi)  # 将截取的结果进行展示
    canvas = np.copy(roi)  # 拷贝 roi区域，因为该部分roi的指向仍为原图，若直接对原图进行操作会出现问题
    canvas = imutils.rotate(canvas, 90)  # image的官方库， 将roi区域旋转90度，方便进行识别
    roi[:, :, 0] = 255  # 直接修改roi的原图背景色， 发现图片直接受到影响
    cv.imshow("result", img)
    canvas[:, :, 2] = 0  # 对拷贝内容进行修改， 不影响原有图片
    cv.imshow("result", img)
    cv.imshow("copy roi", canvas)


"""
    技术路线:
    - ROI mask 提取
    - 像素 and操作
    - 提取非规则ROI区域
    - 创建背景图片
    - 背景图片与roi区域合成 or 操作
    - add 操作 背景图片 与 ROI区域
"""


# 不规则图像ROI提取
# 并替换ROI的背景色（即抠图 - 换背景 - 贴图）
def irregularityROIExtract(img):
    cv.imshow("src", img)
    roi_hsv_min = (0, 0, 46)  # 灰色 hsv 最小值
    roi_hsv_max = (180, 43, 220)  # 灰色 hsv 最大值
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    mask = cv.inRange(hsv, roi_hsv_min, roi_hsv_max)  # 提取模板 - 黑色表示 感兴趣的位置， 白色表示不感兴趣的位置
    mask = cv.bitwise_not(mask)  # 模板取反 - 将两个位置互换
    scale = cv.bitwise_and(img, img, mask=mask)  # 与操作, 将两张图片进行重合 （使用模板进行）， 将ROI抠出
    cv.imshow("roi", scale)
    result = np.zeros(img.shape, img.dtype)
    result[:, :, 0] = 255  # 将新创建的图片转换为 蓝色
    mask = cv.bitwise_not(mask)  # 再取反
    dst = cv.bitwise_or(scale, result, mask=mask)  # 与新创建颜色进行重合，将ROI其他颜色进行修改,已先添加的为准
    dst = cv.add(dst, scale)  # 加 操作 - 一定要注意的是 进行 逻辑操作 图像的dtype要一致！
    cv.imshow("dst", dst)


src = cv.imread("../../pic/1yuan.jpg", cv.IMREAD_COLOR)
ruleROIExtract(src)
cv.waitKey(0)
cv.destroyAllWindows()

src = cv.imread("../../pic/1.jpg", cv.IMREAD_COLOR)
irregularityROIExtract(src)
cv.waitKey(0)
cv.destroyAllWindows()

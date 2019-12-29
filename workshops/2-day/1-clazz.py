#!/usr/bin/env python
# -*- coding=utf-8 -*-

# 图像归一化处理的作用 主要是把各种处理好的数据转换为图像并正常显示或把图像转换为数据进行各种处理
# 归一化处理前 需要将数据转换为 float类型，避免出错

import cv2 as cv
import numpy as np

src = cv.imread("../../pic/rmb/10.png", cv.IMREAD_COLOR)
gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
gray = np.float32(gray)  # 将uint8的图像转换为 float32
print(gray)

dst = np.zeros(gray.shape, dtype=np.float32)  # 输入与输出的参数均为 float32， 避免出现错误
# 第一种 使用 min_max方法进行归一化操作
# 其中 alpha 表示 图像中 最小值； beta 表示图像中的 最大值
cv.normalize(src=gray, dst=dst, alpha=0, beta=1.0, norm_type=cv.NORM_MINMAX)
print("-----------------------> NORM_MINMA")
print(dst)
cv.imshow("NORM_MINMAX", np.uint8(dst * 255))  # 不进行转换会 输出黑色的图像

# 第二种 使用INF进行归一化操作
# 其中 alpha表示 图像中 最大值 1.0； beta 没有作用
dst = np.zeros(gray.shape, dtype=np.float32)
cv.normalize(src=gray, dst=dst, alpha=1.0, norm_type=cv.NORM_INF)
print("-----------------------> INF")
print(dst)
cv.imshow("NORM_INF", np.uint8(dst * 255))

# 第三种 使用L2 进行归一化操作
dst = np.zeros(gray.shape, dtype=np.float32)
cv.normalize(src=gray, dst=dst, alpha=1.0, norm_type=cv.NORM_L2)
print("-----------------------> L2")
print(dst)  # [0.00280968 0.00282692 0.00282692 ... 0.00294758 0.00293034 0.00289586] 否则都是黑色
cv.imshow("NORM_L2", np.uint8(dst * 255 * 100))  # *100 表示增强亮度

# 第四种 使用L1进行归一化操作
dst = np.zeros(gray.shape, dtype=np.float32)
cv.normalize(src=gray, dst=dst, alpha=1.0, norm_type=cv.NORM_L1)
print("-----------------------> L1")
print(dst)  # [4.8607994e-06 6.1377891e-06 6.6321077e-06 ... 4.2840943e-06 4.3252876e-06 4.4488670e-06]
cv.imshow("NORM_L1", np.uint8(dst * 255 * 100000))  # *100000 表示增强亮度, 不用乘的太过分，防止曝光（操作255）

cv.waitKey(0)
cv.destroyAllWindows()

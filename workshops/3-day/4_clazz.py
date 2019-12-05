#!/usr/bin/env python
# -*- coding=utf-8 -*-

import cv2 as cv
import numpy as np

"""
    图像噪声：
        图像噪声在模拟信号传输或数字信号传输过程中，图像发生了丢失或收到干扰而产生，亦或是成像设备如摄像头、照相机等的损
    坏、环境本身导致的成像质量不稳定，反映到图像上就是图像的亮度与颜色呈现某种程度的不一致性。常见噪声有以下几种：
        椒盐噪声： 随机分布在图像中的黑白像素点（使用中值滤波对该类噪声进行处理）
        高斯噪声： 成像设备收到物理/光/电等各种型号干扰产生的高斯分布噪声
        均匀分布噪声： 由于某些规律性的错误导致
"""


# 随机为照片添加椒盐噪声
def add_salt_pepper_noise(image):
    h, w = image.shape[:2]  # h, w, channel
    nums = 100000
    rows = np.random.randint(0, h, nums, dtype=np.int)
    cols = np.random.randint(0, w, nums, dtype=np.int)
    for i in range(nums):
        if 1 == i % 2:
            image[rows[i], cols[i]] = (255, 255, 255)
        else:
            image[rows[i], cols[i]] = (0, 0, 0)
    return image


# 随机为图像添加高斯噪声
def add_gaussian_noise(image):
    noise = np.zeros(image.shape, image.dtype)
    m = (15, 15, 15)
    s = (45, 45, 45)
    cv.randn(noise, m, s)
    dst = cv.add(image, noise)
    return dst


def main():
    src = cv.imread("../../pic/IMG_20191204_151110.jpg")
    cv.imshow("src", src)
    cv.imshow("salt pepper noise", add_salt_pepper_noise(src))
    cv.imshow("gaussian noise", add_gaussian_noise(src))
    cv.waitKey(0)
    cv.destroyAllWindows()


if "__main__" == __name__:
    main()

#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv
import numpy as np

"""
二维码检测与识别
    OpenCV在对象检测模块中QRCodeDetector有两个相关API分别实现二维码检测与二维码解析
    
二维码检测
bool cv::QRCodeDetector::detect(img, points)
    - img输入图像，灰度或者彩色图像
    - points 得到的二维码四个点的坐标信息

解析二维码
cv::QRCodeDetector::decode(img, points, straight_qrcode)
    - img输入图像，灰度或者彩色图像
    - points 二维码ROI最小外接矩形顶点坐标
    - qrcode 输出的是二维码区域ROI图像信息

返回的二维码utf-8字符串

上述两个API功能可以通过一个API调用实现， 该API如下:
cv::QRCodeDetector::detectAndDecode(img, points, straight_qrcode)
    描述如上
"""


def main():
    image = cv.imread("../../../raspberry-auto/pic/qrcode.jpg")
    # image = cv.resize(image, (720, 1280))
    cv.imshow("qrcode", image)
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    qrcode = cv.QRCodeDetector()
    codeinfo, points, straight_qrcode = qrcode.detectAndDecode(gray)
    print(points)
    result = np.copy(image)
    cv.drawContours(result, [np.int32(points)], 0, (255, 0, 0), 2)
    print("qrcode: %s" % codeinfo)
    cv.imshow("result", result)
    cv.waitKey(0)


if "__main__" == __name__:
    main()
    cv.destroyAllWindows()

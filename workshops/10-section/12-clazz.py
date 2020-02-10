#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv
import numpy as np

"""
验证 hog + svm的组合自定义对象检测方法

这种方法的缺点就是开窗检测是从左到右、从上到下，是一个高耗时的操作，
所以步长选择一般会选择HOG窗口默认步长的一半，这样可以减少检测框的数目
"""


def main():
    image = cv.imread("../../../raspberry-auto/pic/elec_watch/test/scene_08.jpg")
    test_img = cv.resize(image, (0, 0), fx=0.2, fy=0.2)
    cv.imshow("input", test_img)
    gray = cv.cvtColor(test_img, cv.COLOR_BGR2GRAY)
    print(test_img.shape)
    h, w = test_img.shape[:2]
    svm = cv.ml.SVM_load('svm_data.dat')
    sum_x = 0
    sum_y = 0
    count = 0
    hog = cv.HOGDescriptor()
    for row in range(64, h - 64, 4):
        for col in range(32, w - 32, 4):
            win_roi = gray[row - 64: row + 64, col - 32: col + 32]
            hog_desc = hog.compute(win_roi, winStride=(8, 8), padding=(0, 0))
            one_fv = np.zeros([len(hog_desc)], dtype=np.float32)
            for i in range(len(hog_desc)):
                one_fv[i] = hog_desc[i][0]
            one_fv = np.reshape(one_fv, [-1, len(hog_desc)])
            result = svm.predict(one_fv)[1]
            # 在predict时候会发现多个重复框，求取它们的平均值即可得到最终的检测框
            if result[0][0] > 0:
                sum_x += (col - 32)
                sum_y += (row - 64)
                count += 1
    x = sum_x // count
    y = sum_y // count
    cv.rectangle(test_img, (x, y), (x + 64, y + 128), (255, 0, 0), 2, cv.LINE_8, 0)
    cv.imshow("result", test_img)
    cv.waitKey(0)


if "__main__" == __name__:
    main()
    cv.destroyAllWindows()

#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv
import numpy as np
import os

"""

"""

test_data = "./test"
classifier = "./svm_number.data"


def get_data_set(image):
    print("generate dataset...")
    contours, hireachy = cv.findContours(image, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    # get all digits
    rois = []
    for c in range(len(contours)):
        box = cv.boundingRect(contours[c])
        if box[3] < 10:
            continue
        rois.append(box)

    # sort(box)
    num = len(rois)
    for i in range(num):
        for j in range(i+1, num, 1):
            x1, y1, w1, h1 = rois[i]
            x2, y2, w2, h2 = rois[j]
            if x2 < x1:
                temp = rois[j]
                rois[j] = rois[i]
                rois[i] = temp
    bgr = cv.cvtColor(image, cv.COLOR_GRAY2BGR)
    index = 0
    digit_data = np.zeros((num, 28*48), dtype=np.float32)
    for x, y, w, h in rois:
        # cv.rectangle(bgr, (x, y), (x+w, y+h), (0, 0, 255), 2, 8)
        # cv.imshow("split digits", bgr[y: h + y, x: w + x])
        # cv.imwrite("0.jpeg", bgr[y: h + y, x: w + x], [cv.IMWRITE_JPEG_QUALITY, 100])
        # cv.waitKey(0)
        cv.putText(bgr, str(index), (x, y+10), cv.FONT_HERSHEY_PLAIN, 1.0, (0, 255, 0), 1)
        digit = image[y:y+h, x:x+w]
        img = cv.resize(digit, (28, 48))
        row = np.reshape(img, (-1, 28 * 48))
        digit_data[index] = row
        index += 1
    cv.imshow("split digits", bgr)
    return digit_data, rois


def main():
    files = os.listdir(test_data)
    svm = cv.ml.SVM_load(classifier)
    for file in files:
        image_path = os.path.join(test_data, file)
        if True is os.path.isfile(image_path):
            image = cv.imread(image_path)
            gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
            # blur = cv.GaussianBlur(gray, (9, 9), 0)
            binary = cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY_INV, 25, 10)
            data, boxes = get_data_set(binary)
            result = svm.predict(data)[1]
            content = []
            for i in range(len(result)):
                content.append(str(np.int32(result[i][0])))
            print("".join(content))
            cv.waitKey(0)


if "__main__" == __name__:
    main()
    cv.destroyAllWindows()

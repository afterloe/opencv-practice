#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv
import os
import imutils

"""

"""


def main():
    dir_path = "G:/Project/new_items"
    items = os.listdir(dir_path)
    for item in items:
        image_path = os.path.join(dir_path, item)
        if True is os.path.isfile(image_path):
            image = cv.imread(image_path, cv.IMREAD_GRAYSCALE)
            image = imutils.resize(image, 23, 43)
            cv.imwrite("G:/Project/{}".format(item), image, [cv.IMWRITE_JPEG_QUALITY, 100])
            cv.imshow("item", image)
            cv.waitKey(0)


if "__main__" == __name__:
    main()
    cv.destroyAllWindows()

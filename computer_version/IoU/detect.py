#!/usr/bin/env python3
# -*- coding=utf-8 -*-

from imutils.object_detection import non_max_suppression
from imutils import paths
import numpy as np
import argparse
import imutils
import cv2 as cv
import os


def run_detector(path_of_image):
    image = cv.imread(path_of_image)
    image = imutils.resize(image, width=min(400, image.shape[1]))
    origin = image.copy()
    rects, weights = hog.detectMultiScale(image, winStride=(4, 4), padding=(8, 8), scale=1.05)
    for x, y, w, h in rects:
        cv.rectangle(origin, (x, y), (x + w, y + h), (0, 0, 255), 2)
    rects = np.array([[x, y, x + w, y + h] for x, y, w, h in rects])
    pick = non_max_suppression(rects, probs=None, overlapThresh=0.65)
    for x_a, y_a, x_b, y_b in pick:
        cv.rectangle(image, (x_a, y_a), (x_b, y_b), (0, 255, 0), 2)
    filename = path_of_image[path_of_image.rfind(os.path.sep) + 1:]
    print("[INFO] {}: {} original boxes, {} after suppression".format(filename, len(rects), len(pick)))
    cv.imshow("before", origin)
    cv.imshow("after", image)
    key = cv.waitKey(0)
    if ord("q") == key:
        return True
    return False


if "__main__" == __name__:
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required=True, help="path to images directory")
    args = vars(ap.parse_args())

    hog = cv.HOGDescriptor()
    hog.setSVMDetector(cv.HOGDescriptor_getDefaultPeopleDetector())
    for image_path in paths.list_images(args["image"]):
        flag = run_detector(image_path)
        if flag:
            break
    cv.destroyAllWindows()

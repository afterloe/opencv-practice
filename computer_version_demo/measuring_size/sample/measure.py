#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv
import imutils
from imutils.contours import sort_contours
from imutils import perspective
from scipy.spatial import distance
import numpy as np
import os


def midpoint(ptA, ptB):
    return (ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5


class Measure(object):

    def __init__(self, path_of_image):
        if False is os.path.isfile(path_of_image):
            assert Exception("图像文件不存在")
        self.__image = cv.imread(path_of_image)
        self.__width = 1
        # cv.namedWindow("origin", cv.WINDOW_FREERATIO)

    def set_width(self, width):
        self.__width = width

    def measure_by_object(self):
        gray = cv.cvtColor(self.__image, cv.COLOR_BGR2GRAY)
        blurred = cv.GaussianBlur(gray, (7, 7), 0)
        edged = cv.Canny(blurred, 50, 100)
        edged = cv.dilate(edged, None, iterations=1)
        edged = cv.erode(edged, None, iterations=1)
        contours = cv.findContours(edged, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(contours)
        contours = sort_contours(contours)[0]
        pixels_per_metric = None
        for contour in contours:
            if 100 > cv.contourArea(contour):
                continue
            orig = self.__image.copy()
            box = cv.minAreaRect(contour)
            box = cv.boxPoints(box)
            box = np.array(box, dtype="int")
            cv.drawContours(orig, [box.astype("int")], -1, (0, 255, 0), 2)
            for (x, y) in box:
                cv.circle(orig, (int(x), int(y)), 5, (0, 0, 255), -1)
            tl, tr, br, bl = box
            tltr_x, tltr_y = midpoint(tl, tr)
            blbr_x, blbr_y = midpoint(bl, br)
            tlbl_x, tlbl_y = midpoint(tl, bl)
            trbr_x, trbr_y = midpoint(tr, br)
            cv.circle(orig, (int(tltr_x), int(tltr_y)), 5, (255, 0, 0), -1)
            cv.circle(orig, (int(blbr_x), int(blbr_y)), 5, (255, 0, 0), -1)
            cv.circle(orig, (int(tlbl_x), int(tlbl_y)), 5, (255, 0, 0), -1)
            cv.circle(orig, (int(trbr_x), int(trbr_y)), 5, (255, 0, 0), -1)
            cv.line(orig, (int(tltr_x), int(tltr_y)), (int(blbr_x), int(blbr_y)), (255, 0, 255), 2)
            cv.line(orig, (int(tlbl_x), int(tlbl_y)), (int(trbr_x), int(trbr_y)), (255, 0, 255), 2)
            dA = distance.euclidean((tltr_x, tltr_y), (blbr_x, blbr_y))
            dB = distance.euclidean((tlbl_x, tlbl_y), (trbr_x, trbr_y))
            if None is pixels_per_metric:
                pixels_per_metric = dB / self.__width
            dimA = dA / pixels_per_metric
            dimB = dB / pixels_per_metric
            cv.putText(orig, "%.1f in" % dimA, (int(tltr_x - 15), int(tltr_y - 10)), cv.FONT_HERSHEY_SIMPLEX,
                       0.65, (255, 255, 255), 2)
            cv.putText(orig, "%.1f in" % dimB, (int(trbr_x + 10), int(trbr_y)), cv.FONT_HERSHEY_SIMPLEX,
                       0.65, (255, 255, 255), 2)
            cv.imshow("origin", orig)
            cv.waitKey(0)
        pass

    def __del__(self):
        cv.destroyAllWindows()

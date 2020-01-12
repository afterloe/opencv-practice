#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv
import numpy as np

"""

"""


def main():
    meter = cv.imread("../../../raspberry-auto/pic/Meter.jpg")
    meter_find = cv.imread("../../../raspberry-auto/pic/Meter_in_word.png")
    if None is meter or None is meter_find:
        print("pic not find")
        return
    meter = cv.medianBlur(meter, 9)
    meter_find = cv.medianBlur(meter_find, 9)
    orb = cv.ORB_create()
    kp1, des1 = orb.detectAndCompute(meter, None)
    kp2, des2 = orb.detectAndCompute(meter_find, None)

    bf = cv.BFMatcher(cv.NORM_HAMMING, crossCheck=True)
    matches = bf.match(des1, des2)

    good_matches = []
    max_dist = 0

    for index in range(len(matches)):
        max_dist = max(max_dist, matches[index].distance)
    for index in range(len(matches)):
        if max_dist * 0.4 > matches[index].distance:
            good_matches.append(matches[index])

    result = cv.drawMatches(meter, kp1, meter_find, kp2, matches[:10], None)
    cv.namedWindow("orb-match", cv.WINDOW_NORMAL)
    cv.imshow("orb-match", result)

    obj_pts = []
    scene_pts = []

    for index in range(len(good_matches)):
        obj_pts.append(kp1[good_matches[index].queryIdx].pt)
        scene_pts.append(kp2[good_matches[index].trainIdx].pt)

    h = cv.findHomography(np.asarray(obj_pts), np.asarray(scene_pts), cv.RHO)

    obj_corners = []
    # shape - width * height
    width, height = meter_find.shape[:2]
    obj_corners.append((0, 0))
    obj_corners.append((width, 0))
    obj_corners.append((width, height))
    obj_corners.append((0, height))
    scene_corners = cv.perspectiveTransform(np.asarray(obj_corners), h)

    cv.line(result, scene_corners[0] + (width, 0), scene_corners[3] + (width, 0), (255, 0, 0), 4)
    cv.line(result, scene_corners[1] + (width, 0), scene_corners[2] + (width, 0), (255, 0, 0), 4)
    cv.line(result, scene_corners[2] + (width, 0), scene_corners[1] + (width, 0), (255, 0, 0), 4)
    cv.line(result, scene_corners[3] + (width, 0), scene_corners[0] + (width, 0), (255, 0, 0), 4)

    cv.namedWindow("orb-match", cv.WINDOW_NORMAL)
    cv.imshow("orb-match", result)

    cv.waitKey(0)
    cv.destroyAllWindows()


if "__main__" == __name__:
    main()

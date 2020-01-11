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
    matches = sorted(matches, key=lambda x: x.distance)
    result = cv.drawMatches(meter, kp1, meter_find, kp2, matches[:10], None)
    cv.namedWindow("orb-match", cv.WINDOW_NORMAL)
    cv.imshow("orb-match", result)

    obj_pts = []
    scene_pts = []
    for i in range(len(good_matches)):
        obj_pts.append(kp1[good_matches[i].queryIdx].pt)
        scene_pts.append(kp2[good_matches[i].trainIdx].pt)
    M, mask = cv.findHomography(obj_pts, scene_pts, cv.RHO)

    # shape - width * height
    width, height = meter_find.shape[:2]
    obj_corners = np.float32([[0, 0], [w, 0], [w, h], [0, h]]).reshape(-1, 1, 2)
    scene_corners = cv.perspectiveTransform(obj_corners, M)
    meter_find = cv.polylines(meter_find, [np.int32(scene_corners)], True, (0, 0, 255), 3, cv.LINE_AA)


    cv.namedWindow("orb-match", cv.WINDOW_NORMAL)
    cv.imshow("orb-match", result)

    cv.waitKey(0)
    cv.destroyAllWindows()


if "__main__" == __name__:
    main()

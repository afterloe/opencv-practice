#!/usr/bin/env python3
# -*- coding=utf-8 -*-


import cv2 as cv
import numpy as np
from .current_util import calculate_distance
# import imutils

hsv_min, hsv_max = (0, 0, 0), (180, 255, 50)


def draw_box(image, padding=300, color=(0, 0, 255)):
    if None is image:
        raise Exception("can't draw line in block image")
    h, w = image.shape[: 2]
    x, y, width, height = w // 2 - padding // 2, h // 2 - padding // 2, padding, padding
    cv.rectangle(image, (x, y), (x + width, y + height), color, 2, cv.LINE_AA)
    return image, (x, y, (x + width), (y + height))


def avg_circles(circles, shape):
    avg_x, avg_y, avg_r = 0, 0, 0
    for i in range(shape):
        avg_x = avg_x + circles[0][i][0]
        avg_y = avg_y + circles[0][i][1]
        avg_r = avg_r + circles[0][i][2]
    return int(avg_x / shape), int(avg_y / shape), int(avg_r / shape)


def meter_detection(image):
    height, width = image.shape[: 2]
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    gray = cv.bilateralFilter(gray, 11, 17, 17)
    blurred = cv.GaussianBlur(gray, (3, 3), 0)
    circles = cv.HoughCircles(blurred, cv.HOUGH_GRADIENT, 1, 20, np.array([]), 100, 50,
                              int(height * 0.35), int(height * 0.48))
    if 3 != len(circles.shape):
        return False, None
    return True, circles


def pointer_detection(image):
    hsv = cv.cvtColor(image.copy(), cv.COLOR_BGR2HSV)
    mask = cv.inRange(hsv, hsv_min, hsv_max)
    edged = cv.GaussianBlur(mask, (0, 0), 3)
    lines = cv.HoughLinesP(edged, 1, np.pi / 180, 130, None, 45, 10)
    if None is lines:
        return False, None
    return True, lines[0][0]


def draw_gauge(image, separation=10):
    flag, circles = meter_detection(image)
    if False is flag:
        return False, image
    a, b, c = circles.shape
    x, y, r = avg_circles(circles, b)
    cv.circle(image, (x, y), r, (0, 0, 255), 3, cv.LINE_AA)
    cv.circle(image, (x, y), 2, (0, 255, 255), 3, cv.LINE_AA)  # 圆心
    interval = int(360 / separation)
    p1, p2, p_text = np.zeros((interval, 2)), np.zeros((interval, 2)), np.zeros((interval, 2))
    for i in range(0, interval):
        for j in range(0, 2):
            if 0 == j % 2:
                p1[i][j] = x + 0.9 * r * np.cos(separation * i * np.pi / 180)
            else:
                p1[i][j] = y + 0.9 * r * np.sin(separation * i * np.pi / 180)
    text_offset_x, text_offset_y = 10, 5
    for i in range(0, interval):
        for j in range(0, 2):
            if 0 == j % 2:
                p2[i][j] = x + r * np.cos(separation * i * np.pi / 180)
                p_text[i][j] = x - text_offset_x + 1.2 * r * np.cos(separation * (i + 9) * np.pi / 180)
            else:
                p2[i][j] = y + r * np.sin(separation * i * np.pi / 180)
                p_text[i][j] = y + text_offset_y + 1.2 * r * np.sin(separation * (i + 9) * np.pi / 180)
    for i in range(0, interval):
        cv.line(image, (int(p1[i][0]), int(p1[i][1])), (int(p2[i][0]), int(p2[i][1])), (0, 255, 0), 2)
        cv.putText(image, "%s" % (int(i * separation)), (int(p_text[i][0]), int(p_text[i][1])),
                   cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1, cv.LINE_AA)
    return True, image


def infer(x, y, pointer, min_angle, max_angle, min_value, max_value):
    start_x, start_y, end_x, end_y = pointer
    dist_pt_0, dist_pt_1 = calculate_distance(x, y, start_x, start_y), calculate_distance(x, y, end_x, end_y)
    if dist_pt_0 > dist_pt_1:
        x_angle, y_angle = start_x - x, y - start_y
    else:
        x_angle, y_angle = end_x - x, y - end_y
    res = np.arctan(np.divide(float(y_angle), float(x_angle)))
    res = np.rad2deg(res)
    final_angle = 0
    if x_angle > 0 and y_angle > 0:
        final_angle = 270 - res
    if x_angle < 0 and y_angle > 0:
        final_angle = 90 - res
    if x_angle < 0 and y_angle < 0:
        final_angle = 90 - res
    if x_angle > 0 and y_angle < 0:
        final_angle = 270 - res
    old_min, old_max = float(min_angle), float(max_angle)
    new_min, new_max = float(min_value), float(max_value)
    old_value = final_angle
    old_range = old_max - old_min
    new_range = new_max - new_min
    new_value = (((old_value - old_min) * new_range) / old_range) + new_min
    return new_value


def infer_diff(previous, now):
    if None is now:
        return False, None
    hsv = cv.cvtColor(now.copy(), cv.COLOR_BGR2HSV)
    mask = cv.inRange(hsv, hsv_min, hsv_max)
    edged = cv.GaussianBlur(mask, (0, 0), 3)
    hist = cv.calcHist([hsv], [0], edged, [180], [0, 180])
    cv.normalize(hist, hist, 0, 255, cv.NORM_MINMAX)
    h, w = now.shape[: 2]

    if None is previous:
        # previous = np.copy(blurred)
        # TODO
        return True, previous
    dst = cv.calcBackProject([hsv], [0], hist, [0, 180], 1)
    box = cv.CamShift(dst, (0, 0, h, w), (cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 1))
    print(len(box))
    # track_window = track_box[1]

    if 1 < len(contours):
        previous = np.copy(blurred)
        return True, previous
    else:
        return False, None

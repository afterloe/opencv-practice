#!/usr/bin/env python3
# -*- coding=utf-8 -*-


import cv2 as cv
import numpy as np
from .current_util import calculate_distance, mean_shift_filtering, calculate_point_2_line
import imutils

hsv_min, hsv_max = (0, 0, 0), (180, 255, 50)
kernel = cv.getStructuringElement(cv.MORPH_RECT, (3, 3))


def draw_box(image, padding=300, color=(0, 0, 255)):
    if None is image:
        raise Exception("无法读取图像")
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
    blurred = cv.GaussianBlur(gray, (0, 0), 3)
    circles = cv.HoughCircles(blurred, cv.HOUGH_GRADIENT, 1, 20, np.array([]), 100, 50,
                              int(height * 0.35), int(height * 0.48))
    if 3 != len(circles.shape):
        return False, None
    return True, circles


def pointer_detection(image, circles):
    x, y, r = circles
    hsv = cv.cvtColor(image.copy(), cv.COLOR_BGR2HSV)
    mask = cv.inRange(hsv, hsv_min, hsv_max)
    blurred = cv.GaussianBlur(mask, (3, 3), 0)
    contours = cv.findContours(blurred, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    min_dis = r
    c = None
    for cnt in contours:
        a, b, w, h = cv.boundingRect(cnt)
        area = cv.contourArea(cnt)
        if 300 > area:
            continue
        rect = cv.minAreaRect(cnt)
        cx, cy = rect[0]
        dis = calculate_distance(x, y, cx, cy)
        if r > dis:
            r = dis
            c = (a, b, w, h)
    a, b, w, h = c
    cv.rectangle(image, (a, b), (a + w, b + h), (255, 0, 0), 1, cv.LINE_AA)
    cv.imshow("mask", blurred)
    lines = cv.HoughLinesP(blurred, 1, np.pi / 180, 100, None, 80, 10)
    if None is lines:
        return False, None
    min_dis, pointer = r, None
    for i in range(len(lines)):
        line = lines[i][0]
        # cv.line(image, (line[0], line[1]), (line[2], line[3]), (255, 0, 0), 1, cv.LINE_AA)
        dis_r = calculate_point_2_line((x, y), line)
        if min_dis > dis_r:
            min_dis = dis_r
            pointer = line
    if None is pointer:
        return False, pointer
    cv.imshow("pointer", image)
    dis = calculate_distance(pointer[0], pointer[1], pointer[2], pointer[3])
    if dis > r / 2:
        pointer = (x, y, pointer[2], pointer[3])
    return True, pointer


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
    return float(new_value)


def infer_diff(previous, now):
    """
        判断两张图像 是否存在差异

    :param previous:
    :param now:
    :return:
    """
    hsv = cv.cvtColor(now, cv.COLOR_BGR2HSV)
    mask = cv.inRange(hsv, hsv_min, hsv_max)
    edged = cv.GaussianBlur(mask, (0, 0), 3)
    if None is now or None is previous:
        return True, edged
    diff = cv.subtract(edged, previous)
    diff = cv.morphologyEx(diff, cv.MORPH_OPEN, kernel)
    contours = cv.findContours(diff, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    flag = False
    for cnt in contours:
        x, y, w, h = cv.boundingRect(cnt)
        if 100 > h and 100 > w:
            continue
        # cv.rectangle(now, (x, y), (x + w, y + h), (0, 0, 255), 2, cv.LINE_AA)
        flag = True
    # cv.imshow("sport", now)
    previous = np.copy(edged)
    return flag, previous

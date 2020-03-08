#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv
import numpy as np
import time

"""

"""

def calculate_distance(x1, y1, x2, y2):
    return np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def avg_circles(circles, b):
    avg_x, avg_y, avg_r = 0, 0, 0
    for i in range(b):
        avg_x = avg_x + circles[0][i][0]
        avg_y = avg_y + circles[0][i][1]
        avg_r = avg_r + circles[0][i][2]
    return int(avg_x / b), int(avg_y / b), int(avg_r / b)


def calibrate_gauge(img):
    """
    This function should be run using a test image in order to calibrate the range available to the dial as well as the
units.  It works by first finding the center point and radius of the gauge.  Then it draws lines at hard coded intervals
(separation) in degrees.  It then prompts the user to enter position in degrees of the lowest possible value of the gauge,
as well as the starting value (which is probably zero in most cases but it won't assume that).  It will then ask for the
position in degrees of the largest possible value of the gauge. Finally, it will ask for the units.  This assumes that
the gauge is linear (as most probably are).
It will return the min value with angle in degrees (as a tuple), the max value with angle in degrees (as a tuple),
and the units (as a string).
    """
    image = img.copy()
    height, width = image.shape[: 2]
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    circles = cv.HoughCircles(gray, cv.HOUGH_GRADIENT, 1, 20, np.array([]), 100, 50, int(height * 0.35),
                              int(height * 0.48))
    a, b, c = circles.shape
    x, y, r = avg_circles(circles, b)
    cv.circle(image, (x, y), r, (0, 0, 255), 3, cv.LINE_AA)
    cv.circle(image, (x, y), 2, (0, 255, 255), 3, cv.LINE_AA)
    """"
    goes through the motion of a circle and sets x and y values based on the set separation spacing.  
Also adds text to each line.  These lines and text labels serve as the reference point for the user to enter
NOTE: by default this approach sets 0/360 to be the +x axis (if the image has a cartesian grid in the middle), 
the addition (i+9) in the text offset rotates the labels by 90 degrees so 0/360 is at the bottom (-y in cartesian).  
So this assumes the gauge is aligned in the image, but it can be adjusted by changing the value of 9 to something else.
    """
    separation = 10.0  # in degrees
    interval = int(360 / separation)
    p1, p2, p_text = np.zeros((interval, 2)), np.zeros((interval, 2)), np.zeros((interval, 2))
    for i in range(0, interval):
        for j in range(0, 2):
            if 0 == j % 2:
                p1[i][j] = x + 0.9 * r * np.cos(separation * i * np.pi / 180)
            else:
                p1[i][j] = y + 0.9 * r * np.sin(separation * i * np.pi / 180)
    text_offset_x = 10
    text_offset_y = 5
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
        cv.putText(image, "%s" % (int(i*separation)), (int(p_text[i][0]), int(p_text[i][1])), cv.FONT_HERSHEY_SIMPLEX,
                   0.3, (0, 0, 0), 1, cv.LINE_AA)
    cv.imshow("image", image)
    # cv.waitKey(0)

    min_angle = 68  # input('Min angle (lowest possible angle of dial) - in degrees: ')  # the lowest possible angle
    max_angle = 320  # input('Max angle (highest possible angle) - in degrees: ')  # highest possible angle
    min_value = 0  # input('Min value: ')  # usually zero
    max_value = 0.25  # input('Max value: ')  # maximum reading of the gauge
    units = "MPa"  # input('Enter units: ')
    return min_angle, max_angle, min_value, max_value, units, x, y, r


def get_current_value(img, min_angle, max_angle, min_value, max_value, x, y, r, gauge_number, file_type):
    # gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    # thresh = 175
    # max_value = 255
    # threshed = cv.adaptiveThreshold(gray, max_value, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY_INV, 25, 10)
    # cv.imshow("threshed", threshed)
    hsv = cv.cvtColor(img.copy(), cv.COLOR_BGR2HSV)
    hsv_min = (0, 0, 0)
    hsv_max = (180, 255, 50)
    mask = cv.inRange(hsv, hsv_min, hsv_max)
    # cv.imshow("mask", mask)

    lines = cv.HoughLinesP(mask, 1, np.pi / 180, 100, None, 30, 10)
    if None is lines:
        print("未检测到直线")
        return
    line = lines[0][0]  # 检测到的直线信息
    # 获取指针位置
    x1, y1, x2, y2 = line
    cv.line(img, (line[0], line[1]), (line[2], line[3]), (0, 255, 255), 1, cv.LINE_AA)
    dist_pt_0 = calculate_distance(x, y, x1, y1)
    dist_pt_1 = calculate_distance(x, y, x2, y2)
    if dist_pt_0 > dist_pt_1:
        x_angle = x1 - x
        y_angle = y - y1
    else:
        x_angle = x2 - x
        y_angle = y - y2
    res = np.arctan(np.divide(float(y_angle), float(x_angle)))
    res = np.rad2deg(res)
    if x_angle > 0 and y_angle > 0:  # in quadrant I
        final_angle = 270 - res
    if x_angle < 0 and y_angle > 0:  # in quadrant II
        final_angle = 90 - res
    if x_angle < 0 and y_angle < 0:  # in quadrant III
        final_angle = 90 - res
    if x_angle > 0 and y_angle < 0:  # in quadrant IV
        final_angle = 270 - res
    old_min, old_max, new_min, new_max = float(min_angle), float(max_angle), float(min_value), float(max_value)
    old_value = final_angle
    old_range = old_max - old_min
    new_range = new_max - new_min
    # print(old_value, old_min, new_range, old_range, new_min)
    new_value = (((old_value - old_min) * new_range) / old_range) + new_min
    return new_value


def log(message, log_type="INFO"):
    content = "[{}][{}]: {}".format(log_type, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())), message)
    print(content)
    return content


def main():
    # img = cv.imread("G:\\Project\\opencv-ascs-resources\\meter_pointer_roi\\2020-03-08_15-06-58.jpeg")
    img = cv.imread("G:\\Project\\opencv-ascs-resources\\meter_pointer_roi\\2020-03-05_22-18-30.jpeg")
    # name the calibration image of your gauge 'gauge-#.jpg', for example 'gauge-5.jpg'.
    # It's written this way so you can easily try multiple images
    min_angle, max_angle, min_value, max_value, units, x, y, r = calibrate_gauge(img)

    # feed an image (or frame) to get the current value, based on the calibration,
    # by default uses same image as calibration
    value = get_current_value(img, min_angle, max_angle, min_value, max_value, x, y, r, 1, "jpeg")
    cv.putText(img, "Current reading: %s %s" % (value, units), (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255))
    cv.imshow("img", img)
    log("Current reading: %s %s" % (value, units))
    cv.waitKey(0)


if "__main__" == __name__:
    main()
    cv.destroyAllWindows()

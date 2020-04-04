#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv
import imutils
from imutils.object_detection import non_max_suppression
from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import time

"""

"""

PATH_OF_NET_BIN = "../../../raspberry-auto/models/yolo/yolov3-tiny.weights"
PATH_OF_NET_CONFIG = "../../../raspberry-auto/models/yolo/yolov3-tiny.cfg"


def log(message, log_type="INFO"):
    content = "[{}][{}]: {}".format(log_type, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())), message)
    print(content)
    return content


def calculate_distance(x1, y1, x2, y2):
    return np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def avg_circles(circles, b):
    avg_x, avg_y, avg_r = 0, 0, 0
    for i in range(b):
        avg_x = avg_x + circles[0][i][0]
        avg_y = avg_y + circles[0][i][1]
        avg_r = avg_r + circles[0][i][2]
    return int(avg_x / b), int(avg_y / b), int(avg_r / b)


def detector_meter(image, net, out_names=None):
    # image = imutils.resize(image, width=416)
    h, w = image.shape[:2]
    data = cv.dnn.blobFromImage(image, 1.0 / 255.0, (416, 416), None, False, False)
    net.setInput(data)
    outs = net.forward(out_names)
    confidences = []
    boxes = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            if class_id != 74:
                continue
            confidence = scores[class_id]
            if 0.5 < confidence:
                center_x = int(detection[0] * w)
                center_y = int(detection[1] * h)
                width = int(detection[2] * w)
                height = int(detection[3] * h)
                left = int(center_x - width / 2)
                top = int(center_y - height / 2)
                confidences.append(float(confidence))
                boxes.append((left, top, width, height))
    targets = non_max_suppression(np.array(boxes), probs=confidences)
    confidences.clear()
    for left, top, width, height in targets:
        confidences.append(image[top: top + height, left: left + width, :])
        # cv.rectangle(image, (left, top), (left + width, top + height), (0, 0, 255), 2, cv.LINE_AA)
        # cv.putText(image, "target", (left, top), cv.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 0), 2)
    return confidences


def calibrate_gauge(img):
    image = img.copy()
    height, width = image.shape[: 2]
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    circles = cv.HoughCircles(gray, cv.HOUGH_GRADIENT, 1, 20, np.array([]), 100, 50, int(height * 0.35),
                              int(height * 0.48))
    a, b, c = circles.shape
    x, y, r = avg_circles(circles, b)
    cv.circle(image, (x, y), r, (0, 0, 255), 3, cv.LINE_AA)
    cv.circle(image, (x, y), 2, (0, 255, 255), 3, cv.LINE_AA)
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
    cv.imshow("debug", image)
    # cv.waitKey(0)

    min_angle = 50  # input('Min angle (lowest possible angle of dial) - in degrees: ')  # the lowest possible angle
    max_angle = 300  # input('Max angle (highest possible angle) - in degrees: ')  # highest possible angle
    min_value = 0  # input('Min value: ')  # usually zero
    max_value = 0.25  # input('Max value: ')  # maximum reading of the gauge
    units = "MPa"  # input('Enter units: ')
    return min_angle, max_angle, min_value, max_value, units, x, y, r


def get_current_value(img, min_angle, max_angle, min_value, max_value, x, y, r):
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
    cv.imshow("line", img)
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


def produce_roi(roi):
    height, width = roi.shape[: 2]
    value = 0
    log(height, width)
    if width <= 0 and height <= 0:
        return
    img = imutils.resize(roi, width=500)
    try:
        min_angle, max_angle, min_value, max_value, units, x, y, r = calibrate_gauge(img)
        value = get_current_value(img, min_angle, max_angle, min_value, max_value, x, y, r)
        log("Current reading: %s %s" % (value, units))
        return value
    except Exception as e:
        log(e, "ERROR")
        return value


def main():
    vs = None
    # try:
    log("load net from disk in {}".format(PATH_OF_NET_BIN))
    dnn = cv.dnn.readNetFromDarknet(PATH_OF_NET_CONFIG, PATH_OF_NET_BIN)
    layout_name = dnn.getUnconnectedOutLayersNames()
    log("starting video steam ... ...")
    vs = VideoStream(src=0).start()
    time.sleep(1.0)
    # fps = FPS().start()
    while True:
        frame = vs.read()
        if None is frame:
            log("can't read any video frame from device-0", "ERROR")
            raise Exception()
        meters = detector_meter(frame, dnn, layout_name)
        for meter in meters:
            value = produce_roi(meter)
            if 0 != value:
                cv.putText(frame, "Current reading: %s %s" % (str(value), "MPa"), (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255))
        cv.imshow("frame", frame)
        key = cv.waitKey(50) & 0xff
        if ord("q") == key:
            log("enter q to quit ...")
            break
        # fps.stop()
        # log("elapsed time: {:.2f}".format(fps.elapsed()))
        # log("approx. FPS: {:.2f}".format(fps.fps()))
    # except Exception as e:
    #     print(e)
    # finally:
    log("stop qt for python ... ...")
    cv.destroyAllWindows()
    if None is not vs:
        log("stop video steam ... ...")
        vs.stop()


if "__main__" == __name__:
    main()

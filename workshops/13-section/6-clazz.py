#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv
import numpy as np
import math

"""

"""

text_features = []
labels = []


def main():
    src = cv.imread("../../../raspberry-auto/pic/td2.png")
    cv.imshow("input", src)
    train()
    forward()
    cv.waitKey(0)


# 训练
def train():
    image = cv.imread("../../../raspberry-auto/pic/td1.png")
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    _, binary = cv.threshold(gray, 0, 255, cv.THRESH_OTSU | cv.THRESH_BINARY_INV)
    contours, hierarchy = cv.findContours(binary, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    result = cv.cvtColor(binary, cv.COLOR_GRAY2BGR)
    points = []
    for contour in contours:
        # x, y, w, h
        rect = cv.boundingRect(contour)
        points.append(rect)
        cv.rectangle(result, rect, (255, 255, 255), 1)
    length = len(points)
    for i in range(length - 1):
        for j in range(i + 1, length):
            if points[i][0] > points[j][0]:
                t = points[j]
                points[j] = points[i]
                points[i] = t
    print(points)
    for t in range(len(points)):
        point = points[t]
        characteristic = extract_feature_characteristic(binary[point[1]: point[1] + point[3],
                                                        point[0]: point[0] + point[2]])
        # for i in range(len(characteristic)):
        #     print("Num. %d, vf = vf[%d] = %.4f" % (t, i, characteristic[i]))
        text_features.append(characteristic)
        if len(points) - 1 == t:
            labels.append(0)
        else:
            labels.append(t + 1)
    #     cv.imshow("item", result[point[1]: point[1] + point[3], point[0]: point[0] + point[2], :])
    #     cv.waitKey(0)
    # cv.imshow("result", result)


def extract_feature_characteristic(binary):
    h, w = binary.shape[:2]
    bins = 10.0
    x_step = np.int32(math.ceil(w / 4.0))
    y_step = np.int32(math.ceil(h / 5.0))
    index = 0
    data = [0 for x in range(40)]
    for y in range(0, h, y_step):
        for x in range(0, w, x_step):
            data[index] = get_weight_black_number(binary, w, h, x, y, x_step, y_step)
            index += 1
    x_step = np.int32(math.ceil(w / bins))
    for x in range(0, w, x_step):
        if 1 < (x + x_step) - w:
            continue
        data[index] = get_weight_black_number(binary, w, h, x, 0, x_step, h)
        index += 1
    y_step = np.int32(math.ceil(h / bins))
    for y in range(0, h, y_step):
        if 1 < (y + y_step) - h:
            continue
        data[index] = get_weight_black_number(binary, w, h, 0, y, w, y_step)
        index += 1
    sum_data = 0
    for i in range(0, 20):
        sum_data += data[i]
    for i in range(0, 20):
        data[i] = data[i] / sum_data
    sum_data = 0
    for i in range(20, 30):
        sum_data += data[i]
    for i in range(20, 30):
        data[i] = data[i] / sum_data
    sum_data = 0
    for i in range(30, 40):
        sum_data += data[i]
    for i in range(30, 40):
        if 0 == sum_data:
            continue
        data[i] = data[i] / sum_data

    return data


def get_weight_black_number(binary, width, height, x, y, x_step, y_step):
    weight_num = 0
    nx = np.int32(math.floor(x))
    ny = np.int32(math.floor(y))
    fx = x - nx
    fy = y - ny
    w = x + x_step
    h = y + y_step
    if w > width:
        w = width - 1
    if h > height:
        h = height - 1
    nw = np.int32(math.floor(w))
    nh = np.int32(math.floor(h))
    fw = w - nw
    fh = h - nh
    c = 0
    ww = np.int32(width)
    weight = 0
    row = 0
    col = 0
    for row in range(ny, nh):
        for col in range(nx, nw):
            c = binary[row, col]
            if 0 == c:
                weight += 1
    w1 = 0
    w2 = 0
    w3 = 0
    w4 = 0
    if 0 < fx:
        col = nx + 1
        if col > width - 1:
            col = col - 1
        count = 0
        for row in range(ny, nh):
            c = binary[row, col]
            if 0 == c:
                count += 1
        w1 = count * fx

    if 0 < fy:
        row = ny + 1
        if row > height - 1:
            row = row - 1
        count = 0
        for col in range(nx, nw):
            c = binary[row, col]
            if 0 == c:
                count += 1
        w2 = count * fy

    if 0 < fw:
        col = nw + 1
        if col > width - 1:
            col = col - 1
        count = 0
        for row in range(ny, nh):
            c = binary[row, col]
            if 0 == c:
                count += 1
        w3 = count * fw

    if 0 < fh:
        row = nh + 1
        if row > height - 1:
            row = row - 1
        count = 0
        for col in range(nx, nw):
            c = binary[row, col]
            if 0 == c:
                count += 1
        w4 = count * fh

    weight_num = (weight - w1 - w2 + w3 + w4)
    if 0 > weight_num:
        weight_num = 0
    return weight_num


def forward():
    image = cv.imread("../../../raspberry-auto/pic/td2.png")
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    _, binary = cv.threshold(gray, 0, 255, cv.THRESH_BINARY_INV | cv.THRESH_OTSU)
    contours, hierarchy = cv.findContours(binary, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    for t in range(0, len(contours)):
        rect = cv.boundingRect(contours[t])
        characteristic = extract_feature_characteristic(binary[rect[1]: rect[1] + rect[3],
                                                        rect[0]: rect[0] + rect[2]])
        label_index = predict_digit(characteristic)
        print("current digit is: %d" % labels[label_index])
        if label_index >= 0:
            cv.putText(image, "%d" % labels[label_index], (rect[0], rect[1]), cv.FONT_HERSHEY_SIMPLEX, 1.0,
                       (0, 0, 255), 1)
        else:
            cv.putText(image, "U", (rect[0], rect[1]), cv.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 1)
    cv.imshow("dist", image)


def predict_digit(characteristic):
    min_dist = 100000000
    label_index = -1
    for i in range(0, len(text_features)):
        dist = 0
        temp = text_features[i]
        for k in range(0, len(characteristic)):
            d = temp[k] - characteristic[k]
            dist += (d * d)
        if min_dist > dist:
            min_dist = dist
            label_index = i
    return label_index


if "__main__" == __name__:
    main()
    cv.destroyAllWindows()

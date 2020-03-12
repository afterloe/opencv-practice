#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import numpy as np
import math


TEMP_VALUE_LIST = []
CONFIDENCE = 20


def average(numbers):
    length = len(numbers)
    sum_value = 0
    for number in numbers:
        sum_value += number
    return sum_value / length


def mean_shift_filtering(value):
    TEMP_VALUE_LIST.append(value)
    length = len(TEMP_VALUE_LIST)
    if 20 < len(TEMP_VALUE_LIST):
        del TEMP_VALUE_LIST[0]
    if 1 == length:
        return False
    mean = average(TEMP_VALUE_LIST)
    reliability = np.sqrt((value - mean) ** 2)
    # print(mean, reliability, (reliability / mean) * 100)
    if CONFIDENCE > (reliability / mean) * 100:
        return True
    return False


def avg_circles(circles, b):
    avg_x, avg_y, avg_r = 0, 0, 0
    for i in range(b):
        avg_x = avg_x + circles[0][i][0]
        avg_y = avg_y + circles[0][i][1]
        avg_r = avg_r + circles[0][i][2]
    return int(avg_x / b), int(avg_y / b), int(avg_r / b)


def calculate_distance(x1, y1, x2, y2):
    return np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def calculate_point_2_line(point, line):
    x, y = point
    start_x, start_y, end_x, end_y = line
    a = end_y - start_y
    b = start_x - end_x
    c = end_x * start_y - start_x * end_y
    dis = (math.fabs(a * x + b * y + c)) / (math.pow(a * a + b * b, 0.5))
    return float(dis)


def is_number(input_str):
    try:
        float(input_str)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(input_str)
        return True
    except (TypeError, ValueError):
        pass

    return False

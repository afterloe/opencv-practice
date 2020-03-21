#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv


WIDTH, HEIGHT = 32, 32


def image_to_feature_vector(image, size=(WIDTH, HEIGHT)):
    return cv.resize(image, size).flatten()


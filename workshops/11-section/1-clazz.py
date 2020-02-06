#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

"""

"""


def main():
    x = np.random.randint(25, 50, (25, 2))
    y = np.random.randint(60, 85, (25, 2))
    pts = np.vstack((x, y))

    data = np.float32(pts)
    print(data.shape)

    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    ret, label, center = cv.kmeans(data, 2, None, criteria, 2, cv.KMEANS_RANDOM_CENTERS)
    print(len(label))
    print(center)

    a = data[label.ravel() == 0]
    b = data[label.ravel() == 1]

    plt.scatter(a[:, 0], a[:, 1])
    plt.scatter(b[:, 0], b[:, 1], c='r')
    plt.scatter(center[:, 0], center[:, 1], s=80, c='y', marker='s')
    plt.xlabel('Height')
    plt.ylabel('Weight')
    plt.show()


if "__main__" == __name__:
    main()
    cv.destroyAllWindows()

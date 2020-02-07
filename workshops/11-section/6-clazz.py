#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv
import numpy as np

"""

"""


def main():
    image = cv.imread("../../../raspberry-auto/pic/digits.png")
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    cells = [np.hsplit(row, 100) for row in np.vsplit(gray, 50)]
    x = np.array(cells)
    train = x[:, : 50].reshape(-1, 400).astype(np.float32)
    test = x[:, 50: 100].reshape(-1, 400).astype(np.float32)
    k = np.array(10)
    train_labels = np.repeat(k, 250)[:, np.newaxis]
    test_labels = train_labels.copy()
    dt = cv.ml.RTrees_create()
    dt.train(train, cv.ml.ROW_SAMPLE, train_labels)
    _, results = dt.predict(test)
    matches = results == test_labels
    correct = np.count_nonzero(matches)
    accuracy = correct * 100.0 / results.size
    print(accuracy)


if "__main__" == __name__:
    main()
    cv.destroyAllWindows()

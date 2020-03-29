#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import numpy as np
import cv2 as cv
import logging

__version__ = "1.0.0"

logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)8s][%(filename)s][%(levelname)s] - %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')
CONSOLE = logging.getLogger("dev")
CONSOLE.setLevel(logging.DEBUG)
CONSOLE.info("线性分类器 %s", __version__)

LABELS = ["dog", "cat", "panda"]
np.random.seed(1)

W = np.random.randn(3, 3072)  # 32 * 32 * 3
b = np.random.randn(3)

orig = cv.imread("G:\\afterloe resources\\animal\\dog\\dog.120.jpg")
image = cv.resize(orig.copy(), (32, 32)).flatten()

scores = W.dot(image) + b
for (label, score) in zip(LABELS, scores):
    CONSOLE.info("{}: {:.2f}".format(label, score))

cv.putText(orig, "Label is %s" % LABELS[np.argmax(scores)], (10, 30), cv.FONT_HERSHEY_SIMPLEX, 0.9,
           (0, 255, 0), 2)
cv.imshow("image", orig)
cv.waitKey(0)
cv.destroyAllWindows()

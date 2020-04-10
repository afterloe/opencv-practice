#!/usr/bin/env python3
# -*- coding=utf-8 -*-

from __future__ import print_function
from license_plate import LicensePlateDetector
from imutils import paths
import numpy as np
import argparse
import imutils
import cv2 as cv
import logging

__version__ = "1.0.0"

logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)8s][%(filename)s][%(levelname)s] - %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')
CONSOLE = logging.getLogger("dev")
CONSOLE.setLevel(logging.DEBUG)
CONSOLE.info("车牌识别 %s", __version__)


if "__main__" == __name__:
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--images", required=True, help="检测的图像的文件夹路径")
    args = vars(ap.parse_args())
    for image_path in list(paths.list_images(args["images"])):
        image = cv.imread(image_path)
        CONSOLE.info(image_path)
        if 600 < image.shape[1]:
            image = imutils.resize(image, width=600)
        lpd = LicensePlateDetector(image)
        plates = lpd.detect()
        for (i, (lp, lp_box)) in enumerate(plates):
            lp_box = np.array(lp_box).reshape((-1, 1, 2)).astype(np.int32)
            cv.drawContours(image, [lp_box], -1, (0, 255, 0), 2)
            candidates = np.dstack([lp.candidates] * 3)
            thresh = np.dstack([lp.thresh] * 3)
            output = np.vstack([lp.plate, thresh, candidates])
            cv.imshow("Plate & Candidates #%d" % int(i + 1), output)
        cv.imshow("Image", image)
        cv.waitKey(0)
        cv.destroyAllWindows()

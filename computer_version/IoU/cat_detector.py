#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import argparse
import cv2 as cv


def main(image, cascade):
    image = cv.imread(image)
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    detector = cv.CascadeClassifier(cascade)
    rects = detector.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=10, minSize=(75, 75))
    for (i, (x, y, w, h)) in enumerate(rects):
        cv.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv.putText(image, "Cat # %d" % (i + 1), (x, y - 10), cv.FONT_HERSHEY_SIMPLEX, 0.55, (0, 0, 255), 2)
    cv.imshow("Cat Faces", image)
    cv.waitKey(0)


if "__main__" == __name__:
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required=True, help="path to the input image")
    ap.add_argument("-c", "--cascade", default="haarcascade_frontalcatface.xml",
                    help="path to cat detector haar cascade")
    args = vars(ap.parse_args())
    main(**args)

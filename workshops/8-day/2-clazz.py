#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv

"""
    
"""


def sort_boxes(rois):
    for i in range(0, len(rois) - 1, 1):
        for j in range(i, len(rois), 1):
            x, y, w, h = rois[j]
            if rois[i][1] > y:
                bx, by, bw, bh = rois[i]
                rois[i] = [x, y, w, h]
                rois[j] = [bx, by, bw, bh]
    return rois


def get_template(binary, boxes):
    x, y, w, h = boxes[0]
    roi = binary[y:y + h, x:x + w]
    return roi


def detect_defect(binary, boxes, tpl):
    height, width = tpl.shape[:2]
    index = 1
    defect_rois = []
    for x, y, w, h in boxes:
        roi = binary[y:y + h, x: x + w]
        roi = cv.resize(roi, (width, height))
        mask = cv.subtract(tpl, roi)
        kernel = cv.getStructuringElement(cv.MORPH_RECT, (5, 5), (-1, -1))
        mask = cv.morphologyEx(mask, cv.MORPH_OPEN, kernel)
        _, mask = cv.threshold(mask, 0, 255, cv.THRESH_BINARY)
        count = 0
        for row in range(height):
            for col in range(width):
                pv = mask[row, col]
                if 255 == pv:
                    count += 1
        if 0 < count:
            defect_rois.append([x, y, w, h])
        index += 1
    return defect_rois


def main():
    src = cv.imread("../../pic/blade.jpeg")
    cv.namedWindow("input", cv.WINDOW_AUTOSIZE)
    cv.imshow("input", src)
    gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
    _, binary = cv.threshold(gray, 0, 255, cv.THRESH_BINARY_INV | cv.THRESH_OTSU)
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (3, 3), (-1, -1))
    binary = cv.morphologyEx(binary, cv.MORPH_OPEN, kernel)
    cv.imshow("binary", binary)

    contours, _ = cv.findContours(binary, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
    height, width = src.shape[:2]
    rects = []
    for index in range(len(contours)):
        contour = contours[index]
        x, y, w, h = cv.boundingRect(contour)
        area = cv.contourArea(contour)
        if height // 2 < h or 150 > area:
            continue
        rects.append([x, y, w, h])
    rects = sort_boxes(rects)
    template = get_template(binary, rects)
    for index in range(len(contours)):
        contour = contours[index]
        x, y, w, h = cv.boundingRect(contour)
        area = cv.contourArea(contour)
        if height // 2 < h or 150 > area:
            continue
        cv.drawContours(binary, contours, index, (0, 0, 0), 2, cv.LINE_8)
    cv.imshow("template", template)
    defect_boxes = detect_defect(binary, rects, template)
    for dx, dy, dw, dh in defect_boxes:
        cv.rectangle(src, (dx, dy), (dx + dw, dy + dh), (0, 0, 255), 1, cv.LINE_8)
        cv.putText(src, "bad", (dx, dy), cv.FONT_HERSHEY_PLAIN, 1.0, (0, 255, 0), 2)
    index = 1
    for dx, dy, dw, dh in rects:
        cv.putText(src, "num: %d" % index, (dx - 65, dy + 25), cv.FONT_HERSHEY_PLAIN, 1.0, (255, 0, 0), 1)
        index += 1
    cv.imshow("result", src)
    cv.waitKey(0)
    cv.destroyAllWindows()


if "__main__" == __name__:
    main()

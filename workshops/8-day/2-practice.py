#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv

"""
    基于第二天的工业刀片检测衍生的练习内容：
        将 +5 的炸弹提取出来并标识
"""


def get_template(binary, boxes):
    x, y, w, h = boxes[26]
    roi = binary[y: y + h, x: x + w]
    return roi


def defect_boxes(binary, boxes, tpl):
    height, width = tpl.shape[:2]
    defect_rois = []
    for x, y, w, h in boxes:
        roi = binary[y: y + h, x: x + w]
        roi = cv.resize(roi, (width, height))
        mask = cv.subtract(tpl, roi)
        kernel = cv.getStructuringElement(cv.MORPH_RECT, (3, 3))
        mask = cv.morphologyEx(mask, cv.MORPH_OPEN, kernel)
        _, mask = cv.threshold(mask, 0, 255, cv.THRESH_BINARY)
        target = 0
        for row in range(height):
            for col in range(width):
                pv = mask[row, col]
                if 255 == pv:
                    target += 1
        if 0 == target:
            defect_rois.append([x, y, w, h])
    return defect_rois


def main():
    """
        思路:
            输入图像 -> 二值化 -> 轮廓发现 -> 模板提取 -> 模板对比 -> 结果输出
    """
    src = cv.imread("../../pic/sw/sw_game_duiduipen.png")
    gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
    blur = cv.medianBlur(gray, 5)  # 去除一些不必要的干扰
    _, binary = cv.threshold(blur, 0, 255, cv.THRESH_BINARY | cv.THRESH_TRIANGLE)  # 图像为单峰图
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (3, 3))
    binary = cv.morphologyEx(binary, cv.MORPH_OPEN, kernel)  # 开操作 - 去除细小结构
    contours, _ = cv.findContours(binary, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
    structure = []
    for index in range(len(contours)):
        contour = contours[index]
        x, y, w, h = cv.boundingRect(contour)
        area = cv.contourArea(contour)
        # 过滤， 将宽度太小的， 面积太小的去除掉
        if 5000 > area or 80 > w:
            continue
        # cv.drawContours(src, contours, index, (0, 0, 255), 2, cv.LINE_8)
        structure.append([x, y, w, h])
    # sort_struct(structure)   # 计划排序，但意义不大
    template = get_template(binary, structure)  # 提取模板
    target = defect_boxes(binary, structure, template)  # 提取模板内容
    cv.imshow("template", template)
    # index = 1
    # 结果绘制
    for dx, dy, dw, dh in target:
        cv.rectangle(src, (dx, dy), (dx + dw, dy + dh), (255, 0, 0), 1, cv.LINE_8)
        cv.putText(src, "this", (dx, dy), cv.FONT_HERSHEY_PLAIN, 1.0, (0, 255, 0), 1, cv.LINE_8)
    cv.namedWindow("dst", cv.WINDOW_AUTOSIZE)
    cv.imshow("dst", src)
    cv.waitKey(0)
    cv.destroyAllWindows()


if "__main__" == __name__:
    main()

#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv

"""
    工业品的缺陷检测
        工业品的缺陷检测是二值图像分析中的经典案例，分为两个部分进行，第一部分是通过图像分析提取指定的轮廓，第二部分是通过对比实现划痕检
    测与缺角检测。
        检测流程如下：
            输入图像 -> 二值化 -> 轮廓发现与分析 -> 轮廓排序 -> 填充/扩大 -> 模板比对 -> 结果输出
"""


# ROI 轮廓排序
def sort_boxes(rois):
    for i in range(0, len(rois) - 1, 1):
        for j in range(i, len(rois), 1):
            x, y, w, h = rois[j]
            # 根据y坐标进行上下排序
            if rois[i][1] > y:
                bx, by, bw, bh = rois[i]
                rois[i] = [x, y, w, h]
                rois[j] = [bx, by, bw, bh]
    return rois


# 获取模板
def get_template(binary, boxes):
    x, y, w, h = boxes[0]  # 以第一个组件作为 轮廓模板
    roi = binary[y:y + h, x:x + w]  # 直接分割
    return roi


# 坏点检测
def detect_defect(binary, boxes, tpl):
    height, width = tpl.shape[:2]  # 获取模板的宽高
    defect_rois = []  # 换点轮廓的存放集合
    for x, y, w, h in boxes:
        roi = binary[y:y + h, x: x + w]   # 逐个区域提取
        roi = cv.resize(roi, (width, height))  # 将区域 缩放至模板大小
        # 模板 减去 提取的区域， 获取具有差异的部分
        mask = cv.subtract(tpl, roi)  # 获取 遮罩
        kernel = cv.getStructuringElement(cv.MORPH_RECT, (5, 5), (-1, -1))  # 声明结构元素
        mask = cv.morphologyEx(mask, cv.MORPH_OPEN, kernel)  # 开操作（先腐蚀, 再膨胀）, 过滤细小的差异
        _, mask = cv.threshold(mask, 0, 255, cv.THRESH_BINARY)  # 二值化, 非0的位置均为255
        count = 0
        for row in range(height):
            for col in range(width):
                pv = mask[row, col]  # 扫描差异部分，提取像素
                if 255 == pv:  # 若存在非零的部位
                    count += 1
        if 0 < count:
            defect_rois.append([x, y, w, h])
    return defect_rois


def main():
    src = cv.imread("../../pic/blade.jpeg")
    cv.namedWindow("input", cv.WINDOW_AUTOSIZE)
    # 转换为灰度图像
    gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
    # 二值化
    _, binary = cv.threshold(gray, 0, 255, cv.THRESH_BINARY_INV | cv.THRESH_OTSU)
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (3, 3), (-1, -1))
    # 形态学处理后的 二值化图片
    binary = cv.morphologyEx(binary, cv.MORPH_OPEN, kernel)
    # 寻找轮廓, 注意获取的是 轮廓列表，否则只有一个最大的轮廓
    contours, _ = cv.findContours(binary, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
    height, width = src.shape[:2]  # 获取宽高用于轮廓过滤
    rects = []  # 分析结果存储的list
    for index in range(len(contours)):
        contour = contours[index]
        x, y, w, h = cv.boundingRect(contour)  # 获取轮廓的外接矩形坐标
        area = cv.contourArea(contour)  # 轮廓面积计算
        # ROI区域过滤 提取
        if height // 2 < h or 150 > area:
            continue
        # cv.drawContours(binary, contours, index, (0, 0, 0), 2, cv.LINE_8)  # 绘制轮廓
        rects.append([x, y, w, h])
    # ROI区域 轮廓排序
    rects = sort_boxes(rects)
    # 提取模板
    template = get_template(binary, rects)
    cv.imshow("template", template)  # 模板
    # 模板对比， 提取被破坏的刀片轮廓
    defect_boxes = detect_defect(binary, rects, template)
    # 将被破坏的轮廓绘制
    for dx, dy, dw, dh in defect_boxes:
        cv.rectangle(src, (dx, dy), (dx + dw, dy + dh), (0, 0, 255), 1, cv.LINE_8)
        cv.putText(src, "bad", (dx, dy), cv.FONT_HERSHEY_PLAIN, 1.0, (0, 255, 0), 2)
    # 将识别的组件进行排序
    index = 1
    for dx, dy, dw, dh in rects:
        cv.putText(src, "num: %d" % index, (dx - 65, dy + 25), cv.FONT_HERSHEY_PLAIN, 1.0, (255, 0, 0), 1)
        index += 1
    cv.imshow("result", src)
    cv.waitKey(0)
    cv.destroyAllWindows()


if "__main__" == __name__:
    main()

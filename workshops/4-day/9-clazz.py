#!/usr/bin/env python
# -*- coding=utf-8 -*-

import cv2 as cv
import numpy as np

"""
    模板匹配：
        模板匹配被称为最简单的模式识别方式，模板匹配的工作条件严苛，因为其并不是基于特征的匹配，需要光照、背景、干扰一致
    的情况下才能更好的工作，在工业、屏幕内容识别上运用广泛。
    
        cv.matchTemplate(image, templ, result, method, mask)
            - image  : 输入进行匹配的图像
            - templ  : 模板图像
            - result : 匹配结果集
            - method : 匹配方法
            - mask   : 二值图遮罩 
            
        匹配方法集如下:
            - TM_SQDIFF = 0
            - TM_SQDIFF_NORMED = 1       # 平方不同与其归一化，值越小相关性越高，匹配程度越高
            - TM_CCORR = 2
            - TM_CCORR_NORMED = 3        # 相关性匹配，值越大相关性越强，匹配程度越高；Normed表示归一化，1表示高度匹配
            - TM_CCOEFF = 4
            - TM_CCOEFF_NORMED = 5       # 相关因子匹配，值越大相关性越强，匹配程度越高；Normed表示归一化，1表示高度匹配
"""


def template_match(image, template):
    th, tw = template.shape[:2]  # 获取模板的 高度与宽度
    result = cv.matchTemplate(image, template, cv.TM_CCORR_NORMED)
    cv.imshow("result", result)
    threshold = 0.952
    loc = np.where(result > threshold)
    for pt in zip(*loc[::-1]):
        cv.rectangle(image, pt, (pt[0] + tw, pt[1] + th), (0, 0, 255), 1, cv.LINE_8, 0)
    cv.imshow("llk-dst", image)


def main():
    src_input = cv.imread("../../pic/sw/sw_game_duiduipen.png")
    cv.imshow("input image", src_input)
    src_temp = cv.imread("../../pic/sw/temp_sw_game_blue.png")
    cv.imshow("find this", src_temp)
    template_match(src_input, src_temp)
    cv.waitKey(0)
    cv.destroyAllWindows()


if "__main__" == __name__:
    main()

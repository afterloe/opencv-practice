#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv
import numpy as np

"""

"""

model_path = "../../../raspberry-auto/models/fast_style/"
models_bin = ["composition_vii.t7", "starry_night.t7", "la_muse.t7", "the_wave.t7",
              "mosaic.t7", "the_scream.t7", "feathers.t7", "candy.t7", "udnie.t7"]
index = 3


def main():
    net = cv.dnn.readNetFromTorch(model_path + models_bin[index])
    net.setPreferableBackend(cv.dnn.DNN_BACKEND_OPENCV)
    image = cv.imread("../../../raspberry-auto/pic/0eb30f2442a7d9337f23fb34a54bd11372f001e9.jpg")
    cv.imshow("src", image)
    h, w = image.shape[:2]
    inp = cv.dnn.blobFromImage(image, 1.0, (255, 255), (103.939, 116.779, 123.68), False, False)
    net.setInput(inp)
    out = net.forward()
    print(out.shape)
    t, _ = net.getPerfProfile()
    freq = cv.getTickFrequency() / 1000
    txt = "fps: %.2f" % (1000 / (t / freq))
    out = out.reshape(3, out.shape[2], out.shape[3])
    print(out.shape)
    out[0] += 103.939
    out[1] += 116.779
    out[2] += 123.68
    out /= 255.0
    out = out.transpose(1, 2, 0)
    print("new shape", out.shape)
    out = np.clip(out, 0.0, 1.0)
    cv.normalize(out, out, 0, 255, cv.NORM_MINMAX)
    out = cv.medianBlur(out, 5)
    result = np.uint8(cv.resize(out, (w, h)))
    cv.putText(result, txt, (0, 15), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
    cv.imshow("fast style demo", result)
    cv.waitKey(0)


if "__main__" == __name__:
    main()
    cv.destroyAllWindows()

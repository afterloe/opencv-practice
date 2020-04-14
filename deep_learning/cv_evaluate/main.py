#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv


def main():
    model_path = "/mount/data/Project/detector_tensorflow/digimon/annotations/export/Servo/1586867572/saved_model.pb"
    pbtxt_path = "/mount/data/Project/detector_tensorflow/digimon/annotations/label_map.pbtxt"
    net = cv.dnn.readNetFromTensorflow(model=model_path, config=pbtxt_path)

    image = cv.imread("/mount/data/Project/detector_tensorflow/digimon/images/train/00000001.jpg")
    origin = image.copy()
    rate = image.shape[:1] / 32
    image = cv.resize(image, (32, 32))
    data = cv.dnn.blobFromImage(image, 1.0, (32, 32), (104.0, 177.0, 123.0), False, False)
    net.setInput(data)
    out = net.forward()
    t, _ = net.getPerfProfile()
    label = "Inference time: %.2f ms" % (t * 1000.0 / cv.getTickFrequency())
    cv.putText(origin, label, (0, 15), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0))
    for det in out[0, 0, :, :]:
        score = float(det[2])
        print(det)
        if 0.5 < score:
            left = det[3] * 32 * rate
            top = det[4] * 32 * rate
            right = det[5] * 32 * rate
            bottom = det[6] * 32 * rate
            cv.rectangle(origin, (int(left), int(top)), (int(right), int(bottom)), (255, 0, 0), 2)
            cv.putText(origin, "score: %.2f" % score, (int(left), int(top)),
                       cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
    cv.imshow("origin", origin)
    cv.imshow("image", image)
    cv.waitKey(0)


if "__main__" == __name__:
    main()
    cv.destroyWindow()

#!/usr/bin/env python3
# -*- coding=utf-8 -*-

from src.conv_net_factory import CONVNetFactory
from tensorflow.keras.optimizers import SGD
from tensorflow.keras.datasets import cifar100
from tensorflow.keras import utils
from sklearn.metrics import classification_report
import argparse
import logging

__version__ = "1.2.3"

logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)8s][%(filename)s][%(levelname)s] - %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')
CONSOLE = logging.getLogger("dev")
CONSOLE.setLevel(logging.DEBUG)
CONSOLE.info("模型训练工具 %s", __version__)


if "__main__" == __name__:
    ap = argparse.ArgumentParser()
    ap.add_argument("-n", "--network", required=True, help="name of network to build")
    ap.add_argument("-m", "--model", required=True, help="path to output model file")
    ap.add_argument("-d", "--dropout", type=int, default=-1, help="whether or net dropout should be used")
    ap.add_argument("-f", "--activation", type=str, default="tanh", help="activation function to use (LeNet only)")
    ap.add_argument("-e", "--epochs", type=int, default=20, help="# of epochs")
    ap.add_argument("-b", "--batch-size", type=int, default=32, help="size of mini-batches passed to network")
    ap.add_argument("-v", "--verbose", type=int, default=1, help="verbosity level")
    args = vars(ap.parse_args())
    CONSOLE.info("加载训练数据")
    (train_data, train_labels), (test_data, test_labels) = cifar100.load_data()
    train_data = train_data.astype("float") / 255.0
    test_data = test_data.astype("float") / 255.0
    train_labels = utils.to_categorical(train_labels, num_classes=100)
    test_labels = utils.to_categorical(test_labels, num_classes=100)
    # collect the keyword arguments to the network
    kargs = {"dropout": args["dropout"] > 0, "activation": args["activation"]}
    CONSOLE.info("编译模型")
    model = CONVNetFactory.build(args["network"], 3, 32, 32, 100, **kargs)
    sgd = SGD(lr=0.01, decay=1e-7, momentum=0.9, nesterov=True)
    model.compile(loss="categorical_crossentropy", optimizer=sgd, metrics=["accuracy"])
    CONSOLE.info("开始训练")
    H = model.fit(train_data, train_labels, validation_data=(test_data, test_labels),
                  batch_size=args["batch_size"], epochs=args["epochs"], verbose=args["verbose"])
    CONSOLE.info("评估模型")
    predictions = model.predict(test_data, batch_size=args["batch_size"])
    CONSOLE.info("输出分类结果")
    print(classification_report(test_labels.argmax(axis=1), predictions.argmax(axis=1),
                                # target_names= ["airplane", "automobile", "bird", "cat", "deer", "dog", "frog",
                                #                "horse", "ship", "truck"]))
                                target_names=["aquatic mammals", "fish", "flowers", "food containers",
                                              "fruit and vegetables", "household electrical devices",
                                              "household furniture", "insects", "large carnivores",
                                              "large man-made outdoor things", "large natural outdoor scenes",
                                              "large omnivores and herbivores", "medium-sized mammals",
                                              "non-insect invertebrates", "people", "reptiles", "small mammals",
                                              "trees", "vehicles 1", "vehicles 2"]))

    model.fit(train_data, train_labels, batch_size=args["batch_size"], epochs=args["epochs"], verbose=args["verbose"])
    loss, accuracy = model.evaluate(test_data, test_labels, batch_size=args["batch_size"], verbose=args["verbose"])
    CONSOLE.info("accuracy: {:.2f}%".format(accuracy * 100))
    CONSOLE.info("dumping architecture and weights to file...")
    model.save(args["model"])

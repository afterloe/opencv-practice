#!/usr/bin/env python3
# -*- coding=utf-8 -*-

from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from simple_preprocessor import SimplePreprocessor
from simple_dataset_loader import SimpleDatasetLoader
from imutils import paths
import argparse
import logging

__version__ = "1.0.0"

logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)8s][%(filename)s][%(levelname)s] - %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')
CONSOLE = logging.getLogger("dev")
CONSOLE.setLevel(logging.DEBUG)
CONSOLE.info("第一个knn练习 %s", __version__)

if "__main__" == __name__:
    ap = argparse.ArgumentParser()
    ap.add_argument("-d", "--dataset", required=True, help="数据存储路径")
    ap.add_argument("-k", "--neighbors", type=int, default=1, help="分类的最近相近点")
    ap.add_argument("-j", "--jobs", type=int, default=1, help="KNN算法的作业数")
    args = vars(ap.parse_args())
    CONSOLE.info("加载图像数据")
    image_paths = list(paths.list_images(args["dataset"]))
    processor = SimplePreprocessor(32, 32)
    data_loader = SimpleDatasetLoader(preprocessor=[processor])
    data, labels = data_loader.load(image_paths, verbose=500)
    data = data.reshape((data.shape[0], 3072))
    CONSOLE.info("特征点: {:.1f}MB".format(data.nbytes / (1024 * 1000.0)))
    le = LabelEncoder()
    labels = le.fit_transform(labels)
    train_x, test_x, train_y, test_y = train_test_split(data, labels, test_size=0.25, random_state=42)
    CONSOLE.info("knn 分类")
    model = KNeighborsClassifier(n_neighbors=args["neighbors"], n_jobs=args["jobs"])
    model.fit(train_x, train_y)
    CONSOLE.info(classification_report(test_y, model.predict(test_x), target_names=le.classes_))

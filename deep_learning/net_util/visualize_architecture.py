#!/usr/bin/env python3
# -*- coding=utf-8 -*-

from src.conv_net_factory import CONVNetFactory
from tensorflow.keras.utils import plot_model
import logging


__version__ = "1.0.0"

logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)8s][%(filename)s][%(levelname)s] - %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')
CONSOLE = logging.getLogger("dev")
CONSOLE.setLevel(logging.DEBUG)
CONSOLE.info("模型可视化 %s", __version__)

if "__main__" == __name__:
    kargs = {"dropout": False, "activation": "tanh"}
    model = CONVNetFactory.build("lenet", 1, 28, 28, 10, **kargs)
    plot_model(model, to_file="lenet.png", show_shapes=True, show_layer_names=True)

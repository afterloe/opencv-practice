#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import logging


__version__ = "1.0.0"

logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)8s][%(filename)s][%(levelname)s] - %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')
CONSOLE = logging.getLogger("dev")
CONSOLE.setLevel(logging.DEBUG)
CONSOLE.info("将模拟数据转换为内存数据 %s" % __version__)


def generate_data(batch_size=100):
    train_x = np.linspace(-1, 1, batch_size)
    train_y = 2 * train_x + np.random.rand(*train_x.shape) * 0.3
    yield train_x, train_y


def main():
    x_input = tf.placeholder("float", None)
    y_input = tf.placeholder("float", None)
    training_epochs = 10 * 100
    with tf.Session() as sess:
        for epoch in range(training_epochs):
            for x, y in generate_data():
                x_value, y_value = sess.run([x_input, y_input], feed_dict={x_input: x, y_input: y})
                CONSOLE.info("{} | x.shape: {} | x[: 3]: {}".format(epoch, np.shape(x_value), x_value[: 3]))
                CONSOLE.info("{} | y.shape: {} | y[: 3]: {}".format(epoch, np.shape(y_value), y_value[: 3]))
    train_data = list(generate_data())[0]
    plt.plot(train_data[0], train_data[1], "ro", label="Original data")
    plt.legend()
    plt.show()


if "__main__" == __name__:
    main()

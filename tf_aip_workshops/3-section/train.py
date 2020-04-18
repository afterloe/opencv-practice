#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import tensorflow as tf
import logging
import os
model_clazz = __import__("model")


CONSOLE = logging.getLogger("dev")

batch_size = 32
train_dir = "data/train"
eval_dir = "data/eval"
learning_rate_1 = 1e-1
learning_rate_2 = 1e-3

mode = model_clazz.CustomizeNASNetModel(r"nasnet-a_mobile_04_10_2017/model.ckpt")
mode.build_model("train", eval_dir, train_dir, batch_size, learning_rate_1, learning_rate_2)

num_epochs_1 = 20
num_epochs_2 = 200

with tf.Session() as sess:
    sess.run(mode.global_init)

step = 0
step = mode.load_cpk(mode.global_step, sess, 1, mode.saver, mode.save_path)
CONSOLE.info(step)

if 0 == step:
    mode.init_fn(sess)
    for epoch in range(num_epochs_1):
        CONSOLE.info("Staring_1 epoch %d / %d" %(epoch + 1, num_epochs_1))
        sess.run(mode.train_init_op)
        while True:
            try:
                step += 1
                acc, accuracy_top_5, summary, _ = sess.run([mode.accuracy, mode.accuracy_top_5, mode.merged,
                                                            mode.last_train_op])
                if 0 == step % 100:
                    CONSOLE.info(f"step: {step} train_1 accuracy: {acc}, {accuracy_top_5}")
            except tf.errors.OutOfRangeError:
                CONSOLE.info("train_1: %d OK" % epoch)
                mode.saver.save(sess, os.path.sep.join([mode.save_path, "digital_nasnet.cpkt"]),
                                global_step=mode.global_step.eval())
                break
        sess.run(mode.step_init)

    for epoch in range(num_epochs_2):
        CONSOLE.info("Staring_2 epoch %d / %d" % (epoch + 1, num_epochs_2))
        sess.run(mode.train_init_op)
        while True:
            try:
                step += 1
                acc, summary, _ = sess.run([mode.accuracy, mode.merged, mode.full_train_op])
                mode.train_writer.add_summary(summary, step)
                if 0 == step % 100:
                    CONSOLE.info(f"step: {step} train_2 accuracy: {acc}")
            except tf.errors.OutOfRangeError:
                CONSOLE.info("train_2 %d OK" % epoch)
                mode.saver.save(sess, os.path.sep.join([mode.save_path, "digital_nasnet.cpkt"]),
                                global_step=mode.global_step.eval())
                break

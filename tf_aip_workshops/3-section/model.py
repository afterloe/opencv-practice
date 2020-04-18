#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import os
import tensorflow as tf
from nets.nasnet import nasnet
import logging

slim = tf.contrib.slim
data_set = __import__("img_to_dataset")
CONSOLE = logging.getLogger("dev")


class CustomizeNASNetModel(object):

    def __init__(self, model_path=""):
        self.__model_path = model_path

    def generator_NASNet(self, images, is_training):
        arg_scope = nasnet.nasnet_mobile_arg_scope()
        with slim.arg_scope(arg_scope):
            logits, end_points = nasnet.build_nasnet_mobile(images, num_classes=self.__num_classes + 1,
                                                            is_training=is_training)
        global_step = tf.train.get_or_create_global_step()
        return logits, end_points, global_step

    def fine_true_NASNet(self, is_training):
        model_path = self.__model_path
        exclude = ["final_layer", "aux_7"]
        variables_to_restore = slim.get_variables_to_restore(exclude=exclude)
        if True is is_training:
            init_fn = slim.assign_from_checkpoint_fn(model_path, variables_to_restore)
        else:
            init_fn = None
        tuning_variables = []
        for v in exclude:
            tuning_variables += slim.get_variables(v)
        return init_fn, tuning_variables

    def build_acc_base(self, labels):
        self.__prediction = tf.cast(tf.argmax(self.__logits, 1), tf.int32)
        self.__correct_prediction = tf.equal(self.__prediction, labels)
        self.__accuracy = tf.reduce_mean(tf.cast(self.__correct_prediction), tf.loat32)
        self.__accuracy_top_5 = tf.reduce_mean(tf.cast(tf.nn.in_top_k(predictions=self.__logits,
                                                                      targets=labels, k=5), tf.float32))

    def load_cpk(self, global_step, sess, begin=0, saver=None, save_path=None):
        if 0 == begin:
            save_path = r"./train_nasnet"
            if not os.path.exists(save_path):
                CONSOLE.info("there is not a model path: %s" % save_path)
            saver = tf.train.Saver(max_to_keep=1)
            return saver, save_path
        else:
            kpt = tf.train.latest_checkpoint(save_path)
            CONSOLE.info("load model: %s" % kpt)
            start_epo = 0
            if None is not kpt:
                saver.restore(sess, kpt)
                ind = kpt.find("-")
                start_epo = int(kpt[ind + 1:])
                CONSOLE.info("global_step = {}".format(global_step.eval()))
                CONSOLE.info(start_epo)
        return start_epo

    def build_model_train(self, images, labels, learning_rate_1, learning_rate_2, is_training):
        self.__logits, self.__end_points, self.__global_step = self.generator_NASNet(images, is_training=is_training)
        self.__step_init = self.__global_step.initializer
        self.__init_fn, self.__tuning_variables = self.fine_true_NASNet(is_training=is_training)
        tf.losses.sparse_softmax_cross_entropy(labels=labels, logits=self.__logits)
        loss = tf.losses.get_total_loss()
        learning_rate_1 = tf.train.exponential_decay(learning_rate=learning_rate_1, global_step=self.__global_step,
                                                     decay_steps=100, decay_rate=0.5)
        learning_rate_2 = tf.train.exponential_decay(learning_rate=learning_rate_2, global_step=self.__global_step,
                                                     decay_steps=100, decay_rate=0.2)
        last_optimizer = tf.train.AdamOptimizer(learning_rate_1)
        full_optimizer = tf.train.AdamOptimizer(learning_rate_2)
        update_ops = tf.get_collection(tf.GraphKeys.UPDATE_OPS)
        with tf.control_dependencies(update_ops):
            self.__last_train_op = last_optimizer.minimize(loss, self.__global_step, var_list=self.__tuning_variables)
            self.__full_train_op = full_optimizer.minimize(loss, self.__global_step)
        self.build_acc_base(labels)
        tf.summary.scalar("accuracy", self.__accuracy)
        tf.summary.scalar("accuracy_top_5", self.__accuracy_top_5)
        self.__merged = tf.summary.merge_all()
        self.__train_writer = tf.summary.FileWriter("./log_dir/train")
        self.__eval_writer = tf.summary.FileWriter("./log_dir/eval")
        self.__saver, self.__save_path = self.load_cpk(self.__global_step, None)

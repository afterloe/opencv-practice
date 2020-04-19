#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import os
import tensorflow as tf
from nets.nasnet import nasnet
import logging

slim = tf.contrib.slim
data_set_util = __import__("img_to_dataset")
CONSOLE = logging.getLogger("dev")


class CustomizeNASNetModel(object):

    def __init__(self, model_path=""):
        self.__model_path = model_path

    def generator_NASNet(self, images, is_training):
        arg_scope = nasnet.nasnet_mobile_arg_scope()
        with slim.arg_scope(arg_scope):
            logits, end_points = nasnet.build_nasnet_mobile(images, num_classes=self.__num_classes + 1,
                                                            is_training=is_training)
        global_step = tf.compat.v1.train.get_or_create_global_step()
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
        self.__prediction = tf.cast(tf.argmax(self.logits, 1), tf.int32)
        self.correct_prediction = tf.equal(self.__prediction, labels)
        self.accuracy = tf.reduce_mean(tf.cast(self.correct_prediction, tf.float32))
        self.accuracy_top_5 = tf.reduce_mean(tf.cast(tf.nn.in_top_k(predictions=self.logits,
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
        self.logits, self.__end_points, self.global_step = self.generator_NASNet(images, is_training=is_training)
        self.step_init = self.global_step.initializer
        self.init_fn, self.__tuning_variables = self.fine_true_NASNet(is_training=is_training)
        tf.losses.sparse_softmax_cross_entropy(labels=labels, logits=self.logits)
        loss = tf.losses.get_total_loss()
        learning_rate_1 = tf.train.exponential_decay(learning_rate=learning_rate_1, global_step=self.global_step,
                                                     decay_steps=100, decay_rate=0.5)
        learning_rate_2 = tf.train.exponential_decay(learning_rate=learning_rate_2, global_step=self.global_step,
                                                     decay_steps=100, decay_rate=0.2)
        last_optimizer = tf.train.AdamOptimizer(learning_rate_1)
        full_optimizer = tf.train.AdamOptimizer(learning_rate_2)
        update_ops = tf.get_collection(tf.GraphKeys.UPDATE_OPS)
        with tf.control_dependencies(update_ops):
            self.last_train_op = last_optimizer.minimize(loss, self.global_step, var_list=self.__tuning_variables)
            self.full_train_op = full_optimizer.minimize(loss, self.global_step)
        self.build_acc_base(labels)
        tf.summary.scalar("accuracy", self.accuracy)
        tf.summary.scalar("accuracy_top_5", self.accuracy_top_5)
        self.merged = tf.summary.merge_all()
        self.train_writer = tf.summary.FileWriter("./log_dir/train")
        self.__eval_writer = tf.summary.FileWriter("./log_dir/eval")
        self.saver, self.save_path = self.load_cpk(self.global_step, None)

    def build_model(self, mode="train", train_data_dir="./data/train", test_data_dir="./data/eval", batch_size=32,
                    learning_rate_1=0.001, learning_rate_2=0.001):
        if "train" == mode:
            tf.compat.v1.reset_default_graph()
            train_data_set, self.__num_classes = data_set_util.create_dataset_fromdir(train_data_dir, batch_size)
            test_data_set, _ = data_set_util.create_dataset_fromdir(test_data_dir, batch_size, is_train=False)
            iterator = tf.compat.v1.data.Iterator.from_structure(tf.compat.v1.data.get_output_types(train_data_set),
                                                                 tf.compat.v1.data.get_output_shapes(train_data_set))
            images, labels = iterator.get_next()
            self.train_init_op = iterator.make_initializer(train_data_set)
            self.test_init_op = iterator.make_initializer(test_data_set)
            self.build_model_train(images, labels, learning_rate_1, learning_rate_2, is_training=True)
            self.global_init = tf.global_variables_initializer()
            tf.get_default_graph().finalize()
        elif "test" == mode:
            tf.reset_default_graph()
            test_data_set, self.__num_classes = data_set_util.create_dataset_fromdir(test_data_dir, batch_size,
                                                                                     is_train=False)
            iterator = tf.compat.v1.data.Iterator.from_structure(tf.compat.v1.data.get_output_types(test_data_set),
                                                                 tf.compat.v1.data.get_output_shapes(test_data_set))

            self.images, labels = iterator.get_next()
            self.test_init_op = iterator.make_initializer(test_data_set)
            self.logits, self.__end_points, self.global_step = self.generator_NASNet(self.images,
                                                                                         is_training=False)
            self.saver, self.save_path = self.load_cpk(self.global_step, None)
            self.build_acc_base(labels)
            tf.get_default_graph().finalize()
        elif "eval" == mode:
            tf.reset_default_graph()
            test_data_set, self.__num_classes = data_set_util.create_dataset_fromdir(test_data_dir, batch_size,
                                                                                     is_train=False)
            iterator = tf.compat.v1.data.Iterator.from_structure(tf.compat.v1.data.get_output_types(test_data_set),
                                                                 tf.compat.v1.data.get_output_shapes(test_data_set))
            self.images, labels = iterator.get_next()
            self.logits, self.__end_points, self.global_step = self.generator_NASNet(self.images,
                                                                                         is_training=False)
            self.saver, self.save_path = self.load_cpk(self.global_step, None)
            tf.get_default_graph().finalize()

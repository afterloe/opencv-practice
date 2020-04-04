#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import time
import os

INFO, ERROR, SUCCESS = "INFO", "ERROR", "SUCCESS"
LOG_SAVE_PATH = "/tmp"
SUFFIX = time.strftime("%Y%m%d", time.localtime(time.time()))
LOG_FILE = "%s/meter_reader_4_pointer-%s.log" % (LOG_SAVE_PATH, SUFFIX)


def log(message, log_type=INFO):
    content = "[{}][{}]: {}".format(log_type, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())),
                                    message)
    os.system("echo '%s' >> %s" % (content, LOG_FILE))
    return content


def get_time_str():
    return time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))

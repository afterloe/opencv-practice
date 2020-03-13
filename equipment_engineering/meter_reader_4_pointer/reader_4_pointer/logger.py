#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import time
import os

INFO, ERROR, SUCCESS = "INFO", "ERROR", "SUCCESS"


def log(message, log_type=INFO):
    content = "[{}][{}]: {}".format(log_type, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())),
                                    message)
    os.system("echo '%s' >> /tmp/python.log" % content)
    return content

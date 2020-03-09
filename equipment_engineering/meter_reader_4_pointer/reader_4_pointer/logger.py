#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import time

INFO, ERROR, SUCCESS = "INFO", "ERROR", "SUCCESS"


def log(message, log_type=INFO):
    content = "[{}][{}]: {}".format(log_type, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())),
                                    message)
    print(content)
    return content

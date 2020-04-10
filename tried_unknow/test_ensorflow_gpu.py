#!/usr/bin/env python3
# -*- coding=utf-8 -*-


from tensorflow.python.client import device_lib as _device_lib


if "__main__" == __name__:
    local_device_protos = _device_lib.list_local_devices()
    print([x.name for x in local_device_protos if x.device_type == 'GPU'])


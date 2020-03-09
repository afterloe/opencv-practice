#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import yaml

# caps = {
#     "min_angle": 40,
#     "max_angle": 320,
#     "min_value": 0,
#     "max_value": 220
# }

with open("./config", "r", encoding="utf-8") as f:
    # yaml.dump(caps, f)
    value = yaml.load(f.read(), Loader=yaml.FullLoader)
    print(value)
    print(value["min_angle"])


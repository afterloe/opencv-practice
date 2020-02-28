#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import time


def main():
    ap = []
    bp = ["afterloe", "joe", "next"]
    ap += bp
    print(len(ap))
    print(ap)
    print(time.time())
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())))
    print("{}.jpeg".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))))


if "__main__" == __name__:
    main()

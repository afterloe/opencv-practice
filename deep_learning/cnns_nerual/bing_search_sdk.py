#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import argparse
import cv2 as cv
import requests
from requests import exceptions
import logging
import os


API_KEY = "b0c8fb60e0df49089860fa80c09d8aba"
MAX_RESULTS = 250
GROUP_SIZE = 50
SEARCH_URL = "https://api.cognitive.microsoft.com/bing/v7.0/images/search"


EXCEPTIONS = {IOError, FileNotFoundError, exceptions.RequestException, exceptions.HTTPError, exceptions.ConnectionError,
              exceptions.Timeout}


logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)8s][%(filename)s][%(levelname)s] - %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')
CONSOLE = logging.getLogger("dev")
CONSOLE.setLevel(logging.DEBUG)


if "__main__" == __name__:
    ap = argparse.ArgumentParser()
    ap.add_argument("-q", "--query", required=True, type=str, help="搜索内容")
    ap.add_argument("-o", "--output", required=True, help="搜索结果存放路径")
    args = vars(ap.parse_args())
    term = args["query"]
    headers = {"Ocp-Apim-Subscription-Key": API_KEY}
    params = {"q": term, "offset": 0, "count": GROUP_SIZE}
    CONSOLE.info("使用搜索引擎API搜索：%s" % term)
    search = requests.get(SEARCH_URL, headers=headers, params=params)
    search.raise_for_status()
    results = search.json()
    est_num_results = min(results["totalEstimatedMatches"], MAX_RESULTS)
    CONSOLE.info("共计 {} 条 关于 {} 的搜索结果".format(est_num_results, term))
    total = 0

    for v in results["value"]:
        search_url = v["contentUrl"]
        CONSOLE.info("正在获取 %s" % search_url)
        ext = search_url[search_url.rfind("."):]
        p = os.path.sep.join([args["output"], "%s%s" % (str(total).zfill(0), ext)])
        CONSOLE.info("存储于 %s" % p)
        try:
            r = requests.get(search_url, timeout=5)
            f = open(p, "wb")
            f.write(r.content)
            f.close()
        except Exception as e:
            if type(e) in EXCEPTIONS:
                CONSOLE.error("跳过 %s" % v["contentUrl"])
                continue
        image = cv.imread(p)
        if None is image:
            CONSOLE.info("%s 无法打开，已删除" % p)
            os.remove(p)
            continue
        total += 1

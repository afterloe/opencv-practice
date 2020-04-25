#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import unittest
from unittest.mock import patch
import sys
import logging
sys.path.append("..")
# from img_to_dataset import get_images_list
data_set_util = __import__("img_to_dataset")

logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)8s][%(filename)s][%(levelname)s] - %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')
CONSOLE = logging.getLogger("dev")


class TestImgToDataset(unittest.TestCase):

    def setUp(self) -> None:
        pass

    # @patch.object()
    def test_get_images_list(self):
        directory = "/home/afterloe/data/afterloe resources/animal/train"
        file_names, labels = data_set_util.get_images_list(directory)
        # CONSOLE.info(file_names)
        # CONSOLE.info(labels)
        pass


if "__main__" == __name__:
    unittest.main()

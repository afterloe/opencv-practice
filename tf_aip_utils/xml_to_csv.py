#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import argparse
import pandas as pd
import glob
import os
import logging
import xml.etree.ElementTree as ET

__version__ = "1.0.0"

logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)8s][%(filename)s][%(levelname)s] - %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')
CONSOLE = logging.getLogger("dev")
CONSOLE.setLevel(logging.DEBUG)
CONSOLE.info("xml to CSV %s", __version__)


def xml_to_csv(input_dir):
    xml_list = []
    for xml_file in glob.glob(os.path.sep.join([input_dir, "*.xml"])):
        tree = ET.parse(xml_file)
        root = tree.getroot()
        for member in root.findall("object"):
            value = (root.find("filename").text,
                     int(root.find("size")[0].text),
                     int(root.find("size")[1].text),
                     member[0].text,
                     int(member[4][0].text),
                     int(member[4][1].text),
                     int(member[4][2].text),
                     int(member[4][3].text)
                     )
            xml_list.append(value)
    column_name = ["filename", "width", "height", "class", "xmin", "ymin", "xmax", "ymax"]
    return pd.DataFrame(xml_list, columns=column_name)


if "__main__" == __name__:
    ap = argparse.ArgumentParser(description="TensorFlow XML to CSV converter")
    ap.add_argument("-i", "--input-dir", help="path to the folder where the input .xml files are stored", type=str)
    ap.add_argument("-o", "--output-dir", help="name of output .csv file (include path)", type=str)
    args = vars(ap.parse_args())
    if None is args.get("input_dir"):
        args["input_dir"] = os.getcwd()
    if None is args.get("output_dir"):
        args["output_dir"] = os.path.sep.join([args["input_dir"], "labels.csv"])
    assert os.path.isdir(args["input_dir"])
    xml_df = xml_to_csv(args["input_dir"])
    xml_df.to_csv(args["output_dir"], index=False)
    CONSOLE.info("Successfully converted xml to cvs.")

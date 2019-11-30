#!/usr/bin/python
# coding=utf-8

import pytesseract
from PIL import Image

image = Image.open("../tmp/3.png")
code = pytesseract.image_to_string(image)

print(code)
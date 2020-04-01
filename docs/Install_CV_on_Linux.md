Opencv 4.1.2 安装手册 - Linux版
===

> create by [afterloe](605728727@qq.com)   
> version is 1.1  
> MIT License  

参考资料 [https://docs.opencv.org/trunk/d7/d9f/tutorial_linux_install.html](https://docs.opencv.org/trunk/d7/d9f/tutorial_linux_install.html)

## 安装前提
- GCC 4.4x 以上或更高
- CMake 2.8.7 以上
- Git
- GTK+2.x 以上，包括头文件（libgtk2.0-dev）
- pkg-config
- Python 2.6 以上

环境准备
```commandline
sudo apt-get update && sudo apt-get upgrade
sudo apt-get install cmake libgtk-3-dev -y
sudo apt-get install build-essential # 安装编译器
sudo apt-get install cmake git libgtk2.0-dev pkg-config libavcodec-dev libavformat-dev libswscale-dev # 安装依赖包
sudo apt-get install python-dev python-numpy libtbb2 libtbb-dev libjpeg-dev libpng-dev libtiff-dev libjasper-dev libdc1394-22-dev # 安装其他语言扩展包
sudo apt-get install libavcodec-dev libavformat-dev libswscale-dev libavutil-dev -y
sudo apt-get install libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev
sudo apt-get install libavresample-dev libgphoto2-dev -y
```

## 源码下载
- zip包下载
两种方式都可以选择，第一种的源码可以在[这里下载](https://opencv.org/releases/)
- Git Repository
```
mkdir -p ~/Project/lib
cd ~/Project/lib
git clone https://github.com/opencv/opencv.git
git clone https://github.com/opencv/opencv_contrib.git
```

## 配置编译内容
```
cd ~/Project/lib
cd opencv
mkdir build && cd build
touch build.sh
vim build.sh

#!/bin/bash

cmake -D CMAKE_BUILD_TYPE=RELEASE \
    -D CMAKE_INSTALL_PREFIX=/usr/local \
    -D WITH_CUDA=OFF \
    -D OPENCV_EXTRA_MODULES_PATH=../../opencv_contrib/modules \
    -D BUILD_opencv_python3=ON \
    -D BUILD_EXAMPLES=OFF ..

chmod +x build.sh
./build.sh
```
> 会出现一些error或 waring，不必管他; 若配置失败，检查内存情况，并重新执行脚本。

## 骚操作
当出现xfeatures2d的 test_包错误时
```commandline
rm -rf opencv_contrib/modules/xfeatures2d/test
cp -r opencv/model/features2d/test opencv_contrib/modules/xfeatures2d/test
```

## 编译
```
make -j8
```
> 7 表示启动7个线程进行同时编译。

## 安装
```
sudo make install
sudo ldconfig
```

## 测试
```
python3 
Python 3.7.5 (default, Nov 20 2019, 09:21:52)
[GCC 9.2.1 20191008] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import cv2
>>> cv2.__version__
'4.1.1'
>>>
```
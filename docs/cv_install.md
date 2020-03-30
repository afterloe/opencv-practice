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
```
sudo apt-get install build-essential # 安装编译器
sudo apt-get install cmake git libgtk2.0-dev pkg-config libavcodec-dev libavformat-dev libswscale-dev # 安装依赖包
sudo apt-get install python-dev python-numpy libtbb2 libtbb-dev libjpeg-dev libpng-dev libtiff-dev libjasper-dev libdc1394-22-dev # 安装其他语言扩展包
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

cmake -D CMAKE_BUILD_TYPE=Release \
        -D CMAKE_EXTRA_MODULES_PATH=../../opencv_contrib/modules/ \
        -D CMAKE_INSTALL_PREFIX=/usr/local \
        ../ \
        -D BUILD_opencv_java=OFF \
        -D BUILD_opencv_python2=OFF \
        -D BUILD_opencv_python3=OFF

chmod +x build.sh
./build.sh
```
> 会出现一些error或 waring，不必管他; 若配置失败，检查内存情况，并重新执行脚本。

## 编译
```
make -j7
```
> 7 表示启动7个线程进行同时编译。

## 安装
```
sudo make install
sudo ldconfig
```


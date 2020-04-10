n10 Tensorflow 安装指南
> create by [afterloe](lm6289511@gmail.com)  
> MIT License  
> version is 1.2.0

## 前言
Tensorflow是一款常用框架，[国外官网](https://www.tensorflow.org/)显示的安装教程是可以直接使用的，但是[国内的]()就算了，按照国内的安装差点扑街，所以写下这篇文章，当在外面需要进行Tensorflow安装时不必进行翻墙操作。  


## 安装
首先，确定自己的条件是否满足，安装的具体条件如下:
```
Python 3.5 ~ 3.7  
# 必须64位，否则安装的时候会报错（can't find version）
```
> Python下载地址: https://www.python.org/downloads/windows/


对运行系统的要求如下:
```
macOS > 10.12.6(即Sierra) [no GPU support]
Ubuntu > 16.04
Raspbian > 9.0
Windows > 7
```

Tensorflow的安装很简单，如下:
```
pip install --upgrade pip  # Tensorflow 需要pip > 19.0
pip install tensorflow  # current stable release for cpu and gpu
```
> pip 安装加速 https://mirrors.tuna.tsinghua.edu.cn/help/pypi/

## 排错
### tensorflow kera not found
tensorflow安装失败，重装！

### load dll failed
加载dll失败的主要原因有两个（目前为止排查到的），一是navid cuda和cudnn没有安装，二是protobuf版本导致的，具体内容如下:
#### cudart64_100.dll not loader
运行tensorflow显示如上dll not load，需要进行GPU支持安装，若没有GPU支持，则降低需要求即将Tensorflow退版到1.15或改成tensorflow-cpu版本。    
windows 10 安装GPU支持的过程如下:
* 安装Navida GPU驱动，驱动下载地址:https://www.nvidia.com/drivers
* 安装CUDA Toolkit，TensorFlow >= 2.1.0 需要安装CUDA 10.1，下载地址: https://developer.nvidia.com/cuda-toolkit-archive
* 安装cuDNN SDK，版本大于7.6，下载地址: https://developer.nvidia.com/cudnn
> * [可选] TensorRT 6.0 这个框架是Navida提出的，据说运行速度相当快，参考地址: https://docs.nvidia.com/deeplearning/sdk/tensorrt-install-guide/index.html


下载完毕后进行环境变量的配置
##### Linux 配置
Append its installation directory to the $LD_LIBRARY_PATH environmental variable:
```
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/cuda/extras/CUPTI/lib64
```

##### Windows 10 配置
Add the CUDA, CUPTI, and cuDNN installation directories to the `%PATH%` environmental variable.   
对`cudnn-10.1-windows10-x64-v7.6.5.32.zip`进行解压操作，安装在`G:/cudnn`, cuad进行默认安装，配置环境变量如下：
```
SET PATH=C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v10.1\bin;%PATH%
SET PATH=C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v10.1\extras\CUPTI\libx64;%PATH%
SET PATH=C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v10.1\include;%PATH%
SET PATH=G:\cudnn\cuda\bin;%PATH%
```

#### dll loader failed
不显示任何缺少的dll，这个比较坑，排查后发现是Protobuf的版本导致的，Tensorflow会自动安装Protobuf，自动安装的版本与其存在冲突，需要卸载Protobuf再指定版本进行安装，具体如下:
```
pip uninstall protobuf
pip install protobuf==3.6.0
```

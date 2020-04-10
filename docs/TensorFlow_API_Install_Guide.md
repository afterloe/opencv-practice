TensorFlow Detector API
===

> create by [afterloe](605728727@qq.com)  
> version is 1.0.3  
> MIT License  

TensorFlow的Detector API的安装经过折腾半个月，现在基本跑通，现在写下这篇博文。首先TensorFLow Detector API的版本还在迭代，现在TensorFLow 2.x出现有一段时间，
然后该API迁移工作并没有完成，所有不能使用TensorFlow 2.x的代码，具体安装步骤如下：

#### 前提准备
硬件
```
x86 Linux Ubuntu 18.04.1
GeForce GTX 1050 Ti (4G Memory)
```

软件
```
NVIDIA Driver:  430
CUDA Version:   10.0
cuDNN Version:  7_7.6.5.32 for CUDA 10.0
tensorflow-gpu: 1.15.2
protobuf:       3.0.0
python:         3.7.5
```

TensorFlow api使用的版本为`1.15.2`，准备完毕后进行安装阶段，另外CUDA与cuDNN的安装和配置请参考[CUDA_Install_Guide.md](./CUDA_Install_Guide.md)
> cuda-repo-ubuntu1804-10-0-local-10.0.130-410.48_1.0-1_amd64.deb | libcudnn7_7.6.5.32-1+cuda10.0_amd64.deb

#### 框架安装与配置
下载源码
```shell script
cd ~
git clone https://github.com/tensorflow/models.git
mv models tensorflow_api
```

安装框架必要依赖
```shell script
sudo apt install protobuf-compiler python-pil python-lxml python-tk -y
pip3 install Cython contextlib2 jupyter matplotlib pillow lxml tensorboard
```

下载coco API 并安装
```shell script
cd ~
git clone https://github.com/cocodataset/cocoapi.git
cd cocoapi/PythonAPI
vim Makefile  # 将 python修改为 python3
make
ln -s pycocotools ~/tensorflow_api/research
```

编译Protobuf文件
```commandline
cd ~/tensorflow_api/research
protoc object_detection/protos/*.proto --python_out=.
```
> linux 下安装protoc可以从[官网](https://github.com/protocolbuffers/protobuf)下载二进制可执行文件，放到`/usr/local/bin`，
> 执行`protoc --version`显示`libprotoc 3.0.0`表示成功，在执行编译

添加库到环境变量
```shell script
vim ~/.profile
export PYTHONPATH=$PYTHONPATH:/home/afterloe/tensorflow_api/research:tensorflow_api/research/slim
```

测试安装
```commandline
cd ~/tensorflow_api/research
python3 object_detection/builders/model_builder_test.py
```
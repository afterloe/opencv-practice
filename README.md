Python3 & OpenCV4 & TensorFlow2 & TensorFlow API
===

> create by [afterloe](605728727@qq.com)  
> version is 2.1  
> MIT License    

机器视觉+深度学习的研究型项目

## 目录结构说明
```
Project
 -- computer_version          # OpenCV的一些应用示例
 -- deep_learning             # 图像识别与Tensorflow的一些示示例
 -- docs                      # 文档，图例等资源
 -- equipment_engineering     # 项目工程化的示例及说明
 -- gui                       # 桌面编程的例子，考虑切换为QT
 -- tried_unknow              # 尝试的代码，没什么意义
 -- cv_workshops              # OpenCV的基础知识点与笔记
 -- tf_aip_workshops          # TensorFlow api 学习
```

<a href="blog">博客</a>
<a href="#note">机器视觉(Computer Vision)笔记</a>  
<a href="#deeplearn">深度学习笔记</a>
<a href="#backup">备忘录</a>  

## 博客
 - [CUDA安装手册](./docs/CUDA_Install_Guide.md)
 - [OpenCV安装手册](./docs/CV_Install_Gudie.md)
 - [Windows下pip3安装手册](./docs/PIP_On_Windows_Install_Guide.md)
 - [Python3.6安装手册](./docs/Python36_Install_Guide.md)
 - [Shadowsockes ssr安装手册](./docs/Shadowsocks_Install_Guide.md)
 - [TensorFlow 安装手册](./docs/TensorFlow_Install_Gudie.md)
 - [TensorFlow API 安装手册](./docs/TensorFlow_API_Install_Guide.md)
 - [TensorFlow API 使用手册 - 本地训练模型](./docs/TensorFlow_API_Run_Local_Guide.md)

#### python3 & opencv4 的参考内容
python3 开发规范，参考自[PEP8标准](https://www.cnblogs.com/rrh4869/p/11177785.html)  
opencv4 使用版本为4.1.1，相关[开发文档](https://docs.opencv.org/4.1.1/)

## <a id="note">OpenCV 笔记</a>

[全十四节笔记](./workshops/SUMMARY.md)  
[第一节 - OpenCV基础操作](./workshops/1-day/summary.md)  
[第二节 - 图像处理相关操作](./workshops/2-day/summary.md)      
[第三节 - 图像卷积相关操作](./workshops/3-day/summary.md)  
[第四节 - 图像卷积相关操作（进阶）](./workshops/4-day/summary.md)  
[第五节 - 二值图像分析](./workshops/5-day/summary.md)  
[第六节 - 二值图像分析（进阶）](./workshops/6-day/summary.md)  
[第七节 - 图像形态学分析](./workshops/7-day/summary.md)    
[第八节 - 综合运用与技能回顾](./workshops/8-day/summary.md)  
[第九节 - 视频综合分析](./workshops/9-section/summary.md)  
[第十节 - 对象检测与特征提取](./workshops/10-section/summary.md)  
[第十一节 - KNN的相关技巧](./workshops/11-section/summary.md)  
[第十二节 - OpenCV模型与对象检测](./workshops/12-section/summary.md)  
[第十三节 - OpenCV模型组合与TensorFlow](./workshops/13-section/summary.md)  


## <a name="deeplearn">深度学习</a>


#### nvidia 相关内容

* TensorRT - [Download](https://developer.nvidia.com/rdp/form/tensorrt-7-survey)  | [HomePage](https://developer.nvidia.com/tensorrt) | [Document](https://docs.nvidia.com/deeplearning/sdk/tensorrt-archived/index.html) | [Guide](https://docs.nvidia.com/deeplearning/sdk/tensorrt-install-guide/index.html#overview) | [Code](https://github.com/NVIDIA/TensorRT) | [For Python](https://docs.nvidia.com/deeplearning/sdk/tensorrt-developer-guide/index.html#importing_trt_python)
* CUPTI - [Document](https://docs.nvidia.com/cupti/Cupti/index.html)
* CUDA - [Download](https://developer.nvidia.com/cuda-10.1-download-archive-base?target_os=Windows&target_arch=x86_64&target_version=10&target_type=exelocal)
* cuDNN - [Download](https://developer.nvidia.com/rdp/cudnn-download)
* Nvidia Driver - [Download](https://www.nvidia.com/download/index.aspx?lang=en-us)
* Jetson-inferenc - [Code](https://github.com/dusty-nv/jetson-inference)
* Jetson Zoo - [Guide](https://elinux.org/Jetson_Zoo)
* Nvidia developer - [Blog](https://devblogs.nvidia.com/speed-up-inference-tensorrt/) | [HomePage](https://developer.nvidia.com/)


## <a name="backup">备忘录</a>

#### 关于git提交的type
根据 Header的内容及描述，type共分为以下8类：
```
feat：新功能（feature）
fix：修补bug
docs：文档（documentation）
style： 格式（不影响代码运行的变动）
refactor：重构（即不是新增功能，也不是修改bug的代码变动）
test：增加测试
chore：构建过程或辅助工具的变动
resources: 资源修改
```

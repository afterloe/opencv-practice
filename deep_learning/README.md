Computer Version With deep learning
===
> create by [afterloe](605728727@qq.com)  
> version is 1.0.3  
> MIT License

##### 检测CUDA及cuDNN模块环境准备
```shell script
& D:\python3\python.exe
>> from tensorflow.python.client import device_lib as _device_lib
>> local_device_protos = _device_lib.list_local_devices()
>> [x.name for x in local_device_protos if x.device_type == 'GPU']
```
> 执行以上内容输出当前可用的GPU列表

##### MiniVGGNet
MiniVGGNet由两套CONV => RELU => CONV => RELU = >池组成
层，后面是一组FC => RELU => FC => 软最大层。前两层CONV
将学习32个过滤器，每个3×3大小。后两个CONV层将学习64个过滤器，同样，每个
尺寸为3×3。我们的POOL图层将在2×2的窗口内以2×2的步幅执行最大池化




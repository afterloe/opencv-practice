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


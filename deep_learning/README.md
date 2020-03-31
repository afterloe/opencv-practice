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

##### LeNet
图层传递: INPUT => CONV => TANH => POOL => CONV => TANH => POOL => FC => TANH => FC

 | 图层类型 | 卷积层大小 | 过滤大小
 | :----- | :--------- | :----
 | Input Image | 28 * 28 * 1 | 
 | CONV | 28×28×20 | 5×5,K = 20
 | ACT | 28×28×20
 | POOL | 14×14×20 | 2×2
 | CONV | 14×14×50 | 5×5,K = 50
 | ACT | 14×14×50
 | POOL | 7×7×50 | 2×2
 | FC | 500
 | ACT | 500
 | FC | 10
 | SOFTMAX | 10

##### MiniVGGNet
由两套 CONV => RELU => CONV => RELU => POOL组成
, 后面是一组FC => RELU => FC => 软最大层。前两层CONV将用32个过滤器，每个3×3大小, 后两个CONV层将用64个过滤器，
同样，每个尺寸为3×3。POOL层在2×2的窗口内以2×2的步幅执行最大池化

 | 图层类型 | 卷积层大小 | 过滤大小
 | :----- | :--------- | :----
 | INPUT IMAGE | 32×32×3 |
 | CONV | 32×32×32 | 3×3,K = 32
 | ACT | 32×32×32
 | BN | 32×32×32
 | CONV | 32×32×32 | 3×3,K = 32
 | ACT | 32×32×32
 | BN | 32×32×32
 | POOL | 16×16×32 | 2×2
 | DROPOUT | 16×16×32
 | CONV | 16×16×64 | 3×3,K = 64
 | ACT | 16×16×64
 | BN | 16×16×64
 | CONV | 16×16×64 | 3×3,K = 64
 | ACT | 16×16×64
 | BN | 16×16×64
 | POOL | 8×8×64 | 2×2
 | DROPOUT | 8×8×64
 | FC | 512 |
 | ACT | 512 |
 | BN | 512 |
 | DROPOUT | 512 |
 | FC | 10 |
 | SOFTMAX | 10 | 


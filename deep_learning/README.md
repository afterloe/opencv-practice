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

> 提升准确率的tip  
> 1.批处理规范化可以导致更快、更稳定和更高精度的收敛。   
> 2.需要更多的次数来训练网络，使网络将获得更高的准确性

##### AlexNet
| 图层类型 | 卷积层大小 | 过滤大小
| :----- | :--------- | :----
| INPUT IMAGE | 227×227×3
| CONV | 55×55×96 | 11×11/4×4,K = 96
| ACT | 55×55×96
| BN | 55×55×96
| POOL | 27×27×96 | 3×3/2×2
| DROPOUT | 27×27×96
| CONV | 27×27×256 5×5,K = 256
| ACT | 27×27×256
| BN | 27×27×256
| POOL | 13×13×256 | 3×3/2×2
| DROPOUT | 13×13×256
| CONV | 13×13×384 3×3,K = 384
| ACT | 13×13×384
| BN | 13×13×384
| CONV | 13×13×384 | 3×3,K = 384
| ACT | 13×13×384
| BN | 13×13×384
| CONV | 13×13×256 | 3×3,K = 256
| ACT | 13×13×256
| BN | 13×13×256
| POOL | 13×13×256 | 3×3/2×2
| DROPOUT | 6×6×256
| FC | 4096
| ACT | 4096
| BN | 4096
| DROPOUT | 4096
| FC | 4096
| ACT | 4096
| BN | 4096
| DROPOUT | 4096
| FC | 1000
| SOFTMAX | 1000
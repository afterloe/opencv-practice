预训练与模型微调
===

> create by [afterloe](605728727@qq.com)  
> version is 1.0  
> MIT License


#### 概念
在既有检查点文件载入已有模型可以实现覆盖已有模型进行二次开发，这种二次开发的技巧被成为**微调**

https://github.com/aianaconda/TensorFlow_Engineering_Implementation/blob/master/code/5-2%20%20model.py

#### 训练模型

```shell script
python3 train.py -m ~/data/afterloe\ resources/models/nasnet-a_mobile_04_10_2017/model.ckpt -t ~/data/afterloe\ resources/animal/train -e ~/data/afterloe\ resources/animal/val
```

#### 测试模型
```shell script
python3 test.py -d /mount/data/afterloe\ resources/animal/train -e /mount/data/afterloe\ resources/animal/train
```
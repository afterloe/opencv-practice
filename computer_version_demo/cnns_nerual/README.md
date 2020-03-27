# CNNs Neural Networks

> create by [afterloe](605728727@qq.com)  
> version is 1.0.4  
> MIT License  

##### CNNs网络实践  
使用Keras和深度学习训练卷积神经网络，以识别和分类指定图像
![VGGNet](../../docs/illustrations/cnn_keras_smallervggnet.png)
> 图一： 所使用的模型示意图

总共分为四层，其特点是， 仅使用3×3卷积层，以越来越大的深度堆叠在一起并通过最大池化来减少卷大小。

##### 训练
```shell script
Using TensorFlow backend.
2020-03-24 22:48:02.663290: I tensorflow/stream_executor/platform/default/dso_loader.cc:44] Successfully opened dynamic library cudart64_101.dll
[Tue, 24 Mar 2020 22:48:06][train.py][INFO] - 模型训练工具 1.0.5
usage: train.py [-h] -d DATASET -m MODEL -l LABELBIN [-p PLOT]

optional arguments:
  -h, --help            show this help message and exit
  -d DATASET, --dataset DATASET
                        图像集路径
  -m MODEL, --model MODEL
                        模型输出路径
  -l LABELBIN, --labelbin LABELBIN
                        标签二进制文件输出路径
  -p PLOT, --plot PLOT  输出训练曲线

& 'D:\Program Files\Python37-64\python.exe' .\train.py -d .\resources\ -m pokedex.model -l lb.pickle
```
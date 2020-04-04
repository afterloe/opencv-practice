KNN 图像分类
===
> create by [afterloe](605728727@qq.com)  
> version is 1.0.2  
> MIT License

##### 训练
```shell script
PS G:\Project\py3\deep_learning\first_image_classifier> & 'D:\Program Files\Python37-64\python.exe' .\knn.py -d 'G:\afterloe resources\animal\'
[Sat, 28 Mar 2020 15:38:53][knn.py][INFO] - 第一个knn练习 1.0.0
[Sat, 28 Mar 2020 15:38:53][knn.py][INFO] - 加载图像数据
[Sat, 28 Mar 2020 15:38:55][simple_dataset_loader.py][INFO] - 处理中 ... 500 / 878
[Sat, 28 Mar 2020 15:38:56][knn.py][INFO] - 特征点: 2.6MB
[Sat, 28 Mar 2020 15:38:56][knn.py][INFO] - knn 分类
[Sat, 28 Mar 2020 15:38:56][knn.py][INFO] - 结果如下:
              precision    recall  f1-score   support

         cat       0.48      0.68      0.56        80
         dog       0.37      0.39      0.38        76
       panda       0.88      0.36      0.51        64

    accuracy                           0.49       220
   macro avg       0.58      0.48      0.48       220
weighted avg       0.56      0.49      0.48       220

```
> precision: 准确性  

“panda”有88%的准确性，可能是因为大熊猫大部分是黑色和
白色，因此这些图像在我们的3072（32 * 32 * 3）的空间中更紧密相连。  
狗和猫的分类准确率分别为37%和48%。
这些结果可以归因于这样一个y原因：狗和猫的皮毛颜色非常相似，故皮毛的颜色和斑点的颜色不能用于区别它们。
而且背景噪声（如后院的草、沙发颜色等）也可能产生“混淆”。  
由于k-NN算法无法学习这些物种之间的任何区别，这个是k-NN算法的主要缺点之一：虽然它很简单，但它
无法从数据中学习。

##### 总结
k-NN算法的一个主要优点时它的实现和理解非常简单，完全不需要时间来训练，他是使用内存进存储特征数据，以便于其他数据直接使用和推断。
这些数据特征点按0(N)的比例变化，进行线性回归，但是在大型数据的处理上还是欠缺很多的。使用k-NN算法是以空间/时间复杂性交换最近相邻
点的正确性。  
k-NN算法更加适合低纬度的特征空间
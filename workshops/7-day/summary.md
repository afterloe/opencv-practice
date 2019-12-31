# 图像形态学分析
> create by [afterloe](605728727@qq.com)  
> version is 1.3  
> MIT License  

常用的图像二值化方法归结如下：
 - inRange 获取mask【颜色分割】
 - canny【边缘轮廓提取】
 - threshold【阈值分割, 设定阈值、自动阈值】
 - adaptiveThreshold【自适应阈值分割】

图像形态学分析与图像的色彩、光照、摄像设备无关，与物体结构有关，所以该类分析更多的是在边缘、轮廓等处理上。

## [图像的膨胀与腐蚀](./1-clazz.py)
图像的膨胀与腐蚀是形态学中的两个最基本的操作，opencv中膨胀与腐蚀均有特定的api来实现。简单而言，膨胀可以看成最
大值滤波，即使用八领域或四领域中像素最高值与中心点进行替换；而腐蚀可以看做是最小值滤波，原理同上。其实，在膨
胀与腐蚀中的kernel指的并不是卷积核，他应该被成为结构元素，也就是说可以使用非矩形的卷积操作。具体的api如下：
```
    膨胀 cv.dilate(src, kernel, anchor, iterations)
        - src: 灰度图相关或bgr图像均可
        - kernel: 结构元素
        - anchor: 中心像素点
        - iterator: default 1， 循环次数

    腐蚀 cv.erode(src, kernel, anchor, iterations)
        - 同上
```

注：也可使用`cv.morphologyEx`进行，option指定`cv.DILATE`进行。

## [结构元素的运用](./2-clazz.py)
图像形态学操作不仅可以对二值图像操作，也可以对灰度图像与彩色图像进行操作。对于二值图像的膨胀与腐蚀而言，选择一个好的结构元素是至
关重要的，Opencv中关于结构元素的获取有一个api，具体如下：
```
        cv.getStructuringElement(shape, ksize, anchor)
            - shape: 结构元素的形状，常用的有矩形、圆形、十字交叉
            - ksize: 结构元素的大小
            - anchor: 结构元素的中心像素点的位置
```
常用的结构元素枚举
```
cv.MORPH_RECT      矩形
cv.MORPH_ELLIPSE   圆形
cv.MORPH_CROSS     十字交叉
```
注:在二值图像中，膨胀可以将二值图像的轮廓进行扩充，实现两个连通组件因为某些像素中断导致的组件分离。而腐蚀刚好相反。

## 图像的开闭操作
开操作 = 腐蚀 + 膨胀    
opencv关于形态学操作进行了封装，所有的形态学操作可使用一个api进行，即
```
cv.morphologyEx(src, option, kernel, anchor, iterations)
            - src: 任意输入图像，可以为灰度、彩色或二值
            - option: 形态学操作的枚举
            - kernel: 结构元素 或 卷积核
            - anchor: 结构元素或卷积核的中心像素点坐标
            - iterations: 形态学操作的次数
```
关于开操作可以理解如下，先对图像进行腐蚀操作，之后对腐蚀的结果进行膨胀。可以删除二值图像中的干扰快，降低图像二值化之后噪点过多的
问题，在api中，它的枚举为`cv.MORPH_OPEN`。[代码在这](./3-clazz.py)    

闭操作 = 膨胀 + 腐蚀  
与开操作的相对应的是闭操作，闭操作是先膨胀，再腐蚀，用于填充图像中缺少的二值区域即中心孔洞填充，形成完整的闭合区域连通组件，使用
同样的api进行操作，闭操作的option枚举是`cv.MORPH_CLOSE`。[代码在这](./4-clazz.py)    
注： 在进行开闭操作时，根据结构元素的不同实现不同的二值图像处理效果，其中使提取二值图像中水平与垂直线比霍夫直线检测要好得多
以下是开闭操作的[练习代码](./5-clazz.py)

## 顶帽操作与黑帽操作
顶帽操作 = 原图 - 开操作    
用于提取图像中细微的部分，由于开操作是先腐蚀，再膨胀，去除了细微部分的变化，使用原图减去开操作的结果，可以获得被去除了的细微部分
的像素，同样使用 morphologyEx进行操作，option枚举为 `MORPH_TOPHAT`。[代码在这](./6-clazz.py)    

黑帽操作 = 闭操作 - 原图    
闭操作是先膨胀，再腐蚀，填充因为某些原因导致的像素断层，而黑帽操作在此基础上将结果减去原图像，可获得修复的结果。黑帽操作常用于工
业上细小零件、组件的边缘提取与分析，使用morphologyEx进行操作，option枚举是`MORPH_BLACKHAT`。[代码在这](./7-clazz.py)

## [图像梯度分析](./8-clazz.py)
形态学分析可以忽略颜色、光照的效果，提取连通组件的边缘与轮廓，根据形态学操作的不同，形态学梯度分为以下几种:
            基本梯度： 原理为膨胀减腐蚀之间的差值, opencv中morphologyEx操作，option枚举 MORPH_GRADIENT
            内梯度： 原理为输入图像与腐蚀之间的差值，opencv中并没有实现，需要自己编码
            外梯度： 原理为膨胀与输入图像之间的差值，opencv中并没有实现，需要自己编码

```
# 内梯度计算方法 输入图像 与 腐蚀图像的差值
kernel = cv.getStructuringElement(cv.MORPH_RECT, (3, 3))
binary = cv.erode(src, kernel)
dst = cv.subtract(src, binary)

# 外梯度计算方法 膨胀图像 与 输入图像的差值
kernel = cv.getStructuringElement(cv.MORPH_RECT, (3, 3))
binary = cv.dilate(src, kernel)
dst = cv.subtract(binary, src)
```

## [使用基本梯度对轮廓边缘进行分析](./9-clazz.py)
使用形态学的二值化处理，对是别内容进行轮廓分析，在OCR上是其处理的手段之一，相比于threshold的二值化而言，对图像会有更好的分割效
果，技术路线如下:    
1 图像形态学梯度    
2 灰度    
3 全局阈值二值化    
4 轮廓分析    

## [hit&miss 运用](./10-clazz.py)
hit&miss操作指的是结构元素对二值图像进行过滤，若领域内的图像符合结构元素描述则保留，若不符合结构元素描述则过滤，可以用于断面检
测，组件连通状态检测等内容，同样使用morphologyEx进行，option为 `MORPH_HITMISS`

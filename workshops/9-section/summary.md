# 视频综合分析
> create by [afterloe](605728727@qq.com)  
> version is 1.3  
> MIT License  

本节会运用之前的知识点，进行综合运用，实现对视频的角点特征分析、shi-tomas角点检测、亚像素级别角点检测、KLT光流分析、帧差版本的移动
对象分析、均值迁移的对象分析及移动对象的轨迹绘制

## [角点特征分析](./1-clazz.py)
角点检测常用于工业仪表分析中提取指针、仪表的明显特征，对于一介倒数而言，角点在各方向的变化是最大的，而边缘区域只有在某一方向具有
明显变化，后续的特征提取均布CNN替换，该示例仅作为示例进行。相关api描述如下：
```
        cv.cornerHarris(gary, blockSize, aperture_size, k)
            - gray: 单通道图像，可以是float、int32、int0等
            - blockSize: 计算方差矩阵的相邻域像素大小
            - aperture_size: soble算子大小(梯度算法 的卷积核)
            - k: 表示系数，经验值 0.04 ~ 0.06
```

## [shi-tomas 角点检测](./2-clazz.py)
harris角点检测算法计算速度慢，很难实时计算，最常用的角点检测算法是shi-tomas，opencv中相关API描述如下：
```
     cv.goodFeaturesToTrack(gray, maxCorners, qualityLevel, minDistance [, mask, blockSize, useHarrisDetector, k])
        - gray: 单通道图像，dtype可以为int32、int32、float32等
        - maxCorners: 最多返回多少个角点
        - qualityLevel: 丢弃阈值， 关键点R < qualityLevel * max_response则会被放弃运算，经验值0.05
        - minDistance: 两个关键点之间的最短距离

        可选参数
        - mask: 做角点检测的mask区域，传入表示只在该区域内做角点检测
        - blockSize: 梯度与微积分的开窗区域
        - useHarrisDetector: 是否使用harris角点检测， bool，默认为false
        - k: 启动harris检测时才有用，表示soble算子系数，默认是 0.04， 经验值 0.04 ~ 0.06
```

## [角点检测 - 亚像素级别角点检测](./3-clazz.py)
角点检测用于物体特征提取与特征匹配，但由于角点检测的结果不够精准，因为真实的计算中有些位置可能实在浮点数空间才是最大值，而通过像
素领域空间进行拟合，实现亚像素级别的焦点检测。相关opencv的api如下：
```
    cv.cornerSubPix(gray, corners, win_size, zero_zone, criteria)
        - gray： 单通道图像，dtype可以为int32、int0、float32等
        - corners： 角点
        - win_size： 差值计算时窗口大小
        - zero_zone： 窗口中间的边长的一半，可以用于避免相关矩阵的奇异性，如果设置为(-1, -1)则表示没有这个区域
        - criteria： 角点精准化迭代过程的终止条件
```

## KLT光流跟踪
### [KLT光流跟踪算法](./4-clazz.py)
光流跟踪算法分为稠密光流跟踪与稀疏光流跟踪两种，而KLT属于稀疏光流跟踪算法，该算法工作需要3个假设的前提条件**一是亮度恒定，即光照条件
不会频繁变动；而是短距离移动，即物体移动幅度不大，不会出现超长距离的快速移动；三是空间一致性，由于KLT算法默认左上角为坐标轴(0, 0)的起点，
摄像头角度不会进行变动，否则结果会出现大面积的偏差**，有关KLT光流跟踪算法的api描述如下：
```
    cv.calcOpticalFlowPyrLK(prevImg, nextImg, prevPts, nextPts [, status=None, err=None, winSize=None, maxLevel=None,
                            criteria=None, flags=None, minEigThreshold=None])
        - prevImg: 前一张单通道灰度图像，dtype可以为int32、int0或float32等
        - nextImg: 当前的单通道灰度图像，dtype可以为int32、int0或float32等
        - prevPts: 前一张图像中的角点
        - nextPts: 当前图像中的光流点；若为None，则作为输出参数

        可选参数
        - status: 输出状态，1表示正常改点保留，否则舍弃；若为None，则作为输出参数
        - err: 错误信息；若为None，则作为输出参数
        - winSize: 光流算法对象的开窗大小
        - maxLevel: 金字塔层数，0表示只检测当前图像，不构建金字塔
        - criteria: 光流算法停止条件

    eg: nextPts, status, err = cv.calcOpticalFlowPyrLK(**param)
```
本次使用了python3的dict的API，dict(): python3的基本数据类型，类似于map，采用key-value存储，支持for循环，使用 `**` 开头可用于函数参数解构

随机颜色    
```
numpy.random.randint(low, high=None, size=None, dtype='l')
size: int or tuple of ints(可选)
```
输出随机数的尺寸，比如size = (m * n* k)则输出同规模即m * n* k个随机数。默认是None的，仅仅返回满足要求的单一随机数。输入内容`output -> array([0, 0, 2], [10, 20, 33] ...)`

跟踪线绘制的要点  
`enumerate()` 函数用于将一个可遍历的数据对象(如列表、元组或字符串)组合为一个索引序列，同时列出数据和数据下标，一般用在 for 循环当中  
`zip()` 函数用于将可迭代的对象作为参数，将对象中对应的元素打包成一个个元组，然后返回由这些元组组成的对象，这样做的好处是节约了不少的内存。
注: 一般用于两个以上的参数循环

数组转换  
`ravel()`  函数实现将多维数组 转换为 一维数组


### [KLT光流跟踪算法](./5-clazz.py)去除禁止点
静止点删除与跟踪轨迹绘制。处置流程为 输入第一帧图像 -> 特征点检测 -> 保持特征点 -> 输入第二帧图像（开始跟踪） -> 跟踪特征点 -> 删除
损失特征点 -> 保存跟踪特征点 -> 用第二帧图像替换第一帧图像 -> 用后续输入帧替换第二帧 -> 选择新的特征点替换损失的特征点 -> 保存特征点数据
并回到输入第二帧图像，开始循环。

```
    import match

    width = math.pow(abs(a - c), 2)
    height = math.pow(abs(b - d), 2)
```

## [稠密光流分析](./6-clazz.py)
光流分析分稀疏与稠密两种，在opencv 4.0后Opencv支持两种稠密光流计算方法, KLT属于稀疏分析的一种。相关api如下
```
    cv.calcOpticalFlowFarneback(prev, next, flow, pyr_scale, levels, winsize, iterations, poly_n, poly_sigma, flags)
        - prev: 前一帧的灰度图像
        - next: 当前帧的灰度图像
        - flow: 输出的光流
        - pyr_scale: 金字塔缩放比率
        - levels: 金字塔层数
        - winszie: 开窗计算的窗口大小
        - iterations: 迭代计算的次数
        - poly_n: 生成光流时，对领域像素的多项展开，n越大越模糊，越稳定
        - poly_sigma: 高斯系数，和n成正相关，当n增大时，sigma对应增大
        - flags: OPTFLOW_USE_INITIAL_FLOW 盒子模糊进行光流初始化
                 OPTFLOW_FARNEBACK_GAUSSIAN 高斯模糊
```
注: `mag, ang = cv.cartToPolar(flow[..., 0], flow[..., 1])`  空间坐标系转换，将hsv中h、s通道转换

## [基于帧差法实现移动对象分析](./7-clazz.py)
 光流跟踪与背景消除都是基于建模(KNN、高斯)的方式进行的，其实，有一种原始的方式较移动分析更为有效，这就是基于帧差法实现
移动对象分析，在监控或固定视角效果明显，帧差法进一步划分可以分为两帧差与三帧差，具体描述如下：
```
两帧差： diff = frame - prev，即当前帧减前一帧
三帧差： diff_1 = prev_2 - prev_1; diff_2 = frame - prev_1
        diff = diff_1 & diff_2
```
帧差法在求取帧差之前进行高斯模糊，可用于降低干扰，通过得到的diff图像进行形态学操作，用于合并与候选区域，提升效率。但帧差
法的缺点如下：一是高斯模糊是高耗时的计算，越模糊效果越好，但耗时越长；二是该方法容易受到噪声与光线干扰。

## 基于均值迁移的对象移动分析
### [非连续](./8-clazz.py)
均值迁移移动对象分析主要是基于ROI区域颜色直方图分布与反向投影实现的，其核心思想是对反向投影后的图像作均值迁移（meanshift）
从而发现密度最高的区域，算法流程如下：
```
        1 读取图像一帧
        2 绘制HSV直方图
        3 反向投影该帧
        4 使用meanshift算法寻找最大分布密度
```
相关api如下:
```
    cv.meanShift(probImage, window, criteria)
        - probImage: 直方图反向投影的结果
        - window： 搜索窗口， ROI对象区域
        - criteria： 均值迁移停止条件
```

### [连续自适应迁移CAM](./9-clazz.py)
CAM是连续自适应的均值迁移跟踪算法，相对于均值迁移相比较他的主要改进点有两处，一是会根据跟踪对象大小变化自动
调整搜索窗口大小；二是会返回更为完整的位置信息，其中包括了位置坐标及角度, 相关api如下:
```
cv.CamShift(probImage, window, criteria)
        - probImage: 输入图像，直方图方向投影结果
        - window: 搜索开窗大小，ROI对象区域
        - criteria: 均值迁移停止条件
```
注: 返回信息中需要手动更新开窗信息


## [移动对象的轨迹绘制](./10-clazz.py)
通过对移动对象进行连续自适应均值分析后，对返回的内容获取中心坐标点，并将中心坐标点放入点阵集合，通过点阵集合绘制其运动路径。大致
步骤如下：
```
        1 初始化路径点集
        2 对每帧的轮廓进行中心化坐标提取
        3 添加坐标到点集的最后位置
        4 绘制路径曲线
```

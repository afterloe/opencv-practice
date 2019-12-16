# 二值图像分析操作总结
> create by [afterloe](605728727@qq.com)  
> version 1.10  
> MIT License  

本章主要描述了二值图像的基础操作与基础分析，涵盖了4种不同类型的二值化阈值的检索算法、组件搜寻、轮廓绘制、组件过滤等，并
与第四章的canny算法进行联动，实现组件轮廓的最小矩形与外接矩形绘制。

## [基础阈值操作，实现二值化](./1-clazz.py)
opencv中的基本阈值操作：
假设已有合适的阈值T，对其进行二值操作可以看成为一种阈值化操作。opencv中的阈值操作API如下。
```
        (double, dst) cv.threshold(src, dst, thresh, maxval, type)
            - thresh: 阈值
            - maxval: 像素二值操作最大值
            - type： 二值操作的方法

        type
            - THRESH_BINARY = 0         二值分割
            - THRESH_BINARY_INV = 1     反向二值分割
            - THRESH_TRUNC = 2          截断  (黑白图)
            - THRESH_TOZERO = 3         取零  (效果同0)
            - THRESH_TOZERO_INV = 4     反向取零
```
前期使用`cv.mean`对图片获取直方图均值，并使用该值进行二值化

## [双峰图像的二值阈值搜寻算法 - OTSU](./2-clazz.py)
OTSU算法适合对直方图具有两个峰的图像，对于只有一个峰的图像，该算法的阈值获取并不是十分理想。
在cv.threshold中使用将type指定为 THRESH_OTSU即可
注意: `cv.threshold`的type为`cv.THRESH_BINARY | cv.THRESH_OTSU`，不输入THRESH_BINARY 可不会进行二值化操作

## [单峰图像的二值阈值搜寻算法 - TRIANGLE](./3-clazz.py)
单峰直方图的波峰与直方图顶部连线，并绘制直接三角形，在三角形上算出高，并将高的位置平移已确定阀值。opencv实现过
程中将单峰直方图进行取反操作（即不用担心波峰离0或255过于接近而导致阈值不准确的问题）,使用时在threshold中将type指定
为THRESH_TRIANGLE即可。 该方法对双峰直方图效果表示并不是很好

## [不均匀光照的二值阈值搜寻算法 - 自适应阈值](./4-clazz.py)
自适应阈值算法适合光照不均匀的图像进行阈值判断，通过均值模糊或 高斯模糊将图像进行光照均匀操作，再使用原图减去
模糊的结果得到插值图像再进行自适应分割。
```
cv.adaptiveThreshold(src, maxValue, adaptiveMethod, thresholdType, blockSize, C, dst)
        - maxValue: 二值化最大值
        - adaptiveMethod: 模糊方法  ADAPTIVE_THRESH_GAUSSIAN_C = 1 高斯; ADAPTIVE_THRESH_MEAN_C = 0 均值
        - thresholdType: 二值操作   THRESH_BINARY       二值图像 = 原图 – 均值图像 > -C ? 255 : 0
                                    THRESH_BINARY_INV   二值图像 = 原图 – 均值图像 > -C ? 0 : 255
        - blockSize: 卷积窗口（经验值: 25）,大的图像可以调整为127进行快速处理
        - C: 均匀阀值，不必设置太大，一般10、15左右
```

## 连通组件搜寻、状态统计
  [这里](./5-clazz.py)为图像降噪与二值化对比，不过注意的是**降噪要在图像灰度转换之前**。
### [连通组件搜寻](./6-clazz.py)

连通组件标记算法是图像分析中最常用的算法之一， 原理是扫描二值图像的每个像素点，对于像素值相同且相互连通的分为一个组，
最终得到图像中所有的像素连通组件。扫描的方式是从上到下，从左到右。最大联通组件个数为N/2，其中N表示图像的总像素个数；
该算法在调用时，必须保证背景像素是黑色，前景像素是白色。最常见的连通组件扫描的有以下两类：
    - 一步法： 基于图的搜索算法
    - 两步法： 基于扫描与等价类合并算法

```
cv.connectedComponents(binary, labels, connectivity, ltype)
        - binary: 输入二值图像， 黑色背景
        - labels: 输出的标记图像，背景index为0
        - connectivity: 连通域， 如8领域、4领域； 默认是8领域
        - ltype: 输出的labels类型，默认是CV_32S
```

### [连通组件状态统计](./7-clazz.py)
opencv中有关联通组件还有一个是携带其状态的api，`cv.connectedComponentsWithStats`， 使用该函数能够输出联通组件的统计情况。
```
        cv.connectedComponentsWithStats(binary, labels, status, centroids, connectivity, ltype, ccltype)
            - binary: 输入的二值图
            - labels: 输出的组件
            - status: 组件状态
            - centroids: 各组件的中心坐标
            - ltype: 组件类型
            - ccltype:

        CC_STAT_LEFT:   连通组件外接矩形左上角坐标的X位置
        CC_STAT_TOP:    连通组件外接左上角坐标的Y位置
        CC_STAT_WIDTH:  连通组件外接矩形的宽度
        CC_STAT_HEIGHT: 连通组件外接矩形的高度
        CC_STAT_AREA:   连通组件的面积大小
```

## [组件的轮廓发现与轮廓绘制](./8-clazz.py)
通过图像连通组件的分析后获取基于二值图像的每个连通组件，通过对应的点连接获取各组件的之间的层次关系与几何拓扑关系，使用opencv
的api 以发现连通组件间的轮廓。
```
        轮廓发现
        contours, hierarchy = cv.findContours(binary, mode, method[, contours[, hierarchy[, offset]]])
            in
            - binary: 二值图
            - mode: 轮廓寻早的拓扑结构返回模式，RETR_EXTERNAL 只返回最外层轮廓；RETR_TREE 返回轮廓树结构
            - method: 轮廓点吉和算法，常见的是基于CHAIN_APPROX_SIMPLE链式编码方法
            - offset: 表示偏移缩放量
            out
            - contours: 轮廓点集合
            - hierarchy: 每个轮廓的四个相关信息，分别是同层下一个轮廓索引、同层上一个轮廓索引、下层第一个子索引、上层父轮廓索引

        轮廓绘制
        image = cv.drawContours(dst, contours, contourIdx, color[, thickness[, lineType[, hierarchy[, maxLevel[, offset]]]]])
            - dst: 绘制的底图, 目标图像
            - contours: 轮廓集
            - contourIdx: > 0 绘制该轮廓， -1 绘制子所有轮廓
            - thickness: 轮廓线厚度，> 0 绘制轮廓， < 0 填充
```

## [Canny算法结合连通组件实现目标外接矩形与最小矩形绘制](./9-clazz.py)
轮廓外接矩形分为最大外接矩形与最小外接矩形两种，使用这种方法可以将物体的轮廓剪切下来并发送到对应的识别软件进行处理。不过需要
注意的是在使用外接矩形的时候不推荐进行二值化操作，因为容易将深颜色的物体过滤掉。应使用形态学操作进行二值化处理。
```
        外接矩形API
        rect = cv.boundingRect(gray)
            - gray: 灰度图像或2D点阵数组
            - rect: 返回矩形轮廓x, y, w, h

        最小外接矩形
        angle, center, size = cv.minAreaRect(points)
            - points: 点阵集
```

形态学操作
```
    k = np.ones((3, 3), dtype=np.uint8)
    binary = cv.morphologyEx(binary, cv.MORPH_DILATE, k)  # cv形态学操作
```

注意：Canndy算法的高低阈值相差最多为2倍，否则在形态学操作上无法获取对应的轮廓.

## [基于矩形面积、弧长实现目标过滤](./10-clazz.py)
通过计算轮廓的矩形与弧长，可以设定某个阈值实现ROI区域的过滤。
```
        轮廓点集的面积计算函数
        cv.contourArea(contour, oriented)
            - contour: 轮廓点集
            - oriented: boolean - default False， False -> 返回面积为正数； True -> 表示根据顺时针或逆时针返回正值或负值的面积

        轮廓点集的弧长计算函数
        cv.arcLength(curve, closed)
            - curve: 轮廓点集
            - closed: boolean， False -> 不闭合； True -> 闭合
```

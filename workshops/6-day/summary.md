# 二值图像分析操作(进阶)总结
> create by [afterloe](605728727@qq.com)  
> version 1.3    
> MIT License  

本章介绍了二值图的进阶分析，包括霍夫空间系转换、轮廓匹配、拟合等操作

## [轮廓逼近](./1-clazz.py)
对图像的二值图各轮廓进行相似操作，逼近每个林廓的真实几何形状，从而通过轮廓判断真实物品是什么形状， 但该种判断
十分脆弱，后续会有更好的算法来实现该功能
```
    cv.approxPolyDP(cure, epsilon, closed)
        - curve: 轮廓曲线点
        - epsilon: 真实曲线的最大距离，值越小越逼近真实轮廓
        - closed: 区域是否闭合, booleand
```

## [几何矩计算轮廓中心与横纵波对比过滤](./2-clazz.py)
对二值图像的各个轮廓进行计算获得对应的几何矩，根据几何矩计算轮廓点的中心位置。
```
    cv.moments(contours, binaryImage)
            - contours: 轮廓点集
            - binaryImage: bool, default False；二值图返回
```
注：若前景物品底色为黑色，建议使用形态学分析进行处理
```
    binary = cv.Canny(src, t, t * 2)
    k = np.ones((3, 3), dtype=np.uint8)
    binary = cv.morphologyEx(binary, cv.MORPH_DILATE, k)
    contours, _ = cv.findContours(binary, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
```

## [Hu矩实现轮廓匹配](./3-clazz.py)
对二值图的各个轮廓进行几何矩计算，根据几何矩获取图像的中心位置，再根据中心位置计算中心矩与hu矩。opencv中通过
一个api就可以计算出上述三种矩。
```
        cv.moments(contours, binaryImage)
            - contours: 轮廓
            - binaryImage: 二值图返回

        cv.HuMoments(&Moments, hu)
            - &Moments: moments计算后的图像矩
            - hu: 输出的hu矩七个值

        cv.matchShapes(contour1, contour2, method)
            - contour1, contour2: 轮库点集合或灰度图像
            - method: 匹配算法
                      CONTOURS_MATCH_I1  常用
                      CONTOURS_MATCH_I2
                      CONTOURS_MATCH_I3
```

## [圆、椭圆的轮廓拟合](./4-clazz.py)
轮廓拟合用于解决二值图像分析过程中，多轮廓缺省或其他原因导致的图像不闭合的问题，通过对轮廓进行进一步处理，满
足对轮廓形状的判断。
```
    cv.fitEllipse(contours)
        - contours: 轮廓

    return:
        - 拟合后的中心位置
        - 长轴与短轴的直径（如果是圆，则两个值相同）
        - 偏移角度
```
注意： contours进行椭圆拟合操作时最少需要5个点

## [凸包检测](./5-clazz.py)
对二值图获取轮廓之后，对获取的轮廓进行排序并链接，并对其进行过滤，将最外侧的定点链接形成一个凸形的区域。也是
最早的一种手势识别的解决方案。
```
        cv.convexHull(contours, closkwise, returnPoints)
            - contours: 轮廓集
            - clockwis: 顺时针或逆时针链接，bool, default False 顺时针
            - returnPoints: 返回类型, bool, default True 默认返回凸包的点集
```

## [点多变检测，判断点是否在轮廓内](./6-clazz.py)
对于轮廓图像， 判断点是否在轮廓内，在opencv被称为点多边形检测，通过该api可以获得点到轮廓的距离。该api也被用于
车辆压线判断等多个场景。
```
    cv.pointPolygonTest(contours, point, measureDist)
        - contours: 轮廓点集
        - point：检测点
        - measureDist: bool， True 返回点到轮廓的距离； False 返回1，0，-1，表示在轮廓内，轮廓边缘上、轮廓外
```

## 霍夫直接检测
霍夫变换是一种图像变换算法，将二维空间坐标系变换到极坐标空间，可提取图像中的直线、圆等内容。opencv中的api如下
```
        cv.HoughLines(binary, rho, theta, threshold, srn, stn, min_theta, max_theta)
            - binary: 二值图，轮廓不宜多并且噪声处理后
            - rho: 极坐标r的步长
            - theta: 角度步长
            - threshold: 累加器阈值,图像在霍夫空间每个像素点都是一条曲线，经过的每个(r,theta)都加1，如果多个曲线都经过同一个
        (r,theta)相交，如果大于给定的域值，说明可能存在一条直线在霍夫空间该点
            - srn, stn: 多尺度霍夫变换时的参数，经典霍夫变换则不需要
            - min_theta: 直线旋转最小角度
            - max_theta: 直线旋转最大角度
```
[例子](./7-clazz.py)

其实opencv中还有一个霍夫直线的检测api，该api更为常用，它会直接返回直线的空间坐标点，比之前点阵集合更加直观，更容易理解。同时该
api能够声明最短线段长度、中间缺省线段等。而前一课的api适用于多个备选线段并进行一系列算法使用，两种api均有自己的使
用场景。
```
    cv.HoughLinesP(binary, rho, theta, threshold, minLineLength, maxLineGap)
        - binary: 具有轮廓的二值图
        - rho: 极坐标 r的步长  经验值：1
        - theta: 角度的步长 经验值: np.pi / 180
        - threshold: 累加器阈值,图像在霍夫空间每个像素点都是一条曲线，经过的每个(r,theta)都加1，如果多个曲线都经过同
一个
    (r,theta)相交，如果大于给定的域值，说明可能存在一条直线在霍夫空间该点
        - minLineLength: 最小线段长度
        - maxLineGap: 最大线段终端像素
```
[例子](./8-clazz.py)

## [霍夫圆检测](./9-clazz.py)
根据极坐标，圆上任意一点的坐标可以表示为（x0, y0），圆半径已知，旋转360度可获取极坐标上的所有坐标；如果只知道
图像上像素点，圆半径旋转360则中心点处的坐标值必定最强
```
        cv.HoughCircles(binary, method, dp, minDist, param1, param2, minRadius, maxRadius)
            - binary: 二值图（高斯模糊后的灰度图像）
            - method: 圆检测的方法（霍夫梯度）
            - dp: 表示图像分辨率是否变化， 为1 表示不变化， 2表示为原来的一半
            - minDist: 两个圆心间的最小距离，用于消除同心圆的情况
            - param1: 边缘提取的高阈值
            - param2: 边缘提取的低阈值
            - mainRadius: 检测圆的最小半径
            - maxRadius: 检测圆的最大半径
```

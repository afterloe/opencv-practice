移动物体检测
===
> create by [afterloe](605728727@qq.com)  
> version is 1.0.0  
> MIT License  

### 常用的移动物体检测方式如下

#### 基于帧差
##### 常规操作
帧差法是常用的移动物体检测的方法，他的原理使用前一张图像与当前图像的像素值差异作为标识。在实际场景中，有使用第一帧图像作为固定比对的，
也有使用连续好几帧在计算均值的。基本套路如下:
```python
# 与第一帧进行对比的演示

# 图像预处理： 转为灰度图像， 并使用高斯模糊去除噪声
gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
blurred = cv.GaussianBlur(gray, (21, 21), 0)
frame_delta = cv.absdiff(preve_frame, blurred)
# 二值化： 使用固定阈值，将像素值25以上的转化为255
_, binary = cv.threshold(frame_delta.copy(), 25, 255, cv.THRESH_BINARY)

# 闭操作： 膨胀+腐蚀, 连通组件需要。
binary = cv.dilate(binary, None, iterations=2)  # 膨胀
binary = cv.erode(binary, None, iterations=2)  # 腐蚀
contours = cv.findContours(binary.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
```
在图像二值化之后进行的形态学操作，根据所使用的设备进行动态调整，如果使用的设备不是高动态的摄像头，那么闭操作可能带来一堆因为光问题形成的变化，
所以一般是使用腐蚀操作，去除小型的干扰，但更多的去除是在外接矩形的面积上下功夫。

```python
# 判断两张图像是否存在差异
hsv = cv.cvtColor(now, cv.COLOR_BGR2HSV)
mask = cv.inRange(hsv, hsv_min, hsv_max)
edged = cv.GaussianBlur(mask, (0, 0), 3)
diff = cv.subtract(edged, previous)
diff = cv.morphologyEx(diff, cv.MORPH_OPEN, kernel)
contours = cv.findContours(diff, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
```
上面这种是使用cv的减法进行处理的，他的减去后有很多细小的像素空洞，所以使用开操作去除。  

另外，三帧差法的理论也差不多，是使用前前一张图像，与前一张图像的差值，与前一张与当前图像的差值进行与操作，具体如下
```python
diff_1 = prev_2 - prev_1
diff_2 = frame - prev_1
diff = diff_1 & diff_2
```
##### 加权平均数
从外面看来的一个骚操作，通过将图像转换为浮点数并计算基数，每次循环的时候平均数进行0.5的权重加持。最后用当前的图像减去权重的扫描值实现移动对象检测
```python
if None is avg:
    print("Starting background model")
    avg = gray.copy().astype("float")
    continue
cv.accumulateWeighted(blurred, avg, 0.5)

# 累积当前帧和之前的帧，然后计算当前帧之间的差帧数和移动平均值
frame_delta = cv.absdiff(blurred, cv.convertScaleAbs(avg))
_, binary = cv.threshold(frame_delta, 25, 255, cv.THRESH_BINARY)
```
#### 基于 KNN/高斯 背景分离 
帧差法对对光照、噪声相当敏感，虽然有形态学处理进行辅助，但难免会有意外。opencv中对背景模型提取的算法有两种，一种是基于高斯模糊模型（GMM）实现背景提取，
另外一种是使用最近相邻模型（KNN）实现的，api如下：
```
GMM cv.createBackgroundSubtractorKNN(history, varThreshold, detectShadows)
GMM cv.createBackgroundSubtractorMOG2(history, varThreshold, detectShadows)
        - history: 过往帧数，默认500帧，历史进行比较
        - varThreshold: 马氏距离，默认16，值越大，最新的像素会归为前景，值越小对光照敏感
        - detectShadow: 是否保留阴影检测，默认True， 开启阴影检测虽然可以提高提取效果，但是效率会变低，推荐不开启
```
使用如下：
```python
bs = cv.createBackgroundSubtractorKNN(detectShadows=True)
"""
图相获取与 预处理
"""
fg_mask = bs.apply(frame)
 _, binary = cv.threshold(fg_mask.copy(), 25, 255, cv.THRESH_BINARY)
binary = cv.erode(binary, None, iterations=2)
contours = cv.findContours(binary.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
```

#### 基于HSV颜色空间
这个比较简单了， 使用特定的颜色的hsv的并进行处理，形成mask，然后进行计算
```python
hsv = cv.cvtColor(blurred, cv.COLOR_BGR2HSV)
mask = cv.inRange(hsv, self.__yellow_lower, self.__yellow_upper)
contours = cv.findContours(mask.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
```

#### 基于颜色直方图反向投影
均值迁移移动对象分析主要是基于ROI区域颜色直方图分布与反向投影实现的，其核心思想是对反向投影后的图像作均值迁移（meanshift）
从而发现密度最高的区域，算法流程如下：
``` 
1 读取图像一帧
2 绘制HSV直方图
3 反向投影该帧
4 使用meanshift算法寻找最大分布密度

cv.CamShift(probImage, window, criteria)
    - probImage: 输入图像，直方图方向投影结果
    - window: 搜索开窗大小，ROI对象区域
    - criteria: 均值迁移停止条件

注：返回信息中需要手动更新开窗信息
```
```python
mask = cv.inRange(hsv_roi, lower, upper)
roi_hist = cv.calcHist([hsv_roi], [0], mask, [180], [0, 180])
cv.normalize(roi_hist, roi_hist, 0, 255, cv.NORM_MINMAX)

hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
dst = cv.calcBackProject([hsv], [0], roi_hist, [0, 180], 1)  # 直方图反向投影 详见2-day/10-clazz.py
ret, track_window = cv.meanShift(dst, track_window, term_criteria)
x, y, w, h = track_window
```
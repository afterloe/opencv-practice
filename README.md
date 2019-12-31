# python3 & opencv4

> create by [afterloe](lm6289511@gmail.com)  
> version is 1.2  
> MIT License    

## 目录
<a href="#note">笔记</a>  
<a href="#backup">备忘录</a>  

## python3 & opencv4 的参考内容
python3 开发规范，参考自[PEP8标准](https://www.cnblogs.com/rrh4869/p/11177785.html)  
opencv4 使用版本为4.1.1，相关[开发文档](https://docs.opencv.org/4.1.1/)

### <a id="note">笔记</a>
[第一节 - OpenCV基础操作](./workshops/1-day/summary.md)
   - 图像读取
   - 颜色空间转换
   - 图像的克隆、拷贝及创建
   - 图像逻辑操作及LUT查找表
   - 抠图、均值、极值及标准方差  
   
[第二节 - 图像处理相关操作](./workshops/2-day/summary.md)    
   - 图像归一化操作
   - 视频及摄像头内容读取与分片存储
   - 图像翻转、缩放（插值计算）、绘图
   - ROI区域提取（规则、非规则）、图像直方图
   - 直方图均衡化（图像增强）、相似度对比（直方图比较）
   - HSV 色系取值范围
   - [直方图反向投影（图像ROI目标检索）](./workshops/2-day/class_10.py)
   
[第三节 - 图像卷积相关操作](./workshops/3-day/summary.md)
   - 图像的卷积操作  
   - 图像噪声去除 均值、高速、非局部、双边滤波  
   - 边缘保留滤波 高斯双边、mean shift 均值迁移、快速滤波、自定义滤波  

[第四节 - 图像卷积相关操作（进阶）](./workshops/4-day/summary.md)
   - 图像梯度算子（一阶求导）Sobel、Robert、Prewitt，寻找图像中的轮廓
   - 图像梯度算子（二阶求导）拉普拉斯，精准寻找图像中的轮廓
   - 八领域、四领域的图像锐化，增强图像中的细节
   - Unsharpen Mask （USM）锐化增强算法与图像权重增强
   - Canny边缘检测算法
   - 图像金字塔与拉普拉斯金字塔
   - 图像模板匹配（最简单的模式识别）
   - 二值图像的初步操作（基于均值的二值化）

[第五节 - 二值图像分析](./workshops/5-day/summary.md)
   - 基础阈值操作，实现二值化
   - 双峰图像的二值阈值搜寻算法 - OTSU
   - 单峰图像的二值阈值搜寻算法 - TRIANGLE
   - 不均匀光照的二值阈值搜寻算法 - 自适应阈值
   - 连通组件搜寻、状态统计
   - 组件的轮廓发现与轮廓绘制
   - Canny算法结合连通组件实现目标外接矩形与最小矩形绘制
   - 基于矩形面积、弧长实现目标过滤

[第六节 - 二值图像分析（进阶）](./workshops/6-day/summary.md)
   - 图像轮廓逼近
   - 几何矩计算轮廓中心与横纵波对比过滤
   - Hu矩实现轮廓匹配
   - 圆、椭圆的轮廓拟合
   - 凸包检测
   - 点多变检测，判断点是否在轮廓内
   - 霍夫直接检测
   - 霍夫圆检测
   
[第七节 - 图像形态学分析](./workshops/7-day/summary.md)  
   - 图像的膨胀与腐蚀
   - 结构元素的运用
   - 开闭操作
   - 顶帽、黑帽操作
   - 图像梯度分析
   - hit&miss 运用

[第八节 - 综合运用与技能回顾](./workshops/8-day/summary.md)
   - 二值图像分析运用，缺陷检测
   - 最大轮廓提取
   - 图像水印去除与修复
   - 图像透视变换
   - 视频的读取与色彩追踪
   - 视频的前景背景分离与ROI区域提取

[第九节 - 视频综合分析](./workshops/9-section/summary.md)
   - 角点特征分析

## <a name="backup">备忘录</a>

### 关于git提交的type
根据 Header的内容及描述，type共分为以下8类：
```
feat：新功能（feature）
fix：修补bug
docs：文档（documentation）
style： 格式（不影响代码运行的变动）
refactor：重构（即不是新增功能，也不是修改bug的代码变动）
test：增加测试
chore：构建过程或辅助工具的变动
resources: 资源修改
```

### 不错的开源框架
#### 优秀的图像处理库 - imutils
#### 直方图GUI绘制库 - matplotlib
#### 数学库 - numpy

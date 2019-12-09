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
   - [直方图反向投影（图像ROI目标检索）](./workshops/2-day/class_10.py)
   
[第三节 - 图像处理相关操作（进阶）](./workshops/3-day/summary.md)
   - 图像的卷积操作  
   - 图像噪声去除 均值、高速、非局部、双边滤波  
   - 边缘保留滤波 高斯双边、mean shift 均值迁移、快速滤波、自定义滤波  

[第四节 - 图像处理相关操作（飞升）](./workshops/4-day/summary.md)


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

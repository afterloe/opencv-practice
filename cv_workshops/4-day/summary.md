# 图像卷积进阶操作总结
> create by [afterloe](605728727@qq.com)  
> version 1.1  
> MIT License

图像卷积操作用于机器视觉在预处理阶段的图像基础处理，主要卷积操作及作用如下:
  - 模糊操作： 去除图像噪声（如椒盐噪声、高斯噪声等）
  - 梯度操作： 获取图像轮廓
  - 锐化操作： 增强图像细节

## [图像梯度 - Sobel算子（一阶导数算子）](./1-clazz.py)
卷积的作用除了实现图像模糊、降噪外，还可实现梯度信息寻找。这类梯度信息是图像的原始特征数据，进行一步处理后可生
成一些比较高级的特征，可用于图像特征的匹配、图像分类等应用，Sobel算子是一种很典型的图像梯度提取算子，其本质是基于
图像空间域卷积，实现思想为一阶导数算子。
```
    cv.Sobel(src, ddepth, dx, dy, ksize, scale, delta, borderType)
        ddepth - 表示输入与输出图像类型关系, CV_32F；若为 -1 则会出现不可预期的结果
        dx - X方向 一阶导数
        dy - Y方向 一阶导数
        ksize - 卷积大小 3*3
        scale - 缩放比率， 1表示不变
        borderType - 边缘类型    
```
注意： 使用`convertScaleAbs`对32位浮点数运算结果进行转化，否则图像是黑色的；
使用`cv.add`方法时，`dtype=cv.CV_16S` 更适合32位浮点数相加，其取值范围是0~512

## [图像梯度 - Robert、Prewitt算子](./2-clazz.py)
对于一阶求导用Sobel算子外，还有robert和prewitt算子， 这两了算子可使用Opencv中的自定义滤波器实现。其中
ddepth 不推荐继续使用-1了，因为其表示输入与输出图像类型关系，涉及浮点运算时，或卷积运算结果为负数时需要使用CV_32F
或np.float32；转换完成后使用convertScaleAbs函数将结果转换为字节类型
```
    robert卷积核如下:
    1, 0      0, -1
    0, -1     1, 0
    x方向      y方向

    prewitt卷积核如下:
    -1, -1, -1       -1, 0, 1
    0, 0, 0          -1, 0, 1
    1, 1, 1          -1, 0, 1
    x方向              y方向
```
注意: 使用`cv.filter2D对图像进行自定义卷积操作操作`

## [图像梯度 - 拉普拉斯算子（二阶导数算子）](./3-clazz.py)
二阶导数算子可快速检测图像边缘，其原理同一阶导数算子类似，只不过在x，y方向的二阶偏导数。一般来说是4领域增强，也
可以进一步扩展增强为8领域。由于二阶偏导数的关系，图像在处理过程易受到噪声的影响， 一般先使用高斯进行降噪，在进行
计算。
```
    cv.Laplacian(src, ddepth, ksize, scale, delta, borderType)
        ddepth - 图像深度，默认为-1， 表示输入输出图像相同
        kszie - 卷积核， 默认是1 （4领域）， 必须为奇数， 大于1则表示为 8领域算子
        scale - 缩放比率， 1表示不变
        delta - 对输出图像加上常量值(即第三通道RGB + delta)
        borderType - 边缘处理方法
```
注意：使用高斯模糊先进行降噪操作，否则噪声会对像素的梯度分布造成影响，同时在8领域求导后颜色接近于0，可使用delta增加亮度；
ksize - 1 4领域 3 - 8领域（经验值）

## [四领域、八领域的图像锐化](./4-clazz.py)
图像卷积的主要三个功能为 图像模糊 -> 去噪、 图像梯度 -> 边缘发现、 图像锐化 -> 细节增强。图像锐化的本质是图像
拉普拉斯滤波器加原图权重像素叠加输出的结果。同样使用自定义滤波器带入对应算子实现
```
    -1 -1 -1
    -1  C -1     --->  当C大于8时，表示图像锐化，越接近8表示锐化效果越好; 等于8时是图像高通滤波()；
    -1 -1 -1
        8领域

    0 -1 0
    -1 5 -1
    0 -1 0
        4领域
```
注意：一般4领域锐化足够使用，8领域锐化效果及其强烈

## [Unsharpen Mask 方法(USM) - 锐化增强算法](./5-clazz.py)
算法公式： 
```
(源图片 - w * 高斯模糊) / (1 - w)
* w -> 权重（0.1 ~ 0.9）, 默认为 0.6
```

原理函数
```
    cv.addWeighted(src1, alpha, src2, beta, gamma)
        - alpha: 第一个输入参数的权重值，可为负数
        - gamma: 类delta效果，色彩增强，总和超过255 就是白色
        - beta: 第二个输入参数的权重值，可为负数
```
注意: 进行处理的时候，图像的shape、dtype一定要相同

## [Canny边缘检测算法](./6-clazz.py)
canny边缘检测算法，该算法是一种经典的图像边缘检测与提取算法，该算法的主要具备以下几个特点:
1. 有效的噪声抑制
2. 更强的完整边缘提取
主要用于机器视觉、内容标注、目标识别等领域。

canny算法的实现步骤如下:
- 对采集图像进行高斯模糊，抑制并去除噪声
- 对x、y两个方向使用二阶偏导数进行像素梯度运算，获得候选边缘
- 角度计算与非最大型号抑制，避免过度曝光与过度黑暗
- 候选边缘过滤，进行高低阀值连接，获取完整边缘。高于高阀值的全部保留，低于低阀值的全部舍弃，在两个阀值之间的按照
8领域方式进行中心像素连接，不能连接的舍弃；
- 输出边缘    

```
    cv.Canny(src, threshold1, threshold2, apertureSize, L2gradient)
        - threshold1 -> 低阀值 (高阀值的一半 或 三分之一，即低高阀值之比为1:2 或 1:3)
        - threshold2 -> 高阀值 (尽量不超过400)
        - apertureSize -> Sobel算子(一阶求导算子，梯度计算)的卷积核大小，默认3即 3 * 3
        - L2gradient -> 连接算法选取 False， 采用L1算法即绝对值计算； false ， 采用L2算法，平方和开根号进行向量计算
```
注意： canny 输入可以是三通道彩色图片，也可以使单通道灰度图像，输出为单通道二值图像

## 图像金字塔与拉普拉斯金字塔
[图像金字塔](./7-clazz.py):  
对一张输入图像进行模糊操作后，再进行采样，大小为原图的1/4 （即宽高缩小一半）
reduce 从原图生成一系列低分辨率图像（逐步缩小）py.pyrDown
expand 从原图生成一系列高分辨率图像（逐步放大）py.pyrUp
图像金字塔必须逐层操作且每次操作后结果都是前一层的1/4      
    
[拉普拉斯金字塔](./8-clazz.py):  
拉普拉斯金字塔基于图像金字塔进行处理，对不同分辨率的结果进行反向扩充，举例如下：
```
    - 输入图像G0
    - 图像金字塔 reduce生成 G1 G2 G3
    - 拉普拉斯金字塔 L0 = G0 - expand(G1)
                         L1 = G1 - expand(G2)
                         L2 = G2 - expand(G3)
```
注意： G0减去expand(G1)得到的结果就是两次高斯模糊输出的不同，所以L0称为DOG（高斯不同）

## [模板匹配](./9-clazz.py)
模板匹配被称为最简单的模式识别方式，模板匹配的工作条件严苛，因为其并不是基于特征的匹配，需要光照、背景、干扰一致
的情况下才能更好的工作，在工业、屏幕内容识别上运用广泛。
```
        cv.matchTemplate(image, templ, result, method, mask)
            - image  : 输入进行匹配的图像
            - templ  : 模板图像
            - result : 匹配结果集
            - method : 匹配方法
            - mask   : 二值图遮罩
```
匹配方法集如下:
    - TM_SQDIFF = 0
    - TM_SQDIFF_NORMED = 1       # 平方不同与其归一化，值越小相关性越高，匹配程度越高
    - TM_CCORR = 2
    - TM_CCORR_NORMED = 3        # 相关性匹配，值越大相关性越强，匹配程度越高；Normed表示归一化，1表示高度匹配
    - TM_CCOEFF = 4
    - TM_CCOEFF_NORMED = 5       # 相关因子匹配，值越大相关性越强，匹配程度越高；Normed表示归一化，1表示高度匹配

注意： 模板的shape和dtype对匹配结果影响巨大， 不同的模板需要进行不同的处理

## [二值图像](./10-clazz.py)
将图像像素点按照一定阈值进行切分，大于该阀值时像素点值为1，小于阀值时像素点值为0。二值图像处理与分析在机器视觉与
机器自动化中非常重要，主要用于解决该领域内的轮廓分析、对象测量、轮廓匹配、识别、形态学处理与分割、各种形状检测、拟
合、投影与逻辑操作、轮廓特征提取与编码等。  
主要流程1) 输入图像； 2）转换为灰度图像； 3）计算图像均值；4）按均值对图像进行二值化操作
```
def binary_pic(mean, gray):
    h, w = gray.shape
    binary = np.zeros((h, w), dtype=np.uint8)
    for row in range(h):
        for col in range(w):
            binary[row, col] = 0 if mean > gray[row, col] else 255
    cv.imshow("binary", binary)
```
注意： 使用`cv.mean`方法获取的图像均值比较适合进行图像二值化操作，并非127

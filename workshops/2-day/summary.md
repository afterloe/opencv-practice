# 像素归一化算法总结
> create by [afterloe](605728727@qq.com)  
> version 1.0  
> MIT License


<script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>

<a href="#hsv">HSV 色系取值范围</a>
<a href="#minmax">MIN_MAX的算法</a>  
<a href="#inf">INF的算法</a>  
<a href="#l2">L2的算法</a>  
<a href="#l1">L1的算法</a>   

## <a id="minmax">MIN_MAX的算法</a>
假设输入图像像素点位 `[2.0, 8.0, 10.0]`  
转换过程：   
根据 delta进行  
![MIN_MAX](./formula/minmax.png)

delta = 10.0 - 2.0 = 8.0

input | process | output
-|-|-
2.0 | (2.0 - 2.0) / 8.0 | 0
8.0 | (8.0 - 2.0) / 8.0 | 0.75
10.0 | (10.0 - 2.0) / 8.0 | 1.0

## <a id="inf">INF的算法</a> 
输入图像像素点位同上即`[2.0, 8.0, 10.0]`   
转换过程：   
根据最大值进行  
![MIN_MAX](./formula/inf.png)

delta = 10.0

input | process | output
-|-|-
2.0 | 2.0 / 10.0 | 0.2
8.0 | 8.0 / 10.0 | 0.8
10.0 | 10.0 / 10.0 | 1.0

## <a id="l2">L2的算法</a> 
输入图像像素点位同上即`[2.0, 8.0, 10.0]`   
转换过程：   
根据平方向量  
![MIN_MAX](./formula/l2.png)

delta = $ \sqrt[2]{168} \quad $  (约等于12.9614)

input | process | output
-|-|-
2.0 | 2.0 / 12.9614 | 0.15
8.0 | 8.0 / 12.9614 | 0.62
10.0 | 10.0 / 12.9614 | 0.77

## <a id="l1">L1的算法</a>   
输入图像像素点位同上即`[2.0, 8.0, 10.0]`   
转换过程：   
根据像素点之和取模  
![MIN_MAX](./formula/l1.png)

$$
delta = p_1 + p_2 ... + p_n
output = p_1 / delta
output = \frac{p_n}{p_1 + p_2 ... + p_n} 
$$

delta = 2 + 8 + 10 = 20.0

input | process | output
-|-|-
2.0 | 2.0 / 20.0 | 0.1
8.0 | 8.0 / 20.0 | 0.4
10.0 | 10.0 / 20.0 | 0.5

## <a id="hsv">HSV颜色空间转换</a>
Opencv中常用的颜色转换为两种，BGR -> Gray, BGR -> HSV；其中Gray与HSV不可以相互转换，HSV颜色空间的取值范围
```
H [0, 180]
S [0, 255]
V [0, 255]
```

常用颜色的HSV取值范围

取值 | 黑 | 灰 | 白 | 红 | 橙 | 黄 | 绿 | 青 | 蓝 | 紫
-|-|-|-|-|-|-|-|-|-|-
hmin | 0 | 0 | 0 | 0[156] | 11 | 26 | 35 | 78 | 100 | 125
hmax | 180 | 180 | 180 | 10[180] | 25 | 34 | 77 | 99 | 124 | 155
smin | 0 | 0 | 0 | 43 | 43 | 43 | 43 | 43 | 43 | 43
smax | 255 | 43 | 30 | 255 | 255 | 255 | 255 | 255 | 255 | 255
vmin | 0 | 46 | 221 | 46 | 46 | 46 | 46 | 46 | 46 | 46
vmax | 46 | 220 | 255 | 255 | 255 | 255 | 255 | 255 | 255 | 255


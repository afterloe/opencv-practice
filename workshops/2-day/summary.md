# 像素归一化算法总结
> create by [afterloe](605728727@qq.com)  
> version 1.0  
> MIT License


<script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>

<a href="#minmax">MIN_MAX的算法</a>  
<a href="#inf">INF的算法</a>  
<a href="#l2">L2的算法</a>  
<a href="#l1">L1的算法</a>   

## <a id="minmax">MIN_MAX的算法</a>
假设输入图像像素点位 `[2.0, 8.0, 10.0]`  
转换过程： 根据 delta进行
$$
delta = max \div min
output = (point - min) \div delta
$$

delta = 10.0 - 2.0 = 8.0

input | process | output
-|-|-
2.0 | (2.0 - 2.0) / 8.0 | 0
8.0 | (8.0 - 2.0) / 8.0 | 0.75
10.0 | (10.0 - 2.0) / 8.0 | 1.0

## <a id="inf">INF的算法</a> 
输入图像像素点位同上即`[2.0, 8.0, 10.0]`   
转换过程： 根据最大值进行
$$
delta = max
output = point \div delta
$$

delta = 10.0

input | process | output
-|-|-
2.0 | 2.0 / 10.0 | 0.2
8.0 | 8.0 / 10.0 | 0.8
10.0 | 10.0 / 10.0 | 1.0

## <a id="l2">L2的算法</a> 
输入图像像素点位同上即`[2.0, 8.0, 10.0]`   
转换过程： 根据平方向量
$$
delta = \sqrt[2]{2.0^2 + 8.0^2 + 10.0^2} \quad
output = \frac{point}{delta}
output = \frac{point}{\sqrt[2]{2.0^2 + 8.0^2 + 10.0^2} \quad}
$$

delta = $ \sqrt[2]{168} \quad $  (约等于12.9614)

input | process | output
-|-|-
2.0 | 2.0 / 12.9614 | 0.15
8.0 | 8.0 / 12.9614 | 0.62
10.0 | 10.0 / 12.9614 | 0.77

## <a id="l1">L1的算法</a>   
输入图像像素点位同上即`[2.0, 8.0, 10.0]`   
转换过程： 根据像素点之和取模

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
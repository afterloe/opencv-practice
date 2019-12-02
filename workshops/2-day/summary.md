# 像素归一化算法总结
> create by [afterloe](605728727@qq.com)  
> version 1.0  
> MIT License . 

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

delta = 根号168  (约等于12.9614)

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

delta = 2 + 8 + 10 = 20.0

input | process | output
-|-|-
2.0 | 2.0 / 20.0 | 0.1
8.0 | 8.0 / 20.0 | 0.4
10.0 | 10.0 / 20.0 | 0.5

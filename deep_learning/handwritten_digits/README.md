LeNet - 手写字体识别
===
> create by [afterloe](605728727@qq.com)  
> version is 1.0.0  
> MIT License  

#### LeNet 网络
 
图层传递: INPUT => CONV => TANH => POOL => CONV => TANH => POOL => FC => TANH => FC
 
 | 图层类型 | 卷积层大小 | 过滤大小
 | :----- | :--------- | :----
 | Input Image | 28 * 28 * 1 | 
 | CONV | 28×28×20 | 5×5,K = 20
 | ACT | 28×28×20
 | POOL | 14×14×20 | 2×2
 | CONV | 14×14×50 | 5×5,K = 50
 | ACT | 14×14×50
 | POOL | 7×7×50 | 2×2
 | FC | 500
 | ACT | 500
 | FC | 10
 | SOFTMAX | 10

# 创建自己的深度学习库
> create by [afterloe](605728727@qq.com)  
> MIT License  
> version is 1.0.3

## 使用JavaScript来收集图像url
Step #1: 打开Chrome浏览器，进入Javascript Console
Step #2: 执行以下脚本
```javascript

// Gooogle 版本
var script = document.createElement('script');
script.src = "https://code.jquery.com/jquery-2.2.0.min.js";
document.getElementsByTagName('head')[0].appendChild(script);

// grab the URLs
var content = $('img.rg_i.Q4LuWd.tx8vtf').map(function() { return $(this)[0].src; });

// write the URls to file (one per line)
var textToSave = content.toArray().join('\n');
var hiddenElement = document.createElement('a');
hiddenElement.href = 'data:attachment/text,' + encodeURI(textToSave);
hiddenElement.target = '_blank';
hiddenElement.download = 'urls.txt';
hiddenElement.click();


// Baidu 版本
var content = $('img.main_img.img-hover').map(function() { return $(this)[0].src; });
``` 

## 启动训练脚本
```shell script
 & 'D:\Program Files\Python37-64\python.exe' .\train_network.py 
-d 'G:\Project\py3\computer_version_demo\deep_learning\resources' 
-m G:\Project\py3\computer_version_demo\deep_learning\resources\nazha_not.model 
-p G:\Project\py3\computer_version_demo\deep_learning\resources\plot.png
```

## 总结
LeNet模型: 对于图像分类器有很多限制，第一个是28×28像素的图像非常小（LeNet体系结构最初旨在识别手写数字，而不是照片中的对象）。   
对于某些示例图像（其中目标对象已经很小），将输入图像的大小调整为28×28像素可有效地将对象缩小为只有2-3像素大小的微小的红色/白色斑点。 

> 输入到卷积神经网络的宽度和高度图像尺寸的常见选择包括32×32、64×64、224×224、227×227、256×256和299×299。
> 在这种情况下，正在预处理（规范化）将图像缩放为227 x 227的尺寸, 所以图像尺寸的大小最号与prototxt定义保持一致   

在这种情况下，LeNet模型很可能只是在预测输入图像中何时有大量红色和白色一起定位（并且绿色，红色，绿色和白色等疑似对象颜色）。
目前最先进的卷积神经网络通常接受最大尺寸为200-300像素的图像，这些较大的图像将有效的构建更强大的对象分类器。
但是使用更高分辨率的图像还需要使用更深的网络体系结构，这反过来需要收集更多的训练数据并利用计算量更大的训练。    
对于优化分类器的建议如下:    
- 收集更多训练数据（理想情况下，有5000多个对象图像）;
- 在训练过程中使用更高分辨率的图像。一般64×64像素会产生更高的精度。 128×128像素更理想;
- 模型训练期间使用更深的网络体系结构;
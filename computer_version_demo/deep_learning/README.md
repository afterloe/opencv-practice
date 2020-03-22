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
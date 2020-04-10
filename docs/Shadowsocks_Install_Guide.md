Shadowsocks Install Guide
===
> create by [afterloe](605728727@qq.com)  
> version is 1.0.3  
> MIT License  


#### 导读
因为做deeping learn的缘故，经常需要上一些国外的网站进行资料和数据的下载，但是国内的经常因为一些莫名奇妙的原因导致网络存在波动，
如DNS污染、GFW等，所以在一些数据集和网络模型的下载上需要一些手段。

#### 免责声明
本篇博文涉及的一切仅用于深度学习和机器视觉的学习与技术研究，不得作为其他用途使用。

#### 前期准备

* [前往](https://github.com/earlyLoe/electron-ssr-backup) 下载对应的软件
```
sudo apt install libcanberra-gtk-module libcanberra-gtk3-module gconf2 gconf-service libappindicator1
sudo dpkg -i electron-*-{version}.deb
sudo electron-ssr
```

* 配置节点信息，这里使用订阅，需要注意的是该软件使用的是python，需要安装好。
```
where python
cd /usr/bin
ln -s ./python2 python
```

* 测试
```
export http_proxy="http://127.0.0.1:12333"
curl www.google.com
```

* Linux下需要手动设置http_proxy, 打开`设置 - 网络 - 网络代理`，设置手动，IP和端口设置为命令行提示的内容


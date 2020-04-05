Python3.6安装
===
> create by [afterloe](605728727@qq.com)  
> version is 1.0.3  
> MIT License

##### 摘要
本文主要说明如何在Ubuntu19上安装Python, 由于项目需要（Tensoflow的版本要求，2.0以上版本仅支持python3.5 ~ python3.7, 而ubuntu自带的版本是python3.7.5， 不支持安装tensorflow2.0），
所以需要在Ubuntu上重新安装python3。

##### 源码安装
从python官方网站下载源码[Python3.6.7](https://www.python.org/ftp/python/3.6.7/Python-3.6.7.tar.xz)

##### 卸载原来的版本
```commandline
sudo apt-get remove python3 python3.7 python3.7m
```

##### 安装步骤
```commandline
wget https://www.python.org/ftp/python/3.6.7/Python-3.6.7.tar.xz -o ~/Download/Python-3.6.7.tar.xz
su
mv ~/Download/Python-3.6.7.tar.xz /usr/local
tar -Jxvf Python-3.6.7.tar.xz
rm -rf Python-3.6.7.tar.xz
cd Python-3.6.7
./configure
make
make test
make install
```

##### 测试
```commandline
python3
>> python 3.6.7
```

##### 升级pip
重新安装后的pip版本为10.0，很多包尤其是tensorflow需要19以上的版本的pip，所以需要对pip进行升级
```commandline
sudo pip3 install --upgrade pip
pip3 -v
pip 20.0 from /usr/bin/pip3 (python 3.7)
```
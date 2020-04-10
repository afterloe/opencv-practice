OpenCV + Deep Learn 项目工程化
===
> create by [afterloe](605728727@qq.com)  
> version is 1.0  
> MIT License

### 工程化概述
OpenCV + Deep Learn主要工程语言为 Python，其中95%为Python3的代码，所以工程化准备工作按照Python的有关插件及C++工程进行筹备。

#### 工程目录结构
工程目录结构结合GoLang、Node.js工程化经验，进行拟定，物理结构细节如下:
```shell script
| - engineer                     # 工程名：使用下划线命名规则
| ---- docs                      # 文档：工程API文档或相关其他文档
| ---- src                       # 源码：可以和工程同名，也可以为src，是一个整体的python自定义模块
| ---- tests                     # 测试用例：CI/CD使用的测试代码，包含单元测试代码
| ---- package.spec              # 编译脚本：将Python工程打包成一个可执行应用，用于快速部署与移植
| ---- README.md                 # 描述文件：Python工程的描述文件
| ---- Makefile                  # makefile： 用于CI/CD 等作业用脚本
| ---- LICENSE                   # 授权说明: 默认为MIT授权
| ---- sample                    # 示例（可选）：若工程为被集成型，里面可以放置一些工程被集成的示例代码
| ---- config                    # 配置文件（可选）: configparser可识别格式的配置文件，可外挂
| ---- resources                 # 资源（可续）：文档中用到的图片、HTML等其他资源
| ---- application.py            # 应用入口（可选）：若工程为独立应用，这里作为独立应用的唯一入口
```

### 工程规范
#### Python版本
Python3 以上， 最低`3.2.x`，其他版本以实验室要求为准

#### 安装依赖
```commandline
pip3 install --upgrade pytest -y
pip3 install --upgrade pyinstaller -y
```
> pytest: https://docs.pytest.org/en/latest/example/simple.html  
> pyinstall: https://pyinstaller.readthedocs.io/en/latest/usage.html  


#### IDE及工具
推荐使用 [Pycharm](https://www.jetbrains.com/pycharm/download/) 社区版本，有条件的可以使用企业版或个人版

#### 源码(src)规范
1. src 模块下必须含有`__init__.py`文件，用于描述为一个python扩展模块  
2. 使用自定义模块应使用`from .model_name import funs`的方式引入函数
3. 有条件尽量避免使用字面量
4. 统一使用`logging`模块作为日志输出对象
5. 有条件为各个函数添加统一的备注，关键函数应该添加逻辑描述
6. 其他编码规范按Pycharm 严苛模式进行

#### 文档(docs)规范
1. 推荐使用Markdown进行编制
2. Markdown结构如下:
```markdown
Title
===
> create by [author](mail)  
> version is     
> License

#### title
content

....
```

#### 测试代码(tests)规范
1. 使用`pytest`命令在工程目录下执行，进行测试
2. 使用`unittest`模块进行断言
3. 若使用到`src`内的源码可参考以下代码进行引入
```python
import unittest
import sys

sys.path.insert(0, ".")

from src.funs import text_elimination, digital_to_consumption_speech

class TestFunc(unittest.TestCase):
    def test_zero_elimination(self):
        self.assertEqual("122.05", text_elimination(122.05000))
        pass
```
> 其他规范参照`unittest`要求进行

#### 打包脚本
1. 使用命令`pyi-makespec -F application.py -n package.spec`生成基础版本的打包脚本
2. 修改`package.spec`脚本，以适应打包
```shell script
vim main.spec

# 把需要编译的脚本写入这里
a = Analysis(['main.py', 'funs.py', 'mode.py', 'utils.py'],
             ...
# 文件也是，左边是源文件， 右边是目标目录
             datas=[('config/log.conf', 'config'), ('config/service.conf', 'config')],
```
具体可参考[这里](https://pyinstaller.readthedocs.io/en/latest/spec-files.html)
> pyi-makespec --key 0123456789abcdef # 设置稍后生成的 **.exe 文件密码，可防 HACK 解包查看核心源文件代码

#### Makefile规范
需要把python的核心模块添加进`path`，否则会报一堆莫名其妙的bug
```makefile
PATH := /home/pi/.local/bin:$(PATH)
SHELL := /bin/bash
```
CI/CD过程以项目实际需求为准，这里不做限制

#### 应用安装规范
环境Ubuntu 18.x 或 Raspberry 4.19.x 及其以上  
目标文件安装位置及说明如下:
```
/opt         测试版应用，装到/opt目录下, 尝试完可直接删除，不影响系统其他任何设置。
/usr/local   正式版应用安装位置
/tmp         测试版日志输出的默认位置
/var/log     正式版日志输出的默认位置
```
> 应用产生的数据及相关配置文件都和应用在同一层


#### 设置应用自启动
环境Ubuntu 18.x 或 Raspberry 4.19.x 及其以上, 使用`systemctl`进行管理  
1. 创建服务脚本文件 `sudo vim /etc/init.d/talk_to_me`
```shell script
#!/bin/sh
### BEGIN INIT INFO
# Provides:          talk_to_me
# Required-Start:    $remote_fs $syslog
# Required-Stop:     $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: power by LeechBox
# Description:       talk wit me, show you tts
### END INIT INFO
# -*- coding: utf-8 -*-
# LeechBox™ talk to me
# Copyright © 2020 afterloe liu (605728727@qq.com)

case "${1:-}" in
  stop|reload|restart|force-reload)
        echo "Stopping app."
	;;
  start)
        echo "Starting talk to me."
        cd /usr/local/talk_to_me && nohup ./main -m d > /tmp/tts.log 2>&1 &
	;;
  *)
        echo "Usage: ${0:-} {start|stop|status|restart|reload|force-reload}" >&2
        exit 1
        ;;
esac
```
2. 赋予执行权限`sudo chmod +x talk_to_me`
3. 设置自启动
```commandline
sudo update-rc.d talk_to_me defaults
sudo systemctl daemon-reload
sudo systemctl start talk_to_me
sudo systemctl enable talk_to_me
```
4. 测试 `sudo shutdown -r now`


#### 备忘: python编译生成应用
pyinstaller的命令描述

| 参数名称 | 描述 |
| :------ | :------ |
| -F, –onefile | 打包一个单个文件，如果你的代码都写在一个.py文件的话，可以用这个，如果是多个.py文件就别用 |
| -D, –onedir | 打包多个文件，在dist中生成很多依赖文件，适合以框架形式编写工具代码，我个人比较推荐这样，代码易于维护 |
| -K, –tk | 在部署时包含 TCL/TK  |
| -a, –ascii | 不包含编码.在支持Unicode的python版本上默认包含所有的编码.  |
| -d, –debug | 产生debug版本的可执行文件  |
| -w,–windowed,–noconsole | 使用Windows子系统执行.当程序启动的时候不会打开命令行(只对Windows有效)  |
| -c,–nowindowed,–console | 使用控制台子系统执行(默认)(只对Windows有效); pyinstaller -c xxxx.py; pyinstaller xxxx.py --console  |
| -s,–strip | 可执行文件和共享库将run through strip.注意Cygwin的strip往往使普通的win32 Dll无法使用.  |
| -X, –upx | 如果有UPX安装(执行Configure.py时检测),会压缩执行文件(Windows系统中的DLL也会)(参见note)  |
| -o DIR, –out=DIR | 指定spec文件的生成目录,如果没有指定,而且当前目录是PyInstaller的根目录,会自动创建一个用于输出(spec和生成的可执行文件)的目录.如果没有指定,而当前目录不是PyInstaller的根目录,则会输出到当前的目录下.  |
| -p DIR, –path=DIR | 设置导入路径(和使用PYTHONPATH效果相似).可以用路径分割符(Windows使用分号,Linux使用冒号)分割,指定多个目录.也可以使用多个-p参数来设置多个导入路径，让pyinstaller自己去找程序需要的资源  |
| –icon=<FILE.ICO> | 将file.ico添加为可执行文件的资源(只对Windows系统有效)，改变程序的图标 pyinstaller -i ico路径 xxxxx.py  |
| –icon=<FILE.EXE,N> | 将file.exe的第n个图标添加为可执行文件的资源(只对Windows系统有效)  |
| -v FILE, –version=FILE | 将verfile作为可执行文件的版本资源(只对Windows系统有效)  |
| -n NAME, –name=NAME | 可选的项目(产生的spec的)名字.如果省略,第一个脚本的主文件名将作为spec的名字  |
| --key | 用于加密Python字节码的密钥 |


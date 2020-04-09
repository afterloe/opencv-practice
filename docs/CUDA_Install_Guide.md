CUDA 安装手册
===
> create by [afterloe](605728727@qq.com)   
> version is 1.1  
> MIT License  

CUDA 是nividia推出的显卡计算扩展，支持linux、windows、macos等平台安装，被各大计算框架使用如Tensorflow、keras使用，
以下是个各平台的安装手册。

<a href="#linux">Linux平台</a>  
> Ubuntu 18.04, Ubuntu 19.10 通用

<a href="#Windows">Windows平台</a>  
<a href="#MacOS">MacOS平台</a>

### <a id="linux"> Linux </a>

#### 卸载之前安装的CUDA
```commandline
sudo dpkg -l cuda-repo-ubuntu1804-10-0-local-10.0.130-410.48
sudo dpkg -r cuda
sudo dpkg -r cudnn
cd /var
rm -rf cuda*
cd /etc/apt/sources.list
rm -rf cuda*
sudo apt-key add /var/cuda-repo-<version>/7fa2af80.pub
sudo apt update && sudo apt upgrade
```
> 卸载还有bug，尝试需谨慎

#### Ubuntu 18.04
1.确认显卡驱动
```commandline
dpkg -l | grep -i nvidia

ii  nvidia-driver-430                  430.50-0ubuntu2  amd64   NVIDIA driver metapackage
ii  nvidia-kernel-common-418:amd64     430.50-0ubuntu2  amd64   Transitional package for nvidia-kernel-common-430
```
会显示出nvidia显卡驱动的版本, 需要注意的是，一台机器不能同时安装多个驱动，会出现桌面无法加载的情况，所以在切换驱动或驱动错误的时候，
需要卸载其他的驱动，卸载代码如下:
```commandline
su
apt remove --purge nvidia-*
```
或输入`dpkg -l | grep -i nvidia`中需要卸载的属性，进行驱动操作后需要进行`shutdown -r now`的重启操作。
> 注: 若启动后无法进入桌面，执行`sudo apt-get install ubuntu-desktop`

搜索合适当前显卡的驱动，并安装
```commandline
ubuntu-drivers devices

== /sys/devices/pci0000:00/0000:00:01.0/0000:01:00.0 ==
modalias : pci:v000010DEd00001C82sv00001043sd000085D6bc03sc00i00
vendor   : NVIDIA Corporation
model    : GP107 [GeForce GTX 1050 Ti]
driver   : nvidia-driver-435 - distro non-free recommended
driver   : nvidia-driver-430 - distro non-free
driver   : nvidia-driver-390 - distro non-free
driver   : xserver-xorg-video-nouveau - distro free builtin

su
apt install nvidia-driver-435
shutdown -r now
```
重启后检查显卡驱动是否生效
```commandline
sudo nvidia-smi
Fri Apr  3 17:34:44 2020
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 430.50       Driver Version: 430.50       CUDA Version: 10.1     |
|-------------------------------+----------------------+----------------------+
| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
|===============================+======================+======================|
|   0  GeForce GTX 105...  Off  | 00000000:01:00.0  On |                  N/A |
| 30%   25C    P8    N/A /  75W |    331MiB /  4036MiB |      0%      Default |
+-------------------------------+----------------------+----------------------+
+-----------------------------------------------------------------------------+
| Processes:                                                       GPU Memory |
|  GPU       PID   Type   Process name                             Usage      |
|=============================================================================|
|    0      1017      G   /usr/lib/xorg/Xorg                            18MiB |
|    0      1577      G   /usr/lib/xorg/Xorg                            59MiB |
|    0      1788      G   /usr/bin/gnome-shell                         133MiB |
+-----------------------------------------------------------------------------+
```
表明显卡安装完成，官方会显示出显卡的版本为`430.50`

2.安装CUDA Toolkit
登录[Nvidia官方网站](https://developer.nvidia.com/cuda-toolkit-archive)下载CUDA Toolkit， 对于CUDA版本选择按应用场景来选择，
本人由于使用的是TensorFlow 2.1.0，该版本最低支持CUDA 10.1，所以我下的是`CUDA 10.1`版本，
各版本对应的显卡支持如[下表](https://docs.nvidia.com/cuda/cuda-toolkit-release-notes/index.html)：

CUDA Toolkit | Linux x86_64 Driver Version | Windows x86_64 Driver Version
:----------- | :-------------------------: | :---------------------------:
CUDA 10.2.89 | &gt;= 440.33 | &gt;= 441.22
CUDA 10.1 (10.1.105 general release, and updates) | &gt;= 418.39 | &gt;= 418.96
CUDA 10.0.130 | &gt;= 410.48 | &gt;= 411.31
CUDA 9.2 (9.2.148 Update 1) | &gt;= 396.37 | &gt;= 398.26
CUDA 9.2 (9.2.88) | &gt;= 396.26 | &gt;= 397.44
CUDA 9.1 (9.1.85) | &gt;= 390.46 | &gt;= 391.29
CUDA 9.0 (9.0.76) | &gt;= 384.81 | &gt;= 385.54
CUDA 8.0 (8.0.61 GA2) | &gt;= 375.26 | &gt;= 376.51
CUDA 8.0 (8.0.44) | &gt;= 367.48 | &gt;= 369.30
CUDA 7.5 (7.5.16) | &gt;= 352.31 | &gt;= 353.66
CUDA 7.0 (7.0.28) | &gt;= 346.46 | &gt;= 347.62

所以`430.50`版本的可以安装CUDA 10.1的版本，安装命令主要参考[下载网站](https://developer.nvidia.com/cuda-toolkit-archive)的提示  
```
wget https://developer.nvidia.com/compute/cuda/10.1/Prod/local_installers/cuda-repo-ubuntu1804-10-1-local-10.1.105-418.39_1.0-1_amd64.deb
sudo dpkg -i cuda-repo-ubuntu1804-10-1-local-10.1.105-418.39_1.0-1_amd64.deb

cuda-repo-<version>

sudo apt-key add /var/cuda-repo-<version>/7fa2af80.pub
sudo apt-get update
sudo apt-get install cuda
```

3.配置CUDA环境变量
```
vim ~/.profile

export CUDA_HOME=/usr/local/cuda 
export PATH=$PATH:$CUDA_HOME/bin 
export LD_LIBRARY_PATH=/usr/local/cuda-10.1/lib64${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}

source ~/.profile
```

4.测试CUDA  
```commandline
cd /usr/local/cuda/samples/1_Utilities/deviceQuery 
sudo make
./deviceQuery

./deviceQuery Starting...

 CUDA Device Query (Runtime API) version (CUDART static linking)

Detected 1 CUDA Capable device(s)

Device 0: "GeForce GTX 1050 Ti"
  CUDA Driver Version / Runtime Version          10.1 / 10.1
  CUDA Capability Major/Minor version number:    6.1
  Total amount of global memory:                 4037 MBytes (4233035776 bytes)
  ( 6) Multiprocessors, (128) CUDA Cores/MP:     768 CUDA Cores
  GPU Max Clock rate:                            1392 MHz (1.39 GHz)
  Memory Clock rate:                             3504 Mhz
  Memory Bus Width:                              128-bit
  L2 Cache Size:                                 1048576 bytes
  Maximum Texture Dimension Size (x,y,z)         1D=(131072), 2D=(131072, 65536), 3D=(16384, 16384, 16384)
  Maximum Layered 1D Texture Size, (num) layers  1D=(32768), 2048 layers
  Maximum Layered 2D Texture Size, (num) layers  2D=(32768, 32768), 2048 layers
  Total amount of constant memory:               65536 bytes
  Total amount of shared memory per block:       49152 bytes
  Total number of registers available per block: 65536
  Warp size:                                     32
  Maximum number of threads per multiprocessor:  2048
  Maximum number of threads per block:           1024
  Max dimension size of a thread block (x,y,z): (1024, 1024, 64)
  Max dimension size of a grid size    (x,y,z): (2147483647, 65535, 65535)
  Maximum memory pitch:                          2147483647 bytes
  Texture alignment:                             512 bytes
  Concurrent copy and kernel execution:          Yes with 2 copy engine(s)
  Run time limit on kernels:                     Yes
  Integrated GPU sharing Host Memory:            No
  Support host page-locked memory mapping:       Yes
  Alignment requirement for Surfaces:            Yes
  Device has ECC support:                        Disabled
  Device supports Unified Addressing (UVA):      Yes
  Device supports Compute Preemption:            Yes
  Supports Cooperative Kernel Launch:            Yes
  Supports MultiDevice Co-op Kernel Launch:      Yes
  Device PCI Domain ID / Bus ID / location ID:   0 / 1 / 0
  Compute Mode:
     < Default (multiple host threads can use ::cudaSetDevice() with device simultaneously) >

deviceQuery, CUDA Driver = CUDART, CUDA Driver Version = 10.1, CUDA Runtime Version = 10.1, NumDevs = 1
Result = PASS
```
> 在Ubuntu 18.04 版本，CUDA 10.0 安装后会出现一个神奇的bug，在GNOME下就是桌面卡死，鼠标、键盘不能动，折腾了一番之后又莫名其妙的恢复了，
> 有执行过 `sudo apt install xserver-xorg-input-all` 和 `sudo apt-get install ubuntu-desktop` 两条命令。

5.配置cuDNN模块  

[官方网站](https://developer.nvidia.com/rdp/cudnn-download)下载对应版本的cuDNN Runtime Library 并安装
```
wget https://developer.nvidia.com/compute/machine-learning/cudnn/secure/7.6.5.32/Production/10.1_20191031/Ubuntu18_04-x64/libcudnn7_7.6.5.32-1%2Bcuda10.1_amd64.deb
sudo dpkg -i libcudnn7_7.6.5.32-1+cuda10.1_amd64.deb
```

6.TensorFlow 测试

```
python3
Python 3.7.5 (default, Nov 20 2019, 09:21:52)
[GCC 9.2.1 20191008] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from tensorflow.python.client import device_lib as _device_lib
>>> local_device_protos = _device_lib.list_local_devices()
 CPU Frequency: 3999980000 Hz
 XLA service 0x507c710 initialized for platform Host (this does not guarantee that XLA will be used). Devices:
 StreamExecutor device (0): Host, Default Version
 Successfully opened dynamic library libcuda.so.1
 successful NUMA node read from SysFS had negative value (-1), but there must be at least one NUMA node, so returning NUMA node zero
 XLA service 0x5112ee0 initialized for platform CUDA (this does not guarantee that XLA will be used). Devices:
 StreamExecutor device (0): GeForce GTX 1050 Ti, Compute Capability 6.1
 pciBusID: 0000:01:00.0 name: GeForce GTX 1050 Ti computeCapability: 6.1
 coreClock: 1.392GHz coreCount: 6 deviceMemorySize: 3.94GiB deviceMemoryBandwidth: 104.43GiB/s
 physical GPU (device: 0, name: GeForce GTX 1050 Ti, pci bus id: 0000:01:00.0, compute capability: 6.1)
>>> [x.name for x in local_device_protos if x.device_type == 'GPU']
['/device:GPU:0']
```

### <a id="windows"> Windows </a>
#### Windows 10

安装步骤同上，本处简写
* 安装Navida GPU驱动，驱动下载地址:https://www.nvidia.com/drivers
* 安装CUDA Toolkit，TensorFlow >= 2.1.0 需要安装CUDA 10.1，下载地址: https://developer.nvidia.com/cuda-toolkit-archive
* 安装cuDNN SDK，版本大于7.6，下载地址: https://developer.nvidia.com/cudnn
> * [可选] TensorRT 6.0 这个框架是Navida提出的，据说运行速度相当快，参考地址: https://docs.nvidia.com/deeplearning/sdk/tensorrt-install-guide/index.html

配置环境变量对`cudnn-10.1-windows10-x64-v7.6.5.32.zip`进行解，解压后在`G:/cudnn`, cuad为默认安装，配置环境变量如下：
```
SET PATH=C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v10.1\bin;%PATH%
SET PATH=C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v10.1\extras\CUPTI\libx64;%PATH%
SET PATH=C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v10.1\include;%PATH%
SET PATH=G:\cudnn\cuda\bin;%PATH%
```

检测步骤如上

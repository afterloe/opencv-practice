CUDA 安装手册
===
> create by [afterloe](605728727@qq.com)   
> version is 1.1  
> MIT License  

CUDA 是nividia推出的显卡计算扩展，支持linux、windows、macos等平台安装，以下是个各平台的安装手册。

### Linux
#### Ubuntu 18.04
1.确认显卡驱动
```commandline
dpkg -l | grep -i nvidia

ii  nvidia-driver-430                               430.50-0ubuntu2                        amd64        NVIDIA driver metapackage
ii  nvidia-kernel-common-418:amd64                  430.50-0ubuntu2                        amd64        Transitional package for nvidia-kernel-common-430
```
会显示出nvidia显卡驱动的版本, 若需要卸载则继续执行如下代码:
```commandline
su
apt remove --purge nvidia-*
```
> 若启动后无法进入桌面，执行`sudo apt-get install ubuntu-desktop`
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
```
执行这条命令会显示出合适的显卡驱动，选择合适的进行安装。
```commandline
su
apt install nvidia-driver-435
shutdown -r now
```
检查显卡驱动是否生效
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

2.登录[Nvidia官方网站](https://developer.nvidia.com/cuda-toolkit-archive)下载CUDA Toolkit， 对于版本而言，本人使用的是TensorFlow 2.1.0，该版本最低支持CUDA 10.1，所以我下的是`CUDA 10.1`版本，
各版本对应的显卡支持如[下表](https://docs.nvidia.com/cuda/cuda-toolkit-release-notes/index.html)：

3.安装CUDnn模块，可以在[官方网站](https://developer.nvidia.com/rdp/cudnn-download)下载
4.配置环境变量
```
export CUDA_HOME=/usr/local/cuda 
export PATH=$PATH:$CUDA_HOME/bin 
export LD_LIBRARY_PATH=/usr/local/cuda-10.1/lib64${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}
```
5.测试
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

python3中tensorflow测试
```
afterloe@leechbox-king:/usr/local/cuda/samples/1_Utilities/deviceQuery$ python3
Python 3.7.5 (default, Nov 20 2019, 09:21:52)
[GCC 9.2.1 20191008] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from tensorflow.python.client import device_lib as _device_lib
2020-04-03 17:41:37.198959: W tensorflow/stream_executor/platform/default/dso_loader.cc:55] Could not load dynamic library 'libnvinfer.so.6'; dlerror: libnvinfer.so.6: cannot open shared object file: No such file or directory; LD_LIBRARY_PATH: /usr/local/cuda-10.1/lib64
2020-04-03 17:41:37.199018: W tensorflow/stream_executor/platform/default/dso_loader.cc:55] Could not load dynamic library 'libnvinfer_plugin.so.6'; dlerror: libnvinfer_plugin.so.6: cannot open shared object file: No such file or directory; LD_LIBRARY_PATH: /usr/local/cuda-10.1/lib64
2020-04-03 17:41:37.199029: W tensorflow/compiler/tf2tensorrt/utils/py_utils.cc:30] Cannot dlopen some TensorRT libraries. If you would like to use Nvidia GPU with TensorRT, please make sure the missing libraries mentioned above are installed properly.
>>> local_device_protos = _device_lib.list_local_devices()
2020-04-03 17:41:49.657680: I tensorflow/core/platform/cpu_feature_guard.cc:142] Your CPU supports instructions that this TensorFlow binary was not compiled to use: AVX2 FMA
2020-04-03 17:41:49.685775: I tensorflow/core/platform/profile_utils/cpu_utils.cc:94] CPU Frequency: 3999980000 Hz
2020-04-03 17:41:49.686129: I tensorflow/compiler/xla/service/service.cc:168] XLA service 0x507c710 initialized for platform Host (this does not guarantee that XLA will be used). Devices:
2020-04-03 17:41:49.686154: I tensorflow/compiler/xla/service/service.cc:176]   StreamExecutor device (0): Host, Default Version
2020-04-03 17:41:49.688202: I tensorflow/stream_executor/platform/default/dso_loader.cc:44] Successfully opened dynamic library libcuda.so.1
2020-04-03 17:41:49.751144: I tensorflow/stream_executor/cuda/cuda_gpu_executor.cc:981] successful NUMA node read from SysFS had negative value (-1), but there must be at least one NUMA node, so returning NUMA node zero
2020-04-03 17:41:49.751414: I tensorflow/compiler/xla/service/service.cc:168] XLA service 0x5112ee0 initialized for platform CUDA (this does not guarantee that XLA will be used). Devices:
2020-04-03 17:41:49.751428: I tensorflow/compiler/xla/service/service.cc:176]   StreamExecutor device (0): GeForce GTX 1050 Ti, Compute Capability 6.1
2020-04-03 17:41:49.751535: I tensorflow/stream_executor/cuda/cuda_gpu_executor.cc:981] successful NUMA node read from SysFS had negative value (-1), but there must be at least one NUMA node, so returning NUMA node zero
2020-04-03 17:41:49.751731: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1555] Found device 0 with properties:
pciBusID: 0000:01:00.0 name: GeForce GTX 1050 Ti computeCapability: 6.1
coreClock: 1.392GHz coreCount: 6 deviceMemorySize: 3.94GiB deviceMemoryBandwidth: 104.43GiB/s
2020-04-03 17:41:49.751869: I tensorflow/stream_executor/platform/default/dso_loader.cc:44] Successfully opened dynamic library libcudart.so.10.1
2020-04-03 17:41:49.752984: I tensorflow/stream_executor/platform/default/dso_loader.cc:44] Successfully opened dynamic library libcublas.so.10
2020-04-03 17:41:49.753773: I tensorflow/stream_executor/platform/default/dso_loader.cc:44] Successfully opened dynamic library libcufft.so.10
2020-04-03 17:41:49.753941: I tensorflow/stream_executor/platform/default/dso_loader.cc:44] Successfully opened dynamic library libcurand.so.10
2020-04-03 17:41:49.755073: I tensorflow/stream_executor/platform/default/dso_loader.cc:44] Successfully opened dynamic library libcusolver.so.10
2020-04-03 17:41:49.755905: I tensorflow/stream_executor/platform/default/dso_loader.cc:44] Successfully opened dynamic library libcusparse.so.10
2020-04-03 17:41:49.758490: I tensorflow/stream_executor/platform/default/dso_loader.cc:44] Successfully opened dynamic library libcudnn.so.7
2020-04-03 17:41:49.758579: I tensorflow/stream_executor/cuda/cuda_gpu_executor.cc:981] successful NUMA node read from SysFS had negative value (-1), but there must be at least one NUMA node, so returning NUMA node zero
2020-04-03 17:41:49.758835: I tensorflow/stream_executor/cuda/cuda_gpu_executor.cc:981] successful NUMA node read from SysFS had negative value (-1), but there must be at least one NUMA node, so returning NUMA node zero
2020-04-03 17:41:49.759021: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1697] Adding visible gpu devices: 0
2020-04-03 17:41:49.759047: I tensorflow/stream_executor/platform/default/dso_loader.cc:44] Successfully opened dynamic library libcudart.so.10.1
2020-04-03 17:41:49.759544: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1096] Device interconnect StreamExecutor with strength 1 edge matrix:
2020-04-03 17:41:49.759555: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1102]      0
2020-04-03 17:41:49.759560: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1115] 0:   N
2020-04-03 17:41:49.759632: I tensorflow/stream_executor/cuda/cuda_gpu_executor.cc:981] successful NUMA node read from SysFS had negative value (-1), but there must be at least one NUMA node, so returning NUMA node zero
2020-04-03 17:41:49.759849: I tensorflow/stream_executor/cuda/cuda_gpu_executor.cc:981] successful NUMA node read from SysFS had negative value (-1), but there must be at least one NUMA node, so returning NUMA node zero
2020-04-03 17:41:49.760055: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1241] Created TensorFlow device (/device:GPU:0 with 3351 MB memory) -> physical GPU (device: 0, name: GeForce GTX 1050 Ti, pci bus id: 0000:01:00.0, compute capability: 6.1)
>>> [x.name for x in local_device_protos if x.device_type == 'GPU']
['/device:GPU:0']
>>>
```
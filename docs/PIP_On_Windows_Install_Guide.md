# Install PIP on Windows
> create by [afterloe](lm6289511@gmail.com)  
> MIT License  
> version is 1.0

## Pre-flight Check
Before you can install Pip on your server, you’ll need to confirm that **Python** is installed.  

The simplest way to test for a Python installation on your Windows server is to open a command prompt (click on the Windows icon and type **cmd**, then click on the command prompt icon). Once a command prompt window opens, type **python** and press **Enter**. If Python is installed correctly, you should see output similar to what is shown below:
```cmd
where python
C:\Users\afterloe\AppData\Local\Microsoft\WindowsApps\python.exe
D:\Program Files\Python38-32\python.exe

Python 3.7.0 (v3.7.0:1bf9cc5093, Jun 27 2018, 04:59:51) [MSC v.1914 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
```

Python is either not installed or the system variable path hasn’t been set. You’ll need to either launch Python from the folder in which it is installed or adjust your system variables to allow Python to be launched from any location. click [here](https://www.python.org/downloads/windows/) to download python.

## Installing Pip
Once you’ve confirmed that Python is correctly installed, you can proceed with installing Pip.
* Download [get-pip.py](https://bootstrap.pypa.io/get-pip.py), or see this in my [github](https://github.com/afterloe/opencv-practice/tree/master/tools).
* Run the following command:
```cmd
python get-pip.py
```
* Pip is now installed!

## Check and Verify
You can verify that Pip was installed correctly by opening a command prompt and entering the following command:
```cmd
pip -v
```

## Where the pip install
You should see output similar to the following:
```
pip 18.0 from c:\users\administrator\appdata\local\programs\python\python37\lib\site-packages\pip (python 3.7)
```
Now that Pip is installed and configured, you can begin using it to manage your Python packages. 

## accelerate the pip
```
pip3 install pip --upgrade
pip3 config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
```
if pip network is down, please use this code: `pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple pip --upgrade`

# dlib install
> create by [afterloe](605728727@qq.com)  
> version is 1.0.0  
> MIT License

## Step #1: Install dlib requisites
[Boost](https://www.boost.org/): Boost is a collection of peer-reviewed (i.e., very high quality) C++ libraries that help programmers not get caught up in reinventing the wheel. Boost provides implementations for linear algebra, multithreading, basic image processing, and unit testing, just to name a few.  
[Boost.Python](https://www.boost.org/doc/libs/1_57_0/libs/python/doc/index.html): As the name of this library suggests, Boost.Python provides interoperability between the C++ and Python programming language.  
[CMake](https://cmake.org/): CMake is an open-source, cross-platform set of tools used to build, test, and package software. You might already be familiar with CMake if you have used it to compile OpenCV on your system.  
[X11/XQuartx](https://www.xquartz.org/): Short for “X Window System”, X11 provides a basic framework for GUI development, common on Unix-like operating systems. The macOS/OSX version of X11 is called XQuartz.  

### Ubuntu
```shell script
sudo apt-get install build-essential cmake
sudo apt-get install libgtk-3-dev
sudo apt-get install libboost-all-dev
```

### macOS
```shell script
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
brew update
nano ~/.bash_profile

# Homebrew
export PATH=/usr/local/bin:$PATH

source ~/.bash_profile

brew install python
brew install python3
brew install cmake
brew install boost
brew install boost-python --with-python3
brew list | grep 'boost'
```

## Step #2: Access your Python virtual environment (optional)
```shell script
workon <your virtualenv name>
workon cv
mkvirtualenv py2_dlib
mkvirtualenv py3_dlib -p python3
```

## Step #3: Install dlib with Python bindings
```shell script
pip install numpy
pip install scipy
pip install scikit-image
pip install dlib
```

## Step #4: Test out your dlib install
```shell script
python
Python 3.6.0 (default, Mar  4 2017, 12:32:34) 
[GCC 4.2.1 Compatible Apple LLVM 8.0.0 (clang-800.0.42.1)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> import dlib
>>>
```

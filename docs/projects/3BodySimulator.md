---
title: 3BodySimulator
categories:
  - Projects
date: 2025-05-23 14:18:21
excerpt: C++简易项目：使用C++实现三体运动的核心逻辑，Python负责可视化部分；使用vcpkg进行C++包管理；使用CMake进行项目构建。本文主要记录整个项目的构建过程，代码逻辑与实现细节后续视情况完善。
authors:
  - virtualguard101
tags:
  - CPP
  - Python
  - 项目构建
  - Projects
---

## 导言
近期刚刚结束[CS106L | Standard C++ features and syntax](https://web.stanford.edu/class/cs106l/)的学习，想借此机会完善一下对C++项目构建的学习，如`CMake`等构建工具的使用，故立此项。

通过本次项目你会了解到：

- 1. [C++](../obsidian/ProgrammingLanguage/cpp/cs106l/初始化与引用操作.md)项目标准化基础

- 2. [CMake](../obsidian/Tools/BuildTools/CMake.md)、[vcpkg](../obsidian/Tools/BuildTools/vcpkg.md)等C++构建工具的基本使用

- 3. 多语言配合构建（C++ & Python）

下面是完成此次项目所需的基本条件：

- C++ 编译器

- [Git](../obsidian/Tools/Git.md)：版本控制

- [CMake(*>= v3.22*)](https://cmake.org/documentation/)：C++构建工具

- [vcpkg](https://learn.microsoft.com/zh-cn/vcpkg/)：C++包管理工具

- [Python(*>= v3.12*)](https://www.python.org/)：可视化模块

- [uv](../obsidian/Tools/Astral%20uv.md)：Python包管理工具

文中的构建平台为**Ubuntu22.04**

此次项目注重C++项目的标准化以及构建工具（`vcpkg`、`CMake`）的使用，代码逻辑部分主体由`DeepSeek`、`ChatGPT`等AI大模型完成。

- 项目仓库：[3BodySimulator](https://github.com/virtualguard101/3BodySimulator)

<!-- more -->

## 初始化项目

首先使用两个语言的包管理器分别对项目进行初始化：

### `vcpkg`

```bash
vcpkg new --application
```

对生成的`vcpkg.json`进行配置：

```json
{
    "name": "three-body-simulator",
    "version-string": "0.1.0",
    "dependencies": [
        {
            "name": "python3",
            "version>=": "3.12.9"
        },
        "pybind11"
    ],
    "builtin-baseline": "a337f5fe100f83026072765ea63a8776f984f6fd"
}
```

>注意所有键值对的内容只能包含**小写字母**，否则后续构建时会报错。

### `uv`

```bash
uv init
```

将项目信息写入`pyproject.toml`
```js
[project]
name = "3BodySimulator"
version = "0.1.0"
description = "The visualization simulation of three-body motion implemented using C++ & Python."
readme = "README.md"
requires-python = ">=3.12"
dependencies = [
    "matplotlib>=3.8.0",
    "ninja>=1.11.1",
    "numpy>=1.26.0",
    "pybind11>=2.11.1",
    "pygame>=2.6.1",
]
```

随后去除无用的生成配置即可。

随后对项目结构初始化：

### 项目结构
```bash
.
├── build.sh              # build shell script
├── CMakeLists.txt        # CMake build config(outer)
├── CMakePresets.json     # vcpkg CMake toolchain config(public)
├── CMakeUserPresets.json # vcpkg CMake toolchain config(private)
├── LICENSE
├── pyproject.toml        # Python project config
├── python                # Python script folder
│   ├── dynamic.py
│   ├── example.json      # example input json data
│   ├── pyonly.py
│   └── visualize.py
├── README.md
├── requirements.txt      # Python dependencies
├── src                   # C++ source folder
│   ├── CMakeLists.txt    # CMake build config(inner)
│   ├── three_body.cpp
│   └── three_body.h
├── uv.lock
├── vcpkg-configuration.json
└── vcpkg.json            # vcpkg dependencies config
```

## 代码实现

这部分并不是我们本次项目的重点，故使用了大语言模型（[chatGPT](https://chatgpt.com/)）负责该部分的实现与完善。~~绝对不是我想偷懒😋~~

其中采用的技术栈在项目的[README](https://github.com/virtualguard101/3BodySimulator?tab=readme-ov-file#tech-stack-in-this-project)中有详细的总结。后续会视情况完善对这一部分的学习和解构。

在实现的代码源文件中，我们使用C++作为**底层物理引擎**的构建语言，使用Python作为**主程序语言**并负责**可视化与用户交互**。二者的源文件分别位于项目根目录的`src`和`python`文件夹下。

## 项目构建

接下来进入本项目的重点。

创建本次项目的主要目的是为学习**CMake**和**vcpkg**的基本使用，故将项目构建配置的部分视为重点。

本项目使用`CMake` & `vcpkg`工具链进行C++的构建，使用`uv`进行Python的依赖与项目管理，可遵循『**获取依赖→配置→编译→虚拟环境运行**』的流程对项目进行构建与测试运行：

### 获取依赖

类似Python的`pip`，`vcpkg`是一个相对简单易用的cpp包管理工具（虽然但是各种配置还是让人用的很难受🙃，毕竟C++的生态就这样），在该项目中，我们将使用它相对容易地获取项目所需的相关依赖。

安装就不再赘述，详情参考[官方文档](https://learn.microsoft.com/zh-cn/vcpkg/)，注意记住自己安装的路径，以便后续工具链的配置。

- 编辑依赖列表

在本项目中，我们选择使用C++配合Python完成模拟实现。chatGPT给出的实现思路是**使用cpp实现天体运动的底层物理引擎，构建输出一个Python可直接调用的共享库（`.so`/`.pyd`），然后由Python在可视化实现中直接调用**。

因此，在C++模块的实现中，我们需要使用[pybind11](https://pybind11.readthedocs.io/en/stable/basics.html)联系二者。

>`pybind11`是一个轻量级的库，用于将C++代码绑定到Python中，使得Python能够调用cpp的高性能代码。

为了引入`pybind11`，我们就需要通过配置`vcpkg.json`的依赖列表使得后续运行构建时能够导入它。

在**初始化项目**的过程中，我们已经对`vcpkg.json`进行了配置。是的，那就是所谓的**依赖列表**。根据[官方文档](https://learn.microsoft.com/zh-cn/vcpkg/get_started/get-started?pivots=shell-bash#3---add-dependencies-and-project-files)的描述，也可通过`port`命令添加依赖：
```bash
vcpkg add port pybind11
```

### 构建配置

这是该项目中最为重要的一步，主要的工作简单来说就是配置`CMakeLists.txt`。

由于我们使用了第三方工具`vcpkg`作为包管理工具，合理配置这二者之间的工具链关系就尤为关键。

我们配置的思路是，在项目的根目录和用于存放C++模块的`src`中分别创建一个`CMakeLists.txt`。前者用于配置CMake在构建过程中与vcpkg的工具链参数；后者则专门用于配置cpp模块的构建逻辑。

由此便有了以下配置：

`CMakeLists.txt`:
```bash
# 项目基本参数
cmake_minimum_required(VERSION 3.20)
project(3BodySimulator LANGUAGES CXX)

# 使用 vcpkg 的 Toolchain
if(NOT DEFINED CMAKE_TOOLCHAIN_FILE)
  set(
    CMAKE_TOOLCHAIN_FILE "~/vcpkg/scripts/buildsystems/vcpkg.cmake"
    DPython3_EXECUTABLE=$(which python)
    DCMAKE_BUILD_TYPE=Release
    CACHE STRING ""
  )
endif()

# 把 src 子目录加入构建
add_subdirectory(src)
```

`src/CMakeLists.txt`:
```bash
# 查找 pybind11（由 vcpkg 安装并集成）
find_package(pybind11 CONFIG REQUIRED)

# 源文件列表
pybind11_add_module(three_body
  three_body.cpp
)

# 设置头文件路径
target_include_directories(three_body
  PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}
)

# 设置 C++17 标准
target_compile_features(three_body PUBLIC cxx_std_17)

# 把生成的共享库 (.so/.pyd) 放到 ../python 目录
set_target_properties(three_body PROPERTIES
  LIBRARY_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/python
  OUTPUT_NAME "three_body"    # 忽略 ABI tag，统一输出 three_body.so
  PREFIX ""                   # 无前缀
  SUFFIX ".so"                # 强制后缀 .so
)
```

正常情况下，按照以上构建配置，只需执行如下命令即可进行C++模块的构建生成与编译：
```bash
# 配置生成
cmake --preset=vcpkg
# 编译生成.so
cmake --build build/
```

如果不出意外的话，cmake会在`python`路径下生成一个名为`three_body`的`.so`共享库（为了方便调用，故将共享库生成到与py脚本相同的目录下）。事实上，到这里，我们的项目就可以直接通过`python`命令直接运行了（当然，前提是你的Python依赖没有问题）。

~~uv：世界，遗忘我...🙃~~

### `uv`Python虚拟环境配置

虽然完成了C++模块的构建工作基本就意味着项目能够跑起来了，但Python混乱的环境依赖问题在某些时候是出了名的让人头痛。为了避免这一情况，我们需要创建一个虚拟环境来运行我们的项目，为此，我们选择了[uv](https://docs.astral.sh/uv/)作为该项目的Python包管理器。

>`uv`是一个由`Rust`编写的高性能Python包管理工具，其安装速度比传统工具要快上不少，同时还支持并行安装。
>
>更重要的是，它提供了一种十分便捷和强大的**项目依赖管理**与**虚拟环境管理**方式。

在初始化项目的过程中，我们已经使用其进行了项目信息的初始化配置，接下来，我们将继续使用它轻松地配置和运行我们的项目：

- 创建Python虚拟环境并激活
```bash
uv venv .venv         # 默认为系统 Python3.12
source .venv/bin/activate
```

- 在虚拟环境中安装依赖
```bash
uv pip install -r requirements.txt
```

安装好依赖后，我们就可以在虚拟环境中完美地运行我们的项目了：
```bash
uv run python/dynaminc.py
```

### 自动化构建脚本

说了这么一堆，有人可能要问了：这么多的构建命令，还挺麻烦的，而且如果不小心搞乱了不就完犊子了？难道就没有方便的构建方式吗？

有的兄弟，有的。

事实上，我们上面讲解的构建顺序本身就有点问题：

如果观察仔细的话，应该会注意到，前文中根目录下的`CMakeLists.txt`中在配置工具链时指定了一个名为`DPython3_EXECUTABLE`的参数，这个参数的功能是显式指定运行Python脚本的Python解释器，作用是强制保持运行环境的Python版本一致性。如果你在系统上使用与`uv`配置中Python版本不一致的解释器，且没有在构建C++模块前创建并激活Python虚拟环境，那么你在尝试运行项目时就会得到类似下面的报错信息：
```bash
Traceback (most recent call last):
  File "/home/virtualguard/projects/researching/cpp-engine/3BodySimulator/python/visualize.py", line 11, in <module>
    from three_body import Body, step
ImportError: Python version mismatch: module was compiled for Python 3.10, but the interpreter version is incompatible: 3.12.9 (main, Feb 12 2025, 14:50:50) [Clang 19.1.6 ].
```

对于这个问题，我们就需要通过强制规范构建顺序来保证项目自始至终是在我们创建的虚拟环境中构建并运行的，以确保项目环境的一致性；结合前面提到的“方便地构建方法”，我们就可以将众多的构建命令依序整合到一个`bash`脚本中，也就是所谓的**自动化构建脚本**：

`build.sh`:
```bash
#!/bin/bash
set -e

#———————————————
# 1. 清理旧构建
#———————————————
echo "清理旧构建文件..."
rm -rf build python/three_body* .venv/ vcpkg_installed/ vcpkg/

#———————————————
# 2. 创建并激活 uv 虚拟环境（Python 3.12）
#———————————————
echo "创建并激活 Python 3.12 虚拟环境..."
uv venv .venv         # 默认为系统 Python3.12
source .venv/bin/activate

# 安装 Python 可视化脚本依赖
uv pip install -r requirements.txt

#———————————————
# 3. 用 venv 中的 Python 配置 & 编译 C++ 扩展
#———————————————
echo "配置 CMake（指向 venv 中的 python）..."
# cmake -B build \
#   -DCMAKE_TOOLCHAIN_FILE=~/vcpkg/scripts/buildsystems/vcpkg.cmake \
#   -DPython3_EXECUTABLE=$(which python) \
#   -DCMAKE_BUILD_TYPE=Release

cmake --preset=vcpkg

echo "开始编译 C++ 扩展..."
cmake --build build

#———————————————
# 4. 检查生成结果
#———————————————
echo "生成的 Python 模块："
ls -l python/ | grep three_body

#———————————————
# 5. 运行可视化脚本
#———————————————
echo "执行 uv run python/visualize.py 启动三体模拟..."
echo "执行 uv run python/dynamic.py 启动动态模拟..."
```

首先为脚本添加运行权限：
```bash
chmod +x build.sh
```

随后就可以直接通过脚本进行自动化构建了：
```bash
./build.sh
```

此时由于项目环境独立于系统全局的Python环境，构建运行均基于这个虚拟环境，确保了环境的一致性，也就不会出现像上面的环境冲突问题了。

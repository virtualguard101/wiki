---
date: 2025-10-07 01:08:00
title: Python包管理
permalink: 
publish: true
---

# Python 包

> [Python Packages | GeeksforGeeks](https://www.geeksforgeeks.org/python/python-packages/)
>
> [Python Packaging User Guide](https://packaging.python.org/en/latest/overview/)

## 定义

与其他主流编程语言类似，Python 也有将代码组织成模块的机制，即所谓的**包 （*Package*）**。

==包本质上是一个包含 `__init__.py` 文件和一个或多个 Python 文件，即[**模块（*Module*）**](https://packaging.python.org/en/latest/overview/#python-modules)的文件夹==。

!!! note
    这里注意不要将**模块**与**包**的概念混淆，二者的关系可简单理解为，==模块是包的组件==。

包也可以**嵌套组织**，即一个包中可以包含另一个包。

!!! example
    ```bash
    .
    ├── package_a # 包
    │   ├── __init__.py
    │   ├── module_a.py # 模块
    │   └── package_a_1 # 子包
    │       ├── __init__.py
    │       └── module_a_1.py # 模块
    └── package_b # 包
        ├── __init__.py
        ├── module_b.py # 模块
        └── package_b_1 # 子包
            ├── __init__.py
            └── module_b_1.py # 模块
    ```

## 包管理机制

Python包管理机制有着一套完整的体系，用于**组织**、**分发**、**安装**和管理第三方代码库。其包括包的导入系统（import机制）、包索引仓库（如PyPI）、包管理工具（如`pip`、`uv`）和虚拟环境管理。

Python包管理机制通过四层架构解决代码分发问题：

<!-- <div align="center"> -->
```
┌─────────────────────────┐
│   应用层：import语句      ← 开发者视角
├─────────────────────────┤
│  工具层：pip/uv/poetry    ← 包管理器
├─────────────────────────┤
│  仓库层：PyPI/镜像源      ← 中心化存储
├─────────────────────────┤
│  存储层：site-packages    ← 本地文件系统
└─────────────────────────┘
```
<!-- </div> -->

### 导入包与模块

Python 的包管理机制主要通过 `import` 语句来实现。常用的导入形式有两种：`import` 和 `from ... import ...`。

!!! example
    ```python
    import math

    math.sqrt(25)
    ```
    ```py
    from math import sqrt

    sqrt(25)
    ```

也可使用 `as` 关键字给导入的模块或函数起别名，这在导入具有冗长名称的模块或函数时非常有用：

!!! example
    ```python
    import matplotlib.pyplot as plt
    import numpy as np

    x = np.linspace(0, 10, 100)
    y = np.sin(x)

    plt.plot([1, 2, 3, 4])
    plt.show()
    ```

### 包索引仓库

Python 的包索引仓库是一个中心化的存储库，用于存储和分发 Python 包。

!!! info
    中心化存储有个比较致命的问题，就是一旦中心化存储失效或遭受恶意攻击，那么所有的包都将不可用或存在被恶意篡改的风险。如[2022年的ctx恶意包事件](https://portswigger.net/daily-swig/malicious-python-library-ctx-removed-from-pypi-repo#:~:text=A%20malicious%20and%20potentially%20hijacked,issue%20impacting%20Python's%20CTX%20library.)

    因此现在 PyPI 官方采用了十分严格的验证机制，强制要求开发者使用[2FA (Two-Factor Authentication, 两步验证)](https://www.microsoft.com/en-sg/security/business/security-101/what-is-two-factor-authentication-2fa)进行身份验证。

### 包管理工具

包管理工具用于管理项目的依赖项，包括安装、升级、卸载等操作。我目前主要使用的是[uv](../../tools/uv.md)。

!!! info "uv"
    [uv](https://docs.astral.sh/uv/) 是[astral-sh](https://astral.sh/)开发的一个高性能的 Python 包管理工具，其设计理念与[cargo](https://doc.rust-lang.org/cargo/)十分相似。有意思的是， uv 本身也是用 Rust 写的。同时，uv 的目标是成为"Python 的 Cargo"，其提供了十分强大的**项目依赖管理**与**虚拟环境管理**功能，并且其性能也得到了广泛的认可。

### 虚拟环境管理

虚拟环境是包管理的核心机制之一，能解决依赖冲突问题。这里我同样主要使用 [uv](../../tools/uv.md) 进行虚拟环境管理。

### 发布包

> [Building and publishing a package | uv](https://docs.astral.sh/uv/guides/package/)

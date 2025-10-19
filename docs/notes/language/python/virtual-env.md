---
date: 2025-10-19 12:28:52
title: Python虚拟环境
permalink: 
publish: true
---

# Python虚拟环境

## 什么是虚拟环境

虚拟环境是一个独立的Python环境，它有自己的Python解释器、库和包，与系统全局环境隔离。


## 创建虚拟环境

- 使用 [uv](../../tools/uv.md)

    ```bash
    uv venv [ENV_NAME] --python=[PYTHON_VERSION]
    ```

- 使用 [conda](../../tools/conda.md)

    ```bash
    conda create -n [ENV_NAME] python=[PYTHON_VERSION]
    ```

- 使用 [venv](https://docs.python.org/zh-cn/3.14/library/venv.html)

    ```bash
    python -m venv [ENV_NAME]
    ```

## 查看虚拟环境信息

### 虚拟环境列表

- uv

    列出所有虚拟环境
    ```bash
    uv venv list
    ```

    列出所有的Python解释器
    ```bash
    uv python list
    ```

- conda

    ```bash
    conda env list
    ```

### 当前虚拟环境

- `uv run`

    ```bash
    uv run python -c "import sys; print(sys.executable)"
    ```

- shell

    ```bash
    echo $VIRTUAL_ENV
    ```

    ```bash
    which python
    ```

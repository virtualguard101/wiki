---
date: 2026-09-20 00:43:52
title: Python虚拟环境
permalink: 
publish: true
tags:
  - 编程语言
  - Python
---

# Python虚拟环境

## 什么是虚拟环境

虚拟环境是一个独立的Python环境, 它有自己的Python解释器、库和包, 与系统全局环境隔离, 避免不同项目之间的依赖冲突.

部分系统甚至不允许在全局环境中安装第三方包(比如 [Arch Linux](../../../blog/posts/Arch%20Linux安装要点记录.md)), 此时就必须使用虚拟环境来隔离项目依赖.

## 创建虚拟环境

- 使用 [Astral uv](../../Tools/Astral%20uv.md)

    ```bash
    uv venv [ENV_NAME] --python=[PYTHON_VERSION]
    ```

- 使用 [Conda](../../Tools/Conda.md)

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

    项目虚拟环境一般就在目录里的 `.venv`, uv 没有 conda 那种全局 env 列表.

    列出本机 Python 解释器:

    ```bash
    uv python list
    ```

    列出用 `uv tool install` 装过的 CLI:

    ```bash
    uv tool list
    ```

- conda

    ```bash
    conda env list
    ```

### 当前虚拟环境

- `uv run` (走的是当前项目的 `.venv`, 不是 `PATH` 上随便一个可执行文件)

    ```bash
    uv run python -c "import sys; print(sys.executable)"
    ```

- shell

    ```bash
    echo $VIRTUAL_ENV
    which python
    ```

提示符里的 `(env_name)` 只说明 **shell 激活了 env_name**. `which executable` 若指向 `~/.local/bin/executable`, 跑起来用的就不是 env_name.

看一个 CLI 实际绑的是哪套 Python: `which <tool>` 之后读第一行 shebang, 例如 `#!/home/.../uv/tools/<tool>/bin/python`. 然后用**这个**解释器探测:

```bash
~/.local/share/uv/tools/<tool>/bin/python -c "import sys; print(sys.executable); print('\n'.join(sys.path))"
```

## 环境隔离

`import` 只看**当前这个解释器**的 `site-packages`. 系统里有 requirement, `(env_name)` 里 `import requirement` 能过, 都不等于 `executable` 看得见 requirement.

同一台机器上常见几套互不相通的环境:

| 种类 | 典型位置 | 谁在用 |
| --- | --- | --- |
| 系统 Python | `/usr/bin/python`, `pacman` / `apt` 装的包 | 发行版工具, 不是项目依赖 |
| 项目 venv | 仓库里的 `.venv` | `uv run`, `source .venv/bin/activate` |
| conda env | `~/miniconda3/envs/<name>` 一类 | `conda activate lab` 之后的 `python` / `pip` |
| uv tool | `~/.local/share/uv/tools/<工具名>/` | `uv tool install` 装到 `PATH` 的 CLI |
| uvx 临时环境 | `~/.cache/uv/` 下的隔离环境 | `uvx <工具>` 一次性跑; 若该工具已经 `uv tool install` 过, 常会复用那份 |

[uv tool / uvx](https://docs.astral.sh/uv/concepts/tools/) 是故意隔离的: 每个 CLI 一份 venv, 避免不同工具和项目依赖互相污染.

### 装错地方

`ModuleNotFoundError: No module named '<pkg>'` 只说明**当前这个解释器**的 `site-packages` 里没有 `<pkg>`. 在别处装一份, 对它无效.

| 执行的命令 | 实际装到哪 | 报错的那个 CLI / 解释器 |
| --- | --- | --- |
| `uv tool install <tool>` | `.../uv/tools/<tool>/` | 只看见自己这份 |
| `uv tool install <pkg>` | 又一个独立 tool 环境 | 看不见 |
| 系统包管理器安装 `python-<pkg>` | 系统 Python | 看不见 |
| 已激活的 conda / 项目 venv 里 `import <pkg>` 能过 | 那份 conda / `.venv` | 也看不见 |

`uv tool install <pkg>` 不会把 `<pkg>` 塞进已经装好的 `<tool>`; 它只是再开一个以 `<pkg>` 为名的工具环境.

包装声明漏依赖时也一样: 代码 `import <pkg>`, metadata 却没写上, 修法仍是往**报错的那个环境**里补, 而不是往系统或当前 shell 环境里补.

### 缺依赖时往哪装

原则: 谁报错, 就往谁的解释器里装.

```bash
# uv 安装的 CLI: 附加依赖用 --with, 不要另装一个同名 tool
uv tool install <tool> --force --with <pkg>

# 一次性跑, 不写入 PATH
uvx --with <pkg> <tool>

# 项目代码 (当前目录的 .venv)
uv add <pkg>          # 或 uv pip install <pkg>

# conda
conda activate <env>
pip install <pkg>     # 或 conda install <pkg>
```

`--with` 把包装进**这个工具的 venv**, 不把对方的可执行文件装到 `PATH`. 需要对方的 CLI 时才用 `--with-executables-from`.

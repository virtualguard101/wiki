---
date: 2026-09-07 16:57:09
title: Man Pages
permalink: man
publish: true
tags:
  - 工具
  - Linux
---

# Man Pages

手册页（`man pages`）是 UNIX 中常被低估的宝贵资源；虽然不如谷歌那样全能，但它们包含了从程序用法、语言标准与规范到更多 UNIX 组件的文档。

最重要的是，`man`支持**离线**使用。

针对UNIX和C语言的问题，手册页仍是可靠的查询工具。

- 如果希望查看某个程序或命令的手册页，可以运行：

    ```bash
    man <command>
    ```

    程序的 `man` 手册通常包含该程序的用途说明、使用特定标志调用时的功能，以及获取更多信息的途径。

- 如果希望搜索与某个关键词相关的命令手册页，可使用 `-k` 选项：

    ```bash
    man -k <keyword>
    ```

    此命令将在手册页中搜索包含关键词 `<keyword>` 的命令。例如，假设希望查询如何在 Vim 中打开文件？可以搜索 `editor` ，获取系统中所有与编辑器相关的命令列表：

    ```bash
    man -k editor
    ```

    这将列出所有与编辑器相关的命令，包括 `vim`、`nano`、`gedit` 等。

## Man与Linux开发

Man Pages 也是 Linux 开发最常用的参考手册, 由很多页面组成, 每个页面描述一个主题, 这些页面被组织成若干个 Section. FHS (Filesystem Hierarchy Standard) 规定了各 Section 的含义如下:

| Section | 描述 |
| --- | --- |
| 1 | 用户命令, 例如 `ls(1)` |
| 2 | 系统调用, 例如 `_exit(2)` |
| 3 | 库函数, 例如 `printf(3)` |
| 4 | 特殊文件, 例如 `null(4)` 描述 `/dev/null`, `/dev/zero` |
| 5 | 系统配置文件格式, 例如 `passwd(5)` 描述 `/etc/passwd` |
| 6 | 游戏 |
| 7 | 其它杂项, 例如 `bash-builtins(7)` 描述 bash 内建命令 |
| 8 | 系统管理命令, 例如 `ifconfig(8)` |

注意区分:

- **用户命令**通常在 `/bin`, `/usr/bin`, 一般用户可执行

- **系统管理命令**通常在 `/sbin`, `/usr/sbin`, 常需 `root` 权限

- **系统调用**(Section 2)与**库函数**(Section 3)也不相同

### 重名页面与写法

有些页面重名. 例如直接 `man printf` 看到的往往是 Section 1 的命令 `printf`, 不是 C 库函数. 查库函数应指定 Section:

```bash
man 3 printf
```

也可用 `man -k printf` 搜索主题含 `printf` 的页面 (见上文).

文档里常见 `printf(3)` 这种写法: 括号中的数字表示 Man Page 的 Section, 也用来标明说的是库函数还是同名命令.

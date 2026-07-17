---
date: 2026-07-17 16:15:09
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

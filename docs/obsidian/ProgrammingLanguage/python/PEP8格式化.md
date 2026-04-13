---
date: 2026-04-13 15:30:40
title: PEP8格式化
permalink: pep8-fmt
publish: true
tags:
  - 编程语言
  - Python
---

# PEP8格式化

> [小插曲：编码风格 - 更多控制流工具 |  Python 教程](https://docs.python.org/zh-cn/3/tutorial/controlflow.html#intermezzo-coding-style)
>
> [PEP 8 – Style Guide for Python Code | Python Enhancement Proposals](https://peps.python.org/pep-0008/)

- 缩进，用 4 个空格，不要用制表符。

- 4 个空格是小缩进（更深嵌套）和大缩进（更易阅读）之间的折中方案。制表符会引起混乱，最好别用。

- 换行，一行不超过 79 个字符。

- 这样换行的小屏阅读体验更好，还便于在大屏显示器上并排阅读多个代码文件。

- 用空行分隔函数和类，及函数内较大的代码块。

- 最好把注释放到单独一行。

- 使用文档字符串。

- 运算符前后、逗号后要用空格，但不要直接在括号内使用： a = f(1, 2) + g(3, 4)。

- 类和函数的命名要一致；按惯例，命名类用 UpperCamelCase，命名函数与方法用 lowercase_with_underscores。命名方法中第一个参数总是用 self (类和方法详见 初探类)。

- 编写用于国际多语环境的代码时，不要用生僻的编码。Python 默认的 UTF-8 或纯 ASCII 可以胜任各种情况。

- 同理，就算多语阅读、维护代码的可能再小，也不要在标识符中使用非 ASCII 字符。

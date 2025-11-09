---
date: 2025-11-09 21:14:52
title: Introduction to Operating Systems
permalink: 
publish: true
---

# Introduction to Operating Systems

>[Introduction to Operating Systems | Operating Systems: Three Easy Pieces](https://pages.cs.wisc.edu/~remzi/OSTEP/intro.pdf)

## What happens when a program runs

一个运行中的程序只做一件十分简单的事——**执行指令**: 处理器从内存中**获取**指令（I/O操作），**解码**指令（判断这是哪条指令），然后**执行**指令（执行指令对应的各种操作，如运算、跳转、访存等）；完成一个指令后继续处理下一条，如此循环往复，直到程序结束。

上面描述的就是**冯诺依曼**体系结构的基本原理。

## OSTEP

[《Operating Systems: Three Easy Pieces》](https://pages.cs.wisc.edu/~remzi/OSTEP/)（简称 OSTEP）聚焦于一个在学习操作系统时十分值得深思的问题:

<div class="text-center-container" style="text-align: center;">
    <strong style="color: yellow;">How dose Operating System virtualize resources?</strong>
</div>

由此引出如下几个问题:

- *What mechanisms and policies are implemented by the OS to attain virtualization?*

- *How dose the OS do so efficiently?*

- *What hardware support is needed?*

除此之外，与国内经典的408大纲不同，ostep将对操作系统的的阐述分为三个核心模块:

- **Virtualization（虚拟化）**

- **Concurrency（并发）**

- **Persistence（持久化）**

我个人认为这是一个十分有趣的分块，相比较408大纲“功能式”的分块（进程管理、内存管理、文件管理、I/O管理），其更能体现出操作系统的本质与理念。前者更适合作为基础的概念学习（~~但分那么细且杂大可不必~~），而后者更适合作为以深入理解操作系统的本质为目的的深入学习。

## Virtualizing The CPU

循环打印传入的字符串[^1]

=== "`cpu.c`"

    ```c
    #include <stdio.h>
    #include <stdlib.h>
    #include "common.h"

    int main(int argc, char *argv[])
    {
        if (argc != 2) {
        fprintf(stderr, "usage: cpu <string>\n");
        exit(1);
        }
        char *str = argv[1];

        while (1) {
        printf("%s\n", str);
        Spin(1);
        }
        return 0;
    }
    ```

这个程序的逻辑十分简单，就是以1秒的间隔循环打印作为参数传入程序的字符串，通过`Spin(1)`函数实现1秒的间隔。

但 ostep 想表达的是: 假设我们同时运行多个这样的程序，由于“死循环打印”的缘故，是否就只有第一个程序能得到执行，即只能得到一种输出呢？

然而，结果是这样的:

```bash
$ ./cpu a & ./cpu b & ./cpu c & ./cpu d & ./cpu e &
[1] 953041
[2] 953042
a
[3] 953043
b
[4] 953044
[5] 953045
d
c
e
$ a
...

[1]    953041 terminated  ./cpu a

$ b
d
c
e
...

[2]    953042 terminated  ./cpu b

$ d
c
e
...

[3]    953043 terminated  ./cpu c

$ d
e
...

[4]  - 953044 terminated  ./cpu d

$ e
e
...
[5]  + 953045 terminated  ./cpu e
```

显然，这三个进程似乎在同时运行。

这是由于操作系统在硬件的辅助下营造了一个假象，让系统看起来拥有大量的虚拟CPU。将单个CPU（或少量CPU）转化为近乎无限的虚拟CPU,从而使多个程序能“同时”运行，这就是所谓的**CPU虚拟化**。

??? tip "一些现象"
    - 命令中的`&`符号用于将程序放入后台运行，这意味着程序不会阻塞用户的输入，使得用户可以继续输入其他命令

        - 这也是为什么可以同时创建那么多`./cpu`进程（`./cpu a & ./cpu b ...`）以及在这段命令执行的过程中在特定情况下（如进程被`kill`）会出现输入提示符（`$`）的原因

        - 验证的方法也很简单，尝试在这个进程持续输出字母时输入其他命令，正常情况下其他命令是可以正常执行的

        - 也可以通过在命令后使用重定向操作符`>`将输出重定向到文件中进行观察，如`./cpu a & ./cpu b & ./cpu c & ./cpu d & ./cpu e & > output.txt`

    - 诸如`[5]  + 953045 terminated  ./cpu e`的输出表示这个进程因为外部原因终止了（这里是因为使用了`kill`命令，因为这串命令似乎无法直接通过`C-c`终止）

    - 这里也可以看出打印的字母顺序实际并没有按照命令中的传入顺序进行输出

## Virtualizing Memory


[^1]: [`cpu.c`](https://github.com/virtualguard101/ostep-code/blob/master/intro/cpu.c)
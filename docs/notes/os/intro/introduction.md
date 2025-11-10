---
date: 2025-11-09 23:23:52
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

    int main(int argc, char *argv[]) {
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

现代计算机所呈现的**物理内存**模型非常简单: **Memory is just an array of bytes!**

要访问读取内存中的数据，必须给出一个特定的**地址**，然后才能根据这个地址读取对应的数据；写入同理。

程序将所有的数据结构都存放在内存中；同时，程序本身的[指令](#What-happens-when-a-program-runs)也存储在内存中，每次执行指令时都需要访问内存。因此，**程序运行时，内存会持续被访问**。

一个访问内存的程序[^2]:

=== "`mem.c`"

    ```c
    #include <unistd.h>
    #include <stdio.h>
    #include <stdlib.h>
    #include "common.h"

    int main(int argc, char *argv[]) {
        int *p = malloc(sizeof(int));
        assert(p != NULL);
        printf("(%d) addr pointed to by p: %p\n", (int) getpid(), p);
        *p = 4; // assign value to addr stored in p
        while (1) {
            Spin(1);
            *p = *p + 1;
            printf("(%d) value of p: %d\n", getpid(), *p);
        }
        return 0;
    }
    ```

上面的程序做了一个很简单的事情: 将一个[右值](../../language/cpp/cs106l/01-init-reference.md#左值与右值)赋值给一个指针变量（由`malloc()`函数分配内存），然后以1秒的间隔，循环地将这个指针指向的值（指针解引用）加1并打印到命令行:

```bash
$ ./mem
(25653) addr pointed to by p: 0x556bd9d43310
(25653) value of p: 5
(25653) value of p: 6
(25653) value of p: 7
(25653) value of p: 8
(25653) value of p: 9
...
```

乍一看上面的这个程序并没有什么新奇的点。现在，我们像[前面](#Virtualizing-The-CPU)那样同时运行多个这样的程序:

```bash
$ ./mem & ./mem & ./mem &
[1] 27081
[2] 27082
[3] 27083
(27081) addr pointed to by p: 0x55a99f4e5310
(27082) addr pointed to by p: 0x55adf4cba310
(27083) addr pointed to by p: 0x55c5755d1310
$ (27081) value of p: 5
(27082) value of p: 5
(27083) value of p: 5
(27081) value of p: 6
(27082) value of p: 6
(27083) value of p: 6
...

[1]    27081 terminated  ./mem

$ ...

[2]    27082 terminated  ./mem

$ ...

[3]    27083 terminated  ./mem
```

仔细观察不难发现，系统为似乎为每个程序（进程）中的变量 `p` 都分配了一个与众不同的地址，并独立更新着这个地址指向的值。这表明每个程序似乎都拥有自己的一块内存空间，这块内存空间是相互独立的，互不干扰的。

!!! warning
    事实上，上面这段理解并不准确，其中“分配的地址不同”并不是决定性证据（从逻辑来看，地址应该要相同才更有说服力，证明尽管指向一个“相同”的地址，但变量本身却是相互独立的）。
    
    至于为什么地址会不同（ostep上的案例是相同的），这是由于现代操作系统引入了地址空间布局随机化（ASLR）等安全机制，它让堆上的虚拟地址随机化，让每次运行显示的数值都不一样。

这就是操作系统虚拟化内存的作用，这样使得每个进程都能独立地访问自己的私有的**虚拟地址空间**，并以某种方式映射到物理内存上，使得各个进程之间互不干扰，同时从进程视角来看似乎自己独占整个物理内存。

## Concurrency


[^1]: [`cpu.c`](https://github.com/virtualguard101/ostep-code/blob/master/intro/cpu.c)

[^2]: [`mem.c`](https://github.com/virtualguard101/ostep-code/blob/master/intro/mem.c)
---
date: 2025-11-16 00:35:52
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

## Virtualization

### Virtualizing The CPU

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

### Virtualizing Memory

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

上面的程序做了一个很简单的事情: 将一个[右值](../../ProgrammingLanguage/cpp/cs106l/初始化与引用操作.md#左值与右值)赋值给一个指针变量（由`malloc()`函数分配内存），然后以1秒的间隔，循环地将这个指针指向的值（指针解引用）加1并打印到命令行:

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

ostep的另一个主题是**并发**，这一术语用于指代在同一程序中**同时处理多个任务**时出现且必须解决的一系列**问题**。

并发性问题起源于操作系统内部——如前面提到的[虚拟化](#Virtualization)，操作系统需要同时处理多项任务。

但并发问题已经已不再局限于操作系统本身，现代多线程程序同样需要解决这些问题。

下面是一个简单的多线程程序示例[^3]:

=== "`threads.c`"

    ```c
    #include <stdio.h>
    #include <stdlib.h>
    #include "common_threads.h"

    volatile int counter = 0;
    int loops;

    void *worker(void *arg) {
        int i;
        for (i = 0; i < loops; i++) {
            counter++;
        }
        return NULL;
    }

    int main(int argc, char *argv[]) {
        if (argc != 2) {
            fprintf(stderr, "usage: threads <loops>\n");
            exit(1);
        }
        loops = atoi(argv[1]);
        pthread_t p1, p2;
        printf("Initial value : %d\n", counter);
        Pthread_create(&p1, NULL, worker, NULL);
        Pthread_create(&p2, NULL, worker, NULL);
        Pthread_join(p1, NULL);
        Pthread_join(p2, NULL);
        printf("Final value   : %d\n", counter);
        return 0;
    }
    ```

简单来说，上面的程序定义了一个自增函数`worker`，然后创建了两个线程，并发执行这个函数，以“更快速地”完成对计数器`counter`的自增操作。

编译后，首先选择一个较小的数进行测试:

```bash
$ ./threads 1000
Initial value : 0
Final value   : 2000
```

在代码中，`loops`变量用于控制每个线程执行的次数，因此最终的值应该是`2 * loops`，因此上面的输出是符合预期的。

但当我们使用一个数量级较大的`loops`值进行测试时，情况却变得不一样了:

```bash
$ ./threads 100000
Initial value : 0
Final value   : 127240
$ ./threads 100000
Initial value : 0
Final value   : 113374
```

输出不仅不符合预期，且每次运行的结果都不尽相同。这是为什么呢？

事实证明，从计算机底层的视角来看，这个“异常”与指令的执行方式有关——指令是逐条执行的。

自增操作并不是原子性的，而是由多个指令组成的: 

```asm
mov eax, [counter] ; 将计数器的值从内存中加载到寄存器中
add eax, 1         ; 将寄存器中的值加1
mov [counter], eax ; 将寄存器中的值写回内存中
```

因此，当上面的两个线程同时执行自增操作时，可能会出现各种各样的异常情况。

!!! question
    - When there are many concurrently executing threads within the same memory space, how can we build a correctly working program?

    - What [primitives](../exam/2-process.md#原语) are needed from the OS?

    - What mechanisms should be provided by the hardware?

    - How can we use them to solve the problems of concurrency?

## Persistence

在系统内存中，由于DRAM的易失性存储方式，当系统崩溃或断电时，内存中的所有数据都会丢失。因此，我们需要硬件和软件能够持久地存储数据。

硬件层面，以**I/O设备**的形式提供为持久化提供辅助。在现代计算机系统中，**磁盘（*Hard Disk Drive*, HDD）**、**固态硬盘（*Solid State Drive*, SSD）**等设备被广泛用于持久化存储。

软件层面，操作系统中提供了**文件系统**作为数据持久化的核心组件。文件系统负责以可靠和高效的方式将用户创建的任何文件存储在磁盘上，并提供对文件的访问和操作。

与系统为CPU和内存提供的抽象机制不同，操作系统并不会为每个应用程序创建私有的虚拟化磁盘，相反，用户在与系统交互时常常需要**共享**文件中的信息，库函数就是一个典型的例子。

下面看一个简单的文件操作示例[^4]:

=== "`io.c`"

    ```c
    #include <stdio.h>
    #include <unistd.h>
    #include <assert.h>
    #include <fcntl.h>
    #include <sys/stat.h>
    #include <sys/types.h>
    #include <string.h>

    int main(int argc, char *argv[]) {
        int fd = open("/tmp/file", O_WRONLY | O_CREAT | O_TRUNC, S_IRUSR | S_IWUSR);
        assert(fd >= 0);
        char buffer[20];
        sprintf(buffer, "hello world\n");
        int rc = write(fd, buffer, strlen(buffer));
        assert(rc == (strlen(buffer)));
        fsync(fd);
        close(fd);
        return 0;
    }
    ```

这个程序的功能比上面的任何程序都要简单，仅仅是将字符串`hello world`写入到文件`/tmp/file`中。

编译并执行这个程序后，可以通过`cat /tmp/file`命令查看文件内容，结果如下:

```bash
$ ./io
$ cat /tmp/file
hello world
```

但为了完成这个看似简单的操作，程序需要进行三次系统调用:

1. 调用`open()`打开并创建文件

2. 调用`write()`将字符串写入到文件中

3. 调用`close()`关闭文件

!!! tip
    在ostep中，`io.c`只用到了三个系统调用，即上面提到的`open()`、`write()`和`close()`。但在这里，实际还用到了`fsync()`系统调用，用于将数据同步到磁盘上；同时，这里还使用了一个缓冲数组`buffer`来存储字符串。

    ??? tip "fsync()"
        `fsync()` 是一个系统调用，强制将文件描述符对应文件的修改从内核缓冲区同步到物理磁盘。

        写操作（如 `write()`）可能只写入内核缓冲区，数据仍在内存中；若系统崩溃，数据可能丢失。`fsync()` 确保数据落盘，保证持久性，这对数据库、日志等关键数据很重要。

        使用 `fsync()` 时，传入文件描述符 `fd`，函数会阻塞直到数据写入磁盘。成功返回 0，失败返回 -1 并设置 errno。

另外，关于系统最终如何将数据写入磁盘，文件系统还需要完成相当的操作。写过设备驱动的同志应该知道这一过程是一个极为精细复杂的过程，这也是为什么I/O设备被认为是操作系统中最为“凌乱”且最具挑战性的部分。

操作系统通过**系统调用**提供了访问设备的标准简易方式，正因如此，操作系统有时也视为**标准库**。

!!! question
    - What techniques are needed to manage persistent data correctly?

    - What mechanisms and policies are required to do so with high performance?

    - How is reliability achieved, in the face of failures in hardware and software?

## Design Goals

简单来说操作系统的实际功能包括:

- 通过**虚拟化**的方式管理CPU、内存、磁盘等硬件**资源**

- 处理与**并发**相关的棘手问题

- **持久化**存储文件，确保其长期安全

在实现这些功能的过程中，我们往往需要在某些方面做出权衡，找到恰当的权衡点往往是构建系统的关键所在。

在设计过程中，最基本的目标之一就是建立若干**抽象层**，使系统便于使用。

!!! tip "抽象"
    **抽象（Abstractions）**是计算机科学中一个十分重要的概念，几乎是计算机科学领域的基石。

    抽象使得通过**模块化**编写大型程序成为可能，使得我们可以使用更高层次的**抽象层**进行软件系统的构建，而无需关心底层具体的实现细节。

    关于抽象的概念与其在程序构造中的应用，可以参考伯克利的[CS61A](https://cs61a.org/)

同时，我们设计与实现操作系统的目标之一是提供**高性能**；换句话说，我们应尽量减少系统的开销，这些开销通常以**时间（指令的数量级）**与**空间（内存或磁盘空间的占用）**的形式体现。

另一个目标是为应用程序与之间以及系统与应用程序之间提供**保护机制**。由于我们希望多个程序能够同时运行，这就要求我们必须确保某个程序的恶意操作或故障不会影响到其他程序的正常运行，这也包括操作系统本身（否则运行在该系统上所有的程序都会受到影响）。

!!! tip "隔离原则"
    保护机制是操作系统核心原则——**隔离原则**的根本体现。

    将进程相互隔离是实现保护的关键，这也构成了操作系统大部分功能的基础。

## Some History

### Early Operating Systems: Just Libraries

早期操作系统的功能十分有限，本质上只是一组常用函数库。

### Beyond Libraries: Protection

开始出现一些保护机制，如区分**用户态**与**内核态**。

### The Era of Multiprogramming

为了更高效地利用机器资源，开始出现多道程序设计，操作系统不再一次只运行一个作业，而是把多个作业加载到内存中并在它们之间快速切换。

从这里开始，开始出现小型计算机，操作系统真正开始腾飞。另外值得说明的是，Unix操作系统就是在这个时期诞生的。

### The Modern Era


[^1]: [`cpu.c`](https://github.com/virtualguard101/ostep-code/blob/master/intro/cpu.c)

[^2]: [`mem.c`](https://github.com/virtualguard101/ostep-code/blob/master/intro/mem.c)

[^3]: [`threads.c`](https://github.com/virtualguard101/ostep-code/blob/master/intro/threads.c)

[^4]: [`io.c`](https://github.com/virtualguard101/ostep-code/blob/master/intro/io.c)
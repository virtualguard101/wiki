---
date: 2026-11-03 12:13:06
title: I/O与系统调用
permalink: io-syscall
publish: true
tags:
  - 编程语言
  - Assembly
  - Computing 101
---

# I/O与系统调用

> [Computing 101. - Output and Input | pwn.college](https://pwn.college/computing-101/hello-hackers/)
>
> [write(2) - Linux manual page](https://man7.org/linux/man-pages/man2/write.2.html) / [read(2)](https://man7.org/linux/man-pages/man2/read.2.html) / [open(2)](https://man7.org/linux/man-pages/man2/open.2.html) / [syscall(2)](https://man7.org/linux/man-pages/man2/syscall.2.html)

在[最简汇编](最简汇编.md)中, 程序只用 `exit` 就能把一个数交给 shell. 但真正有用的程序必须与外界交换数据: 向终端输出, 从标准输入读取, 打开文件. 

在 Linux 上, 这些都通过[系统调用](../../os/408/操作系统运行环境.md#系统调用)完成. 本文以 Linux x86-64 和 Intel 语法为例, 依次介绍 `write`, `read`, `open`, `close` 几个系统调用, 并说明程序如何在不依赖绝对地址的前提下引用自己的字符串.

## 系统调用约定

[系统调用](../../os/408/操作系统运行环境.md#系统调用)是用户程序请求内核服务的入口. Linux x86-64 的约定如下:

| 寄存器 | 作用 |
|:-------|:-----|
| `rax` | 入口: 系统调用号; 返回: 结果 (失败时为负的错误码) |
| `rdi` | 第 1 个参数 |
| `rsi` | 第 2 个参数 |
| `rdx` | 第 3 个参数 |
| `rcx`, `r11` | 被 `syscall` 指令破坏, 不能指望它们保持原值 |

本文用到的系统调用如下:

| 调用号 | 名称 | C 形式 | 作用 |
|:------:|:-----|:-------|:-----|
| `0` | `read` | `read(fd, buf, count)` | 从 `fd` 读取至多 `count` 字节到 `buf` |
| `1` | `write` | `write(fd, buf, count)` | 把 `buf` 开头的 `count` 字节写入 `fd` |
| `2` | `open` | `open(path, flags, mode)` | 打开文件, 返回新的文件描述符 |
| `3` | `close` | `close(fd)` | 关闭文件描述符 |
| `60` | `exit` | `exit(status)` | 结束进程 |

!!! warning
    `rdi` 与 `rdx` 名称相近, 极易写混. 可以记作: `rdi` 是 **i**nitial (第一个) 参数, `rdx` 是 e**x**tra (第三个) 参数.

### 文件描述符

**文件描述符** (file descriptor, fd) 是内核给已打开文件分配的一个小整数, 程序之后用它指代这个文件. 进程启动时就已经打开了三个:

| fd | 名称 | 默认指向 |
|:--:|:-----|:---------|
| `0` | `stdin` | 终端输入 |
| `1` | `stdout` | 终端输出 |
| `2` | `stderr` | 终端输出 (用于错误信息) |

之后 `open` 新打开的文件通常从 `3` 开始依次分配. 所以 `write(1, ...)` 就是写到标准输出, `read(0, ...)` 就是从标准输入读取, 而 `read(3, ...)` 则是从第一个 `open` 的文件读取. 用同一对 `read` / `write` 既能处理终端和管道, 也能处理文件, 差别只在 fd.

## write: 输出一个字符

`write(1, buf, 1)` 的三个参数依次放入 `rdi`, `rsi`, `rdx`, 同时 `rax = 1`. 其中 `buf` 必须是**内存地址**, 而不是字符本身.

在[栈与程序参数](栈与程序参数.md#汇编视角下的程序参数传递)中已经知道, 程序以 `./prog H` 方式运行时, `[rsp+16]` 保存的是 `argv[1]` 这个**指针**, 它恰好就是 `write` 需要的地址:

```asm
.intel_syntax noprefix

.global _start

.section .text

_start:
    mov rax, 1                  # SYS_write
    mov rdi, 1                  # stdout
    mov rsi, [rsp + 16]         # argv[1] 字符串的地址
    mov rdx, 1                  # 只写出一个字符
    syscall

    mov rax, 60                 # SYS_exit
    xor rdi, rdi                # 退出码 0
    syscall
```

`mov rsi, [rsp+16]` 只解引用一次: 取出指针本身放入 `rsi`, 由内核沿着这个地址去读取字符.

如果再多解引用一次 (`mov rsi, [rsi]`), `rsi` 里放的就是字符的值而不是地址, `write` 将因地址无效而失败.

## read: 读入到缓冲区

`read(0, buf, n)` 与 `write` 的参数顺序相同, 但数据流向相反: 内核把读到的字节**写入** `buf`.

若输入为 `HELLO`, `read(0, buf, 5)` 之后内存中是这些字节 (ASCII 的十六进制):

```text
  Address │ Contents
+───────────────────+
│ buf     │ 48  'H' │
│ buf+1   │ 45  'E' │
│ buf+2   │ 4c  'L' │
│ buf+3   │ 4c  'L' │
│ buf+4   │ 4f  'O' │
+───────────────────+
```

### 缓冲区的本质

缓冲区的本质就是一段有效且可写的内存.

最方便的就是栈: `rsp` 本身就是一个可写地址, 因此 `mov rsi, rsp` 即可把栈顶当作缓冲区, 向更高地址延伸. 若要用更大的空间, 先 `sub rsp, N` 向低地址扩展出 `N` 字节, 再把 `rsp` 作为缓冲区起点.

### 精确读取字节数

`read` 的第三个参数只是**上限**, 返回值才是**实际读取的字节数**. 要求读 128 字节而输入只有 50 字节, 则 `rax = 50`.

| 返回值 `rax` | 含义 |
|:------------:|:-----|
| `> 0` | 实际读到的字节数 (可能小于 `count`) |
| `0` | 到达文件末尾 (EOF) |
| `< 0` | 出错, 值为 `-errno` |

所以"读入后原样输出"的正确写法是把 `read` 的返回值交给 `write` 的长度参数:

```asm
.intel_syntax noprefix

.global _start

.section .text

_start:
    xor rax, rax                # SYS_read (0), 异或自身清零
    xor rdi, rdi                # stdin (0)
    mov rsi, rsp                # 将输入读到栈顶
    mov rdx, 128                # 最多读取 128 字节
    syscall                     # rax = 实际读取的字节数

    mov rdx, rax                # 先保存读取长度, 再覆盖 rax
    mov rax, 1                  # SYS_write
    mov rdi, 1                  # stdout
    mov rsi, rsp                # 从同一缓冲区写出
    syscall

    mov rax, 60                 # SYS_exit
    xor rdi, rdi                # 退出码 0
    syscall
```

!!! warning
    `mov rdx, rax` 必须放在 `mov rax, 1` **之前**. 否则 `rax` 里的读取长度已被系统调用号覆盖, `write` 的长度会变成 `1`.

如果图省事固定写出 128 字节, 则输入不足 128 字节时, 多出来的部分是缓冲区里没有初始化的旧内容, 常表现为乱码. 因此 `write` 的长度应当使用 `read` 的返回值, 而不是 `read` 的上限.

## open: 打开文件

`open(path, flags, mode)` 也有三个参数: 

- 第一个参数 `rdi` 是**以 `\0` 结尾的文件名字符串的地址**

- 第二个参数 `rsi` 是访问方式, `0` 表示只读 (`O_RDONLY`)

- 第三个参数 `rdx` 只在**新建文件**时用到

成功时 `rax` 返回新的 fd, 失败时返回负的错误码, 例如 `-2` (`-ENOENT`, 文件不存在) 或 `-14` (`-EFAULT`, 地址无效).

流程只比读标准输入多一步: 先 `open` 得到 fd, 再把这个 fd 作为 `read` 的第一个参数:

```text
open(path, 0)
    │
    ▼
rax = fd 
    │ mov rdi, rax
    ▼
read(fd, buf, n)
    │
    ▼
rax = len
    │ mov rdx, rax
    ▼
write(1, buf, len)
```

!!! tip
    每一步都要把上一步留在 `rax` 的结果在被覆盖前挪走: `open` 的 fd 先移入 `rdi`, 再把 `rax` 改成 `read` 的调用号; `read` 的长度先移入 `rdx`, 再把 `rax` 改成 `write` 的调用号.

### 写文件: flags 与 mode

要向文件写入内容, 需要把 `flags` 设成可写, 这些标志按位或 (`|`) 组合后放入 `rsi`:

| 标志 | 值 | 含义 |
|:-----|:--:|:-----|
| `O_RDONLY` | `0x0` | 只读 |
| `O_WRONLY` | `0x1` | 只写 |
| `O_RDWR` | `0x2` | 读写 |
| `O_CREAT` | `0x40` | 文件不存在时创建 |
| `O_TRUNC` | `0x200` | 文件已存在时先清空 |

"创建并清空, 以只写方式打开"即 `O_WRONLY | O_CREAT | O_TRUNC = 0x1 | 0x40 | 0x200 = 0x241`.

一旦带有 `O_CREAT`, 第三个参数 `rdx` 就是新文件的权限位 `mode`, 如八进制 `0644` 对应 `rw-r--r--` (文件属主可读写, 其他人只读). 文件若已存在, `mode` 会被忽略.

!!! note
    汇编器 `as` 中以 `0` 开头的整数视为八进制.

!!! warning
    `O_CREAT` 之后忘记设置 `rdx`, 新文件的权限就取决于 `rdx` 里恰好遗留的值, 可能得到权限混乱的文件.

用完文件后可以用 `close(fd)` (调用号 `3`) 释放文件描述符. 进程退出时内核也会自动关闭, 但显式关闭是更好的习惯.

### 文件名的来源

文件名是字符串, 而 `open` 要的是它的地址. 常见有三种来源.

1. 来自命令行参数.

    直接用 `mov rdi, [rsp+16]` 取 `argv[1]` 即可, 路径由调用者在运行时传入, 不需要改动程序.

2. 逐字节写到栈上.

    例如:

    ```asm
    mov BYTE PTR [rsp],   '/'
    mov BYTE PTR [rsp+1], 'f'
    ...
    mov BYTE PTR [rsp+5], 0
    mov rdi, rsp          # 别忘了把地址放进 rdi
    ```

    这种写法能工作, 但冗长且容易出错; 而且 `[rsp]` 起始处原本是 `argc`, `[rsp+8]` 是 `argv[0]`, 直接写入会把它们覆盖.

    !!! failure
        最常见的错误是写完字符串后忘记 `mov rdi, rsp`, 此时 `rdi` 仍是进程启动时的初值 (通常是 `0`), 相当于 `open(NULL, 0)`, 返回 `-EFAULT`. 此后 `read` 与 `write` 因 fd 或长度非法接连失败, 但程序依然 `exit` 退出, 终端上**没有任何输出**.

3. 作为数据放在代码之后:

## 字符串与 RIP 相对寻址

### 把字符串放在代码后面

汇编文件中不仅可以放指令, 也可以放**不打算被执行的字节**.

只要放在最后的 `exit` 系统调用**之后**, CPU 就不会走到那里, 这些字节依然存在于程序的内存中. 汇编器提供 `.asciz` 指令来生成字符串字节:

```asm
    mov rax, 60
    syscall             # exit, 不会返回

path:
    .asciz "/flag"      # 从不执行, 但字节仍在内存里
```

- `.asciz` 会在字符串末尾**自动追加 `\0`**. 内核正是靠这个 `\0` 判断文件名的结尾, 因此不要再手写 `\0`. 而 `.ascii` 则不会追加, 需要自己补.

- `path:` 是一个标签, 代表这些字节的起始地址.

!!! warning
    若把字符串放在 `.data` 节而不是紧跟在代码之后, 虽然程序同样可以运行, 但这不是 pwn.college 此处要求的写法, 其检查器会提示"文件名应紧接在代码之后, 以 `.asciz` 存放".

### 为什么不能直接用标签的地址

很自然的想法是直接把标签值放入寄存器:

```asm
mov rdi, path       # 在现代程序中不可行
```

早期程序总是被装入固定地址, 汇编器在汇编时就知道 `path` 的绝对地址. 但现代程序为了安全 (这是后面章节的内容) 被设计成**可以装入内存任意位置**, 汇编时并不知道最终地址, 所以不能把绝对地址编码进指令.

### RIP 相对寻址

[x86_64](x86-64汇编基础.md)的解决办法是**以指令指针 `rip` 为基准**编码地址. `rip` 始终保存**下一条指令**的地址, 而代码与字符串之间的**距离**在汇编时是已知的, 与程序被装到哪里无关. 于是:

```text
 目标地址 = (下一条指令的地址) + (汇编时算好的偏移)
```

不过要注意两种写法的区别, 这在[取地址指令](指针访存的汇编描述.md#取地址指令)中已经介绍过:

```asm
mov rdi, [rip+path]   # 读内存: rdi 得到 path 处的 8 字节内容 ('/', 'f', 'l', ...), 不是地址
lea rdi, [rip+path]   # 只计算地址: rdi = &path
```

`open` 需要的是地址, 所以必须使用 `lea`. 方括号里写的 `rip+path` 看上去像"`rip` 加上标签", 实际编码进指令的是**标签与下一条指令之间的距离**.

## 综合示例

本例综合了 `read`, `open`, `write`, `close`, 完成以下任务: **从终端读取用户输入, 写入文件 `out.txt`, 并回显到终端**. 完整源码为 `io.s`:

```asm
.intel_syntax noprefix

.global _start

.section .text

_start:
    sub rsp, 256                # 在栈上预留 256 字节作为输入缓冲区

    # 1. read(0, buf, 256): 从终端 (stdin) 读取用户输入
    xor rax, rax                # SYS_read (0), xor 异或运算清零 rax 寄存器
    xor rdi, rdi                # stdin (0)
    mov rsi, rsp                # 缓冲区 = 栈顶
    mov rdx, 256                # 最多读取 256 字节
    syscall                     # rax = 实际读取的字节数
    mov r12, rax                # 把长度保存到 r12: syscall 只破坏 rax, rcx, r11,
                                # r12 不会被改写, 后面两次 write 都要用到它

    # 2. open(path, O_WRONLY | O_CREAT | O_TRUNC, 0644): 创建/清空并以只写方式打开文件
    mov rax, 2                  # SYS_open
    lea rdi, [rip + path]       # 文件名的地址 (RIP 相对寻址, 必须用 lea 取地址)
    mov rsi, 0x241              # flags = O_WRONLY (0x1) | O_CREAT (0x40) | O_TRUNC (0x200)
    mov rdx, 0644               # mode = 0644 (八进制), 仅在文件被新建时生效: rw-r--r--
    syscall                     # rax = 新的 fd (通常是 3)
    mov r13, rax                # 保存文件的 fd, 写入和关闭时都要用

    # 3. write(fd, buf, len): 把用户输入写入文件
    mov rdx, r12                # 长度 = read 实际读取的字节数, 而不是上限 256
    mov rax, 1                  # SYS_write
    mov rdi, r13                # 目标是刚打开的文件, 不是 stdout
    mov rsi, rsp                # 数据仍然在栈上的缓冲区里
    syscall

    # 4. write(1, buf, len): 把同样的数据输出到终端 (stdout)
    mov rdx, r12                # 长度不变; rdx 可能已被内核改写, 所以重新设置
    mov rax, 1                  # SYS_write
    mov rdi, 1                  # stdout (1)
    mov rsi, rsp                # 同一块缓冲区
    syscall

    # 5. close(fd): 关闭文件, 释放文件描述符
    mov rax, 3                  # SYS_close
    mov rdi, r13                # 要关闭的 fd
    syscall

    # 6. exit(0)
    mov rax, 60                 # SYS_exit
    xor rdi, rdi                # 退出码 0
    syscall

path:
    .asciz "out.txt"            # 紧跟在代码后面, 永远不会被执行; .asciz 自动补上结尾的 \0
```

运行效果:

```bash
> make asm src=io.s
> echo "hello vglab" | ./io.out
hello vglab
> cat out.txt
hello vglab
> ls -l out.txt
-rw-r--r-- 1 user user 12 ... out.txt
```

这里是管道输入; 在终端直接运行 `./io.out`, 输入一行文本并回车, 效果相同.

由于只调用一次 `read`, 终端默认的行缓冲使它通常一次只能拿到**一行**, 所以输入超过一行的内容时只会处理第一行.

### 数据流

```text
 终端 stdin ──read──▸ 栈缓冲区 ──write(fd)──▸ out.txt
                        │
                        └──write(1)──▸ 终端 stdout
```

同一个缓冲区被写了两次: 一次写到文件 (fd 为 `open` 的返回值), 一次写到标准输出 (fd 为 `1`). 这正说明了 `write` 对目标是"文件"还是"终端"并不关心, 区别仅在 fd.

### `r12` 与 `r13` 的作用

此前的例子都是随手把返回值挪进下一个调用的参数寄存器.

本例需要把 `read` 的长度**跨越多次系统调用**反复使用, 而 `rax`, `rdx` 等寄存器随时会被覆盖, 所以需要找一个 `syscall` 不会改写的寄存器暂存.

约定中 `syscall` 只破坏 `rax` (返回值), `rcx` 和 `r11`, 因此 `r12`, `r13` 这类寄存器足以安全保存长度和 fd. 之所以不用 `rcx`, 与[栈与程序参数](栈与程序参数.md#其他值得注意的点)中不选用 `rcx` 作计数器的原因相同.

!!! tip
    `write` 的 `rdx` 在调用返回后一般不应再依赖, 本例每次 `write` 前都用 `mov rdx, r12` 重新设置, 比"假定它保持不变"更稳妥.

### 其他值得注意的点

- 不使用 C 运行时时 `_start` 不是函数, 因此末尾要用 `exit` 系统调用而不能用 `ret`, 否则程序会继续往下执行, 甚至进入字符串区域.

- 本例没有检查返回值: `read` 返回 `0` (EOF) 时会创建一个空文件; `open` 失败 (如目录不可写) 时 `rax` 为负, 后续 `write` 会因非法 fd 而失败, 终端上仍然会回显, 不容易察觉. 真实程序应检查每个返回值.

- 可以用 `strace ./io.out` 观察每一次系统调用的参数与返回值, 例如 `open("out.txt", O_WRONLY|O_CREAT|O_TRUNC, 0644) = 3`.

- 再次运行会因为 `O_TRUNC` 而覆盖旧内容; 若改为追加写入, 需要换成 `O_APPEND` (`0x400`).

## 构建与运行

练习中的构建流程为:

```bash
as -o io.o io.s
ld -o io.out io.o
./io.out
echo $?
```

也可以把它们写进 [`Makefile`](../../tools/builder/GNU%20Make.md):

```make
.PHONY: asm clean

asm:
	@if [ -z "$(src)" ]; then \
		echo "Usage: make asm src=<file.s>" >&2; \
		exit 2; \
	fi
	$(AS) "$(src)" -o "$(basename $(src)).o"
	$(LD) "$(basename $(src)).o" -o "$(basename $(src)).out"

clean:
	rm -f *.o *.out
```

之后 `make asm src=io.s` 即可. 其中 `$(AS)` 与 `$(LD)` 是 Make 的内置变量, 默认分别为 `as` 和 `ld`.

## 常见误区

- **漏设寄存器**: 注释掉 `mov rdi, ...` 后只准备了缓冲区, 却没有把地址放进 `rdi`, 导致 `open` 返回 `-EFAULT`, 之后各调用连锁失败而无输出.

- **把长度写成 `read` 的上限**: 应使用 `read` 的返回值 (`rax`), 否则会输出缓冲区里的乱码.

- **覆盖 `rax` 之后才取返回值**: 必须先 `mov rdx, rax` 或 `mov rdi, rax`, 再改写 `rax` 为下一个调用号.

- **混淆 `rdi` 与 `rdx`**: 第 1 个参数用 `rdi`, 第 3 个参数用 `rdx`.

- **用 `mov` 代替 `lea` 取标签地址**: `mov rdi, [rip+path]` 读出的是内容, 不是地址.

- **`O_CREAT` 忘记设置 `mode`**: 新建文件的权限由 `rdx` 的遗留值决定, 应显式设置如 `0644`.

- **跨调用复用 `rax`, `rdx`**: 每次系统调用都会改写 `rax`; 需要保留的长度或 fd 应存入 `r12`, `r13` 等不被 `syscall` 破坏的寄存器.

- **字符串缺少结尾 `\0`**: 使用 `.ascii` 时需要自己补 `\0`, 而 `.asciz` 已自动补上, 不要重复书写.

- **把 `[rsp+16]` 当成字符串内容**: 它是 `argv[1]` 的指针, 仅需解引用一次就能作为 `write` / `open` 的地址参数.

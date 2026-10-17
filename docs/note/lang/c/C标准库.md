---
date: 2026-10-07 17:16:46
title: C标准库
permalink: stdlibc
publish: true
tags:
  - 编程语言
  - C
---

# C标准库

> [C标准库 | Linux C编程一站式学习](https://akaedu.github.io/book/ch25.html)
>
> [C Reference | cppreference.com](https://en.cppreference.com/w/c)
>
> [C Standard Library headers | cppreference](https://en.cppreference.com/w/c/header.html)
>
> [Null-terminated byte strings | cppreference](https://en.cppreference.com/w/c/string/byte.html)
>
> [File input/output | cppreference](https://en.cppreference.com/w/c/io.html)
>
> [Dynamic memory management | cppreference](https://en.cppreference.com/w/c/memory.html)

C 标准把语言本身与**标准库**分开规定: 语言管语法与语义, 标准库提供可移植的常用能力 (字符串, I/O, 堆分配, 数值转换等). 在 Linux 上这些函数大多由 `libc` (如 glibc) 实现, 少数 (如数学函数) 在 `libm` 中; 链接时常自动带上 `libc`, 使用 `sin` / `log` 等则往往还要 `-lm`.

查细节应阅读 Man Page (`man 3 strcpy`) 或 [cppreference](https://en.cppreference.com/w/c/header/string.h). 读接口原型与契约的方法见[函数接口](函数接口.md).

!!! abstract
    - 标准库 = **头文件** (类型 / 宏 / 函数声明) + **库文件** (函数实现). `#include` 只引入声明, 真正代码在链接时从共享库或静态库并入.

    - 命名习惯: `str*` 处理以 `'\0'` 结尾的 C 字符串; `mem*` 按字节块操作, 不关心 `'\0'`. 二者都在 `<string.h>`.

    - 出错时许多函数返回「哨兵值」(`NULL` / `EOF` / `-1`) 并设置全局 `errno`. 应在调用失败后**立刻**读 `errno` 或调用 `perror` / `strerror`, 中间不要夹其它可能改写 `errno` 的库调用.

    - Man Page 的 **CONFORMING TO** 区分 C 标准与 POSIX. `strcpy` 属 C; `strdup` / `strcasecmp` / `strtok_r` 等属 POSIX, 在严格 ISO C 环境未必可用.

    - 堆分配 (`malloc` / `free` 等) 与字符串拷贝的接口契约已在[函数接口](函数接口.md)展开; 堆布局与常见 bug 见 [C Memory Management](C-Memory-Management.md#stdlib-Heap-Functions).

## 标准库的组成

> [C Standard Library headers](https://en.cppreference.com/w/c/header.html).

头文件放哪里取决于Linux发行版与编译器. 常见情况是: `stdio.h` / `stdlib.h` / `string.h` / `errno.h` 等在 `/usr/include`; 与编译器强绑定的如 `stddef.h` / `stdarg.h` 可能在GCC自带的 `include` 目录下. C99 起标准头文件有二十余个, 最常用的几个头文件及其典型内容大致如下:

| 用途 | 头文件 | 典型内容 |
|:-----|:-------|:---------|
| 文件与流式输入输出 | [`<stdio.h>`](https://en.cppreference.com/w/c/header/stdio.html) | `FILE *`, `printf` / `scanf`, `fopen` / `fread`, `stdin` / `stdout` / `stderr` |
| 通用工具(堆内存, 串数值转换, 随机数, 进程退出等) | [`<stdlib.h>`](https://en.cppreference.com/w/c/header/stdlib.html) | `malloc` / `free`, `atoi` / `strtol`, `rand` / `srand`, `exit` |
| 空终止字节串与原始内存块 | [`<string.h>`](https://en.cppreference.com/w/c/header/string.html) | `strlen` / `strcpy` / `strcmp`, `memcpy` / `memset`, `strerror` |
| 跨头文件共用的基础类型与宏 | [`<stddef.h>`](https://en.cppreference.com/w/c/header/stddef.html) | `size_t`, `NULL`, `ptrdiff_t`, `offsetof` |
| 库 / 系统调用失败时的错误码 | [`<errno.h>`](https://en.cppreference.com/w/c/header/errno.html) | `errno` 与各类错误码宏 (`ENOENT` 等) |
| 访问 `...` 可变参数列表 | [`<stdarg.h>`](https://en.cppreference.com/w/c/header/stdarg.html) | `va_list` / `va_start` / `va_arg` / `va_end` ([可变参数](函数接口.md#可变参数)) |
| 调试期条件断言 (可被 `NDEBUG` 关掉) | [`<assert.h>`](https://en.cppreference.com/w/c/header/assert.html) | `assert` 宏 |
| 常用实数数学运算 | [`<math.h>`](https://en.cppreference.com/w/c/header/math.html) | `sin` / `log` 等 (常需链接 `libm`) |
| 日历时间, 时钟与格式化 | [`<time.h>`](https://en.cppreference.com/w/c/header/time.html) | `time`, `localtime`, `strftime` 等 |


## 字符串与内存块

符号处理程序最终都落在「长度 / 拷贝 / 连接 / 比较 / 搜索 / 分割」几类操作上. 下面按用途归类; 原型与缓冲区责任见[函数接口 · `strcpy` / `strncpy`](函数接口.md#strcpy--strncpy).

### 初始化与长度

```c
#include <string.h>

void *memset(void *s, int c, size_t n);   /* 把 n 字节都写成 (unsigned char)c, 常用于清零 */
size_t strlen(const char *s);             /* 到 '\0' 为止的字符数, 不含 '\0' */
```

局部数组与 `malloc` 得到的块初值不确定, 需要确定性内容时再 `memset`. `strlen` 要求 `s` 确实以 `'\0'` 结尾; 若缓冲区没有终止符就会越界读, 触发[未定义行为](数据类型详解.md#三种行为).

### 拷贝: `str*` 与 `mem*`

| 函数 | 停在哪里 | 重叠区 |
|:-----|:---------|:-------|
| `strcpy` / `strncpy` | 遇 `'\0'` (或 `strncpy` 写满 `n`) | 不允许重叠 (`restrict`) |
| `memcpy` | 固定拷 `n` 字节 | 不允许重叠 |
| `memmove` | 固定拷 `n` 字节 | **允许**重叠 |

`memcpy` 与 `memmove` 都不把参数当 C 字符串看待, 参数类型是 `void *`. C99 在 `memcpy` 上加了 `restrict`, 等于约定调用者保证区间不重叠, 实现与编译器才可按「无别名」做优化; 可能重叠时用 `memmove`.

POSIX 另有 `strdup`: 内部 `malloc` 再拷贝整串, 返回新指针, 用完必须 `free`. 归属与寿命规则同[堆分配并返回](函数接口.md#堆分配并返回).

### 连接, 比较, 搜索

```c
#include <string.h>

char *strcat(char *dest, const char *src);
char *strncat(char *dest, const char *src, size_t n);  /* 最多再接 n 个字符, 且总会写 '\0' */
int strcmp(const char *s1, const char *s2);            /* <0 / 0 / >0 */
int strncmp(const char *s1, const char *s2, size_t n);
char *strchr(const char *s, int c);                    /* 第一次出现; 找不到返回 NULL */
char *strrchr(const char *s, int c);                   /* 从右向左 */
char *strstr(const char *haystack, const char *needle);
```

`strncat` 的 `n` 是「最多从 `src` 取几个字符」, **不是** `dest` 的总容量; `dest` 至少要有 `strlen(dest) + n + 1` 字节. 这一点与 `strncpy` 的 `n` 含义不同, 读文档时不要混.

POSIX 的 `strcasecmp` / `strncasecmp` 在比较时忽略大小写, 不属于 ISO C.

### 分割: `strtok` 与可重入

```c
#include <string.h>

char *strtok(char *str, const char *delim);
char *strtok_r(char *str, const char *delim, char **saveptr);  /* POSIX */
```

`strtok` 会**就地**把分隔符改成 `'\0'`, 并用函数内部的静态指针记住下次从哪继续. 因此:

1. 不能用于字符串字面量或其它只读区.

2. 分割后原串被破坏, 分隔符不可恢复.

3. 静态状态使它不可重入, 也不适合多线程共用; 需要可重入时用 `strtok_r`, 由调用者提供 `saveptr` (典型的 Value-result 指针, 见[函数接口](函数接口.md#传入-传出与-Value-result)).

第一次调用传入待分割串, 后续传入 `NULL` 表示「接着上次」:

```c
#include <string.h>

char str[] = "root:x:0:0:root:/root:/bin/bash";
char *tok = strtok(str, ":");
while (tok != NULL) {
    /* 使用 tok ... */
    tok = strtok(NULL, ":");
}
```

### 应用示例


## 标准 I/O

### `FILE *` 与打开 / 关闭

对文件或设备做 I/O 前用 `fopen` 打开, 得到不透明指针 `FILE *` (句柄): 调用者把它在库函数之间传来传去, 不应依赖 `FILE` 内部成员. 用完后 `fclose`; 长跑进程若只开不关会耗尽系统资源.

```c
FILE *fopen(const char *path, const char *mode);
int fclose(FILE *fp);   /* 成功返回 0; 失败返回 EOF */
```

常用 `mode` (UNIX 上文本 / 二进制通常无区别, `b` 可省略):

| mode | 含义 |
|:-----|:-----|
| `"r"` | 只读, 文件必须已存在 |
| `"w"` | 只写; 不存在则创建, 已存在则截断为 0 |
| `"a"` | 追加写; 不存在则创建 |
| `"r+"` / `"w+"` / `"a+"` | 在对应基础上允许读写 |

失败时 `fopen` 返回 `NULL` 并设置 `errno`. 错误信息应打到 `stderr`:

```c
FILE *fp = fopen(path, "r");
if (fp == NULL) {
    perror(path);          /* 或 fprintf(stderr, ...) */
    exit(EXIT_FAILURE);
}
```

### `stdin` / `stdout` / `stderr`

进程启动时库会打开三个流: **标准输入** `stdin`, **标准输出** `stdout`, **标准错误** `stderr`. `printf` 写 `stdout`, `scanf` 读 `stdin`. 正常结果与诊断信息分开, 是为了重定向时互不干扰 (例如只把 stdout 接到文件, 错误仍留在终端).

### `errno` 与 `perror`

```c
#include <errno.h>
#include <stdio.h>
#include <string.h>

void perror(const char *s);           /* 打印 s, 再打印 ": " 与 errno 对应说明, 输出到 stderr */
char *strerror(int errnum);           /* 返回指向静态说明串的指针 */
```

`errno` 是线程相关的错误码存储 (历史上是全局 `int`). 许多失败路径会改写它; 成功路径是否清零因函数而异, **不能**靠「调用前 `errno` 非 0」判断失败, 必须先看函数返回值. `strerror` 返回的指针指向静态缓冲, 多次调用会互相覆盖, 规则同[静态缓冲区](函数接口.md#静态缓冲区).

### 读写粒度

在已打开的流上, 可按粒度选择接口 (均需传入 `FILE *`, 对标准流则用 `stdin` / `stdout`):

| 粒度 | 读 | 写 |
|:-----|:---|:---|
| 字节 | `fgetc` / `getc` | `fputc` / `putc` |
| 字符串 (遇换行或满缓冲) | `fgets` | `fputs` |
| 记录 (二进制块) | `fread` | `fwrite` |
| 格式化 | `fscanf` / `scanf` / `sscanf` | `fprintf` / `printf` / `sprintf` / `snprintf` |

定位用 `fseek` / `ftell` / `rewind`. 读到流末尾时, 面向字符的接口常返回 `EOF` (值为 `-1`); 应用 `feof` / `ferror` 区分「真结束」与「出错」.

拼串优先 `snprintf(buf, sizeof buf, ...)`, 避免 `sprintf` 不知缓冲区长度而溢出. [可变参数与格式串类型必须一致](函数接口.md#可变参数).

打印已有字符串时写 `printf("%s", s)`, 不要写 `printf(s)`: 若 `s` 含 `%`, 会被当成转换说明并从栈上误取参数.

### I/O 缓冲区

标准库在用户空间为每个流维护缓冲区, 多数读写先落在缓冲里, 满了或需要时再经系统调用进内核, 从而减少陷入次数.

写方向上常见三种策略:

| 类型 | 何时把数据交给内核 | 典型对象 |
|:-----|:-------------------|:---------|
| 全缓冲 | 缓冲写满, 或 `fflush` / `fclose` | 普通文件 |
| 行缓冲 | 遇到换行, 或缓冲写满, 或 `fflush` | 连到终端时的 `stdout` |
| 无缓冲 | 每次写库调用都尽快交出 | 通常是 `stderr` |

因此 `printf("hello");` 后若进程被信号杀掉且没有换行、也未 `fflush`/`exit`, 终端上可能什么都看不到; `printf("hello\n");` 或正常 `return` 经 `exit` 刷新后才会出现. 需要立刻看到输出时显式 `fflush(stdout)`.

## 数值字符串转换

```c
#include <stdlib.h>

int atoi(const char *nptr);                              /* 简便, 几乎无法区分「真是 0」与「解析失败」 */
long strtol(const char *nptr, char **endptr, int base);  /* 可检查范围与未解析后缀 */
double strtod(const char *nptr, char **endptr);
```

`atoi("123abc")` 得 `123`; `atoi("asdf")` 也得 `0`, 与合法的 `"0"` 无法区分. 严格场景用 `strtol` / `strtod`:

1. 调用前 `errno = 0`.

2. 传入 `endptr`, 返回后若 `endptr == nptr` 表示没有识别到任何数字.

3. 若 `errno == ERANGE` 表示溢出 / 下溢.

4. 若 `*endptr != '\0'` 表示后面还有未吃掉的字符 (是否算错由应用决定).

`base` 为 `0` 时按 C 字面量规则认前缀 (`0` → 八进制, `0x` → 十六进制); 显式传 `10` / `16` 等则按该进制解析.

## 分配内存

```c
#include <stdlib.h>

void *malloc(size_t size);                      /* 未初始化 */
void *calloc(size_t nmemb, size_t size);        /* nmemb * size 字节, 并清零 */
void *realloc(void *ptr, size_t size);          /* 调整大小, 可能搬迁 */
void free(void *ptr);                           /* free(NULL) 合法 */
```

- `malloc` / `calloc` / `realloc` 失败返回 `NULL`; 成功返回的指针必须最终 `free` 恰好一次.

- `realloc` 可能返回**新地址**: 务必 `p = realloc(p, n)` 的写法要先用临时变量接返回值, 失败时旧块仍然有效, 直接赋给 `p` 会丢掉唯一指针.

- `realloc(NULL, n)` 等价 `malloc(n)`; 部分实现对 `realloc(p, 0)` 的语义有历史差异, 新代码避免依赖「用 `realloc` 释放」.

- POSIX 的 `alloca` 在**调用者栈帧**上分配, 函数返回即失效, 不能 `free`, 过大则栈溢出风险高; 与 C99 VLA 类似, 不属于 ISO C 堆接口.

所有权, 泄漏与简易分配器模型见[函数接口 · `malloc` / `free`](函数接口.md#malloc--free) 与 [stdlib Heap Functions](C-Memory-Management.md#stdlib-Heap-Functions).

### 应用示例

---
date: 2026-10-20 16:13:40
title: RISC-V汇编基础
permalink: riscv-asm-overview
publish: true
tags:
  - 编程语言
  - Assembly
---

# RISC-V汇编基础

> [Assembly - RISC-V | CTF Wiki](https://ctf-wiki.org/assembly/risc-v/readme/)
>
> [RISC-V ISA | CS 61C Course Note](https://notes.cs61c.org/content/rv-intro/rv-isa/)
>
> [RISC-V Assembly Programmer's Manual](https://github.com/riscv-non-isa/riscv-asm-manual/blob/main/src/asm-manual.adoc)
>
> [RISC-V psABI](https://github.com/riscv-non-isa/riscv-elf-psabi-doc/blob/master/riscv-cc.adoc)
>
> [RV32I Base Integer Instruction Set | RISC-V Specification](https://docs.riscv.org/reference/isa/v20260120/unpriv/rv32.html)


!!! abstract
    - 汇编语言用助记符和标签描述指令序列; 汇编器再把它们转换为机器码. 伪指令和汇编器指令是写汇编时的便利工具, 不一定对应 CPU 指令.

    - 本文以**RV32I**和GNU汇编常见写法为例, 重点介绍指令操作数、内存访问、分支、函数调用和汇编文本结构.

    - 寄存器、指令编码等要素在不同 XLEN、扩展、工具链和 ABI 下的细节不能直接混用.

!!! review
    汇编语言是 ISA 指令的符号化表示, 不是机器码本身. 源文件通常经过汇编器和链接器, 才成为可执行文件:

    ```text
    C/C++ source
        | compiler
        v
    assembly source (.s)
        | assembler
        v
    object file (.o): machine code + symbols + relocations
        | linker
        v
    executable
    ```

    - **ISA**定义处理器可见的寄存器、指令语义和内存访问规则

    - **ABI**规定不同编译单元之间如何传参、返回结果和保存寄存器

    - **汇编器语法**则规定源文件如何书写

    这些是不同层次的约定, 参见[指令集架构的状态机模型](../../csa/指令集架构的状态机模型.md)和[处理器组成及工作原理](../../csa/处理器组成及工作原理.md).

    本文示例面向 RV32I. `RV32` 表示 XLEN 为 32 位, `I` 表示基础整数指令集. 乘除法、压缩指令、浮点等属于扩展; 编译和汇编时要使用与目标处理器、运行环境相符的 `-march` 和 `-mabi`. 更多基础与扩展的区别见[其他 RISC-V 基础指令集](../../csa/risc-v/RV32I%20Reference%20Card.md#Other-Base-in-RISC-V).

## RISC-V汇编语句的基本形式

一条典型 RISC-V 指令由助记符和操作数组成:

```asm
add  t0, t1, t2       # t0 = t1 + t2
addi t0, t1, 12       # t0 = t1 + 12
```

常见算术指令的操作数顺序是**目标在前, 源在后**:

```text
op  rd, rs1, rs2      # rd = rs1 op rs2
op  rd, rs1, imm      # rd = rs1 op imm
```

寄存器可写作 `x0`-`x31`, 也可使用 ABI 别名, 如 `zero`, `ra`, `sp`, `t0`, `s0`, `a0`. 别名不是额外的硬件寄存器, 而是同一组寄存器的惯用名称. `x0` 恒为 0, 写入会被忽略; 其余寄存器的角色与保存规则见[寄存器约定](../../csa/risc-v/RV32I%20Reference%20Card.md#Register-Convention).

上面的 `#` 是 GNU RISC-V 汇编中常见的行内注释起始符. 注释不参与执行. 源文件中还会出现标签和汇编器指令:

```asm
.text                   # 后续内容放入代码节
.globl add_two          # 使符号可供其他目标文件引用
add_two:                # 标签: 表示当前位置
    add a0, a0, a1      # CPU 指令
    ret                 # 伪指令: 从函数返回
```

- `add` 是 CPU 指令, 由 ISA 定义.

- `ret` 是伪指令, 汇编器会把它展开为真实指令.

- `.text` 和 `.globl` 是汇编器指令, 用于组织代码或目标文件符号, 不作为普通 CPU 指令执行.

- `add_two:` 是标签, 可被分支、跳转或其他目标文件引用.

汇编器指令的具体名称和行为可能因工具链及目标文件格式而异. 详细的 GNU RISC-V 汇编的伪指令与指令说明见[官方手册(RISC-V Assembly Programmer's Manual)](https://github.com/riscv-non-isa/riscv-asm-manual/blob/main/src/asm-manual.adoc).

## 常见指令与寻址

> [RV32I Base Integer Instruction Set](../../csa/risc-v/RV32I%20Reference%20Card.md#RV32I-Base-Integer-Instruction-Set)

### 算术与逻辑

算术和逻辑指令直接读取寄存器并写入寄存器, 不会隐式读取或写入内存:

```asm
add  t0, t1, t2       # t0 = t1 + t2
sub  t0, t1, t2       # t0 = t1 - t2
and  t0, t1, t2       # 按位与
slli t0, t1, 2        # 左移 2 位
```

RISC-V 基础整数指令不设条件码寄存器. 比较和分支通常直接由 `beq`, `bne`, `blt`, `bge` 等指令完成; `blt` / `bge` 按有符号数比较, `bltu` / `bgeu` 按无符号数比较. 读代码时要确认数据的解释方式, 不要把它们混为一谈.

### 内存访问

> [Memory - RV32I Reference Card](../../csa/risc-v/RV32I%20Reference%20Card.md#Memory).

RV32I 是加载-存储架构: 算术指令使用寄存器, 只有 load / store 指令访问内存. 内存操作数常写作 `offset(base)`, 表示有效地址为基址寄存器加偏移:

```asm
lw t0, 0(a0)           # t0 = *(int32_t *)a0
lw t1, 4(a0)           # t1 = *(int32_t *)(a0 + 4)
sw t1, 8(a0)           # *(int32_t *)(a0 + 8) = t1
```

`lw` 从内存加载一个 32 位 word, `sw` 把寄存器低 32 位写入内存. 对字节和半字有 `lb` / `lbu`, `lh` / `lhu` 及 `sb`, `sh`; 带 `u` 的 load 会进行零扩展, 不带 `u` 的 load 会进行符号扩展. 地址对齐要求及不对齐访问行为还取决于执行环境.

与 C 相似, 需要区分一个地址和地址处的数据: `a0` 是寄存器里的地址, `0(a0)` 是通过该地址读取或写入的内存位置. 指令不会替程序检查指针是否有效, 也不会自动知道该地址属于数组或变量.

### 分支与跳转

> [Control - RV32I Reference Card](../../csa/risc-v/RV32I%20Reference%20Card.md#Control)

条件分支把比较和控制流转移合为一条指令:

```asm
    beq  t0, zero, .Ldone  # t0 == 0 时跳转
    blt  t0, t1, .Lless    # 有符号比较: t0 < t1 时跳转
    bltu t0, t1, .Lbelow   # 无符号比较: t0 < t1 时跳转
```

标签 `.Ldone` 等是汇编源文件中的位置名称. 分支条件不成立时, 程序继续执行下一条指令. RISC-V 没有单独的 `cmp` 指令; 若想看某个值是否为零, 常用 `beq reg, zero, label` 等形式.

`jal rd, label` 跳转到标签并将返回地址写入 `rd`; `jalr rd, rs1, imm` 根据寄存器和偏移间接跳转. 常见伪指令 `j label`, `call function` 和 `ret` 会由汇编器展开.

## 函数调用与 ABI

> [Register Convention - RV32I Reference Card](../../csa/risc-v/RV32I%20Reference%20Card.md#Register-Convention)

RISC-V 函数如何传递参数、返回结果及保存寄存器, 由 ABI 决定, 不是 `jal` 自动完成的. 常见整数调用约定如下:

- `a0`-`a7` 用于传递整数或指针参数; `a0` 和 `a1` 也可用于返回值.

- `t0`-`t6` 是临时寄存器, 函数调用后内容不保证保留.

- `s0`-`s11` 是被调用者保存寄存器; 函数若改写, 返回前必须恢复原值.

- `ra` 保存返回地址. 调用其他函数前, 若当前函数之后还要用原来的 `ra`, 就要先保存它.

- `sp` 是栈指针. 需要保存寄存器或局部数据时, 函数可分配栈帧; 返回前要恢复栈指针及保存的寄存器.

这些是标准 ABI 的常用约定; RV32E、RV64、浮点调用约定或特定执行环境可能不同. 参见[RISC-V psABI](https://github.com/riscv-non-isa/riscv-elf-psabi-doc/blob/master/riscv-cc.adoc).

## 示例

> [lang/asm/add-riscv | virtualguard101/vglab](https://github.com/virtualguard101/vglab/tree/main/lang/asm/add-riscv)

还是以在[x86_64](x86-64汇编基础.md#示例)和[ARM](arm汇编基础.md#示例)中使用的 `add.c` 为例:

```c
int add(int a, int b)
{
    return a + b;
}

int main(void)
{
    int res = add(2, 3);

    return 0;
}
```

使用以下命令执行交叉编译, 显式指定 RV32I 和无硬件浮点的 ABI:

```bash
riscv32-unknown-elf-gcc -S -O0 -march=rv32i -mabi=ilp32 add.c -o add.s
```

生成的 `add.s` 以 `.attribute arch, "rv32i2p1"` 标注目标 ISA. 这里的 `-march` 和 `-mabi` 最好显式指定, 不要省略. 我这里的RV工具链的默认值是 `rv32imafdc...` 加 `ilp32d`, 若用默认值编译, 结果会使用 M / A / F / D / C 等扩展, 并采用硬件双精度浮点 ABI, 与 RV32I 不一致. 不同工具链的默认目标可能不同, 应以汇编代码中的 `.attribute arch` 和 `readelf -h -A add.o` 的实际输出为准.

### `add` 函数

RISC-V 整数调用约定将前两个整数参数放在 `a0`、`a1`, 普通 32 位整数返回值放在 `a0`. 与 ARM 示例类似, `-O0` 的输出会先把参数存到栈上, 再读回来运算:

```asm
add:
    addi sp,sp,-32      # 分配 32 字节栈帧
    sw   ra,28(sp)      # 保存返回地址
    sw   s0,24(sp)      # 保存调用者的 s0 (帧指针)
    addi s0,sp,32       # s0 指向栈帧顶部
    sw   a0,-20(s0)     # 将参数 a 保存到栈上
    sw   a1,-24(s0)     # 将参数 b 保存到栈上
    lw   a4,-20(s0)     # 取回 a
    lw   a5,-24(s0)     # 取回 b
    add  a5,a4,a5       # a5 = a + b
    mv   a0,a5          # 返回值放入 a0
    lw   ra,28(sp)      # 恢复 ra
    lw   s0,24(sp)      # 恢复 s0
    addi sp,sp,32       # 回收栈帧
    jr   ra             # 返回
```

`add` 是叶子函数, 没有调用其他函数, 但 `-O0` 仍保存和恢复了 `ra`; 优化版本通常会省掉这些存取. `s0` 是被调用者保存寄存器, 这里被用作帧指针, 因此函数返回前必须恢复. `jr ra` 就是伪指令 `ret` 的展开形式.

栈帧可按 `s0` 周围的偏移理解:

```text
较高地址
  [s0 - 4]   保存的 ra  (= sp + 28)
  [s0 - 8]   保存的 s0  (= sp + 24)
  [s0 - 20]  参数 a 的栈副本
  [s0 - 24]  参数 b 的栈副本  <- 偏移 sp + 8
  ...        (其余为对齐 / 保留空间)
  [sp]       函数体执行时的 sp
较低地址
```

`stack_align, 16` 表示该 ABI 要求栈指针按 16 字节对齐, 所以栈帧大小是 16 的倍数. 这是这份 `-O0` 输出的布局, 不是 ABI 要求所有函数都使用的固定模板.

### 函数调用

`main` 的关键指令如下:

```asm
main:
    addi sp,sp,-32
    sw   ra,28(sp)      # 保存 main 自己的返回地址
    sw   s0,24(sp)
    addi s0,sp,32
    li   a1,3           # 第二个参数 b = 3
    li   a0,2           # 第一个参数 a = 2
    call add            # ra = 返回地址, 然后跳转到 add
    sw   a0,-20(s0)     # 将 add 的返回值保存到局部变量 res
    li   a5,0
    mv   a0,a5          # main 返回 0
    lw   ra,28(sp)
    lw   s0,24(sp)
    addi sp,sp,32
    jr   ra
```

调用过程可以简化成如下形式:

```text
main: a0 = 2, a1 = 3
      |
      | call add: 把返回地址写入 ra
      v
add:  读取 a0 / a1 -> 相加 -> 把结果写入 a0 -> ret
      |
      v
main: 从 a0 取回结果, 保存到 res
```

`main` 不是叶子函数, 因为它调用了 `add`: `call` 会覆盖 `ra`, 所以入口处必须先把 `main` 原来的返回地址保存到栈上, 返回前再恢复. 如果省略这一步, `main` 的最后一条 `ret` 就会跳回 `add` 的返回点, 造成死循环. `call` 本身也是伪指令, 展开见下一节.

### 目标文件反汇编

使用如下代码生成 C 目标文件并对其进行反汇编:

```bash
riscv32-unknown-elf-gcc -march=rv32i -mabi=ilp32 -c add.s -o add.o
riscv32-unknown-elf-objdump -d add.o
```

输出开头的 `file format elf32-littleriscv` 表示目标文件是 32 位小端 RISC-V ELF. `Disassembly of section .text` 说明下面是代码节的内容; `00000000 <add>:` 和 `00000038 <main>:` 是符号及其在 `.text` 中的偏移. 因为是未链接的 `.o`, 地址从 0 开始, 并不是程序运行时的最终地址.

每条指令占一行, 格式为 `偏移: 机器码 助记符 操作数`:

```text
  20:	00f707b3          	add	a5,a4,a5
  34:	00008067          	ret
```

RV32I 指令定长 4 字节, 所以偏移每行加 4. `add` 从 `0x00` 到 `0x34` 共 14 条指令, 因此下一个函数 `main` 从 `0x38` 开始, 并在 `0x70` 的 `ret` 处结束.

#### 机器码对照

机器码按[指令格式](../../csa/risc-v/RV32I%20Reference%20Card.md#Instruction-Format-by-Type)拆分, 可以和汇编逐字段对应. 以 `add` 中几条有代表性的指令为例:

| 偏移 | 机器码 | 格式 | 拆分 | 汇编 |
|:-----|:-------|:----:|:-----|:-----|
| `0x00` | `fe010113` | I | `imm=0xfe0` (-32), `rs1=2`, `funct3=000`, `rd=2`, `opcode=0010011` | `addi sp,sp,-32` |
| `0x04` | `00112e23` | S | `imm=0x01c` (28), `rs2=1`, `rs1=2`, `funct3=010`, `opcode=0100011` | `sw ra,28(sp)` |
| `0x18` | `fec42703` | I | `imm=0xfec` (-20), `rs1=8`, `funct3=010`, `rd=14`, `opcode=0000011` | `lw a4,-20(s0)` |
| `0x20` | `00f707b3` | R | `funct7=0`, `rs2=15`, `rs1=14`, `funct3=000`, `rd=15`, `opcode=0110011` | `add a5,a4,a5` |

几点需要注意:

- 寄存器在机器码里是编号, 汇编里显示的是 ABI 别名: `x2` 是 `sp`, `x1` 是 `ra`, `x8` 是 `s0`, `x14` / `x15` 是 `a4` / `a5`. 对应关系见[寄存器约定](../../csa/risc-v/RV32I%20Reference%20Card.md#Register-Convention).

- `sw` 是 S 型, 12 位偏移被拆开存放: 高 7 位在 `[31:25]`, 低 5 位在 `[11:7]`. 因此 `sw ra,28(sp)` 的机器码 `00112e23` 里, `[11:7]` 为 `11100` (即 28 的低 5 位).

- `lw` 是 I 型, 偏移是连续的 12 位, 按符号扩展处理, `0xfec` 就是 -20.

- `add` 与 `sub` 的 `opcode` 和 `funct3` 相同, 只靠 `funct7` 区分 (`add` 为 `0000000`), 参见 [为什么用多个字段编码指令](../../csa/risc-v/RV32I%20Reference%20Card.md#Arithmetic).

#### 伪指令的展开

反汇编显示的是真实指令的解码结果, 不过 `objdump` 默认会把一些常见组合显示为伪指令别名. 对照 `disasm.s`:

| 反汇编显示 | 机器码 | 真实指令 |
|:-----------|:-------|:---------|
| `mv a0,a5` | `00078513` | `addi a0,a5,0` |
| `li a1,3` | `00300593` | `addi a1,x0,3` |
| `ret` | `00008067` | `jalr x0,0(ra)` |

因此看到别名时, 不要认为 CPU 里有 `mv`、`li`、`ret` 这些独立指令. 可以用 `-M numeric,no-aliases` 让 `objdump` 按真实指令和数字寄存器名输出, 例如把 `ret` 显示为 `jalr x0,0(x1)`.

汇编源文件中的 `jr ra` 在反汇编中也显示为 `ret`: 这两个写法编码相同, 反汇编器无法, 也不需要区分它们.

#### `call` 与重定位

`main` 中调用 `add` 的部分在源汇编里只有一条 `call add`, 但反汇编里是两条指令:

```text
  50:	00000097          	auipc	ra,0x0
  54:	000080e7          	jalr	ra # 50 <main+0x18>
```

`call` 是伪指令, 汇编器把它展开为 `auipc ra, imm20` 加 `jalr ra, imm12(ra)`, 这样可以跳转到当前位置 $\pm 2$ GiB 范围内的任意地址, 比单条 `jal` 的 $\pm 1$ MiB 范围更大. 此时两条指令的立即数字段都是 0, 即机器码里的 `00000097` 和 `000080e7` 里没有目标地址. 原因是 `add` 的最终地址要到链接阶段才能确定, 汇编器只在目标文件中留下**重定位**记录, 交给链接器回填. 行尾的 `# 50 <main+0x18>` 是 `objdump` 按当前 0 立即数算出的跳转目标, 因此指向自己, 不是真实的调用目标.

加上 `-r` 就能看到重定位记录:

```bash
riscv32-unknown-elf-objdump -dr add.o
```

在 `0x50` 处会多出 `R_RISCV_CALL_PLT add`, 说明链接器要在这里填入 `add` 的地址; 同时可能还有 `R_RISCV_RELAX`, 表示链接器允许把这对指令松弛 (relax) 成单条 `jal`. 因此链接后的可执行文件反汇编结果可能不再是 `auipc` + `jalr`.

#### 查看目标文件属性

`readelf -h -A add.o` 可以验证目标文件是 `ELF32`、机器类型为 `RISC-V`, 并显示 `Tag_RISCV_arch: "rv32i2p1"` 和栈对齐属性. 与 ARM 一样, 不能仅凭 `.o` 扩展名判断文件面向哪个目标.

## 交叉编译与调试

RV32 程序一般在 x86-64 等主机上交叉编译. 需要先安装目标为 RISC-V 的工具链; 不同发行版的包名不同, 工具链前缀也可能是 `riscv32-unknown-elf-`、`riscv64-elf-` 或 `riscv64-linux-gnu-` 等. 前缀中的 `elf` 表示面向裸机 / 无操作系统的目标, `linux-gnu` 则面向 Linux 用户态程序, 两者使用的 libc 和系统调用约定不同.

64 位前缀的工具链也可以通过 `-march=rv32*` 和 `-mabi=ilp32*` 生成 RV32 代码, 但只有它带有对应的 multilib (预编译好的 RV32 版 libc / libgcc) 时, 才能链接标准库. 可以用下面的命令检查:

```bash
riscv32-unknown-elf-gcc -print-multi-lib
riscv32-unknown-elf-gcc -march=rv32i -mabi=ilp32 -print-libgcc-file-name
```

如果输出的路径中没有对应的 `rv32i/ilp32` 目录, 链接时就可能报 `cannot find -lc` 或 ABI 不兼容. 此时可以改用带 RV32 multilib 的工具链, 自行构建 [riscv-gnu-toolchain](https://github.com/riscv-collab/riscv-gnu-toolchain), 或者使用 `-nostdlib` / `-ffreestanding` 并自行提供所需函数.

常用命令如下(上面的示例用到的交叉编译工具链命令):

```bash
# 由 C 生成 RV32I 汇编
riscv32-unknown-elf-gcc -S -O0 -march=rv32i -mabi=ilp32 add.c -o add.s

# 组装成 ELF 目标文件; 这里也必须指定 -march / -mabi
riscv32-unknown-elf-gcc -march=rv32i -mabi=ilp32 -c add.s -o add.o

# 查看机器码和反汇编
riscv32-unknown-elf-objdump -d add.o

# 查看 ELF 架构、属性和符号
riscv32-unknown-elf-readelf -h -A -s add.o
```

!!! warning "汇编 `.s` 时也要指定 `-march` 和 `-mabi`"
    `.s` 中的 `.attribute arch` 只记录目标 ISA, 并不会决定 ABI. 以我的环境为例, 若汇编时省略 `-mabi=ilp32`, 工具链会按默认的 `ilp32d` 处理, 并报 `ilp32d/lp64d ABI can't be used when d extension isn't supported`. 因此编译和汇编两步的参数应保持一致.

`-march` 和 `-mabi` 必须匹配:

| `-march` 示例 | 可搭配的 `-mabi` | 说明 |
|:--------------|:-----------------|:-----|
| `rv32i` | `ilp32` | 无硬件浮点 |
| `rv32e` | `ilp32e` | 只有 `x0`-`x15`, 常用于微小核, 如 [minirv32 CPU](../../csa/minirv32%20CPU.md) 使用的 RV32E |
| `rv32imac` | `ilp32` | 含乘除、原子和压缩指令, 仍然使用软浮点 ABI |
| `rv32imafc` | `ilp32f` | 单精度硬件浮点 |
| `rv32imafdc` | `ilp32d` | 单、双精度硬件浮点 |

要把 C 程序链接成可执行文件, 裸机环境还需要启动代码 (设置 `sp`, 清零 `.bss`, 跳转到 `main`) 和链接脚本, 链接地址须与目标板或模拟器的内存映射一致. 这里不展开讨论, 本文的示例只做到生成并检查目标文件.

调试时可以使用支持 RISC-V 目标的 GDB (如 `riscv32-unknown-elf-gdb`). 连接到 QEMU 或硬件调试器后:

```text
break add
continue
disassemble add
info registers a0 a1 sp ra pc
display/i $pc
si
```

- `disassemble add`: 查看 `add` 函数的机器指令.

- `info registers`: 检查参数寄存器、栈指针、返回地址和程序计数器.

- `display/i $pc`: 每次暂停时显示当前指令.

- `si`: 单步执行一条机器指令; 遇到 `call` 展开出的 `jalr` 时会进入被调用函数.

如果需要运行 RV32 程序, 可进一步了解 QEMU 的 `qemu-system-riscv32` 系统模拟或 Linux 用户态模拟.

## 阅读与验证汇编的顺序

阅读一段 RISC-V 汇编时, 可以按以下顺序跟踪:

1. 确认目标是 RV32 还是 RV64, 使用了哪些扩展, 以及采用哪个 ABI.

2. 区分真实指令、伪指令、汇编器指令和标签.

3. 对每条指令标出源寄存器、目标寄存器及立即数, 追踪寄存器值的变化.

4. 遇到 `offset(base)` 时计算有效地址, 并检查访问宽度与符号扩展.

5. 跟踪分支条件和跳转目标, 再按 ABI 还原函数参数、返回值和保存规则.

6. 需要确认伪指令展开或编码时, 查看所用工具链生成的目标文件和反汇编; 不同汇编器选项可能影响展开和代码布局.

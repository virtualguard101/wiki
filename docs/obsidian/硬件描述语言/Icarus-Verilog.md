---
date: 2026-10-10 00:59:33
title: Icarus Verilog
permalink: iverilog
publish: true
tags:
  - 硬件描述语言
  - Verilog
  - 工具
---

# Icarus Verilog

> [Icarus Verilog documentation](https://steveicarus.github.io/iverilog/index.html)
>
> [GTKWave](https://gtkwave.sourceforge.net/)
>
> [Surfer](https://surfer-project.org/)

简单了解[Verilog](Verilog入门要点.md)语法基础和部分写法后, 我们就可以尝试编写一些简单的 Verilog 代码了.

前面我们也了解到, Verilog 是一种[硬件描述语言](Verilog入门要点.md#HDL-概述), 因此其不像普通的编程语言, 可以直接通过[编译](../编程语言/cpp/cs106l/基础类型与结构体.md#基础数据类型)或[解释](../编程语言/cpp/cs106l/基础类型与结构体.md#基础数据类型)直接执行并验证程序行为是否符合预期, 虽然二者有共通之处, 但其还是有一套自己的验证方法, 我们一般称其为**仿真**.

!!! abstract
    - **Icarus Verilog** 是开源 Verilog 仿真器: `iverilog` 编译, `vvp` 运行.

    - 波形用[GTKWave](https://gtkwave.sourceforge.net/)或[Surfer](https://surfer-project.org/)查看. testbench 里使用 `$dumpfile` / `$dumpvars` 写出 VCD/FST 波形文件.

    - 设计文件可综合. testbench 只服务仿真 (`initial`, `#`, `$display` 等通常不可综合).

## 工具

| 工具 | 作用 |
|:--|:--|
| `iverilog` | 读入 `.v`, 预处理 / 编译 / 精化 (*elaboration*), 默认生成 `vvp` 可执行中间文件 |
| `vvp` | Verilog Virtual Processor, 执行仿真 |
| `gtkwave` / `surfer` | 打开 VCD / FST 等波形文件, 对照信号时序排查错误 |

### 安装

```bash
# Arch Linux
sudo pacman -S iverilog gtkwave

# Debian / Ubuntu
sudo apt install iverilog gtkwave

# macOS (Homebrew)
brew install icarus-verilog gtkwave
```

## 仿真示例

以[HDLBits 7458](https://hdlbits.01xz.net/wiki/7458)为例, 对应芯片逻辑: 两组「与门 + 或门」组合.

Verilog 代码如下:

```verilog
module top_module (
    input  p1a, p1b, p1c, p1d, p1e, p1f,
    output p1y,
    input  p2a, p2b, p2c, p2d,
    output p2y
);
  assign p1y = (p1a & p1b & p1c) | (p1d & p1e & p1f);
  assign p2y = (p2a & p2b) | (p2c & p2d);
endmodule
```

仅有**DUT**(*Design Under Test*, 被测设计)时, `iverilog` 能编译, 但没有激励与观察, **无法验证正确性**. 需要编写旁路的**testbench**进行仿真验证.

### Testbench

Testbench 通常具有以下特点:

1. 无端口 (顶层仿真壳).

2. 用 `reg` 驱动 DUT 输入, `wire` 接 DUT 输出.

3. 例化 DUT, 施加向量, 打印或自动比对.

4. (可选) `$dumpfile` / `$dumpvars` 导出波形.

以上面的 `7458.v` 为例, 尝试编写 testbench `7458_tb.v`, 核心结构如下:

```verilog
module tb_7458;
  reg  p1a, p1b, p1c, p1d, p1e, p1f;
  reg  p2a, p2b, p2c, p2d;
  wire p1y, p2y;
  integer errors;

  top_module dut (
    .p1a(p1a), .p1b(p1b), .p1c(p1c),
    .p1d(p1d), .p1e(p1e), .p1f(p1f), .p1y(p1y),
    .p2a(p2a), .p2b(p2b), .p2c(p2c), .p2d(p2d), .p2y(p2y)
  );

  initial begin
    $dumpfile("7458.vcd");
    $dumpvars(0, tb_7458);  // 0 = 本模块及以下全部信号
  end

  // check task: 驱动输入 → #1 等待组合稳定 → 与 golden 比对
  // ... 若干 check(...) 向量 ...
  // $finish;
endmodule
```

!!! tip
    组合逻辑在输入变化后可能有仿真延迟或同一时刻调度顺序问题. 施加输入后用 `#1` (或更长) 再采样输出, 比紧贴赋值立刻读更稳妥. 四值比较用 `!==` / `===`, 以便区分 `x` / `z`.

### 编译与运行

编译与运行命令如下:

```bash
# -g2012: 启用较新的 Verilog / SystemVerilog 子集 (本 TB 用了 automatic function/task)
# -Wall:  打开更多警告
iverilog -g2012 -Wall -o 7458.vvp 7458.v 7458_tb.v

vvp 7458.vvp
```

期望输出类似:

```text
VCD info: dumpfile 7458.vcd opened for output.
PASS t=1 p1=000000 p2=0000 -> p1y=0 p2y=0
...
ALL TESTS PASSED
```

同时生成 `7458.vcd` (波形) 与 `7458.vvp` (编译产物). 二者属构建产物, **一般不进入版本控制系统**.

多文件也可写进命令文件再使用 `-c` 参数引用:

```text
# file_list.txt
7458.v
7458_tb.v
```

```bash
iverilog -g2012 -Wall -o 7458.vvp -c file_list.txt
```

若存在多个未被例化的模块 (多个候选 root), 用 `-s` 指定仿真顶层, 例如 `-s tb_7458`, 避免多余 root 一起被精化.

### 查看波形

```bash
gtkwave 7458.vcd &
```

操作要点:

1. 左侧 SST 选中 `tb_7458`, 再进子 scope `dut`.

2. 将 `p1a`…`p1y`, `p2a`…`p2y` 拖到 Signals.

3. 时间轴缩放, 对照某次 `PASS`/`FAIL` 的 `$time` 看输入输出是否一致.

默认 VCD 兼容性最好. 若主要用 GTKWave, 可用更紧凑的 FST:

```bash
# testbench 里可写 $dumpfile("7458.fst");
vvp -fst 7458.vvp
gtkwave 7458.fst &
```

官方说明见 [Viewing Waveforms](https://steveicarus.github.io/iverilog/usage/waveform_viewer.html).

## 调试思路

| 现象 | 常见原因 / 做法 |
|:--|:--|
| 编译报错找不到模块 | 源文件未列入 `iverilog` 命令行; 或模块名与例化不一致 |
| 多个 root / 仿真异常 | 用 `-s tb_xxx` 固定 testbench 为顶层 |
| 输出一直为 `x` | 输入未驱动; 或时序电路未复位 / 时钟未翻转 |
| 功能与预期不符 | 先看 `$display` 自检; 再在 GTKWave 对拍输入沿与输出变化 |
| 想看预处理结果 | `iverilog -E -o out.v 7458.v` 展开 `` `define`` / `` `include`` |

## 常用命令

```bash
iverilog -g2012 -Wall -o sim.vvp dut.v tb.v   # 编译
vvp sim.vvp                                   # 运行
vvp -fst sim.vvp                              # FST 波形
gtkwave dump.vcd                              # 看波形
iverilog -E -o preprocessed.v dut.v           # 仅预处理
iverilog -s tb_7458 -o sim.vvp dut.v tb.v     # 指定 root
```

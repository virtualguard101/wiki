---
date: 2026-10-08 15:16:48
title: Verilog入门要点
permalink: verilog-intro
publish: true
tags:
  - 硬件描述语言
  - Verilog
---

# Verilog入门要点

> [Verilog 语法入门 | USTC数字电路教程](https://vlab.ustc.edu.cn/guide/doc_verilog.html)
>
> [Verilog Tutorial | ASIC World](https://www.asic-world.com/verilog/veritut.html)

!!! abstract
    - Verilog 是 **HDL** (*Hardware Description Language*), 用文本描述电路结构与行为, 供仿真与综合, 不是在 CPU 上逐行执行的程序.

    - 日常设计以 **RTL** (*Register Transfer Level*) 为主: 用寄存器之间的数据传输描述硬件.

    - 最有效的写法: **先想清楚电路, 再用 Verilog 描述它**, 行为级语法看起来像 C, 但随意当软件写往往综合出糟糕甚至错误的硬件.

    - `assign` / 组合 `always` 描述[组合逻辑](../计算机系统与体系结构/组合逻辑电路.md); 带 `posedge` / `negedge` 的 `always` 描述[时序逻辑](../计算机系统与体系结构/时序逻辑电路.md).

## HDL 概述

**HDL** (*Hardware Description Language*, 硬件描述语言) 用于描述数字电路的结构与行为, 其出现的主要目标有三:

1. **文本化交换与层次化描述** — 用 `module` 组合子电路, 类似原理图中的子模块封装.

2. **先仿真再流片 / 上板** — 在硅片或 FPGA 上调试前, 用模型排查功能错误.

3. **综合** (*synthesis*) — 工具把可综合描述映射为门级网表, 再做布局布线.

业界常用 Verilog / SystemVerilog 与 VHDL. Verilog 语法更接近 C, 入门成本通常更低; 语义层面二者高度相似.

Verilog 可在**系统级**, **算法级**, **RTL**, **门级**, **开关级**描述电路. 教学与工程中最常用的是**RTL 代码**.

## 模块: 基本构造单元

`module` / `endmodule` 划定一个电路单元的边界. 端口列表是对外接口; `input` / `output` / `inout` 标明方向. 模块定义不可嵌套, 但可通过**例化** (*instantiation*) 组成层次.

下面是 CS61C 教程中的 2 路选择器结构描述 (门级):

```verilog
module mux2 (in0, in1, select, out);
  input  in0, in1, select;
  output out;
  wire   s0, w0, w1;

  not (s0, select);
  and (w0, s0, in0),
      (w1, select, in1);
  or  (out, w0, w1);
endmodule
```

- 模块体更像在声明**互联的数据结构**, 而不是顺序执行的语句; 功能来自原语门及其连线.

- 内建门约定: **输出在前**, 其余为输入; 除 `not` / `buf` 外, 输入个数可变.

- 内部连线声明为 `wire`. 未显式指定类型的端口默认为 `wire`.

用已有 `mux2` 搭 4 路选择器, 体现层次化:

```verilog
module mux4 (in0, in1, in2, in3, select, out);
  input        in0, in1, in2, in3;
  input  [1:0] select;
  output       out;
  wire         w0, w1;

  mux2 m0 (.select(select[0]), .in0(in0), .in1(in1), .out(w0));
  mux2 m1 (.select(select[0]), .in0(in2), .in1(in3), .out(w1));
  mux2 m2 (.select(select[1]), .in0(w0),  .in1(w1),  .out(out));
endmodule
```

!!! tip "两种例化写法"
    - **按位置**: `mux2 m0 (a, b, s, y);` — 顺序必须与端口表严格一致, 易错.

    - **按名字** (推荐): `mux2 m0 (.in0(a), .in1(b), .select(s), .out(y));` — 可读性更好, 端口顺序无关.

同一模块可多次例化; 实例名在同一父模块内必须唯一.

## 信号, 位宽与四值逻辑

### `wire` 与 `reg`

| 类型 | 典型含义 | 常见用法 |
|:--|:--|:--|
| `wire` | 线网, 对应连线 | `assign` 驱动; 模块输出默认; 连接子模块 |
| `reg` | 寄存器型变量 (名字易误导) | 在 `always` / `initial` 中被赋值的信号 |

判断规则更实用: **在 `always` / `initial` 里被赋值 → 声明为 `reg`; 用 `assign` 驱动 → 声明为 `wire`**. `reg` 综合后不一定是触发器, 组合 `always` 里的 `reg` 往往只是组合逻辑的中间量.

### 四值与字面量

每个 bit 可取 `0`, `1`, `x` (未知), `z` (高阻). 未初始化信号常为 `x`; 多驱动总线常用 `z`.

字面量格式: `<位宽>'<进制><数值>`, 例如 `4'b1010`, `8'hFF`, `3'd7`. 下划线可穿插以提高可读性: `32'hFFFF_0000`.

### 位向量与拼接

`[3:0]` 表示 4 bit, 推荐高位在左 (`[n-1:0]`). 可用 `a[2]` 取单 bit, 用 `{ }` 拼接:

```verilog
assign y = {a[3:2], b[1:0]};   // 拼成更宽的向量
assign {cout, sum} = a + b + cin; // 左侧也可拼接
```

重复拼接 `n{m}` 常用于符号扩展, 例如把 16 bit 有符号数扩到 32 bit:

```verilog
assign Y = {{16{X[15]}}, X};
```

## 组合逻辑

> [组合逻辑电路](../计算机系统与体系结构/组合逻辑电路.md)
>
> [组合逻辑电路设计原理](../计算机系统与体系结构/组合逻辑电路的设计原理.md)

### 连续赋值 `assign`

`assign` 声明的是**持续有效的组合关系**: 右侧任一信号变化, 左侧随之更新. 它对应一块组合电路, 而不是程序里执行一次的赋值语句.

```verilog
module mux2 (in0, in1, select, out);
  input  in0, in1, select;
  output out;
  assign out = select & in1 | ~select & in0;
endmodule
```

可写延迟: `assign #3 out = ...;` (仿真用; 综合通常忽略或另有约定).

### 常用运算符

| 类别 | 符号 | 说明 |
|:--|:--|:--|
| 按位 | `~` `&` `\|` `^` `~^` | 按位非 / 与 / 或 / 异或 / 同或 |
| 归约 | `&a` `\|a` `^a` | 对向量各位做与 / 或 / 异或 |
| 逻辑 | `!` `&&` `\|\|` | 逻辑非 / 与 / 或 (结果多为 1 bit) |
| 条件 | `?:` | 硬件上的多路选择 |
| 拼接 | `{ }` | 位拼接 / 拆分 |

`&` 优先于 `|`. 复杂表达式建议加括号, 避免优先级陷阱.

也可用组合型 `always @(*)` (或列出全部敏感量) 写 `if` / `case`; 此时左侧仍须为 `reg`, 且应使用**阻塞赋值** `=`. `case` 在组合逻辑中务必写 `default`, 否则易综合出无意的锁存器.

## 时序逻辑

同步时序电路在统一时钟沿更新状态, 对应[时序逻辑](../计算机系统与体系结构/时序逻辑电路.md)与[同步时序设计流程](../计算机系统与体系结构/同步时序逻辑电路设计原理.md).

带同步复位的[D 触发器](../计算机系统与体系结构/时序逻辑电路.md#D-触发器):

```verilog
module dff (
  input      clk, reset, d,
  output reg q
);
  always @(posedge clk) begin
    if (reset)
      q <= 1'b0;
    else
      q <= d;
  end
endmodule
```

异步复位则把复位沿放进敏感列表, 例如 `always @(posedge clk or posedge reset)`, 并让复位分支优先级最高.

### 阻塞 vs 非阻塞

| 写法 | 符号 | 建议场景 |
|:--|:--|:--|
| 阻塞 | `=` | 组合逻辑 `always` |
| 非阻塞 | `<=` | 时序逻辑 `always` (时钟沿) |

时序里若误用阻塞赋值, 同块内多句赋值会按软件顺序“吃掉”中间结果, 综合出与预期不符的电路. 实践约定:

1. 组合用 `=`, 时序用 `<=`.

2. 同一 `always` 内不要混用两种赋值.

3. 同一信号只在一个 `always` 或一个 `assign` 中驱动.

4. `always` 内不能例化模块, 只能给 `reg` 赋值.

## 有限状态机 (FSM)

FSM 是控制器的常用骨架. 推荐**三段式**:

1. 时序块: 现态 ← 次态 (`posedge clk`).

2. 组合块: 由现态与输入计算次态.

3. 组合块 / `assign`: 由现态 (与输入) 产生输出.

状态编码可用 `parameter` / `localparam`, 或 SystemVerilog 的 `enum`. 设计流程与状态图 / 次态方程与在学习[同步时序逻辑电路设计原理](../计算机系统与体系结构/同步时序逻辑电路设计原理.md)时的内容大致相同.

## Testbench 与仿真

Testbench 是**不综合**的顶层模块: 无端口, 负责产生激励, 例化 DUT (*Design Under Test*), 观察或自动比对输出. DUT 的输入用 `reg` 驱动, 输出接到 `wire`.

```verilog
module testmux;
  reg  a, b, s;
  wire f;
  reg  expected;

  mux2 dut (.select(s), .in0(a), .in1(b), .out(f));

  initial begin
    #0  s=0; a=0; b=1; expected=0;
    #10      a=1; b=0; expected=1;
    #10 s=1; a=0; b=1; expected=1;
    #10 $stop;
  end

  initial
    $monitor("sel=%b in0=%b in1=%b out=%b exp=%b t=%0d",
             s, a, b, f, expected, $time);
endmodule
```

常用仿真设施:

| 设施 | 作用 |
|:--|:--|
| `initial` | 仿真开始时执行一次; 多个 `initial` **并行**启动 |
| `#n` | 推进仿真时间 n 个单位 |
| `$display` / `$monitor` / `$strobe` | 打印; `$monitor` 随信号变化打印, `$strobe` 在时间步末打印稳定值 |
| `forever` / `always #5 clk = ~clk` | 产生时钟 |
| `repeat` | 循环施加激励 (如穷举输入) |

为门级仿真加延迟时, 输入变化瞬间输出可能仍为旧值或 `x`, 需等组合路径稳定后再采样. FSM 测试应尽量覆盖**每个状态对每种输入的转移**.

开源仿真常用 [Icarus Verilog](https://steveicarus.github.io/iverilog/): `iverilog -o sim.vvp dut.v tb.v && vvp sim.vvp`, 波形可用 GTKWave 查看.

## 参数化

`parameter` 可在例化时覆盖, 便于复用位宽:

```verilog
module mux2 #(parameter WIDTH = 8) (
  input  [WIDTH-1:0] in0, in1,
  input              select,
  output [WIDTH-1:0] out
);
  assign out = select ? in1 : in0;
endmodule

mux2 #(.WIDTH(12)) u0 (...);  // 例化为 12 bit
```

## 新手上路

- 先画电路 (或状态图), 再写代码. 不要把 Verilog 当 C 来“编程出”硬件.

- 区分**可综合设计**与**仅仿真 testbench** (`initial`, `#`, `$display` 等通常不可综合).

- 组合: `assign` 或 `always @(*)` + 阻塞 `=`; 时序: `always @(posedge clk)` + 非阻塞 `<=`.

- 例化优先命名端口连接; 敏感列表完整, 组合 `case` 带 `default`.

- 一个信号单一驱动源; 复位逻辑放在条件分支最前.

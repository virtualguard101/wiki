---
date: 2026-10-11 15:55:19
title: Verilog向量
permalink: verilog-vec
publish: true
tags:
  - 硬件描述语言
  - Verilog
---

# Verilog向量

> [Vectors | HDLBits](https://hdlbits.01xz.net/wiki/Vector0) · [Vector1](https://hdlbits.01xz.net/wiki/Vector1) · [Vectorgates](https://hdlbits.01xz.net/wiki/Vectorgates) · [Vectorr](https://hdlbits.01xz.net/wiki/Vectorr) · [Vector4](https://hdlbits.01xz.net/wiki/Vector4) · [Vector5](https://hdlbits.01xz.net/wiki/Vector5)
>
> [Verilog 语法入门 | USTC](https://vlab.ustc.edu.cn/guide/doc_verilog.html)
>
> [Verilog Tutorial | ASIC World](https://www.asic-world.com/verilog/veritut.html)

在[入门要点](Verilog入门要点.md)中我们大致介绍了Verilog的[位向量与拼接](Verilog入门要点.md#位向量与拼接), 本节来详细学习一下Verilog的向量操作.

!!! abstract
    - **向量** (*vector* / *bus*) 用一个名字捆绑多根相关信号, 便于按位 / 按段操作.

    - 声明写在名字**前**: `wire [7:0] w;`; 选取写在名字**后**: `w[3:0]`.

    - 推荐统一用小端下标 `[n-1:0]` (高位在左); part-select 方向必须与声明一致.

    - 核心操作: **part-select**, **按位 vs 逻辑**, **拼接 `{ }`**, **复制 `{n{m}}`**.

## 声明与位序

一个多位向量输入既可以整段输出, 也可以拆成单位逐位操作:

```verilog
module top_module (
  input  wire [2:0] vec,
  output wire [2:0] outv,
  output wire o2, o1, o0
);
  assign outv = vec;
  assign o0 = vec[0];
  assign o1 = vec[1];
  assign o2 = vec[2];
endmodule
```

向量的声明形式:

```verilog
type [upper:lower] name;
```

`type` 指定向量的数据类型, 通常是 `wire` 或 `reg`. 如果声明的是输入或输出端口，类型还可以额外包含端口类型(例如 `input` 或 `output`):

```verilog
wire [7:0] w;         // 8-bit wire
reg  [4:1] x;         // 4-bit reg
output reg [0:0] y;   // 1-bit reg that is also an output port (this is still a vector)
input wire [3:-2] z;  // 6-bit wire input (negative ranges are allowed)
output [3:0] a;       // 4-bit output wire. Type is 'wire' unless specified otherwise.
wire [0:7] b;         // 8-bit wire where b[0] is the most-significant bit.
```

!!! warning "端序约定"
    一旦用 `[3:0]` 声明, 就不能再写 `vec[0:3]` 做选取; 不同端序的向量互相赋值极易埋雷. 工程上尽量全程 `[n-1:0]`.

!!! tip "隐式网络"
    隐式网络通常是难以检测的错误的来源. 在 Verilog 中, 网络类型信号可以通过 `assign` 语句或通过将未声明的内容附加到模块端口来隐式创建. 隐式网络始终是一位线网, 如果打算使用向量, 则会导致错误:

    ```verilog
    wire [2:0] a, c;   // Two vectors
    assign a = 3'b101;  // a = 101
    assign b = a;       // b =   1  implicitly-created wire
    assign c = b;       // c = 001  <-- bug
    my_module i1 (d,e); // d and e are implicitly one-bit wide if not declared.
                        // This could be a bug if the port was intended to be a vector.
    ```
    
    可以使用 `default_nettype none` 指令禁用隐式网络的创建, 在这里, 添加 `default_nettype none` 会使第三行代码出错, 从而使这个 bug 更加明显.

!!! info "Packed vs Unpacked"
    声明里名字**前**的维度是 packed (连成总线的那些 bit); 名字**后**的是 unpacked, 多用于存储器, 例如 `reg [7:0] mem [255:0]`.

## part-select

对已声明向量, 可用:

- 整段: `assign w = a;`

- 单 bit: `a[2]`

- 连续段: `a[7:4]`

有点类似Python的[切片操作](https://liaoxuefeng.com/books/python/advanced/slice/index.html).

左右位宽不一致时, 右侧按规则**零扩展**或**截断**. 段选方向必须与声明一致, 且下标落在范围内.

!!! failure
    part-select 只是按声明顺序取出**连续一段** bit, **不会**做位序翻转. 若 `in` / `out` 声明为 `[7:0]`, 想得到 `out[7]=in[0]`, …, `out[0]=in[7]`, 不能靠反向切片, 因此下面的写法是错误的:

    ```verilog
    assign out[7:0] = in[-7:-1];  // 非法
    assign out      = in[0:7];    // 对 [7:0] 声明同样非法
    ```

    对已声明为 `[7:0]` 的向量, `in[L:R]` 须同时满足:

    1. **下标在范围内** — 合法下标只有 `0`…`7`; `-7` / `-1` 越界.

    2. **方向与声明一致** — 声明是左大右小, 选取也必须左 ≥ 右 (如 `in[7:4]`). `[-7:-1]` 与 `[0:7]` 都是左小右大 → elaboration 报 `part select ... is out of order`.

    3. **语义不是翻转** — 即便选取合法 (如 `in[7:0]`), 得到的仍是原序 MSB→LSB, 不是位反转.

    只有声明本身是 `[0:7]` 时 `in[0:7]` 才合法, 那时 `in[0]` 反而是 MSB, 仍不等于对 `[7:0]` 做翻转.

    正确做法是用拼接显式重排每一位:

    ```verilog
    assign out = {in[0], in[1], in[2], in[3], in[4], in[5], in[6], in[7]};
    ```

    `{ }` 左侧是结果的 MSB[^bit-numbering] 侧, 故放 `in[0]`, 右侧放 `in[7]`.

## 按位运算 vs 逻辑运算

| 运算 | 符号 | 行为 | 结果位宽 |
|:--|:--|:--|:--|
| 按位或 | `a \| b` | 每一位各自或 | 与操作数同宽 |
| 逻辑或 | `a \|\| b` | 把整段向量当布尔 (非零为真) | **1 bit** |
| 按位非 | `~a` | 每一位取反 | 同宽 |
| 逻辑非 | `!a` | 把整段向量当布尔 (非零为真) | **1 bit** |

与运算同理(逻辑与`&`, 按位与`&&`); 异或`^`没有逻辑运算.

```verilog
assign out_or_bitwise = a | b;
assign out_or_logical = a || b;          // 真值上等价于 (|a) || (|b)
assign out_not        = {~b, ~a};        // [5:3]=~b, [2:0]=~a
```

逐位展开, 等效于:

```verilog
assign out_or_bitwise[2] = a[2] | b[2];
// ...
assign out_not[5] = ~b[2];
assign out_not[0] = ~a[0];
```

按位运算符还可当[归约](https://oj.ustc.edu.cn/p/137)用: 单操作数时 `&a` / `|a` / `^a` 把各位压成 1 bit.

## 位拼接

拼接把若干已知位宽的片段合成更宽向量; **左侧 / 右侧**都可写 `{ }`. 未标明位宽的常量不能出现在拼接里 (`{1, 2}` 非法).

### 位反转

```verilog
assign out = {in[0], in[1], in[2], in[3], in[4], in[5], in[6], in[7]};
```

同类操作还有按字节重排:

```verilog
assign out = {in[7:0], in[15:8], in[23:16], in[31:24]};
```

### 拼拆组合

```verilog
assign {out[7:0], out[15:8]} = in;   // 左侧拼接: 拆 / 重排
assign out = {in[7:0], in[15:8]};    // 右侧拼接: 合成后赋给更宽向量时高位补 0
```

## 位复制

语法 `{num{vector}}`, `num` 必须为常量, **两层花括号都要写**. 例:

```verilog
{5{1'b1}}        // 5'b11111
{2{a,b,c}}       // {a,b,c, a,b,c}
{3'd5, {2{3'd6}}} // 9'b101_110_110
```

### 符号扩展

把有符号 8 bit 扩成 32 bit, 复制符号位 `in[7]` 共 24 次再接原值:

```verilog
assign out = {{24{in[7]}}, in};
```

这与算术里的**符号扩展**一致: 正数高位补 `0`, 负数高位补 `1`, 数值不变.

### 成对比较

五个 1 bit 输入做全部 25 对相等比较, `out[i]==1` 表示对应两位相等. 相等可用 `~(x^y)` (XNOR).

用复制 + 拼接构造两个 25 bit 向量再按位 XNOR:

```verilog
// 上行: aaaaa bbbbb ccccc ddddd eeeee
// 下行: abcde abcde abcde abcde abcde
assign out = ~{ {5{a}}, {5{b}}, {5{c}}, {5{d}}, {5{e}} }
              ^ {5{a, b, c, d, e}};
```

`~` 与 `^` 的优先级使得 `~(A^B)` 即按位同或; 也可写成 `~A ^ B` 需小心括号.


[^bit-numbering]: 这里的MSB指*Most Significant Bit*(最高有效位), LSB指*Least Significant Bit*(最低有效位); 按照二进制数位序的约定, 最高有效位在左边, 最低有效位在右边. 可参考[这篇百科](https://en.wikipedia.org/wiki/Bit_numbering).

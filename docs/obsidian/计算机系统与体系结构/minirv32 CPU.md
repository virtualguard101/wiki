---
date: 2026-08-21 17:20:43
title: minirv32处理器
permalink: minirv32-cpu
publish: true
tags:
  - 计算机系统与体系结构
  - RISC-V
---

# minirv32处理器

> [F6 功能完备的迷你RISC-V处理器 | 一生一芯 v24.07 学习讲义](https://ysyx.oscc.cc/docs/2407/f/6.html)

## minirv32 ISA

[一生一芯 F6](https://ysyx.oscc.cc/docs/2407/f/6.html) 从 RV32I 中抽出**8条**指令，组成迷你指令集**minirv**。用它们组合即可模拟其余 RV32I 功能，从而不必一次实现完整的四十多条指令。

除下列特别约定外，**其余细节与 RV32I 相同**（定长 32 位指令、字节编址、立即数符号扩展、`x0` 恒为 0 等）。完整的 RV32I ISA 可参考[RV32I Reference Card](risc-v/RV32I%20Reference%20Card.md)。

### PC

- 位宽 **32 bit**（与 RV32I 的 XLEN 一致），按**字节地址**计数。

- **初值为 `0`**。

- 顺序执行时每次 `PC ← PC + 4`（一条指令占 4 字节）；`jalr` 会改写 PC。

### GPR

- 数量上不采用[RV32I](risc-v/RV32I%20Reference%20Card.md#Register-Convention)的32个，而是与[RV32E](risc-v/RV32I%20Reference%20Card.md#Other-Base-in-RISC-V)一致：**16** 个，原始命名为 `x0`–`x15`。

- 每个寄存器的数据位宽为 **32 bit**。

- `x0` / `zero` [硬接线为 0](https://en.wikipedia.org/wiki/Zero_register)：读恒为 0，写忽略。与 [sISA](支持数列求和的sCPU.md#引入新指令后的sISA约定) 里可当作普通数据寄存器的 `R[0]` 不同。

### 支持的指令

接下来的设计将支持以下 8 种指令：

```text
31         25 24    20 19   15 14    12 11        7 6        0
+------------+--------+-------+--------+-----------+----------+
|  0000000   |  rs2   |  rs1  |  000   |    rd     | 0110011  |  add   R[rd]=R[rs1]+R[rs2]
+------------+--------+-------+--------+-----------+----------+
|      imm[11:0]      |  rs1  |  000   |    rd     | 0010011  |  addi  R[rd]=R[rs1]+imm
+------------+--------+-------+--------+-----------+----------+
|              imm[31:12]              |    rd     | 0110111  |  lui   R[rd]=imm<<12
+--------------------------------------+-----------+----------+
|      imm[11:0]      |  rs1  |  010   |    rd     | 0000011  |  lw    R[rd]=M[R[rs1]+imm]
+------------+--------+-------+--------+-----------+----------+
|      imm[11:0]      |  rs1  |  100   |    rd     | 0000011  |  lbu   zero-ext byte load
+------------+--------+-------+--------+-----------+----------+
| imm[11:5]  |  rs2   |  rs1  |  010   | imm[4:0]  | 0100011  |  sw    M[R[rs1]+imm]=R[rs2]
+------------+--------+-------+--------+-----------+----------+
| imm[11:5]  |  rs2   |  rs1  |  000   | imm[4:0]  | 0100011  |  sb    store low byte
+------------+--------+-------+--------+-----------+----------+
|      imm[11:0]      |  rs1  |  000   |    rd     | 1100111  |  jalr  R[rd]=PC+4; PC=(R[rs1]+imm)&~1
+------------+--------+-------+--------+-----------+----------+
```

涉及的指令布局类型有：**R**（`add`）、**I**（`addi` / `lw` / `lbu` / `jalr`）、**S**（`sw` / `sb`）、**U**（`lui`）。格式总览见 [Instruction Format by Type](risc-v/RV32I%20Reference%20Card.md#Instruction-Format-by-Type)。

#### 算术运算指令

| Instruction | Description | Type | Opcode | funct3 | funct7 |
|:------------|:------------|:----:|:------:|:------:|:------:|
| `add rd, rs1, rs2` | `R[rd] = R[rs1] + R[rs2]` | R | `0110011` | `000` | `0000000` |
| `addi rd, rs1, imm` | `R[rd] = R[rs1] + imm`（imm 符号扩展） | I | `0010011` | `000` | — |
| `lui rd, imm` | `R[rd] = imm << 12`（低 12 位清零） | U | `0110111` | — | — |

`addi` 可配合 `x0` 装小立即数；大常数常用 `lui` + `addi` 拼出。

#### 加载-存储指令

实际就是[操作内存](risc-v/RV32I%20Reference%20Card.md#Memory)的指令，之所以称之为加载-存储指令，是因为RISC-V采用[加载-存储架构](risc-v/RV32I%20Reference%20Card.md#Core-Concepts)，只有load和store指令可以访问内存，ALU指令只能访问寄存器。

| Instruction | Description | Type | Opcode | funct3 |
|:------------|:------------|:----:|:------:|:------:|
| `lw rd, imm(rs1)` | 读字：`R[rd] = M[R[rs1]+imm][31:0]` | I | `0000011` | `010` |
| `lbu rd, imm(rs1)` | 读字节并**零扩展**到 32 位 | I | `0000011` | `100` |
| `sw rs2, imm(rs1)` | 写字：`M[R[rs1]+imm] = R[rs2]` | S | `0100011` | `010` |
| `sb rs2, imm(rs1)` | 写字节：只更新目标字中的对应字节 | S | `0100011` | `000` |

#### 控制指令

minirv32只实现一条控制流指令，用于**间接跳转**（也可做函数返回：`jalr x0, ra, 0`）。

| Instruction | Description | Type | Opcode | funct3 |
|:------------|:------------|:----:|:------:|:------:|
| `jalr rd, rs1, imm` | `R[rd] = PC+4`；`PC = (R[rs1]+imm) & ~1` | I | `1100111` | `000` |

## 电路实现

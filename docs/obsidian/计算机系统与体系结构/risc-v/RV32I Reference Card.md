---
date: 2026-08-20 23:58:49
title: RV32I Reference Card
permalink: rv32i-refer
publish: true
tags:
  - 计算机系统与体系结构
  - RISC-V
---

# RV32I Reference Card

> [RV32I "Green Card" | CS 61C Course Notes](https://notes.cs61c.org/content/misc/rv32i-green-card/)
>
> [RV32I Base Integer Instruction Set, Version 2.1 | RISC-V Specification](https://docs.riscv.org/reference/isa/v20260120/unpriv/rv32.html)
>
> [The RISC-V Instruction Set Manual](https://riscv.github.io/riscv-isa-manual/snapshot/spec/)
>
> [RISC-V Assembly Programmer's Manual](https://github.com/riscv-non-isa/riscv-asm-manual/blob/main/src/asm-manual.adoc)
>
> [RISC-V | OSDev Wiki](https://wiki.osdev.org/RISC-V)

## Core Concepts

- **RV32I** = **RV** (RISC-V) + **32** (XLEN = 32 bits) + **I** (base Integer ISA). It is a concrete [ISA](../指令集架构的状态机模型.md#指令集架构的本质) / [RISC](RISC-V%20Introduction.md#Whats-RISC-V) contract: software and hardware agree on instructions, registers, and memory.

- **Architectural state** the programmer sees: **PC** + **32 GPRs** (`x0`–`x31`) + **memory**. Running a program = repeatedly: fetch `M[PC]`, update state by that instruction’s rule. See [状态机视角下的 ISA](../指令集架构的状态机模型.md#状态机视角下的ISA) for more explanation.

- **Registers**: 32 × 32-bit. `x0` is [hardwired to 0](https://en.wikipedia.org/wiki/Zero_register) (writes are ignored). [ABI (Application Binary Interface)](https://en.wikipedia.org/wiki/Application_binary_interface) names (`ra`, `sp`, `a0`, …) are software convention, not extra hardware, see [Register Convention](#Register-Convention) and [RV32I Registers](RISC-V%20Introduction.md#RV32I-Registers) for more details.

- **Load–store architecture (加载-存储架构)**: only **load/store** touch memory; ALU ops use registers only. Address form: `base + offset` → `imm(rs1)`.

- **Fixed 32-bit instructions**, 4-byte aligned. There are six layouts: **R / I / S / B / U / J** (plus **I\*** for shifts). Fields `rs1`, `rs2`, `rd` stay in the same bit positions across formats to simplify decode[^fmt].

    !!! tip "Instruction Layout"
        Think of a layout as a **fill-in-the-blank form** for one 32-bit instruction: which blanks are register numbers, which blank is a constant (*immediate*), and what the instruction is allowed to change. Bit-level packing is in [Instruction Format by Type](#Instruction-Format-by-Type).

        - **R**egister: *two registers in, one register out*.

            For example, `add t0, t1, t2` means `t0 = t1 + t2`. No constant baked into the instruction.

        - **I**mmediate: *one register + a small constant (*immediate*) → one register*.

            For example, `addi t0, t1, 5` means `t0 = t1 + 5`. Also used for **loads** (e.g. `lw t0, 8(sp)`: read memory at `sp+8` into `t0`) and for `jalr`.

        - **S**tore: *write a register into memory*.

            For example, `sw t0, 8(sp)` means “store `t0` at address `sp+8`”. The constant offset is still there, but the encoding splits it across two places in the 32 bits (that’s what “split” means, awkward packing, same idea as I’s offset).

        - **B**ranch: *compare two registers; maybe jump nearby*.
        
            For example, `beq t0, t1, label` means “if `t0 == t1`, go to `label`”. If not, just fall through to the next instruction. The “immediate” here is a **PC-relative distance**, not a data value.

        - **U**pper: *load a large constant’s upper bits into a register*.

            For example, `lui t0, 0x12345` puts `0x12345000` into `t0` (low 12 bits cleared). Often paired with `addi` to finish a full 32-bit constant.

        - **J**ump: *jump farther and (usually) save the return address*.

            For example, `jal ra, func` jumps to `func` and writes “come back here” into `ra`. The immediate is again a PC-relative distance, but wider than B’s.

        - **I\*** (shifts by a constant, e.g. `slli`): still the I “form”, but a few bits that would normally be part of the immediate are reused to say *which kind of shift*. Treat it as a footnote to I, not a 7th layout.

- **Immediates are sign-extended** to 32 bits (except where noted). Integers use [two’s complement](../cs61c/Number%20Representation.md#Twos-Complement); arithmetic overflow wraps, no trap in the base ISA[^imm].

#### Wrap and Trap {#Wrap-and-Trap}

!!! info
    - **Wrap** ([integer overflow](../cs61c/Number%20Representation.md#Integer-Overflow)): the true result does not fit in 32 bits, so only the low 32 bits are kept, like a binary odometer rolling over. For example, in 8-bit unsigned, `255 + 1` will wrap to `0`.

    - **Trap**: a *synchronous* jump to a trap handler (usually in a more privileged mode). In RISC-V jargon[^trap]:

        - **Exception**: unusual condition tied to the *current* instruction (illegal opcode, page fault, `ecall`, …).

        - **Interrupt**: *asynchronous* external event (timer, device); hardware picks some instruction to “take” it.

        - **Trap**: the control-transfer itself: leave normal flow and turn to run the handler.

    Base RV32I integer arithmetic (**does not** trap on overflow): it just wraps. If you care about overflow, check it in software (e.g. compare after `add`), or use an extension later, the hardware will not stop for you.

## Instruction Format by Type

All instructions are 32 bits. Bit 31 is always the immediate’s sign bit (speeds sign-extension)[^fmt].

```text
31         25 24    20 19   15 14    12 11        7 6        0
+------------+--------+-------+--------+-----------+----------+
|   funct7   |  rs2   |  rs1  | funct3 |    rd     |  opcode  |  R: reg–reg ALU (add, sub, …)      
+------------+--------+-------+--------+-----------+----------+
|      imm[11:0]      |  rs1  | funct3 |    rd     |  opcode  |  I: ALU imm, loads, jalr
+------------+--------+-------+--------+-----------+----------+
|   funct7   |imm[4:0]|  rs1  | funct3 |    rd     |  opcode  |  I*: shifts by imm (slli/srli/srai)
+------------+--------+-------+--------+-----------+----------+
| imm[11:5]  |  rs2   |  rs1  | funct3 | imm[4:0]  |  opcode  |  S: stores
+------------+--------+-------+--------+-----------+----------+
|imm[12|10:5]|  rs2   |  rs1  | funct3 |imm[4:1|11]|  opcode  |  B: conditional branches
+------------+--------+-------+--------+-----------+----------+
|              imm[31:12]              |    rd     |  opcode  |  U: lui, auipc
+--------------------------------------+-----------+----------+
|        imm[20|10:1|11|19:12]         |    rd     |  opcode  |  J: jal
+--------------------------------------+-----------+----------+
```

!!! note "How to read scrambled immediates"
    Labels like `imm[12|10:5]` mean: those instruction bits are *reordered* pieces of the immediate value, not a contiguous field. Hardware reassembles them, then sign-extends. Branch/jump offsets are in multiples of 2 bytes (LSB of the offset is always 0).

## Register Convention

Hardware only provides `x0`–`x31`. Names and **Caller / Callee** rules come from the ABI ([psABI](https://github.com/riscv-non-isa/riscv-elf-psabi-doc/blob/master/riscv-cc.adoc)).

| Register(s) | ABI name | Role | Saver |
|:------------|:---------|:-----|:-----:|
| `x0` | `zero` | Constant $0$ | — |
| `x1` | `ra` | Return address | Caller |
| `x2` | `sp` | Stack pointer | Callee |
| `x3` | `gp` | Global pointer[^gp-tp] | — |
| `x4` | `tp` | Thread pointer[^gp-tp] | — |
| `x5`–`x7` | `t0`–`t2` | Temporaries | Caller |
| `x8` | `s0` / `fp` | Saved / frame pointer | Callee |
| `x9` | `s1` | Saved | Callee |
| `x10`–`x11` | `a0`–`a1` | Args / return values | Caller |
| `x12`–`x17` | `a2`–`a7` | Args | Caller |
| `x18`–`x27` | `s2`–`s11` | Saved | Callee |
| `x28`–`x31` | `t3`–`t6` | Temporaries | Caller |

- **Caller-saved** (`t*`, `a*`, `ra`): may be clobbered by a call — save yourself if you still need them.

- **Callee-saved** (`s*`, `sp`): callee must restore them before returning.

## RV32I Base Integer Instruction Set

Opcodes / funct fields below match the [CS 61C green card](https://notes.cs61c.org/content/misc/rv32i-green-card/) and the [RV32I spec](https://docs.riscv.org/reference/isa/v20260120/unpriv/rv32.html).

### Arithmetic

| Instruction | Description | Type | Opcode | funct3 | funct7 |
|:------------|:------------|:----:|:------:|:------:|:------:|
| `add rd, rs1, rs2` | `R[rd] = R[rs1] + R[rs2]` | R | `0110011` | `000` | `0000000` |
| `sub rd, rs1, rs2` | `R[rd] = R[rs1] − R[rs2]` | R | `0110011` | `000` | `0100000` |
| `and rd, rs1, rs2` | `R[rd] = R[rs1] & R[rs2]` | R | `0110011` | `111` | `0000000` |
| `or rd, rs1, rs2` | `R[rd] = R[rs1] \| R[rs2]` | R | `0110011` | `110` | `0000000` |
| `xor rd, rs1, rs2` | `R[rd] = R[rs1] ^ R[rs2]` | R | `0110011` | `100` | `0000000` |
| `sll rd, rs1, rs2` | `R[rd] = R[rs1] << R[rs2]` | R | `0110011` | `001` | `0000000` |
| `srl rd, rs1, rs2` | logical `>>` (zero-fill) | R | `0110011` | `101` | `0000000` |
| `sra rd, rs1, rs2` | arithmetic `>>` (sign-fill) | R | `0110011` | `101` | `0100000` |
| `slt rd, rs1, rs2` | signed: `R[rd] = (R[rs1] < R[rs2]) ? 1 : 0` | R | `0110011` | `010` | `0000000` |
| `sltu rd, rs1, rs2` | unsigned compare | R | `0110011` | `011` | `0000000` |
| `addi rd, rs1, imm` | `R[rd] = R[rs1] + imm` | I | `0010011` | `000` | — |
| `andi rd, rs1, imm` | `R[rd] = R[rs1] & imm` | I | `0010011` | `111` | — |
| `ori rd, rs1, imm` | `R[rd] = R[rs1] \| imm` | I | `0010011` | `110` | — |
| `xori rd, rs1, imm` | `R[rd] = R[rs1] ^ imm` | I | `0010011` | `100` | — |
| `slli rd, rs1, imm` | `R[rd] = R[rs1] << imm` | I\* | `0010011` | `001` | `0000000` |
| `srli rd, rs1, imm` | logical `>> imm` | I\* | `0010011` | `101` | `0000000` |
| `srai rd, rs1, imm` | arithmetic `>> imm` | I\* | `0010011` | `101` | `0100000` |
| `slti rd, rs1, imm` | signed compare vs imm | I | `0010011` | `010` | — |
| `sltiu rd, rs1, imm` | unsigned compare vs imm | I | `0010011` | `011` | — |

Shift amount: lower **5** bits of `rs2` / imm (0–31).

!!! info "Why use multiple fields to encode an instruction?"
    In [sISA](../支持数列求和的sCPU.md#引入新指令后的sISA约定), a short **opcode** (e.g. `00` / `10` / `11`) already names the *exact* instruction: see `00` → `ADD`, `10` → `LI`. One field, one meaning.

    RV32I has far more instructions, so it uses a **layered** ID:

    1. **`opcode`**: which *family*? (e.g. R-type ALU, I-type ALU, load, store, …)

    2. **`funct3`**: which op inside that family? (e.g. `add` vs `sll` vs `and` …)

    3. **`funct7`**: only when `funct3` is still shared (classic: `add` vs `sub`, `srl` vs `sra`)

    Example from the table above: `add` and `sub` share `opcode = 0110011` and `funct3 = 000`; only **`funct7`** differs. 
    
    Hardware must read **all** of these fields when decoding an instruction, not just the opcode.

### Memory

| Instruction | Description | Type | Opcode | funct3 |
|:------------|:------------|:----:|:------:|:------:|
| `lb rd, imm(rs1)` | load byte, **sign**-extend | I | `0000011` | `000` |
| `lbu rd, imm(rs1)` | load byte, **zero**-extend | I | `0000011` | `100` |
| `lh rd, imm(rs1)` | load halfword, sign-extend | I | `0000011` | `001` |
| `lhu rd, imm(rs1)` | load halfword, zero-extend | I | `0000011` | `101` |
| `lw rd, imm(rs1)` | load word: `R[rd] = M[R[rs1]+imm]` | I | `0000011` | `010` |
| `sb rs2, imm(rs1)` | store byte | S | `0100011` | `000` |
| `sh rs2, imm(rs1)` | store halfword | S | `0100011` | `001` |
| `sw rs2, imm(rs1)` | store word | S | `0100011` | `010` |

Sizes: byte = 8 bit, half = 16 bit, word = 32 bit. Address = `R[rs1] + sign_ext(imm)`.

### Control

| Instruction | Description | Type | Opcode | funct3 |
|:------------|:------------|:----:|:------:|:------:|
| `beq rs1, rs2, label` | if equal, `PC += offset` | B | `1100011` | `000` |
| `bne rs1, rs2, label` | if not equal | B | `1100011` | `001` |
| `blt rs1, rs2, label` | signed `<` | B | `1100011` | `100` |
| `bltu rs1, rs2, label` | unsigned `<` | B | `1100011` | `110` |
| `bge rs1, rs2, label` | signed `≥` | B | `1100011` | `101` |
| `bgeu rs1, rs2, label` | unsigned `≥` | B | `1100011` | `111` |
| `jal rd, label` | `R[rd] = PC+4`; `PC += offset` | J | `1101111` | — |
| `jalr rd, rs1, imm` | `R[rd] = PC+4`; `PC = (R[rs1]+imm) & ~1` | I | `1100111` | `000` |

Branch range $\approx \pm 4$ KiB; `jal` $\approx \pm 1$ MiB (both PC-relative). If the branch is **not** taken, `PC` just advances by 4.

### Other

| Instruction | Description | Type | Opcode | funct3 |
|:------------|:------------|:----:|:------:|:------:|
| `lui rd, imm` | `R[rd] = imm << 12` (low 12 bits cleared) | U | `0110111` | — |
| `auipc rd, imm` | `R[rd] = PC + (imm << 12)` | U | `0010111` | — |
| `ecall` | environment call (trap to OS / runtime) | I | `1110011` | `000` |
| `ebreak` | breakpoint (debugger) | I | `1110011` | `000` |

`lui` + `addi` builds full 32-bit constants; `auipc` + load/jalr builds PC-relative addresses.

## Pseudoinstructions

**Pseudoinstructions (伪指令)** are convenient *aliases* in assembly source (e.g. `mv`, `ret`, `li`). The **assembler** will replace each pseudoinstruction with one or more real RV32I instructions. The CPU only ever executes those real instructions — pseudoinstructions are **not** extra hardware.

Not separate opcodes, the assembler expands them ([ASM Manual](https://github.com/riscv-non-isa/riscv-asm-manual/blob/main/src/asm-manual.adoc#pseudoinstructions)):

| Pseudo | Meaning | Expands to (typical) |
|:-------|:--------|:---------------------|
| `nop` | do nothing | `addi x0, x0, 0` |
| `mv rd, rs` | copy | `addi rd, rs, 0` |
| `li rd, imm` | load immediate | `lui` / `addi` as needed |
| `not rd, rs` | bitwise NOT | `xori rd, rs, -1` |
| `neg rd, rs` | negate | `sub rd, x0, rs` |
| `beqz rs, label` | branch if zero | `beq rs, x0, label` |
| `bnez rs, label` | branch if nonzero | `bne rs, x0, label` |
| `j label` | unconditional jump | `jal x0, label` |
| `jal label` | call (link in `ra`) | `jal ra, label` |
| `jr rs` | jump to register | `jalr x0, rs, 0` |
| `ret` | return | `jalr x0, ra, 0` |
| `la rd, label` | load address | `auipc` + `addi` |

## Other Base in RISC-V

RISC-V is a **family** of base integer ISAs. A base is fixed by two knobs: **XLEN** (register / address width) and **how many `x` registers**. Others share the same encoding ideas with RV32I; they are not “add-ons” like `M` / `C` (those are *extensions* stacked on a base).

| Base | XLEN | GPRs | Rough role |
|:-----|-----:|:-----|:-----------|
| **RV32I** | 32 | 32 (`x0`–`x31`) | Default 32-bit teaching / general-purpose base |
| **RV32E** | 32 | 16 (`x0`–`x15`) | Tiny embedded cores; fewer regs → smaller / cheaper |
| **RV64I** | 64 | 32 (`x0`–`x31`) | Common 64-bit servers / OS / phones’ application cores |
| **RV64E** | 64 | 16 (`x0`–`x15`) | 64-bit but still register-light (embedded / special cases) |
| **RV128I** | 128 | 32 (`x0`–`x31`) | Spec’d future-facing flat 128-bit address space; rare in practice |

Naming convention is **RV** + bit-width + **I** (full Integer base) or **E** (Embedded, half the registers). 

All bases share the same load–store style and `x0` = zero; wider bases mainly widen words / addresses and add width-specific ops (e.g. RV64’s `*w` variants for 32-bit-in-64-bit).


[^fmt]: [RV32I Base Integer Instruction Set § Base Instruction Formats](https://docs.riscv.org/reference/isa/v20260120/unpriv/rv32.html#base-instruction-formats) — fixed 32-bit encodings; `rs1`/`rs2`/`rd` positions held constant across formats.

[^imm]: [RV32I § Integer Computational Instructions](https://docs.riscv.org/reference/isa/v20260120/unpriv/rv32.html#integer-computational-instructions) — immediates sign-extended; no arithmetic exceptions on overflow in the base ISA.

[^trap]: [OSDev · RISC-V](https://wiki.osdev.org/RISC-V#Exceptions.2C_Traps_and_Interrupts)

[^gp-tp]: For early learning, treat `gp` / `tp` as off-limits; using them casually breaks convention.
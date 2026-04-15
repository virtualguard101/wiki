---
date: 2026-04-15 12:52:19
title: Rust数据类型
permalink: data-type
publish: true
tags:
  - 编程语言
  - Rust
---

# Rust数据类型

## 基本数据类型

### 整数类型

| 长度 | 有符号类型 | 无符号类型 |
|:---:|:---:|:---:|
| 8位 | `i8` | `u8` |
| 16位 | `i16` | `u16` |
| 32位 | `i32` | `u32` |
| 64位 | `i64` | `u64` |
| 128位 | `i128` | `u128` |
| 依赖平台（x64/x86） | `isize` | `usize` |

[绑定](Rust变量.md#变量绑定)一个整形变量时，默认使用i32类型。

#### 整型溢出

以u8为例，范围是0~255，如果运算时结果超过这个范围就会发生溢出。

针对溢出，Rust标准库提供了以下几种显式处理方式：

> [lang/rust/data-type | vglab](https://github.com/virtualguard101/vglab/blob/main/lang/rust/data-type/src/main.rs#L2)

- `wrapping_*` 方法在所有模式下都按照补码循环溢出规则处理，例如 wrapping_add

- 如果使用 `checked_*` 方法时发生溢出，则返回 None 值

- `overflowing_*` 方法返回该值和一个指示是否存在溢出的布尔值

- `saturating_*` 方法，可以限定计算后的结果不超过目标类型的最大值或低于最小值

### 浮点类型

#### 浮点数操作的陷阱

基于浮点数的底层表示，浮点数操作通常需要注意两点：

- **浮点数的近似问题**：由于浮点数的表示方式，某些十进制数无法精确表示为二进制浮点数，这可能导致计算结果出现微小的误差。例如，0.1在二进制中是一个无限循环小数，因此在计算时可能会得到一个近似值而不是精确的0.1。

    > [lang/rust/data-type | vglab](https://github.com/virtualguard101/vglab/blob/main/lang/rust/data-type/src/main.rs#L32)

- **浮点数在某些特性上是反直觉的**[^1]：比方说在比较上，因为 `f32`、`f64` 上的比较运算实现的是 `std::cmp::PartialEq` 特征(类似其他语言的接口)，但是并没有实现 `std::cmp::Eq` 特征，但是后者在其它数值类型上都有定义；在这样的差别下，如果还想当然的凭直觉直接比较，会带来很多意想不到的错误。

    !!! example "HashMap[^1]"
        Rust 的 HashMap 数据结构，是一个 KV 类型的 Hash Map 实现，它对于 K 没有特定类型的限制，但是要求能用作 K 的类型必须实现了 `std::cmp::Eq` 特征，因此这意味着你无法使用浮点数作为 HashMap 的 Key，来存储键值对，但是作为对比，Rust 的整数类型、字符串类型、布尔类型都实现了该特征，因此可以作为 HashMap 的 Key。

!!! tip "浮点数操作准则"
    针对上面提到的两个问题，在使用浮点数进行运算时，需要遵循以下准则：

    - 避免在浮点数上测试相等性

    - 当结果在数学上可能存在未定义时，需要格外的小心

#### NaN

NaN（Not a Number）是一个特殊的浮点数值，表示未定义或不可表示的结果，例如0除以0、无穷大减去无穷大、负数开平方等操作都会产生NaN。

NaN具有以下特点：

- NaN不等于任何值，包括它自己。这意味着**NaN不能用于比较**。若尝试比较NaN与任何值（包括NaN本身），结果总是返回false。
  
    ```bash
    thread 'main' (61907) panicked at src/main.rs:50:5:
    assertion failed: f64::NAN == f64::NAN
    note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace
    ```

- **所有跟NaN相关的操作都会返回NaN**

### Rust By Practice

> [数值类型 | Rust By Practice( Rust 练习实践 )](https://practice-rust-zh.beatai.org/basic-types/numbers.html)


[^1]: [浮点数陷阱 - 数值类型 | Rust语言圣经](https://beatai.org/rust-course/basic/base-type/numbers#%E6%B5%AE%E7%82%B9%E6%95%B0%E9%99%B7%E9%98%B1)
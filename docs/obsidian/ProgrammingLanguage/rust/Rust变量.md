---
date: 2026-04-14 21:42:29
title: Rust变量
permalink: rust-variables
publish: true
tags:
  - 编程语言
  - Rust
---

# Rust变量

## 变量命名

遵循驼峰命名法（camelCase）或蛇形命名法（snake_case），而且两种方法都有对应的适用场景，具体规范可参考[命名规范 | Rust语言圣经](https://beatai.org/rust-course/practice/naming)

## 变量绑定

与其他语言所谓的**赋值**，不同在Rust中，采用了**绑定**这个名词来描述变量的初始化操作，这牵扯到Rust中的一个核心语言特性：**所有权系统**。

简单来说，任何内存对象都是有主人的，而且一般情况下完全属于它的主人，绑定就是把这个对象绑定给一个变量，让这个变量成为它的主人，在这种情况下，该对象之前的主人就会丧失对该对象的所有权[^1]。

## 变量可变性

在Rust中，变量默认是**不可变**的，这意味着一旦一个值被绑定到一个变量上，就不能再改变这个值了。如果需要改变变量的值，必须使用`mut`关键字来声明一个**可变**变量。

```rust
let x = 5;     // immutable variable
let mut x = 5; // mutable variable
```

如果尝试修改一个不可变变量的值，那么你就会吃到如下报错：

```bash
$ cargo run 
   Compiling variables v0.1.0 (/home/virtualguard/vg101/notebooks/vglab/lang/rust/variables)
error[E0384]: cannot assign twice to immutable variable `x`
  --> src/main.rs:12:5
   |
 7 |     let x = 5;       // immutable variable
   |         - first assignment to `x`
...
12 |     x = 6;
   |     ^^^^^ cannot assign twice to immutable variable
   |
help: consider making this binding mutable
   |
 7 |     let mut x = 5;       // immutable variable
   |         +++

For more information about this error, try `rustc --explain E0384`.
error: could not compile `variables` (bin "variables") due to 1 previous error
```

## 格式化输出的三种形式

- 一种是**命名捕获**（直接从当前作用域取变量）:

    ```rust
    println!("The value of x is: {x}");  // named capture (std::fmt::Display)
    ```

- 另一种是**位置参数**（位置占位符 + 逗号传参）:
  
    ```rust
    println!("The value of x is: {}", x);// position placeholder + comma argument (std::fmt::Display)
    ```

- 还有一种是**调试输出**（Debug占位符 + 逗号传参）:

    ```rust
    println!("a: {:?}, b: {:?}", a, b);  // Debug placeholder + comma argument (std::fmt::Debug)
    ```

## 变量解构

!!! example "code"
    > [lang/rust/variables | vglab](https://github.com/virtualguard101/vglab/blob/main/lang/rust/variables/src/main.rs#L15)

`let` 表达式不仅仅用于变量的绑定，还能进行复杂变量的解构：从一个相对复杂的变量中，匹配出该变量的一部分内容。类似 C++ 中的[结构化绑定](../cpp/cs106l/初始化与引用操作.md#结构化绑定)。

自 Rust1.59 起，左值开始支持使用元组、切片和结构体模式。

## 常量

和其他语言类似，Rust使用`const`关键字来声明一个常量。常量必须在编译时就能确定其值，并且在运行时不能被修改。

```rust
const MAX_POINTS: u32 = 100_000;
```

!!! warning
    注意常量和普通变量的区别，前者是至始至终不可变，后者只是默认不可变。

## 变量遮蔽

在Rust中，变量遮蔽（variable shadowing）是指在同一作用域内，后面声明的变量可以覆盖前面声明的同名变量。这种机制允许我们在不使用`mut`关键字的情况下改变变量的值。

!!! example "code"
    > [lang/rust/variables | vglab](https://github.com/virtualguard101/vglab/blob/main/lang/rust/variables/src/main.rs#L32)

## Rust By Practice

> [变量绑定与解构 | Rust By Practice( Rust 练习实践 )](https://practice-rust-zh.beatai.org/variables.html)


[^1]: [变量绑定 - 变量绑定与解构 | Rust语言圣经](https://beatai.org/rust-course/basic/variable)
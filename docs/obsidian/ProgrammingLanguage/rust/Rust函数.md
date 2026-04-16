---
date: 2026-04-16 09:02:13
title: Rust函数
permalink: func
publish: true
tags:
  - 编程语言
  - Rust
---

# Rust函数

Rust 函数体由一系列**语句**组成，最后由一个表达式来返回值。

```rust
fn sum_with_add_five(a: i32, b: i32) -> i32 {
    let a = a + 5; // statement
    let b = b + 5; // statement
    a + b // expression
}
```

**语句会执行一些操作但是不会返回一个值，而表达式会在求值后返回一个值。**

## 语句和表达式

对于 Rust 语言而言，这种基于语句（statement）和表达式（expression）的方式是非常重要的，要能明确的区分这两个概念。

### 语句

语句用于完成一个具体操作，但是不返回值，`let` 就是一个典型的语句。

没有返回值，意味着不能将语句赋值给其他变量，因此下面的代码是错误的：

```rust
let result = (let a = result + 5);
```

```bash
error: expected expression, found `let` statement
 --> src/main.rs:9:19
  |
9 |     let result = (let a = result + 5);
  |                   ^^^
  |
  = note: only supported directly in conditions of `if` and `while` expressions
```

### 表达式

表达式会进行求值，然后返回一个值。**表达式可以成为语句的一部分**。

!!! warning
    注意表达式不能包含分号，加上分号就变成了语句。

表达式如果不返回任何值，则隐式返回`()`（[单元类型](Rust数据类型.md#单元类型)）。

## 函数

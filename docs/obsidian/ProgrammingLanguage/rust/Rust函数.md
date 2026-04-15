---
date: 2026-04-15 17:19:13
title: Rust函数
permalink: func
publish: false
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

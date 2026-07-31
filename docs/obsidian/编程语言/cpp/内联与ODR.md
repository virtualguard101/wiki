---
date: 2026-06-01 01:41:36
title: 内联与ODR
permalink: inline
publish: true
tags:
  - 编程语言
  - C++
---

# 内联与ODR

> 与头文件分工相关：[C++头文件](C++头文件.md) · 类内函数与友元：[运算符重载](cs106l/运算符重载.md)

!!! abstract
    | 场景 | 是否使用 `inline` |
    |------|-------------------|
    | 头文件中的自由函数定义 | 需要 |
    | 头文件中的全局/命名空间变量定义（C++17+） | 需要 |
    | 类内定义的成员函数 | 隐式具备，一般不必再写 |
    | 类外但在头文件中的成员函数定义 | 需要显式 `inline` |
    | 仅存在于单个 `.cc` 中的定义 | 不需要 |
    | 指望「一定更快」 | 不要只依赖 `inline` |

`inline` 在 C++ 里主要有两层含义：

1. **链接（linkage）**：允许多个翻译单元包含**同一份定义**而不违反 ODR。

2. **优化（常被误解）**：口语里说的「内联展开」——现代编译器**不保证**因写了 `inline` 就一定展开；是否内联由优化级别等决定。

教学与工程上应把 **`inline` 首先当作 ODR/头文件机制**，而不是「加速开关」。

---

## ODR：单一定义规则

**ODR**（One Definition Rule，单一定义规则）要求：整个程序中，每个非 `inline` 的变量、函数、类等**最多只能有一份定义**。

头文件会被多个 `.cpp` / `.cc` 反复 `#include`，每个翻译单元都会复制头里的内容。若在头里写：

```cpp
// bad.h
int Factorial(int n) {
  return n <= 1 ? 1 : n * Factorial(n - 1);
}
```

每个包含 `bad.h` 的源文件都会生成一份 `Factorial` 定义 → 链接阶段报 **multiple definition**。

**解决办法（二选一）**：

- 声明放头文件，**定义只放在一个** `.cc` 里；

- 或定义放在头文件里，并标记为 **`inline`**（以及 C++17 的 `inline` 变量等，见下文）。

---

## `inline` 函数

### 头文件中的函数体

```cpp
// good.h
inline int Factorial(int n) {
  return n <= 1 ? 1 : n * Factorial(n - 1);
}
```

多个翻译单元可以各含一份**相同**的 `inline` 定义，链接器合并为一份实体。

| 位置 | 建议 |
|------|------|
| `.h` / `.hh` 里的函数实现 | 使用 `inline`（或类内成员定义，见下） |
| 仅在一个 `.cc` 中的实现 | 一般**不要** `inline`；头文件只保留声明 |

### 类内成员函数：隐式 `inline`

在类（或 `struct`）**内部**定义的成员函数，**自动**具有 `inline` 性质：

```cpp
struct Foo {
  int Get() const { return x_; }  // 隐式 inline
private:
  int x_{};
};
```

若在类外写定义且定义仍在头文件中，需**显式** `inline`：

```cpp
struct Foo {
  int Get() const;
};
inline int Foo::Get() const { return x_; }
```

与 [运算符重载](cs106l/运算符重载.md) 中在类内定义的 `friend operator==` 同理：类内定义 → 隐式 inline，通常不必再写 `inline`。

---

## `inline` 变量（C++17）

C++17 之前，命名空间作用域的变量若在头文件中定义，也容易触发 ODR 冲突。

C++17 起可对变量使用 `inline`：

```cpp
inline constexpr int kMaxRetries = 3;
```

这样多个源文件 include 同一头文件时，仍只有**一份**变量实体。

**没有 `inline` 时**（头文件中）：

```cpp
const int kVersion = 1;  // 每个 .cc 可能各有一份 → 链接 duplicate symbol
```

---

## `inline` 与 `constexpr`

二者常一起出现，职责不同：

| 关键字 | 主要作用 |
|--------|----------|
| `constexpr` | 在满足条件时于**编译期**求值；可用于常量表达式上下文 |
| `inline` | 允许多个翻译单元共享**同一定义**（ODR） |

```cpp
inline constexpr size_t kBufferSize = 4096;
```

- `constexpr`：表达「可作为编译期常量」。

- `inline`：表达「可以安全地写在头文件里被多处 include」。

!!! tip
    类内的 `static constexpr` 整型成员有时仅在类内初始化即可；**类类型的常量对象**（如自定义 `struct`）在头文件中定义时，C++17 起通常需要 **`inline`**（或改为 `static inline` / 仅在 `.cc` 定义）。

### 工程示例（协议栈常量）

头文件中常被多个翻译单元包含的全局常量：

```cpp
inline constexpr IPv4Address kIPv4Any{{0, 0, 0, 0}};
inline constexpr Subnet kIPv4EmptySubnet{kIPv4Any, 0};
```

若去掉 `inline`，每个 `.cc` include 该头后可能各生成一份 `kIPv4Any`，链接失败。

---

## 与「内联优化」的关系

| 说法 | 是否准确 |
|------|----------|
| `inline` = 编译器一定把函数展开到调用处 | ❌ 不准确 |
| 未写 `inline` 的函数不会被内联 | ❌ 编译器在 `-O2` 等级别仍可能内联 |
| `inline` 允许在头文件中放函数/变量定义 | ✅ 标准主语义 |

是否做内联展开由编译器决定；`inline` 关键字的首要用途是 **ODR / 链接**，不是性能保证。

---

## 与 `#define` 宏的对比

早期常用宏在头文件中「仿函数」以避免链接错误，但缺少类型与作用域检查。现代 C++ 更推荐：

```cpp
inline int Max(int a, int b) { return a > b ? a : b; }
```

需要编译期常量时，配合 `constexpr` 使用，而不是宏。

---

## `inline namespace`

```cpp
inline namespace v2 {
  void Foo();
}
```

用于版本/ABI 与名称查找（例如标准库实现中的 `inline namespace std::__1`），与「函数内联优化」**不是同一概念**。日常写业务代码时较少手写。

---

# `std::optional`与类型安全

*该笔记基于课程CS106L的学习，用于记录一些cpp的重要特性以及先前不曾了解的cpp特性。*

## 类型安全概述

**类型安全**（*Type Safety*）是指编程语言确保程序按照预期行为执行的能力，特别是在处理数据类型时避免错误。

例如，在函数定义上的表现为使用**函数签名**(*Function Signature*)以规范函数的行为：
```cpp
void removeOddsFromEnd(std::vector<int>& vec) {
    // while(vec.back()%2 == 1)
    /*In this case, if vec is empty, back() will return Undefined Behavior! */
    while(!vec.empty() && vec.back()%2 == 1) {
        vec.pop_back();
    }
}
```

!!! note "未定义行为"

    **未定义行为**（*Undefined Behavior, UB*）是指程序在执行过程中遇到了语言标准没有明确规定的行为。当出现未定义行为时，程序可能会崩溃、产生垃圾数据、意外地给出某个实际值，或者表现出其他不可预测的行为。

## `std::optional`

### 概述

`std::optional<T>` 是 C++17 引入的一个模板类，它可以包含一个类型为 `T` 的值，或者不包含任何值（用 `std::nullopt` 表示）。

!!! note "`nullopt` vs `nullptr`
    注意区别二者

    - `nullptr`：是一个指针字面量，**可以转换为任何指针类型**，表示空指针。

    - `std::nullopt`：是一个特殊值，用于表示 `std::optional` 不包含值的状态。它是 **`std::nullopt_t` 类型**的常量。

```cpp
#include <optional>
#include <iostream>

void main() {
    std::optional<int> num1 = {}; // num1 does not have a value
    num1 = 1; // now it does!
    num1 = std::nullopt; // now it doesn't anymore
}
```

```cpp
std::optional<valueType> vector<valueType>::back() {
    if(empty()) {
        return {};
    }
    return *(begin() + size() - 1);
}
```

### 常用接口

```cpp
#include <optional>
#include <iostream>
#include <string>

int main() {
    // 构造
    std::optional<int> a;                  // 空 optional
    std::optional<int> b = std::nullopt;   // 空 optional
    std::optional<int> c = 42;             // 包含值 42 的 optional
    
    // 状态检查
    if (c.has_value()) {
        std::cout << "c has value" << std::endl;
    }
    
    if (c) {  // 使用 bool 转换
        std::cout << "c is true" << std::endl;
    }
    
    // 访问值
    try {
        std::cout << "a.value() = " << a.value() << std::endl;  // 抛出异常
    } catch (const std::bad_optional_access& e) {
        std::cout << "Exception: " << e.what() << std::endl;
    }
    
    std::cout << "a.value_or(0) = " << a.value_or(0) << std::endl;  // 输出 0
    std::cout << "c.value() = " << c.value() << std::endl;          // 输出 42
    std::cout << "*c = " << *c << std::endl;                        // 输出 42
    
    // 修改值
    c.reset();                   // c 变为空
    c.emplace(100);              // c 包含值 100
    
    // 赋值
    c = 200;                     // c 包含值 200
    c = std::nullopt;            // c 变为空
    
    return 0;
}
```

## C++设计理念概述

=== "English"

    - Only add features if they solve an actual problem

    - Programmers should be free to choose their own style

    - Compartmentalization is key

    - Allow the programmer full control if they want it

    - Don’t sacrifice performance except as a last resort

    - Enforce safety at compile time whenever possible


=== "中文"

    - 只有在解决实际问题时才添加新特性

    - 程序员应该可以自由选择自己的编程风格

    - 模块化是关键

    - 允许程序员在需要时完全控制

    - 除非万不得已，否则不牺牲性能

    - 尽可能在编译时强制安全性

1. 只有在解决实际问题时才添加新特性

C++ 的设计遵循实用主义原则，不会为了语言的完美性或理论上的一致性而添加特性。每个新特性的引入都必须解决实际编程中遇到的问题。例如：

- std::unique_ptr 和 std::shared_ptr 解决了动态内存管理的问题

- Lambda 表达式解决了创建小型匿名函数的问题

- std::optional 解决了表示可能不存在的值的问题

2. 程序员应该可以自由选择自己的编程风格

C++ 不强制特定的编程范式或风格，而是提供多种工具和方法，让程序员可以根据问题的性质选择最合适的解决方案。C++ 支持：

- 过程式编程

- 面向对象编程

- 泛型编程

- 函数式编程

- 元编程

程序员可以混合使用这些范式，根据具体情况选择最合适的方法。

3. 模块化是关键

C++ 强调代码的模块化，通过以下机制支持这一原则：

- 命名空间（namespace）避免名称冲突

- 类和结构体封装数据和行为

- 头文件和实现文件分离

- 模板提供类型无关的代码复用

- C++20 引入的模块系统进一步增强了模块化能力

- 模块化使得大型项目可以被分解为可管理的部分，提高了代码的可维护性和可重用性。

4. 允许程序员在需要时完全控制

C++ 提供了从高级抽象到底层控制的全方位能力：

- 可以使用高级抽象（如标准库容器、算法）

- 也可以直接操作内存（通过指针、引用）

- 提供内联汇编能力

- 允许位级操作

- 支持直接内存布局控制

这种灵活性使 C++ 适用于从系统编程到应用开发的各种场景。

5. 除非万不得已，否则不牺牲性能

C++ 的设计理念是"零开销抽象"（zero-overhead abstraction），即抽象不应该引入额外的运行时成本。例如：

- 模板在编译时展开，不产生运行时开销

- RAII（资源获取即初始化）模式提供安全的资源管理，无需额外的运行时检查

- 移动语义减少了不必要的复制操作

- 编译时多态（通过模板）避免了运行时虚函数调用的开销

6. 尽可能在编译时强制安全性

C++ 通过类型系统和编译时检查来捕获错误：

- 强类型系统防止类型错误

- const 和 constexpr 确保不可变性

- 模板元编程允许编译时计算和验证

- C++20 的概念（Concepts）提供了更强大的编译时约束

- static_assert 允许编译时断言

这种方法使得许多错误可以在编译时被发现，而不是在运行时导致程序崩溃。


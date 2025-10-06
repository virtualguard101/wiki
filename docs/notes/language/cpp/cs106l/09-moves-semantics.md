# 移动语义

*该笔记基于课程CS106L的学习，用于记录一些cpp的重要特性以及先前不曾了解的cpp特性。*

- [std::move in Utility in C++ | Move Semantics, Move Constructors and Move Assignment Operators | GeeksForGeeks](https://www.geeksforgeeks.org/stdmove-in-utility-in-c-move-semantics-move-constructors-and-move-assignment-operators/)

## 左值与右值

- 左值(*L-value*)
    - 代表一个内存位置，它有一个可访问的地址，并且可以被赋值

    - **生命周期通常持续到其所在的代码块（或作用域）结束**。例如，在函数内部声明的变量，其生命周期在函数执行完毕后结束

- 右值(*R-value*)
    - 通常是一个临时值，它没有可访问的内存地址，不能被赋值

    - 生命周期非常短暂，通常**只持续到它所在的语句结束**。例如，表达式的结果是一个R值，它的生命周期在语句执行完毕后即结束

```cpp
int x = 3;                      // 3 is an r-value
int *ptr = 0x02248837;          // 0x02248837 is an r-value
vector<int> v1{1, 2, 3};        // {1, 2, 3} is an r-value,v1 is an l-value
size_t size = v.size();         // v.size()is an r-value
v1[1] = 4*i;                    // 4*i is an r-value, v1[1] is an l-value
ptr = &x;                       // &x is an r-value
v1[2] = *ptr;                   // *ptr is an l-value
MyClass obj;                    // obj is an l-value
x = obj.public_member_variable; // obj.public_member_variable is l-value
```

## 移动语义与`std::move`

在 C++ 中，移动语义（move semantics）是一种优化技术，它允许在对象之间转移资源（如动态分配的内存、文件句柄等），而不是复制这些资源。这样可以显著提高性能，特别是在处理大型对象或资源密集型对象时。

`std::move` 是 C++ 标准库中的一个模板函数，它的主要作用是将一个对象转换为右值引用（r-value reference），从而允许该对象的内容被移动（move）而不是复制（copy）。

需要注意的是，`std::move()` 本身并不执行任何移动操作，它只是将一个对象转换为右值引用，从而使得移动构造函数或移动赋值运算符被调用。实际上的资源转移是在**移动构造函数**或**移动赋值运算符**中完成的。

被移动后的源对象将处于一个“有效但未知”的状态，意味着它仍然是一个有效对象，但它的资源已经被转移，不能再被正常使用。

```cpp
class HumanGenome {
  public:
    // Copy assignment operator
    HumanGenome& operator=(const HumanGenome& other) { 
      if (&other == this) { return *this; }
      data = other.data;

      return *this;
    }

    // Move assignment operator
    HumanGenome& operator=(HumanGenome&& other) noexcept {
      if (this != &other) {
        data = std::move(other.data);
        std::cout << "HumanGenome moved within stage." << std::endl;
      }
      return *this;
    }
  private:
    std::vector<char> data;
}
```

在上面的代码中，`data = std::move(other.data)` 就使用了 `std::move` 将 `other.data` 转换为右值，从而将资源移动到当前对象的 `data` 成员中。

!!! note "`noexcept`"
    `noexcept`关键字表示该运算符不会抛出任何异常。

当原始对象不再需要时，你可以使用 `std::move()` 来转移（而不是复制）其资源。关于`std::move`的应用场景，还可参考[What is `std::move()`, and when should it be used? | stackoverflow](https://stackoverflow.com/questions/3413470/what-is-stdmove-and-when-should-it-be-used)

通常，我们希望避免在应用程序代码中使用 `std::move()`。直接在应用程序代码中使用 `std::move()` 可能会导致代码的可读性和可维护性降低。在类定义中使用它，比如构造函数和运算符。

如果你定义了移动构造函数和移动赋值运算符，编译器可以在很大程度上进行优化，而不需要你显式地使用 `std::move()`。

## SMFs的一些应用理念

### 规则零(*Rule of Zero*)

如果你的类能够依赖编译器生成的默认特殊成员函数（包括默认构造函数、析构函数、拷贝构造函数、拷贝赋值运算符、移动构造函数和移动赋值运算符）来正确管理资源，那么你应该让编译器生成这些函数，而不是手动定义它们。这**通常适用于不管理任何动态分配资源的类**。规则零是规则三和规则五的扩展，它建议**尽可能避免手动定义特殊成员函数**。

### 规则三(*Rule of Three*)

如果一个类定义了析构函数、拷贝构造函数或拷贝赋值运算符**中的任何一个**，那么它很可能**也需要定义其他两个**。这是因为这些函数通常一起工作，以正确管理对象的生命周期和资源。

在这种情况下，由于采用了手动管理内存的方式，编译器就无法自动为用户生成这些内容。

规则三在 C++11 之前非常重要，因为那时还没有移动语义。

### 规则五(*Rule of Five*)

规则五是在 C++11 引入移动语义后对规则三的扩展。如果一个类定义了**任何一个拷贝操作（拷贝构造函数或拷贝赋值运算符）或析构函数**，那么它很可能**也需要定义移动操作（移动构造函数或移动赋值运算符）**。这是因为现代 C++ 支持移动语义，允许更**高效**的资源管理。规则五建议你同时考虑拷贝语义和移动语义。

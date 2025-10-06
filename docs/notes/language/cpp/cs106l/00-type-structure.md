
# 基础类型与结构体

*该笔记基于课程CS106L的学习，用于记录一些cpp的重要特性以及先前不曾了解的cpp特性。*

## 基础数据类型

加上STL（Standard Template Library, 标准模板库）中的`string`类型，C++共有六种基本类型：

```cpp
int num = 5;        
char c = 'e';       
float num = 5.0;    
double num = 5.00;  
bool val = true;    
std::string = "101";
```

C++是静态类型语言，也称强类型语言。其中的变量、函数返回值类型需要在声明或定义时显式声明。

!!! note "**静态类型语言（编译型语言）** vs **动态类型语言（解释型语言）**"
    静态类型语言：  

    - 类型检查在编译时、运行前进行；类型检查严格，类型错误只可能发生在编译时  

    动态类型语言：

    - 类型检查在程序解释并运行时（**`runtime`**）进行。解释器自行判定变量、函数类型，可能导致意料之外的运行结果

## 函数重载

严格的类型检查机制使得C++可同时存在多个不同返回值类型的同名函数，称为**函数重载**

**e.g**:

```cpp
int half(int x, int divisor=2) {  // version (1)
    return x / divisor;
}

double half(double x) {           // version (2)
    return x / 2;
}

int main() {
    half(2);     // uses (1) returns 1
    half(5, 5);  // uses (1) returns 1
    half(2.0);   // uses (2) returns 1.000...
}
```


## `auto` 关键字

`auto`关键字可使编译器在编译时根据上下文信息自行判定变量或函数返回值的类型。注意不要混淆——使用`auto`时，类型检查仍是在编译时进行，并不是像解释型语言那样在程序运行时进行。

!!! note

    `auto`关键字一般用于以下两种情况：  

    - 修饰变量的类型显而易见时

    - 变量类型编写过于冗长且明确时

二者的目的均为提高生产效率

下面是`auto`的一个使用案例：

```cpp
#include <cmath>
#include <iostream>
#include <cassert>

using quadratic = std::pair<bool, std::pair<double, double>>;

quadratic quadraticSolution(double a, double b, double c) {
    assert (a != 0)

    double delta = b*b - 4*a*c;
    std::pair<double, double> solution = {
        (-b + sqrt(delta)) / 2*a,
        (-b - sqrt(delta)) / 2*a
    }

    if (delta < 0) {
        return {false, {std::nan(""), std::nan("")}};
    } else {
        return {true, solution};
    }
}

int main() {
    auto sol = quadraticSolution(1, -2, 1);

    return 0;
}
```

在上面的代码中，我们定义并使用了一个二元一次方程的求根函数，其中函数返回值的类型是我们定义的一个别名`quadratic`。在`main`函数中我们调用该函数时，我们通过`auto`关键字将接受该函数返回值的变量`sol`的类型交由编译器判定，编译时，编译器就会自动将`sol`的类型解析为`quadratic`，即`std::pair<bool, std::pair<double, double>>`。

## 结构体（`struct`）

本质上是一组变量，每个变量可拥有不同的类型。结构体可作为参数传递，也可作为函数返回值。

**e.g**：

```cpp
struct Student {
    std::string name;
    long int id;
    int age;
};

Student s1;
s1.name = "Ben";
s1.id = 110100010;
s1.age = 22;

Student s2 = {"A", 1010001001, 22};

void printStudentInfo(Student s) {
    std::cout << s.name << ': ' << s.id << '\n';
}

Student setStudentInfo(std::string name, long int id, int age) {
    Student s;
    s.name = name;
    s.id = id;
    s.age = age;
    return s;
}
```

前面我们提到`auto`关键字时曾使用了STL中的`std::pair`，其本质上也是结构体的一种，因此，`quadraticSolution`中的`solution`变量也可以使用以下形式替代：

```cpp
struct Solution {
    double x1;
    double x2;
};

Solution solution = {
    (-b + sqrt(delta)) / 2*a,
    (-b - sqrt(delta)) / 2*a
}
```

二者在效果上是一致的。


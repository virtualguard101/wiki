# 初始化和引用操作(`&`)

*该笔记基于课程CS106L的学习，用于记录一些cpp的重要特性以及先前不曾了解的cpp特性。*

## 初始化

在C++中，变量初始化有三种方式：**直接初始化**、**统一初始化**和**结构化绑定**。

### 直接初始化

直接初始化使用**赋值操作符**`=`或包含常量值的括号`()`进行：

```cpp
#include <iostream>

int main() {
    int num = 5;
    double val(5.5);

    std::cout << "num = " << num << " val = " << val << '\n';

    return 0;
}
```

然而在使用直接初始化可能会出现一个致命问题：**数据丢失**。

假设有以下程序，需要传递并操作一个重要参数：

```cpp
#include <iostream>

int main() {
    int criticalSystemVal(5.5); // Direct initialization with a float-point value

    // Some system operation
    // .....
    
    std::cout << "Critical system value: " << criticalSystemVal << '\n';

    return 0;
}
```

编译并执行后上述程序后，结果如下：

```bash
Critical system value: 5
```

可以看出，当初始化的数据类型与声明类型不对应时，变量`criticalSystemVal`的数据出现了丢失。

在直接初始化中，编译器不会对变量和赋值数据进行严格的类型检查，因此极易触发**窄化转换（Narrow Conversion）**导致数据失真，这在数据精确度要求较高的项目环境中是一个致命的问题。

### 统一初始化

为了提供一种一致、简化和更加安全的对象初始化方法，C++11标准中引入了一种新的初始化语法，称为**统一初始化(Uniform initialization)**。统一初始化使用大括号`{}`进行，语法如下：

```cpp
#include <iostream>

int main() {
    int num{5};
    double val{5.5};

    std::cout << "num = " << num << " val = " << val << '\n';

    return 0;
}
```

若对上文的变量`critialSystemVal`使用统一初始化：

```cpp
#include <iostream>

int main() {
    int criticalSystemVal{5.5}; // Uniform initialization with a float-point value

    // Some system operation
    // .....
    
    std::cout << "Critical system value: " << criticalSystemVal << '\n';

    return 0;
}
```

编译时就会出现如下错误：

```bash
demo.cpp: In function ‘int main()’:
demo.cpp:4:30: error: narrowing conversion of ‘5.5e+0’ from ‘double’ to ‘int’ [-Wnarrowing]
    4 |     int criticalSystemVal{5.5}; // Direct initialization with a float-point value
      |                              ^
```

使用统一初始化方法对变量进行初始化，编译时编译器就会对变量类型与初始化值进行严格的类型检查，从而将因类型问题导致的数据失真问题拦截在编译时，使程序更加**安全**的同时提升代码可读性与**一致性**。

**一致性**是指任何数据类型和对象都可使用统一初始化方法进行初始化，如：

```cpp
// Map
std::map<int std::string> id{
    {"A", 101},
    {"B", 102}
};

// Vector
std::vector<int> nums{1, 2, 3, 4, 5};

// Struct
struct Student {
    std::string name;
    long int id;
};
Student s{"A", 100100101};

// Other objects in cpp.....
```

### 结构化绑定

C++17引入了了一个新特性，称为**结构化绑定**。结构化绑定是一种从固定大小的多变量数据结构（元组、数组、结构体、`std::pair`）初始化变量的初始化方式，其允许通过返回多变量数据结构的函数访问对象的数据成员。

直接通过定义理解可能会比较抽象，下面给出语法实例：

```cpp
#include <iostream>
#include <tuple>

// tuple returned by funtion
std::tuple<std::string, std::string> getClassInfo() {
    std::string classCode = "CS106L";
    std::string programLanguage = "C++";
    return {classCode, programLanguage};
}

// use struct
struct Person {
    std::string name;
    int age;
};

int main() {
    // binding
    auto [classCode, programLanguage] = getClassInfo();
    // or 
    auto classInfo = getClassInfo();
    std::string classCode = std::get<0>(classInfo);
    std::string programLanguage = std::get<1>(classInfo);

    // binding from struct
    Person person{"A", 19};
    auto [name, age] = person;

    // binding from array
    int arr[]{1, 2, 3, 4, 5};
    auto [a, b, c, d, e] = arr;

    return 0;
}
```

结构化绑定为多变量聚合性数据结构提供了一个简洁高效的初始化方式。注意使用时需确保绑定变量和对象成员数量相同。

## 引用(`&`)

### 引用基础

声明具名变量为引用，即既存对象或函数的别名。（Declares a named variable as a reference, that is, an alias to an already-existing object or function.）

引用使用操作符`&`(ampersand)，语法如下：

```cpp
int num = 5;
int& ref = num;
ref = 10; // Assigning a new value through the reference.
std::cout << num << '\n';  // Output 10
```

在上面的代码中，`num`是一个`int`型变量，被初始化为`5`。`ref`是一个`int&`类型变量，是变量`num`的**别名**。

因此当我们将`10`赋值给`ref`时，会同时改变变量`num`的值，等效于直接将`10`赋给`num`。

可视化：

```md
int num = 5;                int &ref = num;              ref = 10;

 Memory
---------                   ---------                    ----------
|   5   | 0 <-- num         |   5   | 0 <-- num          |~~5~~ 10| 0 <-- num
---------                   ---------   \                ----------   \
|       | 1                 |       | 1  -> ref          |        | 1  -> ref
---------                   ---------                    ---------- 
|       | 2         ====>   |       | 2          ====>   |        | 2
---------                   ---------                    ----------
|       | 3                 |       | 3                  |        | 3
---------                   ---------                    ----------
|       | 4                 |       | 4                  |        | 4
---------                   ---------                    ----------
```

### 通过引用传递变量

向函数传递引用变量在C++中是一个常见且重要的操作。

```cpp
#include <iostream>
#include <math.h>

void square(int& x) { // n is a referenced value!
    x = std::pow(n, 2);
}

int main() {
    int n = 5;
    square(n);
    std::cout << n << '\n'; // Output 25

    return 0;
}
```

通过引用传参的本质是对内存中的值直接进行操作，**避免拷贝**，提高函数调用效率。对变量的引用同理。

若通过拷贝进行参数传递，拷贝的变量值需要额外占用内存空间。这在降低效率的同时也意味着拷贝变量受**作用域**约束，当接收变量的函数在调用完成后，其栈帧空间被释放，拷贝变量也随之丢失。同时由于函数的操作只作用在拷贝变量上，因此这些操作在函数调用完成后不会反映在原参数上，具体表现为被传递参数的值并不会改变。

简易可视化：

```cpp
#include <iostream>
#include <math.h>

void square(int x) { // Passing n without referenced
    n = std::pow(n, 2);
}

int main() {
    int n = 5;
    square(n);
    std::cout << n << '\n'; // Output 5

    return 0;
}
```

```md
In main()          Calling void square(int x)     After calling square(int x)

 Memory
---------   ---             ---------   ---              ---------   ---
| n = 5 | 0  |              | n = 5 | 0  |               | n = 5 | 0  |
---------  main()           ---------  main()            ---------  main()
|       | 1  |              |       | 1  |               |       | 1  | 
---------   ---             ---------   ---              ---------   ---
|       | 2       ====>     |       | 2          ====>   |       | 2
---------                   ---------    ---             ---------
|       | 3                 | x = 25| 3   |              |       | 3
---------                   ---------  square()          ---------
|       | 4                 |       | 4   |              |       | 4
---------                   ---------    ---             ---------
```

但若是最初采用引用的版本，则调用`square`时，由于其在传参时使用了引用，其对`x`的操作就会直接反映在从`main`函数传递的`n`上：

```md
In main()           Calling void square(int& x)   After calling square(int& x)

 Memory
---------   ---             ---------   ---              ---------   ---
| n = 5 | 0  |            ->| n = 5 | 0  |               | n = 25| 0  |
---------  main()         | ---------  main()            ---------  main()
|       | 1  |            | |       | 1  |               |       | 1  | 
---------   ---           | ---------   ---              ---------   ---
|       | 2       ====>   | |       | 2          ====>   |       | 2
---------                 | ---------    ---             ---------
|       | 3               --|   x   | 3   |              |       | 3
---------                   ---------  square()          ---------
|       | 4                 |       | 4   |              |       | 4
---------                   ---------    ---             ---------
```

### 引用案例

```cpp
#include <iostream>
#include <cmath>
#include <vector>

void shift(std::vector<std::pair<int , int>>& nums) { //Passed in by reference
    for(auto& [num1, num2]: nums) { // In for-each, note the ampersand(&) after auto
        num1++;
        num2++;
    }
}
```

在上面的代码中，需要特别注意`for-each`中`auto`后的`&`。`for-each`中的操作是典型的**结构化绑定**，在绑定过程中，`auto`提示编译器自动判定变量类型。若未进行显式声明，在这里`num1`和`num2`就会被判定为`int`型而不是引用类型`int&`，函数对这两个变量的操作也就不会对通过引用传递的对象`nums`生效。这种现象被称为**剥离引用**。

### 左值与右值

左值可以位于等号的左侧或右侧：

```cpp
int x = 1;
int y = x;
```

右值只能位于等号的右侧：

```cpp
int n = 0;
0 = m;  // Error!
```
同时，我们认为右值是**临时值**。

现有以下代码：

```cpp
#include <iostream>
#include <cmath>

void square_L(int& x) {
    x = std::pow(x, 2);
}

int main() {
    int n = 5;
    square_L(n);
    square_L(5);    // Error
 
    return 0;
}
```
编译以上代码，我们会得到类似如下的错误：

```bash
demo.cpp: In function ‘int main()’:
demo.cpp:23:14: error: cannot bind non-const lvalue reference of type ‘int&’ to an rvalue of type ‘int’
   23 |     square_L(5);
      |              ^
demo.cpp:4:20: note:   initializing argument 1 of ‘void square_L(int&)’
    4 | void square_L(int& x) {
      |               ~~~~~^
```

对于引用操作而言，在一次引用中确定了一个引用对象，我们就无法改变这个引用所指向的对象（注意不是对象的值，不要混淆）。由于我们认为右值是**临时的**，故在引用中我们不能传递右值。

但自C++11起，cpp引入了一种新的语法，使得我们可以在引用中传递右值。

我们可以通过使用操作符`&&`显式声明一个右值引用：

```cpp
#include <iostream>
#include <cmath>

void square_R(int&& x) {
    x = std::pow(x, 2);
}

int main() {
    square_R(5);

    return 0;
}
```
上面的操作称为**右值引用**，前文的则称为**左值引用**。更多关于引用的用法，可参考[cppreference](https://zh.cppreference.com/w/cpp/language/reference)

## `const` 关键字

`const`关键字用于在修饰对象时声明对象的值**不可修改**。

```cpp
#include <iostream>
#include <vector>

int main() {
    std::vector<int> vec{1, 2, 3}; // normal vector
    const std::vector<int> const_vec{1, 2, 3}; // a const vetor
    std::vector<int>& ref{ vec }; // a reference to 'vec'
    const std::vector<int> const_ref{ vec }; // a const reference

    vec.push_back(3);
    const_vec.push_back(3); // error! it's const!
    ref.push_back(3);
    const_ref.push_back(3); // this is const too!

    return 0;
}
```

若尝试编译上述源码，则会产生以下错误信息：

```bash
demo.cpp: In function ‘int main()’:
demo.cpp:11:24: error: passing ‘const std::vector<int>’ as ‘this’ argument discards qualifiers [-fpermissive]
   11 |     const_vec.push_back(3);
      |     ~~~~~~~~~~~~~~~~~~~^~~
In file included from /usr/include/c++/11/vector:67,
                 from demo.cpp:2:
/usr/include/c++/11/bits/stl_vector.h:1203:7: note:   in call to ‘void std::vector<_Tp, _Alloc>::push_back(std::vector<_Tp, _Alloc>::value_type&&) [with _Tp = int; _Alloc = std::allocator<int>; std::vector<_Tp, _Alloc>::value_type = int]’
 1203 |       push_back(value_type&& __x)
      |       ^~~~~~~~~
demo.cpp:13:24: error: passing ‘const std::vector<int>’ as ‘this’ argument discards qualifiers [-fpermissive]
   13 |     const_ref.push_back(3);
      |     ~~~~~~~~~~~~~~~~~~~^~~
In file included from /usr/include/c++/11/vector:67,
                 from demo.cpp:2:
/usr/include/c++/11/bits/stl_vector.h:1203:7: note:   in call to ‘void std::vector<_Tp, _Alloc>::push_back(std::vector<_Tp, _Alloc>::value_type&&) [with _Tp = int; _Alloc = std::allocator<int>; std::vector<_Tp, _Alloc>::value_type = int]’
 1203 |       push_back(value_type&& __x)
      |       ^~~~~~~~~
```

使用`const`修饰的对象在引用时也必须在引用声明前加上`const`修饰：

```cpp
#include <iostream>
#include <vector>

int main() {
    const std::vector<int> nums{1, 2, 3, 4, 5};

    std::vector<int>& ref{ nums }; // Bad work
    const std::vector<int>& ref{ nums }; // OK!

    return 0;
}
```

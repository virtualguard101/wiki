# 特殊成员函数

*该笔记基于课程CS106L的学习，用于记录一些cpp的重要特性以及先前不曾了解的cpp特性。*

## 概述

特殊成员函数也叫**静态成员函数(SMFs, Static Member Functions)**，指一些具有特殊语义和默认行为的成员函数，通常用于对象的生命周期管理、拷贝控制和移动操作等。**特殊成员函数只会在它们被调用和用户显式定义时生成。**

特殊成员函数共有六种：

- **默认构造函数**(*Default constructor*)
    - 创建的对象未指定任何参数，也未实例化任何成员变量

- **析构函数**(*Destructor*)
    - 在对象离开作用域后将其**销毁**

- **拷贝构造函数**(*Copy constructor*)
    - 基于现有对象进行**逐成员拷贝**来创建新的拷贝副本

- **赋值运算符**(*Copy assignment operator*)
    - 将现有对象替换为另一个现有对象的**运算符**

- **移动构造函数**(*Move constructor*)
    - 基于现有对象进行**逐成员移动**来创建新的拷贝副本

- **移动赋值运算符**(*Move assignment operator*)
    - 将现有对象移动至另一个现有对象的**运算符**

```cpp
class Widget {
  public:
    /* Takes no parameters and creates a new object. */
    Widget();                             // default constructor

    /* Creates a new object as member-wise copy of another. */
    Widget(const Widget& w);              // Copy constructor

    /*Assigns an already exisiting object to another. */
    Widget& operator = (const Widget& w); // Copy assignment operator

    /* Called and delete the object when it goes out of scope. */
    ~Widget();                            // Destructor

    Widget(Widget&& rhs);                 // Move constructor
    Widget& operator = (Widget&& rhs);    // Move assignment operator
};
```

最后两个特殊成员函数是我们前面所不曾见过的，我们将在这个章节学习它们。

## 拷贝与赋值(*Copy* & *Copy assignment*)

默认情况下（未重载），拷贝构造函数在被调用时会对对象的每个成员变量进行拷贝，即**逐成员拷贝(*member-wise copy*)**。但这样足够了吗？

如果一个成员变量是指针变量，那么逐成员拷贝就会使新对象的这个成员变量指向相同的已分配的数据，而不是生成一个新的拷贝。

```cpp
template<typename Type>
vector<Type>::vector<Type>(const vector::vector<Type>& other) : 
  _size(other.size),
  _capacity(other.capacity),
  _elems(other.elems) { }
```

在上面的拷贝构造中，针对`_elems`的拷贝就仅仅只是简单地复制了指针或引用。如果成员变量`elems`是一个指针，那么拷贝操作后的新对象和传入这个拷贝构造函数的`other`对象在底层上将**共享同一块内存空间。**具体表现就是**新对象的成员变量`elems`在底层上与旧对象`other`的`elems`指向同一个数组。**

这就是我们通常所说的**浅拷贝(*shallow copy*)**，与之对应的就是**深拷贝(*deep copy*)**。

深拷贝会创建一个与原始对象完全相同且与之相互独立的全新副本。与类的普通成员函数类似，深拷贝的拷贝构造函数需要用户在源文件`.cpp`中自行实现，以覆盖编译器默认的浅拷贝构造。

更多有关浅/深拷贝的内容，可参考[Shallow Copy and Deep Copy in C++ | GeeksForGeeks](https://www.geeksforgeeks.org/shallow-copy-and-deep-copy-in-c/)

## `default` & `delete`

### 用法与作用

在定义类时，可通过显式定义为特殊成员函数设置为**默认**行为或**移除**这个成员函数的功能。

- `default`用于在用户自定义了构造函数后保留编译器默认生成的构造函数

- `delete`用于声明禁用该特殊成员函数

```cpp
class PasswordManager {
  public:
    /* Keep the default copy constructor (if we declare other constructors). 
    /* Declaring any user-defined constructor will make the default disappear without this! */
    PasswordManager() = default;    //     
    PasswordManager(const PasswordManager& pm) = default;
    ~PasswordManager();
    // other method ...

    PasswordManager(const PasswordManager& rhs) = delete;
    PasswordManager& operator = (const PasswordManager& rhs) = delete;
    /* Now copying isn't a possible operation. */

  private:
    // some important member vars.
};
```

### 约定俗成的规则

默认的特殊成员函数在很多情况下都能正常工作，特别是当类没有管理任何资源时。如果默认的SFM功能能够满足需求，就不需要自定义新功能！只有编译器生成的默认功能无法满足需求，我们才应定义新的。

通常情况下，我们在使用动态分配的内存时（如指向堆中数据的指针），默认的功能就无法满足需求了。

当一个类管理了某些资源（如动态分配的内存、文件句柄、网络连接等）时，大多数情况下就必须定义**析构函数**、**拷贝构造函数**和**拷贝赋值运算符**。这三个成员函数合在一起，通常被称为“**三大法则**”（*The Rule of 3*）。

这三个特殊成员函数有一个需要进行自定义就意味着你正在**手动管理**某些资源；接下来就需要我们自己来处理这些资源的**创建**、**分配**、**使用**以及**销毁**事宜。这就意味着，这三个SMF但凡有一个需要进行自定义，那剩下的两个也逃不了。

## 移动和移动赋值(`std::move`)

### 概述

假设我们想要将一个字符串表复制到一个新的字符串表只中，且后续我们不再需要原来的字符串表。

```cpp
class StringTable {
  public:
    StringTable() {}
    StringTable(const StringTable& st) {}
    // other member functions, like insertion, look up, etc.
    // no move/dtor functionality

  private:
    std::map<int, std::string> values;
};
```

根据前面所学的知识，我们可能会选择使用**拷贝构造函数**创建一个新的拷贝副本，然后将原先的对象删除。

但这样高效吗？

拷贝构造函数会从成员变量`values`中逐个拷贝`std::map`中的值，这个过程是低效的。

这个时候就应该学习使用SMFs中的最后两个：**移动构造函数**和**移动赋值函数**了。

移动构造函数和移动赋值运算符是C++11引入的两种特殊成员函数，它们允许将资源从一个对象“移动”到另一个对象，而不是复制。移动语义可以提高程序的性能，特别是在处理大型对象或涉及动态分配资源的对象时。

与拷贝类似的是，移动也是**逐成员**的。

注意移动操作的参数是一个**右值引用**。

```cpp
#include <iostream>
#include <utility> // for std::swap

class MyClass {
  public:
    // Default constructor
    MyClass() : data(new int[100]) {
        std::cout << "Default constructor\n";
    }

    // Copy constructor
    MyClass(const MyClass& other) : data(new int[100]) {
        std::cout << "Copy constructor\n";
        std::copy(other.data, other.data + 100, data);
    }

    // Copy assignment operator
    MyClass& operator=(const MyClass& other) {
        std::cout << "Copy assignment operator\n";
        if (this == &other) return *this;
        MyClass temp(other); // Create a temporary object using the copy constructor
        std::swap(data, temp.data); // Swap resources
        return *this;
    }

    // Move constructor
    MyClass(MyClass&& other) noexcept : data(other.data) {
        std::cout << "Move constructor\n";
        other.data = nullptr; // Ensure the old object no longer owns the resource
    }

    // Move assignment operator
    MyClass& operator=(MyClass&& other) noexcept {
        std::cout << "Move assignment operator\n";
        if (this == &other) return *this;
        MyClass temp(std::move(other)); // Create a temporary object using the move constructor
        std::swap(data, temp.data); // Swap resources
        return *this;
    }

    // Destructor
    ~MyClass() {
        std::cout << "Destructor\n";
        delete[] data;
    }

    // Other member functions...
  private:
    int* data;
};

int main() {
    MyClass obj1; // Calls the default constructor
    MyClass obj2 = obj1; // Calls the copy constructor
    MyClass obj3;
    obj3 = obj1; // Calls the copy assignment operator

    MyClass obj4 = MyClass(); // Calls the move constructor
    MyClass obj5;
    obj5 = MyClass(); // Calls the move assignment operator

    return 0;
}
```

### 注意事项

只有在以下情况编译器才会自动生成移动构造函数和操作符：

- 未声明任何复制操作

- 未声明任何移动操作

- 未声明析构函数

用户声明任何一项都意味着取消C++**默认**的生成操作。

当然也可通过显式声明支持移动操作：

```cpp
Widget(Widget&& ) = default;
Widget& operator=(Widget&&) = default;    // support moving

Widget(Widget& ) = default;
Widget& operator=(Widget&) = default;     // support copying
```

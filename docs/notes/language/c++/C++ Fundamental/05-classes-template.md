# 类与模板

*该笔记基于课程CS106L的学习，用于记录一些cpp的重要特性以及先前不曾了解的cpp特性。*

## 成员访问

在C++中，使用类时需要为其成员配置访问等级权限。访问等级分为三级：`public`、`protected`、`private`。

- `public`（公有）表示该成员可由该类的对象直接访问，通常用于向外部提供类的接口。

- `protected`（保护）表示该成员在类的外部只能由该类的派生类（子类）访问，用于类的继承，允许派生类进行合理的扩展。

- `private`（私有）表示该成员只能在类的内部访问，在类的外部（包括派生类）都是不可访问的，这通常用于隐藏类的内部数据和实现细节，防止外部直接访问和修改，以保证类的稳定性与安全性。

!!! note "`Class` VS `Struct`"
    类成员的访问操作与结构体类似，但二者的区别在于类的成员具有严格的访问权限设置，而结构体的成员没有。使用类成员的访问权限等级进行类比，结构体成员的访问权限等级都是`public`。

## 定义类

### 多文件（`.h`&`.cpp`）

**头文件（`.h`/`.hpp`）**

- 用于定义类并存放它的接口

- 内容上包含：

    - 函数（类方法）原型

    - 变量（类成员变量）声明

    - 类定义

    - 类型定义

    - 宏和常量

    - 模板定义

!!! note
    有关类模板的介绍，移步[Class Templates | CS106L-TextBook](https://cs106l.github.io/textbook/templates/class-templates)

**源文件（`.cpp`）**

- 用于存放头文件中声明的类方法和类定义的实现

- 内容上包含：

    - 函数（类方法）实现

    - 可执行代码

简单来说，头文件用于定义类的结构，源文件用于实现类的定义细节。

![](../../../../assets/images/cpp/head-source_1.png)

![](../../../../assets/images/cpp/head-source_2.png)

*以上图片来源于[CS106L](https://web.stanford.edu/class/cs106l/)的课程幻灯片。*

### 设计类

一个类的大致包含以下几个模块：

- **构造函数（Constructor）**

- **私有成员变量/函数**

- **公有成员变量/函数**

- **析构函数（Destructor）**

#### 构造函数（Constructor）

**构造器/构造函数**用于在创建类的新对象时初始化该对象的状态。

假设我们想实现一个`Student`类，我们可以这样定义：

Header File:
```cpp
class Student {
private:
    std::string name;
    long int id;
    int age;

public:
    // constructor
    Student(std::string name, long int id, int age);
    // memeber methods
    std::string getName();
    long int getID();
    int getAge();
};
```
Source File:
```cpp
#include "Student.h"
#include <string>

// implement constructor
Student::Student(std::string name, long int id, int age) {
    /// keyword 'this' is neccessary in here in order to avoid naming conflict
    this->name = name;
    this->id = id;
    this->age = age;
}

// implemented members
std::string Student::getName() {
    // return name; /// alternative
    return this->name;
}

long int Stdudent::getID() {
    return this->id;
}

int Student::getAge() {
    return this->age;
}

// implemented setter functions
void Student::setName(std::string name) {
    // use 'this' and '=' here!
    this->name = name;
}

void Student::setID(long int id) {
    this->id = id;
}

void Student::setAge(int age) {
    this->age = age;
}
```

注意在源文件中实现类方法时需要在函数名前添加它的`namespace`（命名空间），通常是类的名称。

自C++11起，**构造器**支持使用**列表初始化**：

```cpp
Student::Student(std::string name, long int id, int age) name{name}, id{id}, age{age} {}
```

对于构造函数，我们还能定义其**默认构造**方式：

```cpp
// defualt constructor
Student::Student() name{"virtualguard"}, id{100100101}, age{18} {}

// overload by parameterized constructor
Student::Student(std::string name, long int id, int age) name{name}, id{id}, age{age} {}
```

#### 析构函数（Destructor）

在C++中，析构函数用于在对象生命周期结束时执行清理工作，是对象生命周期中的重要部分。

析构函数不需要显示调用，它会在对象离开其作用范围时自动调用。

析构函数的语法如下：
```cpp
Student::~Student() {
    // free/deallocate any data here

    delete [] some_array; // for illastration
}
```

## 类继承

下图展示的是`stream`的继承关系。

![](../../../../assets/images/cpp/iostream_inheritance.png)

*以上图片来源于[CS106L](https://web.stanford.edu/class/cs106l/)的课程幻灯片。*

针对继承在面向对象编程中的作用与使用思想，课程[CS61A | UC Berkeley](https://cs61a.org/)有详尽的讲解，这里直接看示例。

以几何图形的定义与性质为例：

Header File:
```cpp
class Shape {
public:
    // virtual function
    virtual double area() const = 0;
};

class Circle: public Shape {
public:
    Circle(double radius): _radius{radius} {};
    double area() const {
        return M_PI * _radius * radius;
    }
private:
    // private members are marked by '_'
    double _radius;
};

class Rectangle: public Shape {
public:
    Rectangle(double width, double height): _height{height}, _width{width} {};
    double area() const {
        return _width * _height;
    }
private:
    double _width, _height;
}
```

## 杂项

### 类型别名

允许用户为现有类型创建别名。一般有两种方式：

#### `typedef`

```cpp
// typedef [origin] [aliasing]
typedef int Integer;
typedef double Real;
```

#### `using`

使用`using`关键字进行类型别名定义是C++11引入的一个特性。第一节的学习中我们就有用到它。
```cpp
// using [aliasing] = [origin]
using String = std::string;
using quadratic = std::pair<bool, std::pair<double, double>>;
```

## 模板

### 模板类

- [Class Templates | CS106L-TextBook](https://cs106l.github.io/textbook/templates/class-templates)

模板类是一种基于多种类型进行**参数化定义**的类，具有通用类型组成的成员变量构成。

模板类用于泛化类跨数据类型，使用模板类能够极大地提升代码的复用性。

假设我们想要实现多个自定义容器，但它们在某些功能上具有通用性，我们就可以使用模板类：
```cpp
template <typename T>
class Container {
public:
    Container(T val);
    T getValue();

private:
    T value;
};
```

也可同时传入多个类型名作为模板参数：
```cpp
template <typename T, typename U>
```

!!! note
    在STL中，所有的容器都是**类**。

### 模板函数

模板函数与模板类的声明类似，即使用`template`关键字进行声明：
```cpp
// swap template function
template <typename T>
void swap(T& a, T& b) {
    T temp = a;
    a = b;
    b = temp;
}
```

也可为模板参数设置默认类型：
```cpp
template <typename Type=int>
Type customMin(Type a, Type b) {
    return a < b ? a : b;
}

int main() {
    std::cout << customMin<int>(101, 5) << std::endl;
    return 0;
}
```

多参数：
```cpp
template <typename T, typename U>
auto smartMin(T a, U b) {
    return a < b ? a : b;
}

int main() {
    std::cout << smartMin(101, 5.5) << std::endl;
    return 0;
}

针对上面在头文件中定义的模板类的结构，我们可以在源文件中通过模板函数来完成其成员函数的实现：
```cpp
template <class T>
Container<T>::Container(T val) {
    this->value = val;
}

template <typename T>
T Container<T>::getValue() {
    retutn value;
}
```

在绝大多数情况下，模板参数中的`class`和`typename`可以互换。

!!! note
    需注意若上述模板函数为以下形式，即未在类的命名空间后添加模板类的参数类型，**模板参数将不会传递**：
    ```cpp
    template <class T>
    Container::Container(T val) {
        this->value = val;
    }

    template <typename T>
    T Container::getValue() {
        retutn value;
    }
    ```
    C++要求我们在命名空间中确定模板参数，因为根据参数的不同，我们的类可能会有不同的表现。

### 注意事项

在创建模板类时，需要在定义模板类结构的`.h`文件中包含对应的`.cpp`实现：

```cpp
template <typename T>
class Container {
public:
    Container(T val);
    T getValue();

private:
    T value;
};

// must do this!
#include "Container.cpp"
```

### 模板元编程(TMP, Template Metaprogramming)

合理使用模板可以提高效率。

```cpp
template<unsigned n>
struct Factorial {
    enum { value = n * Factorial<n - 1>::value };
}

template<> // template class "specialization"
struct Factorial {
    enum { value = 1 };
}

int main() {
    std::cout << Factorial<10> << '\n'; // 3628800
}
```

上面是一个阶乘程序，但`Factorial<10>`的结果会在**编译时**直接计算，而不是通常情况下的**运行时**。这能提高程序在运行时的效率，同时也为类似递归的资源密集型操作提供了接口模板。

### `constexpr`

在C++中，也可使用`constexpr`声明表达式在编译时运行。`constexpr`关键字用于指定一个常量表达式。

```cpp
constexpr double fib(int n) {
    if (n == 1) { return 1; }
    return fib(n - 1) * n;
}
```

!!! note
    - 常量表达式必须在声明时立即进行初始化，以便于编译器在编译时直接运行它

    - 传递给常量表达式的参数也应当是常量/常量表达式

变量也可以使用`constexpr`修饰。

## 常量接口

现有一个用户自定义类`Student`：
```cpp
class Student {
public:
    Student(String name, long int id, int age);
    void setName(String name);
    String getName();
    long int getID();
    int getAge();

private:
    using String = std::string;
    String _name;
    long int _id;
    int _age;
}
```

同时有如下函数：
```cpp
std::string getAgeInfo(const Student& s) {
    return s.getName() + "is" + std::to_string(s.getAge()) + "years old."
}
/// compile error
```

那么在编译时就会出现错误，原因如下：

- 在`getAgeInfo()`中，我们使用`const`修饰了对象`s`，以声明其不会被修改

- 然而，编译器并不知道`getName()`和`getAge()`是否会修改对象`s`

- 根据类的特性，成员函数能够**访问并修改成员变量**

解决的方法也很简单，在成员函数声明（头文件）和实现（源文件）的地方中分别在各个函数的参数列表后添加`const`修饰即可：
```cpp
class Student {
public:
    Student(String name, long int id, int age);
    void setName(String name);
    String getName() const;
    long int getID() const;
    int getAge() const;

private:
    using String = std::string;
    String _name;
    long int _id;
    int _age;
};
```

```cpp
#include <string>
#include "Student.h"

std::string Student::getName() const {
    return this->_name;
}

long int Student::getID() const {
    return this->_id;
}

int Student::getAge() const {
    return this->_age;
}
```

被`const`所修饰的函数就是所谓的**常量接口**，即**不会改变类的对象/示例属性的函数**。

**具有`const`属性的对象只能与常量接口进行交互**。

### 应用实例

现有一个用户自定义类`IntArray`：
```cpp
class IntArray {
public:
    IntArray(size_t size);
    ~IntArray();
    int& at(size_t index);
    int size();

private:
    int *_array;
    size_t _size;
}
```

```cpp
IntArray::IntArray(size_t size) : _size(size), _array(new int[size]) {}

IntArray::~IntArray() {
    delete [] _array;
}

int& at(size_t index) {
    return  _array[index];
}

// overload const interface
int& at(size_t index) const {
    return  _array[index];
}

int size() {
    return this->_size;
}
```

在`main`函数调用该类：
```cpp
#include "IntArray.h"
#include <iostream>

static void printElement(const IntArray& arr, size_t index) {
    std::cout << arr.at(index) << std::endl;
}

int main() {
    IntArray arr = IntArray(5);
    int& secondVal = arr.at(1);
    secondVal = 101;
    printElement(arr, 1);

    return 0;
}
```

### `const_cast`

在`IntArray`中，现有一个成员函数`findItem`，用于查找元素：
```cpp
int& findItem(int value) {
    for (auto& elem : arr) {
        if (elem == value) { return elem; }
    }

    throw std::out_of_range("value not found");
}

// overload const interface
const int& findItem(int value) const {
    for (auto& elem : arr) {
        if (elem == value) { return elem; }
    }

    throw std::out_of_range("value not found");
}
```

对于常量接口的重写版本，我们可以使用`const_cast`将其简化为一行：
```cpp
int& findItem(int value) {
    for (auto& elem : arr) {
        if (elem == value) { return elem; }
    }

    throw std::out_of_range("value not found");
}

// use const_cast
const int& findItem(int value) const {
    return const_cast<IntArray&>(*this).findItem(value);
}
```

- `const_cast`用于将当前的`const`引用转换为非`const`引用

- `<IntArray&>`表示转换的非`const`引用目标

- `(*this)`表示对指针`this`进行解引用操作，以将其转换为非`const`引用

- `findItem(value)`表示调用成员函数

总结起来，使用`const_cast`通常分为三步：

1. 设置指向一个非常量对象的状态

2. 调用该函数的非常量版本

3. 将函数调用中非常量类型的返回值转换为常量版本

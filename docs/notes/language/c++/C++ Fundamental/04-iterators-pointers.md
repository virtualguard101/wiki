# 迭代器和指针

*该笔记基于课程CS106L的学习，用于记录一些cpp的重要特性以及先前不曾了解的cpp特性。*

## 迭代器

在遍历容器元素时，除了使用`for`循环，C++还提供了一个叫**迭代器（iterator）**的东西用于访问容器元素。

将容器视作存放文件的文件夹，迭代器就是遍历这些文件的高效工具。

**在STL中**，不同的容器具有不同的迭代器，但所有迭代器都共享以下特性：

- 初始化：`iter = s.begin()`

!!! note
    容器的`begin()`和`end()`方法返回迭代器。

- 自增：`++iter`

- 解引用：`*iter`

- 比较：`iter != s.end()`

- 拷贝：`iter2 = iter1`

针对其他操作，不同的容器具有差异，以下是CS106L的课程幻灯片提供的一幅文档截图：

![iterator_type](../../../../assets/images/cpp/iterators_type.png)

这几个迭代器的功能包含关系大致可由下图概括：

```md

-----------------------------------------
|            Random-Access              |
|   ---------------------------------   |
|   |        Bidirectional          |   |
|   |   -------------------------   |   |
|   |   |       Forward         |   |   |
|   |   |  --------- ---------- |   |   |
|   |   |  | Input | | Output | |   |   |
|   |   |  --------- ---------- |   |   |
|   |   |                       |   |   |
|   |   -------------------------   |   |
|   |                               |   |
|   ---------------------------------   |
|                                       |
-----------------------------------------
```

### 前向迭代器

**前向迭代器（Forward iterators）**是标准容器所具有的最基本功能级别的迭代器。其在容器中只能**单向**移动。

- **输入迭代器（Input iterators）**可出现在`=`操作符的右侧（RHS, Right Hand Side）

```cpp
auto elem = *it;
```

- **输出迭代器（Output iterators）**可出现在`=`操作符的左侧（LHS, Left Hand Side）

```cpp
*elem = value;
```

### 双向迭代器

**双向迭代器（Bidirectional iterators）**可向前移动，同时也可向后移动。

- `--iter;`

!!! note
    自增或自减运算将运算符置于迭代器前（前置自增/自减），迭代器返回迭代器自增或自减后的值，置后反之。实际编程中推荐使用前者，因为其通常比后者更加高效。

- 功能本质上与前向迭代器没有区别

### 随机访问迭代器

**随机访问迭代器（Random-Access iterators）**允许用户直接访问容器中的某个元素而不需要依次访问所有元素。

- `iter += 5;`

- 向量访问：`vec[1]`, `vec[5]`.....

- 需要注意避免越界访问

### STL 迭代器分类

对于STL中的不同容器，它们对应的迭代器如下：

| 容器 | 迭代器类型 |
|:---:|:---------:|
|`std::vector`| Random-Access |
|`std::deque`| Random-Access |
|`std::list`| Bidirectional |
|`std::map`| Bidirectional |
|`std::set`| Bidirectional |
|`std::stack`| No iterator |
|`std::queue`| No iterator |
|`std::priority_queue`| No iterator |

*以上表格来源于[CS106L](https://web.stanford.edu/class/cs106l/)的课程幻灯片。*

创建一个容器意味着同时创建一个对应的迭代器。对于*queue*和*stack*，可以通过改变容器来访问容器元素。

!!! warning
    在使用迭代器进行迭代时，迭代对象必须是`const`，即不可变。

### 使用迭代器

```cpp
for (auto iter=set.begin(); iter != set.end(); ++iter) {
    const auto& elem = *iter;
}
```
当我们需要元素本身而不是它的引用，我们则需要对迭代器进行解引用（`*iter`）。

若迭代对象是`std::map`，则可使用**结构化绑定**进行高效解引用：

```cpp
std::map<int, int> map{
    {0, 000},
    {1, 001},
    {2, 010},
    {3, 011},
    {4, 100},
    {5, 101}
}

for (auto iter=map.beging(); iter != map.end(); ++iter) {
    const auto& [key, value] = *iter;
}
```

上面的`for`语句等效于：

```cpp
for (auto& elem : map) {
    const auto [key, value] = elem;
}
```
本质其实就是`for-each`

学习迭代器时，可简单将其理解为指向容器元素的指针，虽然这并不准确。关于迭代器的底层原理，可参考[Iterators | CS106L-TextBook](https://cs106l.github.io/textbook/containers/iterators)

## 指针

了解过C语言的话，这部分内容可直接跳过。是的，二者的指针没有本质上的区别。

详细概念、底层原理可参考[Pointers and Memory | CS106L-TextBook](https://cs106l.github.io/textbook/cpp-fundamentals/pointers-and-memory)

### 指针与引用的区别

引用本质上是一个变量的**别名**，而指针的本质是其指向变量的**内存地址**。访问引用变量的值只需要使用引用的名称即可，而访问一个指针指向的变量的值则需进行**解引用**操作（`*`）。

在灵活性上，指针更胜一筹，它可以指向内存中的任何对象，包括`nullptr`；引用操作则只能指向一个有效对象，且引用变量一经初始化后便无法再改变其引用对象。

当然，安全和灵活二者是守恒的。指针灵活的特性导致其在使用过程中可能会出现**空指针解引用**等危险操作；而引用的对象不可变（`const`）及对象有效性则有效避免了这些可能在开发过程中被忽略的，但可能在程序运行过程中被触发的问题。

[Pointers and Memory | CS106L-TextBook](https://cs106l.github.io/textbook/cpp-fundamentals/pointers-and-memory#relationship-to-references)中也介绍了这部分的内容。

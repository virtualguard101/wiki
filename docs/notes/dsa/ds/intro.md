# 结构分类与基本数据类型

>[数据结构 | Hello 算法](https://www.hello-algo.com/chapter_data_structure/){target="_blank"}

## 结构分类

### 逻辑结构

==逻辑结构揭示了数据元素之间的逻辑关系==[^1]。在形式上，我个人认为称其为“顺序结构”或许会更加容易理解——在可迭代对象[^2]中，数据逻辑往往以顺序为主，而可迭代对象在编程中极其常见。当然，严格意义上来说，这样的理解是狭义的。

!!! warning
    “顺序结构”在计算机科学中有特定含义，通常指**程序控制结构：顺序执行、分支、循环**；这里的理解接近接下来会提到的**线性结构**。初学阶段，更多接触的是线性结构的数据结构，故这样的理解虽然具有局限性，但在该阶段还是可以接受的。

逻辑结构可分为**线性结构**与**非线性结构**，非线性结构还可细分为**树型结构**和**网状结构**。可参考下图理解：

![线性数据结构与非线性数据结构](classification_logic_structure.png)
*图片来源：[数据结构分类 | Hello 算法](https://www.hello-algo.com/chapter_data_structure/classification_of_data_structure/)*

线性与非线性的区别主要在于数据元素的 ==$n$ 对 $n$== 问题：

- 线性为**一对一**
- 非线性**树**为**一对多**
- 非线性**图**为**多对多**

### 物理结构

==物理结构反映了数据在计算机内存中的存储方式==。物理结构**从底层决定**了数据的访问、更新、增删等操作方法，两种物理结构在 ==时间效率== 和 ==空间效率== 方面呈现出互补的特点[^3]。

形式上，物理结构可分为**连续空间存储**和**分散空间存储**，可结合下图理解：
![连续空间存储与分散空间存储](classification_phisical_structure.png)
*图片来源：[数据结构分类 | Hello 算法](https://www.hello-algo.com/chapter_data_structure/classification_of_data_structure/)*

!!! tip
    所有数据结构都是基于数组、链表或二者的组合实现的。例如，栈和队列既可以使用数组实现，也可以使用链表实现；而哈希表的实现可能同时包含数组和链表[^4]:

    - **基于[数组](linear/array.md)可实现**：栈、队列、哈希表、树、堆、图、矩阵、张量（维度 $\geqslant 3$ 的数组）等。
    - **基于[链表](linear/linked-list.md)可实现**：栈、队列、哈希表、树、堆、图等。

## 基本数据类型

==基本数据类型以**二进制**的形式存储在计算机中，是 CPU 可以直接进行运算的数据类型==。

!!! note inline end "`string`"
    在计算机科学理论中，字符串（`string`）通常不被认为是基础数据类型，其更多被看作是字符类型的**数组**形式；在现代编程语言中（如 Python、JavaScript），字符串类型则通常是内建的。

在不同的编程语言中，基础数据类型的形式或许会有所不同，但大致包括以下几类：

- 整数型：`int`、`long`、`short`、...
- 浮点型：`float`、`double`、...
- 字符型：`char`
- 布尔型：`bool`

基础数据类型通常作为数据结构的基本数据元素，因此学习数据结构可以看作是学习如何组织这些不同的基本数据类型。


[^1]: [数据结构分类 | Hello 算法](https://www.hello-algo.com/chapter_data_structure/classification_of_data_structure/){target="_blank"}

[^2]: [可迭代对象有什么特点？| GitHub Issues](https://github.com/YvetteLau/Step-By-Step/issues/28){target="_blank"}

[^3]: [数据结构分类 | Hello 算法](https://www.hello-algo.com/chapter_data_structure/classification_of_data_structure/){target="_blank"}

[^4]: [数据结构分类 | Hello 算法](https://www.hello-algo.com/chapter_data_structure/classification_of_data_structure/#312){target="_blank"}
# 结构分类与基本数据类型

## 结构分类

>[数据结构分类 | Hello 算法](https://www.hello-algo.com/chapter_data_structure/classification_of_data_structure/)

### 逻辑结构

==逻辑结构揭示了数据元素之间的逻辑关系==[^1]。在形式上，我个人认为称其为“顺序结构”或许会更加容易理解——在可迭代对象[^2]中，数据逻辑往往以顺序为主，而可迭代对象在编程中极其常见。当然，严格意义上来说，这样的理解是狭义的。

!!! warning
    “顺序结构”在计算机科学中有特定含义，通常指**程序控制结构：顺序执行、分支、循环**；这里的理解接近接下来会提到的**线性结构**。初学阶段，更多接触的是线性结构的数据结构，故这样的理解虽然具有局限性，但在该阶段还是可以接受的。

逻辑结构可分为**线性结构**与**非线性结构**，非线性结构还可细分为**树型结构**和**网状结构**。可参考下图理解：

![线性数据结构与非线性数据结构](../../../assets/images/dsa/classification_logic_structure.png)
*图片来源：[数据结构分类 | Hello 算法](https://www.hello-algo.com/chapter_data_structure/classification_of_data_structure/)*

线性与非线性的区别主要在于数据元素的 ==$n$ 对 $n$== 问题：

- 线性为**一对一**
- 非线性**树**为**一对多**
- 非线性**图**为**多对多**


[^1]: [数据结构分类 | Hello 算法](https://www.hello-algo.com/chapter_data_structure/classification_of_data_structure/)

[^2]: [可迭代对象有什么特点？| GitHub Issues](https://github.com/YvetteLau/Step-By-Step/issues/28)
# Java 入门要点

> - [1. Intro, Hello World Java | UCB CS 61B Data Structures, Spring 2021](https://sp21.datastructur.es/index.html)
>
> - [Introduction to Java-Essentials | Hug61B](https://joshhug.gitbooks.io/hug61b/content/chap1/chap11.html)

Java 的大体形式与 C++ 等主流静态类型语言类似，部分地方甚至与 Python 等动态类型语言相通。

## 重要特性

条件语句、循环语句等这些老生常谈的细节这里就不再赘述，下面记录一些 Java 的部分重要特性以及一些不同于其他语言的特性。

1. Java 是一种**面向对象**的语言

    - 每个`.java`文件都必须包含至少一个**类声明**

    - ==所有的代码实现均位于**类**中，包括全局常量与辅助函数==

    - Java 程序的主调逻辑通常需要在`public static void main(String[] args)`**方法**中定义

2. Java 是一个**静态类型**语言

    - 源码中的所有变量、方法（函数）、参数等都需要**显式声明**类型

    - 一旦声明完成，对象的数据类型就**不可改变**

    - 类型问题与错误只会在**编译过程**中出现，不会出现在**程序运行时**

    !!! note "静态类型语言的优点与缺点"

        - **优点**：

            - 可以很轻松地捕捉并定位类型错误，方便Debug

            - 类型问题与错误基本只会在编译过程中出现，即几乎不可能出现在用户计算机上

            - 能够提升代码的运行效率，因为不需要在程序运行时进行类型检查

        - **缺点**：

            - 代码冗长

            - 代码复用性较低（不同返回类型的相同处理逻辑需要进行**类型重载**）

## 如何编写并运行一个 Java 程序

<!-- *图片来源: [Essentials | Hug61B](https://joshhug.gitbooks.io/hug61b/content/chap1/chap11.html)* -->

根据前面学习的特性，我们便可以开始着手编写一个简单的 Java 程序。

环境配置这里不再赘述，可以参考[这篇文章](https://www.geeksforgeeks.org/installation-guide/download-and-install-jdk-on-windows-mac-and-linux/)。

以经典的 `Hello World` 为例，首先创建一个`.java`文件，取名为`HelloWorld`：

```java
public class HelloWorld {
    public static int main(String[] args) {
        System.out.println("Hello, World!");
    }
}
```

!!! important
    - 需要注意，==包含主调方法（main方法）且使用`public`修饰的类必须与文件同名，且大小写敏感！==

    - 如果类不是`public`的（例如使用默认访问修饰符），则类名可以与文件名不同——但这种方式不推荐，因为不符合Java的惯例，且可能导致代码管理混乱。

    - 一个`.java`文件中可以定义多个类，但最多只能有一个`public`类，且`public`类的名称必须与文件名一致。其他非`public`类可以有不同名称。

    为保持代码清晰和遵循Java规范，一般建议始终让包含`main`方法的类名与文件名一致，并使用`public`修饰。

编写完成后，需要对源码进行**编译**。这里需要用到 Java 编译器，即`javac`：
```bash
javac HelloWorld.java
```

编译顺利完成后会在当前路径下生成一个与源文件同名的`.class`文件，这个文件包含了**Java字节码**，是一种**中间代码**，需要通过JVM（Java Virtual Machine, Java虚拟机）**解释执行**，即Java解释器（`java`），而不是像`.exe`文件那样可以直接在操作系统上运行：
```java
$ java HelloWorld
Hello, World!
```

!!! tip "JVM"
    Java虚拟机有自己完善的硬件架构，如处理器、堆栈、寄存器等，还具有相应的指令系统。JVM屏蔽了与具体操作系统平台相关的信息，使得Java程序只需生成在Java虚拟机上运行的目标代码（字节码），就可以在多种平台上不加修改地运行[^1]。

    JVM是Java跨平台特性的核心，其架构十分复杂，详情可参考[How JVM Works - JVM Architecture](https://www.geeksforgeeks.org/java/how-jvm-works-jvm-architecture/)


[^1]: [Java虚拟机 | 维基百科](https://zh.wikipedia.org/wiki/Java%E8%99%9A%E6%8B%9F%E6%9C%BA)

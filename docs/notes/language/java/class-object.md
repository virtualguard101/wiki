---
date: 2025-10-13 23:03:00
title: Java类与对象
permalink: 
publish: true
---

# Java类与对象

> [cs61b lec2 2021 intro2(slide) | cs61b-sp21](https://docs.google.com/presentation/d/1gEHCa3PLFE3FikAwwO1WhZAXKjWEQ9F1HM9qECoZCUo/edit?slide=id.g5849d008c_081#slide=id.g5849d008c_081)
>
> [Intro2 Study Guide | CS 61B Data Structures, Spring 2021](https://sp21.datastructur.es/materials/lectures/lec2/lec2.html)
>
> [Defining and Using Classes | Hug61B](https://joshhug.gitbooks.io/hug61b/content/chap1/chap12.html)

如[前文](intro.md)所学，在 Java 中，我们需要将所有的代码实现放在一个个不同的类中。这一节，我们将学习**如何在 Java 中定义并实例化类**。

## `Dog`(一个类的实例)

### 调用与`main`方法

- 所有的方法（函数）都需要包含在某个类中

- 想要运行一个类，必须定义一个 `main` 方法，并在其中调用其他方法（函数）

!!! note
    但不是所有类都需要定义一个主调方法

以下面的代码为例:
```java
public class Dog {
    public static void makeNoise() {
        System.out.println("Bark!");
    }
}

public class DogLauncher {
    public static void main(String[] args) {
        Dog.makeNoise();
    }
}
```

上面的`Dog`类不包含`main`方法，因此其中的`makeNoise`方法无法直接运行，就需要在下面包含`main`方法的`DogLauncher`类中的`main`方法中调用。

!!! review
    根据之前所学，想要这段Java源码（`.java`）能够被正确编译，就应该为其取名为`DogLauncher`，而不是`Dog`——因为主调方法位于`DogLauncher`中。

### 典型实现

```java
public class Dog {
    // 实例变量
    public String dogName;

    // 构造方法
    public Dog(String name) {
        dogName = name;
    }

    // 静态方法
    public static void makeNoise() {
        System.out.println("Bark!");
    }

    // 实例方法
    public int reply(String call) {
        if (call.equals(dogName)) {
            Dog.makeNoise();
            return 1;
        } else {
            System.out.println(".....");
            return 0;
        }
    }
}
```

!!! tip "`.equals()`"
    在上面的实现中，`.equals()`方法用于比较两个字符串的**值是否相等**。在Java中，若使用`==`比较两个字符串，则比较的是**引用相等性**，即**二者是否指向相同对象**。

    详情可参考[How do I compare strings in Java? | stackoverflow](https://stackoverflow.com/questions/513832/how-do-i-compare-strings-in-java)

在上面的实现中: 

- `dogName`是一个实例变量，用于存储不同实例的数据

- ==`Dog`为**构造方法**，用于定义如何实例化类的实例，**一般与类名相同**==

- `makeNoise`为静态方法，可以通过类名直接调用，不依赖实例状态

- `reply`为实例方法（非静态方法），可被实例直接访问，常作为类的**调用接口**

## 对象实例化

### 单对象实例化

以上面实现的`Dog`类为例:

```java
public class DogLauncher {
    public static void main(String[] args) {
        Dog dogBlack;                   // 声明`Dog`类对象
        new Dog("Black");               // 实例化一个`Dog`对象
        dogBlack = new Dog("Black");    // 实例化一个`Dog`对象并将其赋值给变量`dogBlack`

        Dog dogWhite = new Dog("White");// 声明 + 实例化 + 赋值

        dogBlack.call("Black");         // 调用实例方法
        dogWhite.call("Black");

        return 0;
    }
}
```

### 批量实例化(对象数组)

可通过以下步骤创建一个对象数组:

- 首先使用`new`**关键字**创建一个对应类型的数组

- 然后再对数组中的各个元素分别使用`new`进行具体的实例化

```java
public class DogLauncher {
    public static void main(String[] args) {
        Dog[] dogs = new Dog[2];    // 创建一个含有2个`Dog`对象的数组
        // 元素实例化
        dogs[0] = new Dog("Black");
        dogs[1] = new Dog("White");

        // 调用实例方法
        dogs[0].call("Black");
        dogs[1].call("White");

        return 0;
    }
}
```

## 静态成员 vs 实例成员

### 方法调用概述

- ==静态方法由类名直接调用==，如前面典例的: `Dog.makeNoise()`

- 实例方法则通过实例对象调用，如前面典例的: `dogBlack.call("Black")`

!!! note
    事实上，静态方法也可以通过实例对象访问，但不推荐这样做:

    - **语义混淆**: 静态方法属于类级别，不依赖于任何特定实例。通过实例调用静态方法会让人误以为这个方法依赖于该实例的状态，但实际上它完全独立于实例。

    - **代码可读性差**: 通过实例调用静态方法会让代码的意图不清晰，其他开发者需要额外思考这个方法是否真的依赖于实例状态。

    - ==**违反面向对象设计原则**==: 在面向对象编程中，静态方法属于类本身的属性，不依赖于实例状态；而实例方法属于对象，**用于访问与修改特定实例对象的状态**。

    - **性能考虑**: 虽然性能差异微乎其微，但通过类名调用静态方法在编译时就能确定方法位置，而通过实例调用需要额外的间接寻址。

    - **代码维护性**: 如果将来需要将静态方法改为实例方法，通过实例调用的代码需要大量修改，而通过类名调用的代码则不需要改动。

- ==静态方法无法访问实例成员==，这就不是因为简单的“约定俗成”的原因了，而是底层设计的原因:

    - **生命周期不同**: 静态方法在类加载时就被创建，属于类级别；而实例变量/方法只有在创建对象实例时才存在

    - **内存分配不同**： 静态方法存储在方法区，所有实例共享；实例变量/方法储在堆内存中，每个实例都有独立的空间

    静态方法没有 `this` 引用，无法知道要访问哪个实例的变量。    

    ==简单来说，**从静态方法的视角来看**，其与特定的实例成员在时间与空间上都是没有交集的，因此无法访问到它们==。

### 为什么使用静态方法

静态成员可以被实例方法直接访问，而其却不能访问任何实例成员，那么我们为什么还要使用它？

- **工具类**：一些类从创建开始就不会被实例化，比如`Math`类，有点类似于Python中的`os`模块

- **程序入口**：有时，一个类可能含有一个静态方法与实例方法的**混合体**——最经典的例子就是`main`方法: `public static void main(String[] args)`

- **共享数据**：静态变量可以在所有实例间共享，比如计数器、配置信息等

- **工厂方法**：静态方法常用于创建对象实例，如`Integer.valueOf()`

### 成员访问规则

- **静态成员**：

    - 可以通过类名访问：`Dog.makeNoise()`

    - 也可以通过实例访问（不推荐）：`dog.makeNoise()`

    - ==无法访问实例成员==（技术限制）

- **实例成员**：

    - 必须通过实例访问：`dog.reply("test")`

    - 不能通过类名访问：`Dog.reply()` ❌

    - 可以访问静态成员：`Dog.makeNoise()`

## 通过辅助方法控制程序复杂度

### 类与静态方法

!!! questions

    - 为什么 Java 要求程序员必须使用类呢？

    - 静态方法存在的理由究竟是什么？

[CS61B官方](https://docs.google.com/presentation/d/1gEHCa3PLFE3FikAwwO1WhZAXKjWEQ9F1HM9qECoZCUo/edit?slide=id.gafa0a497a3_0_0#slide=id.gafa0a497a3_0_0)给出的原因听上去令人有些匪夷所思：

<div style="text-align: center">
    <strong>为了让程序员“无法做出选择”</strong>
</div>

选择越少，意味着做事的方式也就越少——例如，将一个方法声明为静态变量就意味着你不能在该方法中使用任何实例变量

做事的方式越少，通常就**意味着越简单**。

### 通用理念

一门优秀的计算机科学课程应当教会人们**如何妥善处理复杂性问题**[^1]。

- 使用辅助方法能够将复杂问题**分解成若干简单问题**，从而使得其更具可控性

- ==通过将注意力集中在一项任务上，犯错的概率会大大降低==


[^1]: [Managing Complexity More Generally | cs61b lec2 2021 intro2(slide)](https://docs.google.com/presentation/d/1gEHCa3PLFE3FikAwwO1WhZAXKjWEQ9F1HM9qECoZCUo/edit?slide=id.gafa0a497a3_0_22#slide=id.gafa0a497a3_0_22)
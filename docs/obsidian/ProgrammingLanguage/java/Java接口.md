---
date: 2026-07-05 23:09:06
title: Java接口
permalink: java-interface
publish: true
tags:
  - 编程语言
  - Java
---

# Java接口

如[前文](Java类与对象.md)所学，类是 Java 组织代码的基本单元。但有时我们并不关心对象"是什么"，而更关心它"能做什么"，这时就需要**接口（Interface）**。

!!! abstract
    - 接口定义**行为契约**，实现类用 `implements` 承诺遵守

    - 支持**多实现**，弥补 Java 单继承的限制

    - 是**多态**的重要基础：用接口类型引用，运行时绑定具体实现

    - Java 8+ 支持 `default` 和 `static` 方法，兼顾演进与兼容

    - 只有一个抽象方法的接口是**函数式接口**，可用 Lambda 表达式


## 什么是接口

接口是一种**只定义行为规范、不提供（或少量提供）具体实现**的类型。可以把它理解成一份**契约**：实现类签字承诺"我会提供这些方法"，调用方只依赖这份契约，而不依赖具体实现。

```java
public interface Flyable {
    void fly();  // 抽象方法，默认 public abstract
}
```

```java
public class Bird implements Flyable {
    @Override
    public void fly() {
        System.out.println("鸟在飞");
    }
}
```

!!! note
    - 接口**不能被实例化**，不能写 `new Flyable()`

    - 实现类用 `implements` 关键字声明对接口的实现

    - 实现类必须实现接口中**所有抽象方法**，否则该类也必须声明为 `abstract`

## 为什么需要接口

### 弥补单继承的局限

Java 类只能**单继承**一个父类，但可以**同时实现多个接口**：

```java
public interface Swimmable {
    void swim();
}

public class Duck implements Flyable, Swimmable {
    @Override
    public void fly() { System.out.println("鸭子飞"); }

    @Override
    public void swim() { System.out.println("鸭子游"); }
}
```

### 实现多态与解耦

调用方可以只依赖接口类型，而不关心具体实现类：

```java
public class Zoo {
    public static void letItFly(Flyable animal) {
        animal.fly();  // 运行时决定调用哪个类的实现
    }

    public static void main(String[] args) {
        letItFly(new Bird());
        letItFly(new Duck());
    }
}
```

这就像插座标准：只要符合插脚规格，吹风机和台灯都能插上去用——调用方只认"插座"，不认具体电器。

## 接口中可以有什么

### 常量

接口中的字段默认是 `public static final`（常量），修饰符可省略：

```java
public interface Config {
    int MAX_SIZE = 100;  // 等价于 public static final int MAX_SIZE = 100;
}
```

### 方法（随 Java 版本演进）

| 方法类型 | 引入版本 | 说明 |
|---------|---------|------|
| 抽象方法 | Java 1.0 | 只有声明，无方法体，实现类必须重写 |
| 默认方法 `default` | Java 8 | 带方法体，实现类可不重写 |
| 静态方法 `static` | Java 8 | 属于接口本身，通过 `接口名.方法()` 调用 |
| 私有方法 `private` | Java 9 | 仅供接口内部复用，外部不可见 |

```java
public interface Logger {
    void log(String msg);  // 抽象方法

    default void logError(String msg) {
        log("[ERROR] " + msg);  // 默认方法
    }

    static Logger console() {
        return msg -> System.out.println(msg);  // 静态方法
    }
}
```

!!! tip "默认方法的意义"
    Java 8 引入默认方法，是为了在**不破坏已有实现类**的前提下，给接口添加新方法。例如 `Collection` 接口新增的 `stream()` 方法就用了这种方式。

## 接口 vs 抽象类

两者都能包含抽象方法，但设计意图不同：

| | 接口 | 抽象类 |
|---|------|--------|
| 关键字 | `interface` / `implements` | `abstract class` / `extends` |
| 继承/实现数量 | 多实现 | 单继承 |
| 构造方法 | 无 | 有 |
| 实例字段 | 只有常量 | 可以有 |
| 设计意图 | 定义"能做什么"（能力） | 定义"是什么"（is-a 关系） |

!!! review
    - 若多个不相关的类需要共享同一组行为 → 用**接口**（如 `Comparable`）

    - 若一组类有共同的父类状态和逻辑 → 用**抽象类**（如 `AbstractList`）

## 函数式接口

若一个接口**只有一个抽象方法**，它就是**函数式接口**，可以用 Lambda 表达式简化实现：

```java
@FunctionalInterface
public interface Greeting {
    void say(String name);
}

public class Demo {
    public static void main(String[] args) {
        Greeting g = name -> System.out.println("Hello, " + name);
        g.say("Java");
    }
}
```

常见函数式接口：`Runnable`、`Comparator`、`Predicate`、`Consumer` 等，都在 `java.util.function` 包中。

!!! note
    `@FunctionalInterface` 注解不是必须的，但加上后编译器会检查接口是否满足"只有一个抽象方法"的条件。

## 典型使用场景

- **统一 API 规范**：`List`、`Map`、`Set` 等集合框架都基于接口设计，底层实现可互换

- **回调机制**：`Runnable` 定义"可运行的任务"，`Thread` 接受 `Runnable` 对象

- **策略模式**：将不同算法封装为同一接口的不同实现，运行时可切换

- **解耦测试**：业务代码依赖接口，测试时注入 Mock 实现

```java
List<String> names = new ArrayList<>();   // 声明为接口类型
names.add("Alice");
names.add("Bob");
names.sort(String::compareTo);            // 接受 Comparator 函数式接口
```

## 与 Go 接口对比

[Go 的接口](../golang/Golang接口.md)设计思路与 Java 有显著差异：

### 实现方式：显式 vs 隐式

| | Java | Go |
|---|------|-----|
| 实现声明 | 必须写 `implements` | **隐式满足**，无需声明 |
| 类型检查 | 名义类型（Nominal） | 结构类型（Structural） |
| 比喻 | 需要"签字画押"才算履约 | "走起来像鸭子就是鸭子" |

```java
// Java：不声明 implements，即使有同名方法也不能当 Writer 用
class FileWriter implements Writer {
    @Override
    public void write(byte[] data) { /* ... */ }
}
```

```go
// Go：只要方法签名匹配，自动满足接口
type FileWriter struct{}
func (f FileWriter) Write(data []byte) (int, error) { /* ... */ }
var w Writer = FileWriter{}  // ✅ 无需 implements
```

### 接口能包含什么

| 成员 | Java | Go |
|------|------|-----|
| 抽象方法 | ✅ | ✅（只有方法签名） |
| 默认方法 `default` | ✅（Java 8+） | ❌ |
| 静态方法 | ✅（Java 8+） | ❌ |
| 常量/字段 | ✅ `public static final` | ❌ |
| 空接口（任意类型） | ❌（有 `Object` 根类） | ✅ `interface{}` / `any` |

### 设计理念

| 维度 | Java | Go |
|------|------|-----|
| 继承模型 | 单继承类 + 多实现接口 | 无继承，靠**组合 + 嵌入** |
| 接口粒度 | 可大可小（如 `List` 方法较多） | 倾向**小接口**，按需组合（`Reader` + `Writer`） |
| 第三方扩展 | 需修改源码或包装类 | 第三方类型可**直接**满足你的接口 |
| 函数式支持 | 函数式接口 + Lambda | 函数是一等公民，`func` 类型 |

### 相同点

- 都用于定义**行为契约**，实现多态与解耦

- 都支持一个类型**同时满足多个接口**

- 都可以把接口作为**函数参数/返回值**类型

- 调用方都只依赖接口，不依赖具体实现

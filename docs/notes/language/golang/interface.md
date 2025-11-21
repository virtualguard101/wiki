---
date: 2025-11-22 01:33:16
title: Golang接口
permalink: 
publish: true
---

# Golang 接口

## 什么是接口

Go 的接口是一组**方法签名的集合**，定义对象能做什么，不关心对象是什么类型。当某一类型满足接口定义的所有方法时，即认为该类型实现了该接口。

## 接口的使用

>[Go语言接口 | Go语言进阶之路](https://golangstar.cn/go_series/go_base/go_interface.html)

### 定义接口与使用接口

```go
type 接口名 interface {
    方法名1(参数列表1) (返回值列表1)
    方法名2(参数列表2) (返回值列表2)
}
```

一个接口包含以下要素:

- 接口名

- 方法名

- 参数列表

- 返回值列表

下面是一个 Go 接口的简单示例：

!!! example

    ```go
    // ========== 阶段 1：定义接口（契约）==========
    type Writer interface {
        Write([]byte) (int, error)  // 只是签名，没有实现
    }

    // ========== 阶段 2：具体类型实现（满足契约）==========
    type File struct {
        filename string
    }

    // 这里才是真正的实现
    func (f File) Write(data []byte) (int, error) {
        // 实现逻辑已经写好了
        fmt.Printf("Writing to %s: %s\n", f.filename, string(data))
        return len(data), nil
    }

    // ========== 阶段 3：使用接口（调用已实现的方法）==========
    func main() {
        file := File{filename: "test.txt"}
        var w Writer = file  // File 已经实现了 Write，所以可以赋值
        
        // 这里调用的是 File 已经实现好的 Write 方法
        w.Write([]byte("hello"))  // 输出: Writing to test.txt: hello
    }
    ```

    简单来说，三个阶段分别对应三个关键点:

    - 接口定义 -> 契约（方法签名集合）

    - 类型实现 -> 满足契约（在类型上实现方法）

    - 使用接口 -> 通过契约调用（调用已实现的方法）

### 空接口

没有任何方法声明的接口被称为**空接口`interface{}`**。

所有的类型都实现了空接口，因此`interface{}`（Go 1.18+ 可用 `any`）可以用于存储任意类型的数值，常用于需要处理未知类型的场景：

```go
// 可以存储任何类型的值
var anything interface{} = 42
anything = "hello"
anything = []int{1, 2, 3}
```

Golang很多标准库函数都使用了空接口，如`fmt.Println`、`fmt.Printf`、`fmt.Sprintf`等，表示接受任意类型的参数。

### 接口作为函数参数

接口作为函数参数，在定义函数时，形参为接口类型；函数调用时，实参为该接口的具体实现。

```go
package main

import "fmt"

type Reader interface {
   Read() int
}

type MyReader struct {
   a, b int
}

// Reader 接口实现
func (m *MyReader) Read() int {
   return m.a + m.b
}

// 参数类型为接口类型
func DoJob(r Reader) {
   fmt.Printf("myReader is %d\n", r.Read())
}

func main() {
   myReader := &MyReader{2, 5}
   DoJob(myReader)  // 输出: myReader is 7
}
```

若形参为空接口，则实参可以是任意类型:

```go
package main

import "fmt"


func DoJob(value interface{}) {
   fmt.Printf("value is %v\n", value)
}

func main() {
   val := 10
   DoJob(val)  // 输出: value is 10
   DoJob("hello")  // 输出: value is hello
   DoJob([]int{1, 2, 3})  // 输出: value is [1 2 3]
}
```

## 设计理念

!!! abstract "Go接口的设计理念"
    - **"满足即实现"**：只要方法匹配，自动满足接口

    - **"小而专一"**：接口小，通过组合扩展

    - **"解耦优先"**：类型不需要知道接口，接口不需要知道类型

    - **"组合优于继承"**：通过组合和接口实现代码复用

    这样的设计能让代码更灵活、更易测试、更易扩展。

### 类比虚函数

Go 接口类似C++中的[虚函数](../cpp/cs106l/06-lambda_function.md#虚拟函数virtual):

```cpp
// C++ 抽象基类（纯虚函数）
class Writer {
public:
    virtual int Write(const std::vector<uint8_t>& data) = 0;  // 纯虚函数
    virtual ~Writer() = default;
};

// 具体实现类
class FileWriter : public Writer {
public:
    int Write(const std::vector<uint8_t>& data) override {
        // 实现逻辑
        return data.size();
    }
};

// 使用
std::unique_ptr<Writer> writer = std::make_unique<FileWriter>();
writer->Write({1, 2, 3});
```

但是 C++ 的虚函数在实现时需要**显式继承**（`class FileWriter : public Writer`）；而 Go 的接口是**隐式实现**的：只要一个类型实现了接口中定义的所有方法，它就自动实现了该接口，无需显式声明。

### 与传统OOP的差异

!!! abstract
    | 特性 | 传统OOP | Go 接口 |
    |:-|:-|:-|
    |实现方式|显式继承/实现|隐式实现|
    |类型关系|类层次结构|扁平结构|
    |接口大小|倾向于大接口|小接口 + 组合|
    |耦合度|类型与接口耦合|类型与接口解耦|
    |灵活性|需要提前规划|运行时动态匹配|
    |可扩展性|修改类层次|添加新接口|



1. **隐式实现 vs 显式继承**

    在传统oop中，实现一个接口需要显式继承该接口。而在Go中，实现一个接口只需要实现该接口中定义的所有方法，无需显式继承该接口:

    ```java
    // Java - 必须显式声明实现接口
    interface Writer {
        void write(byte[] data);
    }

    // 必须用 implements 关键字
    class FileWriter implements Writer {
        @Override
        public void write(byte[] data) {
            // 实现
        }
    }
    ```

    ```go
    // Go - 隐式实现，无需声明
    type Writer interface {
        Write([]byte) (int, error)
    }

    // 只要实现了方法，就自动满足接口
    type FileWriter struct {}
    func (f FileWriter) Write(data []byte) (int, error) {
        // 实现
    }
    // 无需显式声明 "implements Writer"
    ```

    - 传统 OOP: **编译时**检查继承关系，类型与接口耦合

    - Go: **运行时**检查方法集，类型与接口解耦

    !!! tip "鸭子类型（Duck Typing）"

        ```java
        // Java - 必须显式实现
        class MyClass implements Writer {
            // 即使有 write 方法，不声明 implements 就不能用
        }
        ```

        ```go
        // Go - "如果它走起来像鸭子，叫起来像鸭子，那它就是鸭子"
        type MyType struct {}

        func (m MyType) Write(data []byte) (int, error) {
            return len(data), nil
        }

        // 自动满足 Writer 接口，无需声明
        var w Writer = MyType{}  // ✅ 可以
        ```

2. **组合优于继承**

    在传统oop中，**继承**是建立类型层次的主要方式。而得以于Go接口灵活的特性，**组合**通常是更好的选择:

    ```java
    // Java - 类层次结构
    class Animal {
        void eat() { ... }
    }

    class Dog extends Animal {
        void bark() { ... }
    }

    class Cat extends Animal {
        void meow() { ... }
    }
    ```

    ```go
    // Go - 通过组合和接口
    type Eater interface {
        Eat()
    }

    type Dog struct {
        // 组合其他类型
        Animal Animal
    }

    func (d Dog) Eat() { ... }
    func (d Dog) Bark() { ... }
    ```

    - 传统 OOP: 静态继承关系，类型层次固定，难以灵活组合

    - Go：通过接口和组合，支持更灵活地组合行为，从而实现**多态**

        !!! review "多态与接口"
            多态对象与接口的概念在[cs61a](https://cs61a.org/)中有详尽的介绍。在学习完cs61a后，我曾尝试基于该思想实现了一个[简易的立体几何计算器](../../../projects/SpaceCaculator.md)，里面记录有当时对多态对象与接口的理解。

    !!! tip "类型系统的差异"
        在传统oop中，类型系统基于类层次:

        ```java
        // Java - 类层次
        Object
        └── Animal
            ├── Dog
            └── Cat
        ```

        而在Go中，类型关系通过接口动态建立，类型系统更加**扁平**:

        ```go
            // Go - 扁平的类型系统
        // 没有基类，没有继承
        // 只有接口和实现
        type Dog struct {}
        type Cat struct {}

        // 通过接口定义行为
        type Animal interface {
            Eat()
            Sleep()
        }
        ```

3. **小接口原则（接口隔离）**

    个人认为这是一个十分显著且意义非凡的差异。

    传统oop在定义接口时，通常会倾向于定义**大接口**，即在方法集合中尽可能包含更多的方法。这导致在实现接口时不得不统一实现所有方法，即便某些方法对于某些类型来说没必要或并不适用:

    ```java
    // Java - 大接口
    interface FileOperations {
        void read();
        void write();
        void delete();
        void rename();
        void copy();
        void move();
        // ... 很多方法
    }

    // 实现类必须实现所有方法
    class File implements FileOperations {
        // 即使只需要 write，也要实现所有方法
    }
    ```

    而在Go中，接口的定义能够做到**小而专一**，在使用时**按需组合**即可:

    ```go
    // Go - 小接口，按需组合
    type Reader interface {
        Read([]byte) (int, error)
    }

    type Writer interface {
        Write([]byte) (int, error)
    }

    type Closer interface {
        Close() error
    }

    // 需要多个功能时组合接口
    type ReadWriter interface {
        Reader
        Writer
    }

    type ReadWriteCloser interface {
        Reader
        Writer
        Closer
    }
    ```

    !!! tip "灵活解耦"
        传统oop的“大接口”决定了接口与实现者之间必然存在较高的耦合度:

        ```java
        // Java - 接口和实现类需要提前规划
        // 如果第三方库的类型想实现你的接口，需要修改代码
        interface MyInterface {
            void doSomething();
        }

        // 第三方库的类型无法实现你的接口（除非修改源码）
        ```

        而Go接口的灵活性则允许第三方库的类型**动态**实现接口，而无需修改源码:

        ```go
        // Go - 接口定义者不需要知道实现者
        // 任何类型都可以实现你的接口
        type MyInterface interface {
            DoSomething()
        }

        // 第三方库的类型也可以实现你的接口
        import "thirdparty"

        type ThirdPartyType struct {}
        func (t ThirdPartyType) DoSomething() { ... }

        var m MyInterface = ThirdPartyType{}  // ✅ 可以
        ```

### 一个实际应用场景

```java
// 需要定义基类或接口，所有数据源必须继承
interface DataSource {
    String read();
    void write(String data);
}

class FileSource implements DataSource { ... }
class DatabaseSource implements DataSource { ... }
class APISource implements DataSource { ... }
```

```go
// 定义小接口
type Reader interface {
    Read() (string, error)
}

type Writer interface {
    Write(string) error
}

// 任何有 Read/Write 方法的类型都可以使用
// 包括标准库、第三方库、你自己的类型
func processData(r Reader, w Writer) {
    data, _ := r.Read()
    w.Write(data)
}

// 标准库的 os.File 自动满足 Reader/Writer
// 第三方库的类型也可以
// 你的自定义类型也可以
```

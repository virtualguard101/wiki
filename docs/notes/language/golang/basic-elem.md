---
date: 2025-11-17 20:41:14
title: Golang程序结构
permalink: 
publish: true
---

# Golang 程序结构

## 变量

### 变量类型

Golang 支持以下几种变量类型：

- 布尔类型：`bool`

- 整数类型：`int`, `int8`, `int16`, `int32`, `int64`, `uint`, `uint8`, `uint16`, `uint32`, `uint64`, `uintptr`

- 浮点数类型：`float32`, `float64`

- 复数类型：`complex64`, `complex128`

- 字符串类型：`string`

详情可参考[基本类型 | Go语言中文文档](https://www.topgoer.com/go%E5%9F%BA%E7%A1%80/%E5%9F%BA%E6%9C%AC%E7%B1%BB%E5%9E%8B.html)。

### 变量声明

在Golang中，变量声明有三种方式:

- 使用 `var` 关键字声明变量

    - 显式声明变量类型

        ```go
        var identifier1, identifier2 type = value1, value2
        ```
    
    - 隐式判定

        ```go
        var identifier1, identifier2 = value1, value2
        ```

- 使用 `:=` 关键字声明变量（初始化声明）

    ```go
    identifier1, identifier2 := value1, value2
    ```

    这种方式是声明变量的首选方式，但只能用于**局部变量**的声明。

    注意使用这种方式时不能**重复**声明，否则会产生编译错误。

#### 多变量声明

除了上面提到的三种基本方式的变种外，还可以通过下面的方式声明变量:

```go
var (
    value1 type1
    value2 type2
)
```

这种声明方式**一般用于声明全局变量**。

### 变量的生命周期

```go
package main

import "fmt"

var globalStr string
var globalInt int

func main() {
   var  localStr string
   var  localInt int
   localStr = "first local"
   localInt = 2021
   globalInt = 1024
   globalStr = "first global"
   fmt.Printf("globalStr is %s\n", globalStr)   //globalStr is first global
   fmt.Printf("globalStr is %d\n", globalInt)   //globalStr is 1024
   fmt.Printf("localInt is %s\n", localStr)     //localInt is first local
   fmt.Printf("localInt int is %d\n", localInt) //localInt int is 2021
}
```

## 常量

与其他主流语言类似，Golang也使用 `const` 关键字声明常量:

```go
const identifier1, identifier2 [type] = value1, value2
```

常量不可以在运行时被修改。

常量声明可以以**编译期**中可以确定结果的表达式作为[右值](../cpp/cs106l/01-init-reference.md#左值与右值):

```go
const (
    str = "hello world"
    strLength = len(str)
    strUpper = strings.ToUpper(str)
)
```

### 常量用作枚举

Golang与C++不同，没有枚举类型，但可以使用常量来实现枚举:

```go
const (
    Unknown = 0
    Success = 1
    Failure = -1 
)
```

### iota

`iota`是Golang中的一个常量计数器，用于生成递增的常量值，通常用于枚举类型的定义。`iota`可简单理解为可以被编译器修改的常量。

`iota`在`const`块中被重置为0，每次遇到新的`const`块时，`iota`都会被重置为0。

```go
const (
    Unknown = iota // 0
    Success = iota // 1
    Failure = iota // 2
)
```

在新的一行中，`iota`会继续递增，因此下面的代码与上面等效:

```go
const (
    Unknown = iota // 0
    Success        // 1
    Failure        // 2
)
```

注意变量本身的值与`iota`是相互独立的，可通过以下示例验证:

```go
package main

import "fmt"

func main() {
    const (
        a = iota      // 0
        b             // 1
        c             // 2
        d = "ha"      // 独立值，iota = 3
        e             // "ha"，iota = 4
        f = 100       // iota = 5
        g             // 100，iota = 6
        h = iota      // 7，恢复计数
        i             // 8
    )
    fmt.Println(a, b, c, d, e, f, g, h, i) // 0 1 2 ha ha 100 100 7 8
}
```

## 运算符

与其他主流静态类型语言没什么不同。可参考[Go运算符 | Go语言进阶之路](https://golangstar.cn/go_series/go_base/go_operators.html)

## 结构体

与C++中的[结构体](../cpp/cs106l/00-type-structure.md#结构体struct)类似，Golang中的结构体也是一种复合数据类型，用于表示一组相关数据的集合。

```go
type Person struct {
    Name string
    Email string
}

// 键值对初始化
person := Person{
    Name: "John",
    Email: "john@example.com"
}

// 列表初始化
person := Person{
    "John",
    "john@example.com"
}
```

访问也与C++中的结构体类似，使用`.`运算符访问结构体的成员:

```go
fmt.Println(person.Name)    // output: John
fmt.Println(person.Email)   // output: john@example.com
```

## 数组与切片

### 数组

在Golang中，数组用于存放一系列**同类型**的数据。

有多种方式定义数组:

```go
// 1. 最基础的定义方式
var scores [3]int  // 定义一个能存放3个整数的数组

// 2. 定义时直接赋值
var prices = [3]float64{10.99, 20.99, 30.99}

// 3. 让编译器自动计算长度
names := [...]string{"张三", "李四", "王五"}

// 4. 指定特定位置的值
colors := [5]string{0: "红", 2: "蓝", 4: "绿"}  // [红 "" 蓝 "" 绿]
```

Golang的数组是**定长数组**，一旦定义，数组长度不可变。同时，在Golang中，**数组的长度是类型的一部分**，因此`[3]int`与`[4]int`是两种不同的类型。

### 切片

**切片(Slice)**可以看作是一种**动态数组**，其长度可变。

切片是基于数组实现的，因此切片的长度不能超过其底层数组的长度。

创建切片的方式也有多种:

```go
// 1. 从数组创建
arr := [5]int{1, 2, 3, 4, 5}
s1 := arr[1:4]  // [2, 3, 4]

// 2. 直接创建
s2 := []int{1, 2, 3}

// 3. 使用 make 创建
s3 := make([]int, 3, 5)  // 长度3，容量5
```

切片包含指向底层数组的**指针**、**长度**和**容量**。

切片是**引用类型**，多个切片可共享同一底层数组，修改一个可能影响另一个。

#### 基本操作

```go
s := []int{1, 2, 3}
s = append(s, 4)      // 追加元素
fmt.Println(len(s))   // 长度: 4
fmt.Println(cap(s))   // 容量: 可能大于长度
```

`append`可能导致重新分配内存，生成新的底层数组；使用`make`创建切片时，可以指定容量来减少重新分配内存的次数。


## 映射

在Golang中，映射(Map)是一种无序的键值对集合，用于存储和检索数据，类似Python中的字典(dict)与数据结构中的**哈希表**的具象化。

### 定义映射

```go
// 1. 使用make函数创建
scoreMap := make(map[string]int)

// 2. 创建时直接初始化
studentScores := map[string]int{
    "张三": 95,
    "李四": 88,
    "王五": 92,
}

// 3. 声明一个空map
var prices map[string]float64
// 注意：声明后需要通过make初始化才能使用
prices = make(map[string]float64)
```

#### 基本操作

```go
// 1. 添加或修改键值对
scoreMap["王五"] = 92

// 2. 获取值
score := scoreMap["张三"]
fmt.Println(score)    // output: 95

// 3. 删除键值对
delete(scoreMap, "张三")

// 4. 遍历
for key, value := range scoreMap {
    fmt.Println(key, value)
}
```

#### 嵌套映射

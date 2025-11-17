---
date: 2025-11-17 09:41:14
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

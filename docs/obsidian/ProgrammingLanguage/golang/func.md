---
date: 2025-11-18 16:47:36
title: Golang函数
permalink: 
publish: true
---

# Golang 函数

## 函数定义

```go
func functionName([parameter list] paraType) returnType {
    // function body
}
```

## 函数调用

## 参数传递

在Golang中，参数传递都是**值传递**，不存在[引用传递](初始化与引用操作.md#通过引用传递变量)，即函数中对形参的操作不会改变函数作用域外实参的值。

## 函数变量

在Golang中，**万物皆变量**，函数也不例外。

Golang可以很灵活地创建函数，并作为另外一个函数的实参:

```go
package main

import (
   "fmt"
   "math"
)

func main(){
   /* 声明函数变量 */
   getSquareRoot := func(x float64) float64 {
      return math.Sqrt(x)  // 求一个数的平方根
   }

   /* 使用函数变量调用函数 */
   fmt.Println(getSquareRoot(9))
}
```

熟悉JS的话应该能发现这类似JavaScript中[回调函数](JavaScript入门要点.md#回调函数)的使用:

```go
package main 

import "fmt" 

// 声明一个函数类型 
type fc func(int) int

func main() { 
   CallBack(1, callBack)//执行函数---CallBack 
} 

func CallBack(x int, f fc) {  //定义了一个函数 testCallBack
    f(x)  //由于传进来的是callBack函数，该函数执行需要传入一个int类型参数，因此传入x 
} 

func callBack(x int) int { 
   fmt.Printf("我是回调，x：%d\n", x) 
   return x 
}
```

## 函数闭包

所谓**闭包**，其实就是**匿名函数**+**捕获的变量**，类似C++中的[lambda表达式](Lambda表达式.md)与JavaScript中的[箭头函数](JavaScript入门要点.md#箭头函数)。

```go
func counter() func() int {
    i := 0
    return func() int {
        i += 1          // 这里捕获了变量i，每次调用匿名函数时，i的值都会被更新
        return i
    }
}

func main() {
    nextCounter := counter()
    fmt.Println(nextCounter())  // 1
    fmt.Println(nextCounter())  // 2

    nextCounter2 := counter()
    fmt.Println(nextCounter2())  // 1
    fmt.Println(nextCounter2())  // 2
}
```

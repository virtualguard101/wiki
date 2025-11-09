---
date: 2025-11-08 19:24:54
title: Golang入门要点
permalink: 
publish: true
---

# Golang 入门要点

>[Tutorials | The Go Programming Language](https://go.dev/doc/tutorial/)
>
>[Go语言圣经（中文版）](https://golang-china.github.io/gopl-zh/)


## 概述

Go（Golang） 是由 Google 于 2007 年设计、2009 年开源的一门**静态类型、编译型、并发友好**的编程语言。其核心设计理念是**简单**、**高效**、**可并发**、**可维护**。

Go 常被称为 “现代C语言”，但相较于 C/C++，它更强调：

- 开发效率与易读性

- 原生支持高并发

- 快速编译与部署

- 内置内存管理（垃圾回收）

- 丰富的标准库

值得注意的是，**Go 是云原生生态的核心语言**，从 Docker 到 Kubernetes 再到 Terraform、Prometheus，几乎所有现代云基础设施项目都使用 Go。

## Hello, World

```go
package main

import "fmt"

func main() {
	fmt.Println("Hello, World!")
}
```

单次运行:

```bash
$ go run main.go
Hello, World!
```

Go 是编译型语言，可通过 `build` 子命令将源码编译为可执行文件:

```bash
$ go build main.go
$ ./main
Hello, World!
```

## 包与模块系统

>[Go Modules Reference | The Go Programming Language](https://go.dev/ref/mod)

Go 语言的程序通过**包（package）**组织，类似Python中的*模块（module）*与C++中的*库（library）*。

每个源文件都以一条 `package` 声明语句开始，用于指定源文件所属的包，在上面的例子中就是 `package main`；`package` 语句后紧跟着的就是**导入语句（import）**。

### 依赖管理

当项目需要依赖第三方包或模块时，可以使用 `go mod` 命令进行依赖管理。

在早期版本中（`1.11` 之前），Go 使用 `$GOPATH` 来组织代码。自 `v1.13` 起，Go 引入了 **Go Modules** 作为其正式的依赖管理系统。

- 使用 `init` 子命令初始化当前模块:

    ```bash
    go mod init [module-name]
    ```

    这会在项目的根目录下生成一个名为 `go.mod` 的文件，用于记录项目的依赖信息。

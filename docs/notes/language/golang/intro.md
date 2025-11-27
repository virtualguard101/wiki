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

![](assets/intro/lang_compare.jpg)

Go（Golang） 是由 Google 于 2007 年设计、2009 年开源的一门**静态类型、编译型、并发友好**的编程语言。其核心设计理念是**简单**、**高效**、**可并发**、**可维护**。

Go 常被称为 “现代C语言”，但相较于 C/C++，它更强调：

- 开发效率与易读性

- 原生支持高并发

- 快速编译与部署

- 内置内存管理（垃圾回收）

- 丰富的标准库

值得注意的是，**Go 是云原生生态的核心语言**，从 Docker 到 Kubernetes 再到 Terraform、Prometheus，几乎所有现代云基础设施项目都使用 Go。

![](assets/intro/golang.png)

### 语言特性概览

| 特性                | 说明                          |
| ----------------- | --------------------------- |
| **静态类型、编译型**      | 编译成单个二进制文件，无需虚拟机。           |
| **内存安全与GC**       | 自动垃圾回收，无需手动释放内存。            |
| **协程（Goroutine）** | 轻量线程模型，百万级并发不是问题。           |
| **通道（Channel）**   | 原生 CSP 并发模型（通信顺序进程）。        |
| **包（package）机制**  | 模块化结构清晰。                    |
| **简洁语法**          | 无类、无继承、无泛型（Go 1.18 起引入了泛型）。 |
| **跨平台**           | 一次编译，支持多系统和多架构交叉编译。         |


### Golang 适合做什么

| 领域          | 应用                                       |
| ----------- | ---------------------------------------- |
| **后端服务开发**  | 高并发 API 服务、Web 框架                        |
| **分布式系统**   | etcd、Consul、NATS、CockroachDB             |
| **云原生基础设施** | Docker、Kubernetes、Prometheus、Istio       |
| **命令行工具**   | Hugo、Cobra、Helm                          |
| **区块链**     | Ethereum（go-ethereum）、Hyperledger Fabric |
| **网络编程**    | 高性能代理、P2P系统（IPFS）                        |


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

Go 语言的程序通过**包（package）**组织，类似[Python中的*模块（module）*](../python/package.md#定义)与C++中的*库（library）*。

每个源文件都以一条 `package` 声明语句开始，用于指定源文件所属的包，在上面的例子中就是 `package main`；`package` 语句后紧跟着的就是**导入语句（import）**（⚠️注意这个顺序是必须的）。

### 多文件编译

Go 以包为单位进行编译，假设有这样一个目录结构:

```bash
.
├── echo.go
├── go.mod
└── main.go
```

`echo.go` 用于存放业务逻辑代码，`main.go` 用于存放主调函数。那么在编译时就要将这两个文件一起编译:

```bash
go build .
# Or
go build echo.go main.go
```

否则若`main.go`中应用了`echo.go`中的函数，那么编译时就会报错，提示`echo.go`中被`main.go`调用的函数未定义:

```bash
$ go build ./main.go
./main.go:5:2: undefined: echo1
./main.go:6:2: undefined: echo2
./main.go:7:2: undefined: echo3
```

### 依赖管理

当项目需要依赖第三方包或模块时，可以使用 `go mod` 命令进行依赖管理。

在早期版本中（`1.11` 之前），Go 使用 `$GOPATH` 来组织代码。自 `v1.13` 起，Go 引入了 **Go Modules** 作为其正式的依赖管理系统。

- 使用 `init` 子命令初始化当前模块:

    ```bash
    go mod init [module-name]
    ```

    这会在项目的根目录下生成一个名为 `go.mod` 的文件，用于记录项目的依赖信息。

    在编写代码后，可通过 `go mod tidy` 命令自动更新依赖信息:

    ```bash
    go mod tidy
    ```

    这会自动删除未使用的依赖，并更新 `go.mod` 文件。

## 代码格式化

Golang 在代码格式化这方面采取了十分强硬的措施，`gofmt` 在格式化时没有任何可选的参数。这样保证了团队成员在代码风格上的一致性，能避免一些不必要的冲突。

安装了Golang的LSP（[Gopls](https://go.dev/gopls/#editors)）后，很多文本编辑器在保存文件时默认会自动调用 `gofmt` 进行格式化。另外，还有一个导入相关的工具 `goimports`，可根据代码需要自动创建或删除导入语句。

## 一些入门小练习

>[Github Repository | vg101's Wiki](https://github.com/virtualguard101/wiki/tree/main/code/lang/golang/)

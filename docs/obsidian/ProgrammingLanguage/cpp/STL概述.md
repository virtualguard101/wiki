---
date: 2026-05-18 11:37:55
title: STL概述
permalink: stl-overview
publish: true
tags:
  - 编程语言
  - C++
---

# STL概述

**STL**（*Standard Template Library*，标准模板库）是C++标准库中的一个重要组成部分，提供了一系列的容器、算法和迭代器，用于解决常见的数据结构和算法问题。

STL主要由以下几个部分组成：

- [*Containers*（容器）](cs106l/STL容器.md): How do we store groups of things?

- [*Iterators*（迭代器）](cs106l/迭代器和指针.md#迭代器): How do we traverse containers?

- [*Functors*（函数对象/函子）](cs106l/Lambda表达式.md#函数对象函子Function-ObjectFunctor): How can we represent functions as objects?

- *Algorithms*（算法）: How do we transform and modify containers in a generic way?

## 容器

> [STL容器](cs106l/STL容器.md)

## 迭代器

> [迭代器 - 迭代器和指针](cs106l/迭代器和指针.md#迭代器)

## 函数对象/函子

> [函数对象/函子 - Lambda表达式](cs106l/Lambda表达式.md#函数对象函子Function-ObjectFunctor)

**函子**（*Functor*）是C++中的一种**对象**，可以像函数一样被调用，因此也叫函数对象。

!!! quote "Definition[^1]"
    A functor is any object that defines an `operator()`.
    
    In English: an object that acts like a function.

函子通常用于实现回调函数、事件处理等。

## 算法


[^1]: [Lambda And Functors | CS106L Spring26 Lecture 11 Slide](https://github.com/virtualguard101/cs106l/blob/main/assets/slides/2026Spring-11-LambdasAndFunctors.pdf)
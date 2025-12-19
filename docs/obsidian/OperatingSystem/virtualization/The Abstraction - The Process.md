---
date: 2025-12-19 22:50:54
title: "The Abstraction: The Process"
permalink:
publish: true
tags:
  - 操作系统
---

# The Abstraction: The Process

>[The Abstraction: The Process | Operating Systems: Three Easy Pieces](https://pages.cs.wisc.edu/~remzi/OSTEP/cpu-intro.pdf)

!!! abstract "Key Terms"
    - The process is the major OS abstraction of a running program. At any point in time, the process can be described by its state: the contents of memory in its address space, the contents of CPU registers (including the program counter and stack pointer, among others), and information about I/O (such as open files which can be read or written).

    - The process API consists of calls programs can make related to processes. Typically, this includes creation, destruction, and other useful calls.

    - Processes exist in one of many different process states, including running, ready to run, and blocked. Different events (e.g., getting scheduled or descheduled, or waiting for an I/O to complete) transition a process from one of these states to the other.

    - A process list contains information about all processes in the system. Each entry is found in what is sometimes called a process control block (PCB), which is really just a structure that contains information about a specific process.

## Overview

!!! question "How to provide the illusion of many CPUs?"
    Although there are only a few physical CPUs available, how can the OS provide the illusion of a nearly-endless supply of said CPUs?

操作系统为**正在运行的程序**提供的抽象概念我们称之为**进程**。

要理解进程的构成，首先要理解其**状态机（Machine State）**:

- 一个组成部分是其**内存**（其地址空间）: 指令存储在内内存中；运行中的程序读取与写入的数据也存储在内存中。

- 另一个组成部分是**寄存器**: 许多指令显式地读取或更新寄存器。

    一些特殊的寄存器构成了该状态机的一部分，例如:

      - 程序计数器（PC）/指令指针（IP, Instruction Pointer）: 保存下一条要执行的指令的地址。

      - 堆栈指针（SP）及其关联帧。

## Program Creation

![](assets/process/program_to_process.jpg)

简单概括来说，可大致分为以下几个步骤:

1. 将其代码和所有静态数据从磁盘加载到内存中

2. 为该程序的**运行时栈**分配内存

3. 为该程序的**堆**分配内存。（在C语言中，堆用于显式请求动态分配数据）

4. 执行一些初始化操作，特别是一些与**I/O**相关的任务

## Process State

>[三种基本状态-进程的控制与描述](../408/进程的描述与控制.md#三种基本状态)

除了三种基本状态，进程还可能进入已退出但是尚未完全清理的状态，在基于Unix的系统中，我们称这种状态为**僵尸状态（Zombie State）**。

## Data Structures

xv6的进程结构:

```c
// the registers xv6 will save and restore
// to stop and subsequently restart a process
struct context {
  int eip;
  int esp;
  int ebx;
  int ecx;
  int edx;
  int esi;
  int edi;
  int ebp;
};

// the different states a process can be in
enum proc_state { UNUSED, EMBRYO, SLEEPING,
RUNNABLE, RUNNING, ZOMBIE };

// the information xv6 tracks about each process
// including its register context and state
struct proc {
  char *mem; // Start of process memory
  uint sz; // Size of process memory
  char *kstack; // Bottom of kernel stack
  // for this process
  enum proc_state state; // Process state
  int pid; // Process ID
  struct proc *parent; // Parent process
  void *chan; // If !zero, sleeping on chan
  int killed; // If !zero, has been killed
  struct file *ofile[NOFILE]; // Open files
  struct inode *cwd; // Current directory
  struct context context; // Switch here to run process
  struct trapframe *tf; // Trap frame for the
  // current interrupt
};
```

## Process API

>[Interlude: Process API](Process%20API.md)

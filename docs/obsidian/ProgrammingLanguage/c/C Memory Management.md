---
date: 2026-07-16 22:42:43
title: C Memory Management
permalink: c-mem-management
publish: true
tags:
  - 编程语言
  - C
  - CS61C
---

# C Memory Management

> [L05 C Memory Management | CS61C: Course Notes](https://notes.cs61c.org/content/c-memory-management/)

<div class="responsive-video-container">
    <iframe src="https://player.bilibili.com/player.html?isOutside=true&aid=1806497713&bvid=BV17b42177VG&cid=1621699590&p=5&autoplay=0" 
    scrolling="no" 
    border="0" 
    frameborder="no" 
    framespacing="0" 
    allowfullscreen="true"> 
    </iframe>
</div>

!!! abstract "Learning Outcomes"
    - Learn characteristics of the C memory layout.

    - Differentiate between storage allocation and variable declaration.

    - Know where variables are stored in C, i.e., which memory segment data is allocated in.

    - Understand how the stack pointer automatically allocates and deallocates stack frames.

    - Understand when it is safe to pass pointers into the stack between functions.

    - Contrast the heap’s dynamic memory with stack memory.

    - `free` every block allocated with `malloc`, `realloc`, or `calloc`

    - Practice reading Linux `man` pages to determine specific behavior of C `stdlib` functions.

## Memory Layout

So far we have talked about *how much* space types occupy (`sizeof`), but not *where* things live in memory.

### Memory Allocation

In C, storage can be allocated in three ways:

| Kind | Where you declare / allocate it | When | Notes |
|------|----------------------------------|------|-------|
| **Local variable** | Inside a function | Compile time | Visible only in that function’s namespace |
| **Global variable** | Outside any function | Compile time | Visible to the whole program; use sparingly |
| **Dynamic allocation** | Via library calls like `malloc` | Runtime | Size can depend on input (e.g. file length) |

- **Storage allocation** means setting aside a block of memory.  

- **Variable declaration** means allocating a block *and* giving it a name (and a type, which implies size).

Declaration always implies allocation, but allocation does not always imply a named variable (e.g. `malloc` returns an address with no name attached).

!!! warning
    Avoid overusing globals. They make accidental sharing and hard-to-track edits easy, and weaken abstraction between functions.

### Four Regions of Memory

> [内存管理概述 - 进程的内存映像](../../OperatingSystem/408/内存管理概述.md#进程的内存映像)

A C program’s address space typically has four segments:

| Segment | Contents | Management |
|---------|----------|------------|
| **Stack** | Local variables, parameters, return addresses | Automatic; grows **downward** |
| **Heap** | Dynamically allocated storage (`malloc` / `free`) | On demand; grows **upward** |
| **Data** (Static) | Global variables | Fixed size for the whole run |
| **Text** (Code) | Program instructions | Fixed size; loaded when the program starts |

Rough layout from low to high addresses:

![](assets/c-mem-management/1.png)

!!! tip "Name traps"
    - The **stack** behaves like the stack data structure; the **heap** here is *not* a heap data structure—just a “heap of memory.”

    - The **data** segment means *global/static* data, not “all data.”

    - **Text** means code (often treated as read-only), like written text you don’t rewrite.

In C you must know *which segment* your data lives in, because each region is managed differently. Wrong assumptions about memory are a major source of C bugs. Later sections focus on the stack and the heap.

## Stack and Heap

### Stack

### Heap and Dynamic Memory Allocation

---
date: 2026-07-15 18:32:36
title: Number Representation
permalink: num-repr
publish: true
tags:
  - 计算机系统与体系结构
  - CS61C
---

# Number Representation

> [L02 Number Representation | CS 61C Course Notes](https://notes.cs61c.org/content/number-rep/)

<div class="responsive-video-container">
    <iframe src="https://player.bilibili.com/player.html?isOutside=true&aid=1806497713&bvid=BV17b42177VG&cid=1621699328&p=2&autoplay=0"
    scrolling="no" 
    border="0" 
    frameborder="no" 
    framespacing="0" 
    allowfullscreen="true"> 
    </iframe>
</div>

!!! abstract "Learning Outcomes"
    - Know the terms: bits, bytes, bitstrings

    - Compute how many bits you need to represent $k$ items.

## Introduction

### Digital Data

- *Analog data*(**模拟数据**): values are *continuous* and can take on any value within a range.

- *Digital data*(**数字数据**): values are *discrete* and can take on only a finite number of values.

Conver analog data to digital data:

![](assets/num-repr/1.png)

1. *Sample* (**采样**): We **ask the signal at every time step**: “What’s your value?” This usually occurs at a **regular interval**.

    For example, for music on CDs, that’s 44,100 times a second we’re asking it what its height is.

2. *Quantize* (**量化**): Because the height might come out at some fractional number, we need to **divide it up in its amplitude using a “yardstick.”**
   
    We divide it up into a 16-bit number, which is $2^16 = 65536$ possible tick marks. Then, the sample “snaps” to the closest tick mark.

### Bits, Bytes and Nibbles

- *Bits* (**位**): A binary digit, the smallest unit of digital data. Only takes on the two *discrete* values (usually 0 and 1).

- *Bytes* (**字节**): A *bitstring* of 8 bits. A byte can represent $2^8 = 256$ things.

- *Nibbles* (**半字节**): A *bitstring* of 4 bits. A nibble can represent $2^4 = 16$ things. This is equivalent to one hexadecimal digit.

### Bits can represent anything

The big idea: *Bits can represent anything*.

- Logical Values: Commonly, 0 means false and 1 means true.

- Characters: 

    - [ASCII](https://en.wikipedia.org/wiki/ASCII): an expanded 8-bit representation that can represent uppercase, lowercase, and punctuation as used in standard American English.

    - [Unicode](https://home.unicode.org/): represents all the world’s symbols and languages, including emojis. There are [8-bit](https://en.wikipedia.org/wiki/UTF-8), [16-bit](https://en.wikipedia.org/wiki/UTF-16), and [32-bit](https://en.wikipedia.org/wiki/UTF-32) versions of Unicode.

- Colors: HTML color codes are 24-bit (3-byte) representations.

- And so on...

Anything you can itemize, you can digitize. With $N$ bits, you can represent at most $2^N$ things. Put another way, you can represent $k$ things in at minimum $N$ bits, where $N = \lceil \log_2 k \rceil$.

!!! tip "How many bits do you need to represent $\pi$?"
    We use bits to represent **sets of things**, not just a single thing. All answers are possible, depending on how many things beyond $\pi$ you are looking to represent.

    To use 1 bit, consider representing the two things:

    - $\pi$

    - not $\pi$

## Binary, Decimal, Hex

> [数制与编码 - 进制计数制及其相互转换](../408/数制与编码.md#进制计数制及其相互转换)

## Integer Representations

How can we use $N$ bits to represent a set of integers? There are many systems, and not all of them can represent $2^N$ unique integers with $N$ bits. We focus on two kinds:

- *Signed integers* (**有符号整数**): positive integers, negative integers, and zero.

- *Unsigned integers* (**无符号整数**): non-negative integers (i.e. zero and positive).

### N-bit Unsigned Integer Representation

The simplest scheme: **just treat the bitstring as a plain base-2 number and convert**. With $N$ bits we can represent $2^N$ unsigned integers.

- `0b0...0` ($N$ zeros) represents $0$.

- `0b1...1` ($N$ ones) represents $2^N - 1$ (the largest value — *not* $2^N$, because we start counting from $0$).

- Everything else: assume the bitstring is the base-2 representation of a number, and convert.

So the representable range is $[0,\ 2^N - 1]$.

!!! info "Unsigned integers in C"
    C supports this representation. Built-in types like `unsigned int` are ambiguous because the standard doesn't fix the **width** of an `int`. The header `inttypes.h` provides fixed-width typedefs — `uint8_t`, `uint16_t`, `uint32_t`, etc. — to specify 8-bit, 16-bit, 32-bit unsigned integers explicitly.

### Desigin Considerations

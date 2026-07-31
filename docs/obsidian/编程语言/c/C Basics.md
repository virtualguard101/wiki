---
date: 2026-07-16 20:39:03
title: C Basics
permalink: c-basics
publish: true
tags:
  - 编程语言
  - C
  - CS61C
---

# C Basics

<div class="responsive-video-container">
    <iframe src="https://player.bilibili.com/player.html?isOutside=true&aid=1806497713&bvid=BV17b42177VG&cid=1621699383&p=3&autoplay=0" 
    scrolling="no" 
    border="0" 
    frameborder="no" 
    framespacing="0" 
    allowfullscreen="true"> 
    </iframe>
</div>

!!! abstract "Learning Outcomes"
    - Declare and initialize basic variable types in C.

    - Use `stdint.h` typedefs where possible, because widths of basic integer types are processor-dependent.

    - Always remember that uninitialized variables contain garbage.

    - Remember that all values in C can be cast to booleans, and the only false values are `0`, `NULL`, and `false`.

    - Navigate the large laundry list of C topics here, and use the K&R reference to fill in details.

    - Pay special attention to `typedef` and `struct`, which are used to declare and organize more complex data types.

## Variables

### C Basic Types

| Type | Size (`sizeof(type)`) | Range | Description | Example |
|------|------|-------|-------------|---------|
| `int` | 4 bytes | $-2^{31} \sim 2^{31}-1$ | Integer numbers (positive and negative) | `10`, `-5`, `0x2233` |
| `unsigned int` | 4 bytes | $0 \sim 2^{32}-1$ | Unsigned integer numbers | `10u`, `42`, `0xffu` |
| `float` | 4 bytes | About $\pm 3.4 \times 10^{38}$ | Single-precision floating-point number | `3.14f`, `-0.5f` |
| `double` | 8 bytes | About $\pm 1.7 \times 10^{308}$ | Double-precision floating-point number | `3.1415926`, `-2.5` |
| `char` | 1 byte | $-128 \sim 127$ or $0 \sim 255$ | Single character / small integer | `'A'`, `'z'`, `65` |
| `short` | 2 bytes | $-2^{15} \sim 2^{15}-1$ | Short integer | `123`, `-20` |
| `long` | 8 bytes | $-2^{63} \sim 2^{63}-1$ | Long integer | `123456L`, `-99L` |
| `long long` | 8 bytes | $-2^{63} \sim 2^{63}-1$ | Longer integer type | `123456789LL`, `-1LL` |

!!! info
    - The size of `long` may vary across platforms, so the same code can behave differently on 32-bit and 64-bit systems.

    - Whether `char` is signed or unsigned depends on the compiler and target platform; use `signed char` or `unsigned char` when you need to be explicit.

    - `float` and `double` store approximate values, so calculations and equality comparisons can be affected by precision errors.

!!! tip "`inttypes.h` and `stdint.h`"
    In C99 and later, `inttypes.h` or `stdint.h` are recommended for portable integer types. It specifies unsigned and signed types like `uint8_t` and `int32_t`, where **width is specified in bits**. So `int32_t x;` would declare `x` as a 32-bit wide signed integer that uses two's complement representation.

### Variable declaration and initialization

Attention that C variable declarations do not initialize variables to default values. So the program below will cause an error:

```c
#include <stdio.h>
int main(int argc, char *argv[]) {
  int32_t x = 0;
  int32_t y;
    
  printf("before: x=%d, y=%d\n", x, y);
  x++;
  y += x;

  printf(" after: x=%d, y=%d\n", x, y);
  return 0;
}
```

The program just declares `y` as type `int`; it does not initialize `y` to any default value.

Recall that any 32-bit value can be interpreted as a two's complement integer. At compilation time, the compiler recognizes that `y += x;` is a valid operation based on the types of `x` and `y`. At runtime, the program simply takes whatever 32 bits are at `y` and adding the value of `x`, then updating those 32 bits.

### Booleans Type in C

After [C23](https://cppreference.com/c/23), C has a built-in boolean type `bool` with two values. But before that, we need to `#include <stdbool.h>` for definitions of `true` and `false`.

And notice that, values in C are **truthy—meaning**, means every value can be interpreted as true or false.

False values:

  - `0`, i.e., all bits of this value are $0$

  - `NULL`, which is also defined as $0$, but is commonly used for pointers. More later.

  - `false`, if `stdbool.h` is used

Everything else True values.

## C Syntax

### `typedef`

`typedef` used to create an additional name (alias) for another data type (a little bit like [`using` in C++](../cpp/cs106l/基础类型与结构体.md#auto-关键字)).

```c
typedef uint8_t Byte;
Byte b1 = 0x12, b2 = 0x34;
```

!!! note
    Declaring multiple variables within the same value as above is not recommended, it will leads to confusing types when we introduce pointers next time.

### `struct`

> [基础类型与结构体 - 结构体（struct）](../cpp/cs106l/基础类型与结构体.md#结构体struct)

`struct` is used to declare structured groups of variables. A `struct` is an *abstract data* type definition.

### Preprocessor Macros

`#define` is a C Preprocessor (CPP) macro. Before compilation, the preprocessor does **text replacement** based on all `#define` macros. For example:

```c
#define PI (3.14159)
```

replaces every `PI` with `(3.14159)`, so `PI` behaves like a “constant.”

Macros are also often used to create small “functions,” but they are **not** real functions—only text substitution:

```c
#define min(X, Y) ((X) < (Y) ? (X) : (Y))
next = min(w, foo(z));
```

is expanded to:

```c
next = ((w) < (foo(z)) ? (w) : (foo(z)));
```

!!! warning
    If `foo(z)` has a side effect (e.g. modifies a variable), that side effect may run **twice**. Prefer real functions when side effects matter.

### Constants and Enums

`const` declares a typed constant: assign once, then the value cannot change during execution.

```c
const float  golden_ratio = 1.618;
const int    days_in_week = 7;
const double the_law      = 2.99792458e8;
```

An `enum` groups related integer constants:

```c
enum cardsuit { CLUBS, DIAMONDS, HEARTS, SPADES };
enum color { RED, GREEN, BLUE };
```

By default, the first name is `0`, then `1`, `2`, and so on. Prefer using the names (`RED`, `GREEN`, …) instead of hard-coding their integer values.

### Control Flow

Control flow in C is similar to Java. A few details worth remembering:

- **Curly braces:** Bodies of `if`/`else` and loops may use braces or a single statement. Prefer braces for clarity.

- **`while` and `do-while`:**

    ```c
    while (condition) {
      /* ... */
    }

    do {
      /* ... */
    } while (condition);
    ```

    `do-while` runs the body **at least once**, then checks the condition.

- **`switch`:** Execution falls through into later `case`s until a `break` (or the end of the `switch`):

    ```c
    switch (x) {
      case 1:
        printf("one\n");
        break;
      case 2:
        printf("two\n");
        break;
      default:
        printf("other\n");
    }
    ```

!!! note
    Avoid `do-while` and `goto` in everyday C. Both ideas become useful later when studying assembly control flow.

### Functions

Every function must declare its return type and parameter types:

```c
int number_of_people(int class1, int class2) {
  return class1 + class2;
}

float dollars_and_cents(float cost) {
  return cost;
}

void say_hi(void) {
  printf("hi\n");
}
```

- Return type sits to the left of the function name; use `void` when nothing is returned.

- Parameters must also be typed.

- Variables and functions must be **declared before use**. In practice, put prototypes (or implementations) near the top of the file, or share them via header files.

!!! tip "Header files"
    Header files (`.h`) let you share function declarations and macros across multiple `.c` source files. See the [GCC Header Files docs](https://gcc.gnu.org/onlinedocs/cpp/Header-Files.html) for details.

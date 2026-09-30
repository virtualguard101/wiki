---
date: 2026-09-30 23:55:00
title: C Odds And Ends
permalink: odds-and-ends
publish: true
tags:
  - 编程语言
  - C
  - CS61C
---

# C Odds And Ends

> [L06 C Odds and Ends | CS61C: Course Notes](https://notes.cs61c.org/content/c-odds-and-ends/)

!!! abstract
    - Use bitwise operators and bitmasks (details in the Chinese bitwise note).

    - Distinguish little-endian vs big-endian layouts, and why struct padding appears.

    - Build a heap-backed linked list of strings, including why `add_to_front` takes `node_t **`.

    - Separate a small C library into an opaque `.h` API and a `.c` implementation.

This lecture unit bundles leftovers after pointers and memory: bit tricks, how multi-byte values sit in RAM, and a first “real” data structure that ties `struct`, `malloc`, and double pointers together.

## Bitwise Operations

> [位运算和其他运算符](位运算和其他运算符.md).

Operators `&`, `|`, `^`, `~`, `<<`, `>>` work **bit by bit**. Do not confuse them with logical `&&`, `||`, `!`.

Useful single-bit identities (`x` is 0 or 1):

| Op | With 0 | With 1 |
|:---|:-------|:-------|
| `&` | clear → 0 | keep `x` |
| `\|` | keep `x` | set → 1 |
| `^` | keep `x` | flip `x` |

Bitmasks update packed flags or extract bytes, e.g. `N & 0xFF` for the least significant byte of a 32-bit word.

## Words, Endianness, Alignment

### Word Size and Pointers

> [三种常见数据模型 | 数据类型详解](数据类型详解.md#三种常见数据模型)

A **hardware word** is the natural access unit of the machine. Rough CS61C intuition:

| Architecture | Word | Typical `sizeof` of any object pointer |
|:-------------|:----:|:--------------------------------------:|
| 32-bit | 4 bytes | 4 |
| 64-bit | 8 bytes | 8 |

Pointer width tracks the address space.

### Endianness

When a value spans several bytes, **endianness** chooses which byte sits at the **lowest** address:

- **Little endian**: least significant byte first (almost all modern desktops / servers).

- **Big endian**: most significant byte first (still common on some networks / protocols).

E.g., `uint32_t x = 0x12345678` starting at address `0x1000`.

| Endian | `0x1000` | `0x1001` | `0x1002` | `0x1003` |
|:-------|:--------:|:--------:|:--------:|:--------:|
| Little | `0x78` | `0x56` | `0x34` | `0x12` |
| Big | `0x12` | `0x34` | `0x56` | `0x78` |

The **address of `x`** is still the lowest byte address in either case. Endianness only reorders the payload bytes.

### Alignment and Struct Padding

Many CPUs load words fastest when the address is a multiple of the word size (**alignment**). Compilers often insert **padding** between `struct` members (and at the end) so each field stays naturally aligned.

```c
struct foo {
    int32_t a;       /* 4 bytes */
    char b;          /* 1 byte + often 3 bytes of padding on 32-bit */
    struct foo *c;   /* 4 bytes on ILP32, 8 on LP64 */
};
```

On a typical 32-bit ABI, `sizeof(struct foo)` is often **12**, not 4+1+4 = 9. Exact layout is implementation-defined — measure with `sizeof` / `offsetof` / `gdb` rather than guessing. Reordering fields can shrink padding; packing attributes trade size for slower or unaligned access.

## Linked List

Recursive node type (incomplete type + pointer, same idea as [指针详解](指针详解.md#不完全类型与复杂声明)):

```c
typedef struct _node node_t;
struct _node {
    char *data;
    node_t *next;
};
```

`main` holds a `node_t *head`. Updating that pointer from a callee requires its **address** (`node_t **`), because C is pass-by-value:

```c
void add_to_front(node_t **head_ptr, char *data)
{
    node_t *node = malloc(sizeof(node_t));
    node->data = malloc(strlen(data) + 1);  /* room for '\0' */
    strcpy(node->data, data);               /* copy; do not alias a string literal */
    node->next = *head_ptr;
    *head_ptr = node;
}

int main(void)
{
    node_t *head = NULL;
    add_to_front(&head, "abc");
    /* ... free every data string, then every node ... */
}
```

Why copy the string onto the heap?

Ownership stays with the node: the list can free `data` later without dangling into a caller’s buffer or a read-only literal.

!!! review
    - String / `NULL` rules kept in note [C Strings](C-Pointers-Arrays-and-Strings.md#C-Strings)
    
    - Heap discipline kept in note [C Memory Management](C-Memory-Management.md#Heap)

Step summary of `add_to_front`:

1. `malloc` a `node_t`.

2. `malloc(strlen(data) + 1)` and `strcpy` into `node->data`.

3. `node->next = *head_ptr` (link to the old head).

4. `*head_ptr = node` (publish the new head back to `main`).

## Linked List as a Small Library

Hide the node layout behind an **opaque** list type. Header declares only what clients need:

```c
/* linkedlist.h */
#ifndef LINKEDLIST_H
#define LINKEDLIST_H

typedef struct _node node_t;              /* incomplete for clients */
typedef struct _linked_list linked_list_t;

linked_list_t *list_create(void);
void list_add_front(linked_list_t *list, const char *data);
void list_print(const linked_list_t *list);
void list_free(linked_list_t *list);

#endif
```

Implementation owns the real layouts. Because `list` is a pointer to a heap object that contains `head`, `list_add_front` can update `list->head` with a **single** pointer parameter — no `node_t **` at the API boundary:

```c
/* linkedlist.c (sketch) */
struct _node {
    char *data;
    node_t *next;
};

struct _linked_list {
    node_t *head;
};

void list_add_front(linked_list_t *list, const char *data)
{
    node_t *node = malloc(sizeof(node_t));
    node->data = malloc(strlen(data) + 1);
    strcpy(node->data, data);
    node->next = list->head;
    list->head = node;
}

void list_free(linked_list_t *list)
{
    node_t *current = list->head;
    while (current) {
        node_t *next = current->next;
        free(current->data);  /* free payload before the node */
        free(current);
        current = next;
    }
    free(list);
}
```

Clients `#include "linkedlist.h"` only — never `#include` the `.c`. Include guards and opaque structs keep the global namespace clean; naming helpers with a `list_` prefix does the same.

!!! review
    - `struct` / `typedef` basics: [C Basics](C-Basics.md)
    
    - Preprocessor include guards: [预处理](预处理.md).


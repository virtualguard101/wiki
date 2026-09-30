---
date: 2026-10-01 00:05:00
title: C Generics And Function Pointers
permalink: generics-func-ptr
publish: true
tags:
  - 编程语言
  - C
  - CS61C
---

# C Generics And Function Pointers

> [L05 C Generics and Function Pointers | CS61C: Course Notes](https://notes.cs61c.org/content/c-generics/)
>
> [qsort | cppreference](https://en.cppreference.com/w/c/algorithm/qsort.html)
>
> [memcpy | cppreference](https://en.cppreference.com/w/c/string/byte/memcpy.html)

!!! abstract
    - Identify generic functions used in heap memory management (`malloc`, `free`, `realloc`).

    - Understand why `void *` cannot be dereferenced, and use `memcpy` / `memmove` instead.

    - Write byte-oriented pointer arithmetic with an explicit `(char *)` cast.

    - Declare, initialize, and call through function pointers; use them for higher-order helpers such as map / sort.

## Why Generics

A typed pointer (`int *`) fixes both **stride** (pointer arithmetic) and **width** (how many bytes a dereference reads). That is great for safety, but it forces one near-identical helper per type (`swap_int`, `swap_short`, `swap_string`, …).

C’s “generics” for this course means: operate on **raw memory blocks** through `void *`, and pass enough size information that the callee can copy / walk bytes without knowing the element type. Goals:

1. One function works for many argument types.

2. Access is by bytes in memory, not by a fixed C type.

You already use generics in `<stdlib.h>`:

```c
void *malloc(size_t n);
void free(void *ptr);
void *realloc(void *ptr, size_t size);
```

Cast the result to a typed pointer only when you are ready to interpret those bytes as a concrete type.

## Typed Swaps

Same logic, different types:

```c
void swap_int(int *p1, int *p2)
{
    int temp = *p1;
    *p1 = *p2;
    *p2 = temp;
}

void swap_string(char **p1, char **p2)
{
    char *temp = *p1;
    *p1 = *p2;
    *p2 = temp;
}
```

`swap_string` swaps two **pointers** (addresses of C strings), so the parameter type is `char **`, which is a [Double Pointers](C-Pointers-Arrays-and-Strings.md#Double-Pointers).

## Do not Dereference `void *`

This does not compile:

```c
void swap_faulty(void *p1, void *p2)
{
    void temp = *p1;  /* error: cannot declare void object; cannot deref void * */
    *p1 = *p2;
    *p2 = temp;
}
```

Dereference needs a known width at compile time. `void *` only stores an address; it does not name an object type.

Contrast: `void **` **is** typed — it points to a `void *`, and every pointer has a known size — so `*double_ptr` (yielding a `void *` value) is fine. That is still not “dereference the thing the `void *` points at.”

## Generic Swap with `memcpy`

Copy `n` bytes with `<string.h>`:

```c
void *memcpy(void *dest, const void *src, size_t n);
void *memmove(void *dest, const void *src, size_t n);
```

Prefer `memcpy` when regions do not overlap; use `memmove` when they might. A working generic swap needs an explicit size:

```c
void swap(void *p1, void *p2, size_t nbytes)
{
    char temp[nbytes];           /* VLA: nbytes bytes of scratch */
    memcpy(temp, p1, nbytes);
    memcpy(p1, p2, nbytes);
    memcpy(p2, temp, nbytes);
}

int a = 22, b = 61;
swap(&a, &b, sizeof(a));
```

`char` has `sizeof` 1, so `char temp[nbytes]` is a convenient untyped buffer. Overlapping `p1` / `p2` regions are outside this API’s contract (same assumption as `memcpy`).

!!! warning
    Byte-oriented code can silently “Frankenstein” unrelated objects if `nbytes` or pointer arithmetic is wrong. Generics trade type checking for flexibility — keep sizes and alignment honest.

## Walking a Generic Array

To swap the first and last elements of an array of unknown element type:

```c
void swap_ends(void *arr, size_t nelems, size_t nbytes)
{
    swap(arr, (char *)arr + (nelems - 1) * nbytes, nbytes);
}
```

Standard C does **not** define arithmetic on `void *`. Cast to `char *` first so `+` advances by bytes. (GNU C lets you add on `void *` as if it were `char *`; do not rely on that for portable code.)

```c
int32_t arr[] = {1, 2, 3, 4, 5};
size_t n = sizeof(arr) / sizeof(arr[0]);
swap_ends(arr, n, sizeof(arr[0]));
```

## Function Pointers

A *function pointer*([函数指针](指针详解.md#函数指针)) stores an **entry address** (usually in the text segment).

```c
int (*fn)(void *, void *) = &foo;
(*fn)(x, y);   /* call through pointer; fn(x, y) is also valid */
```

`&foo` and `*fn` are optional for functions (the name decays to a pointer), but writing them makes intent clearer.

### Map as a Higher-Order Helper

```c
void mutate_map(int arr[], int n, int (*fp)(int))
{
    for (int i = 0; i < n; i++)
        arr[i] = (*fp)(arr[i]);
}

int multiply2(int x) { return 2 * x; }
int multiply10(int x) { return 10 * x; }

int arr[] = {3, 1, 4};
int n = (int)(sizeof(arr) / sizeof(arr[0]));
mutate_map(arr, n, &multiply2);   /* 6 2 8 */
mutate_map(arr, n, &multiply10);  /* 60 20 80 */
```

The callee decides which transformation to apply by which function pointer you pass.

### Library Pattern: `qsort`

`qsort` combines both ideas: a `void *` array plus a comparator function pointer:

```c
int cmp_int(const void *a, const void *b)
{
    int x = *(const int *)a;
    int y = *(const int *)b;
    return (x > y) - (x < y);
}

int vals[] = {3, 1, 4, 1, 5};
qsort(vals, 5, sizeof(vals[0]), cmp_int);
```

The comparator receives pointers to **elements**, casts them to the real type, and returns negative / zero / positive.

## Convention Checklist

| Do | Do not |
|:---|:-------|
| Pass `sizeof` (or element count × element size) into generics | Assume the callee can recover array length from a decayed pointer |
| Use `memcpy` / `memmove` on `void *` | Write `*p` when `p` is `void *` |
| Cast to `char *` before byte arithmetic | Rely on GNU `void *` arithmetic for portability |
| Keep function-pointer types matching the callee | Forget that string literals passed as `char *` are still read-only |

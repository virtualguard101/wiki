---
date: 2026-07-17 17:06:46
title: Floating Point
permalink: float
publish: true
tags:
  - 计算机系统与体系结构
  - CS61C
---

# Floating Point

> [L08 Floating Point | CS61C Course Notes](https://notes.cs61c.org/content/floating-point/)

<div class="responsive-video-container">
    <iframe src="https://player.bilibili.com/player.html?isOutside=true&aid=1806497713&bvid=BV17b42177VG&cid=1621699865&p=6&autoplay=0" 
    scrolling="no" 
    border="0" 
    frameborder="no" 
    framespacing="0" 
    allowfullscreen="true"> 
    </iframe>
</div>

!!! abstract "Learning Outcomes"
    - Understand the limits of a “fixed point” representation of numbers with fractional components.

    - Compute range and step size for integer and fixed-point representations.

    - Identify limitations of fixed-point representations.

    - Understand how the normalized number representation in the IEEE 754 single-precision floating point standard is inspired by scientific notation.

    - Identify how the [IEEE 754](../408/浮点数表示与运算.md#IEEE-754标准) single-precision floating point format uses three fields:

        - The sign bit represents sign

        - The exponent field represents the exponent value.

        - The significand field represents the fractional part of the mantissa value.

    - For [normalized numbers](#Normalized-Numbers):

        - The exponent field represents the exponent value as a bias-encoded number

        - The mantissa always has an implicit, leading one.

## Fixed Point

To represent numbers with fractional parts in 32 bits (e.g. `4.25`, `5.17`), start with a strawman: **fixed point** — the binary point’s position is **fixed**.

### Metrics: Range and Step Size

Two metrics for any number system:

| Metric | Meaning |
|--------|---------|
| **Range** | Smallest / largest representable value |
| **Step size** | Spacing between consecutive representable values (precision) |

For integer systems, step size is always 1:

| System | # bits | Min | Max | Step |
|--------|--------|-----|-----|------|
| Unsigned | 32 | $0$ | $2^{32}-1$ | 1 |
| Two’s complement | 32 | $-2^{31}$ | $2^{31}-1$ | 1 |

With fractions, infinitely many reals lie between consecutive values, so **step size becomes a key measure of precision**.

### Binary Point

Left of a decimal point: $10^0, 10^1, \ldots$; right: $10^{-1}, 10^{-2}, \ldots$.  
A **binary point** works the same way: left $2^0, 2^1, \ldots$; right $2^{-1}, 2^{-2}, \ldots$.

Fixed point = a fixed-width bit string with a **pre-agreed** binary-point position.

Example: 6-bit unsigned fixed point, binary point 4 bits from the right (2 integer bits + 4 fractional bits):

```text
  1 0 . 1 0 1 0
  ↑ ↑   ↑ ↑ ↑ ↑
  2¹ 2⁰  2⁻¹ … 2⁻⁴
```

$2.625$ encodes as `101010`:

$$
1\cdot 2^1 + 0\cdot 2^0 + 1\cdot 2^{-1} + 0\cdot 2^{-2} + 1\cdot 2^{-3} + 0\cdot 2^{-4}
= 2 + 0.5 + 0.125 = 2.625
$$

#### Range & Step Size

| | Value |
|--|-------|
| Min | `000000` → $0$ |
| Max | `111111` → $4 - 2^{-4} = 3.9375$ |
| Step size | LSB = $2^{-4} = 1/16$ |

### Arithmetic

- **Addition**: align binary points, then reuse an integer adder (e.g. $1.5 + 0.5 = 2$).
- **Multiplication**: must **shift** the binary point by the number of fractional digits (e.g. $1.5 \times 0.5 = 0.75$) — more awkward than addition.

### Use Cases & Limits

Fixed point is still useful when the value range is known and fast arithmetic matters (e.g. some graphics rendering).

Once the binary point is fixed, you are stuck: the 6-bit example cannot represent numbers much larger than $3.94$, nor nonzero values between $0$ and $1/16$.

Scientific apps often need all of:

- Very large: seconds in a millennium $\approx 3.16\times 10^{10}$

- Very small: Bohr radius $\approx 5.29\times 10^{-11}\,\mathrm{m}$

- Mixed integer + fraction: e.g. $2.625$

Covering all three with fixed point needs **≥ 92 bits** (~34 integer + ~58 fractional), far beyond a typical 32-bit integer width.

It means that we need a representation that can **move** the binary point with the magnitude — **floating point**, inspired by [scientific notation](https://en.wikipedia.org/wiki/Scientific_notation).

## Normalized Numbers

Floating point does **not** fix one binary-point location for all numbers. For each value, it stores *what the significant bits are* and *which power of two they sit at* — the same idea as scientific notation.

### Inspirations about Scientific Notation

Take decimal $0.1640625$. Its binary is roughly $\dots000000.001010100000\dots$: long runs of zeros, with only a short “energetic” stretch of bits (`10101`). Scientific notation keeps that energy and records the scale separately.

**Base-10 scientific notation** for the same value: $1.640625 \times 10^{-1}$.

| Term | Meaning | In the example |
|------|---------|----------------|
| **Radix** | Base | $10$ |
| **Mantissa** | Significant figures (“energy”) | $1.640625$ |
| **Exponent** | Power of the radix | $-1$ |

**Normalized form**: exactly **one non-zero digit** left of the point. For a given significant-figure budget, that form is unique (e.g. $1.0\times 10^{-9}$, not $0.1\times 10^{-8}$ or $10\times 10^{-10}$).

### Binary Normalized Form

Same idea in binary: $0.1640625 = 1.0101_{\text{two}} \times 2^{-3}$.

| Term | Binary |
|------|--------|
| Radix | $2$ |
| Mantissa | $1.0101$ |
| Exponent | $-3$ |

Two consequences for a 32-bit float design:

1. Split the bits into at least **mantissa** and **exponent** fields.

2. In binary, the only non-zero digit is `1`, so a normalized mantissa is always `1.xyz...` — the leading `1` is **redundant**.

!!! tip "Normalize by shifting"
    $0.1101_{\text{two}} \times 2^{2}$ is *not* normalized; scale to $1.101_{\text{two}} \times 2^{1}$.

### IEEE 754 Single-Precision Floating Point and Normalized Numbers

!!! abstract
    In simply, Floating Point just introduces some new fields that contains informations about *how to move the binary point with the magnitude*($\text{Exponent}$ with $\text{Bias}$) and the $\text{significand}$ field that *contains the energy(significant figures, 有效位) of fractional part*.

IEEE 754 single precision is C’s `float` (32 bits). UC Berkeley’s William Kahan led the standard (Turing Award, 1988) so machines would agree on floating-point results.

Two useful notions:

| Term | Meaning |
|------|---------|
| **Precision** | How many bits represent a value |
| **Accuracy** | How close the representation is to the true number |

Layout (MSB = bit 31, LSB = bit 0):

![](assets/float/1.png)

| Field | Width | Role |
|-------|-------|------|
| `s` | 1 bit | Sign |
| `exponent` | 8 bits | Biased exponent |
| `significand` | 23 bits | Fraction of the mantissa |

Normalized numbers (when `exponent` $\in [1, 254]$, i.e. not all-0 / all-1) decode as:

$$
(-1)^{s} \times (1 + \text{significand}) \times 2^{\text{exponent} - \text{bias}}
$$

with $\text{bias} = 127$ for single precision.

How each field is interpreted (none of the three fields use two’s complement):

| Field | Represents | How to read (normalized) |
|-------|------------|--------------------------|
| `s` | Sign | `1` → negative; `0` → positive |
| `exponent` | [Bias-encoded](Number%20Representation.md#Bias-Encoding) exponent | True exponent $= \text{stored} - 127$ |
| `significand` | Fractional part of mantissa | Treat as $0.xx\ldots xx$ (23 bits), then add the implicit $1$ |

#### Design Principles

The three fields are shaped to **squeeze more accurate normalized values into 32 bits**, not to look like integer encodings.

!!! info "Why bias-encoded exponents (not two’s complement)?"
    Early systems needed floats to work even without a floating-point unit — e.g. **sort same-sign floats with ordinary integer compares**.

    For that, a larger `exponent` field must mean a larger magnitude. With two’s complement, negative exponents would start with `1` and look *larger* under unsigned/integer comparison. With bias:

    - smaller stored values → smaller true exponents

    - larger stored values → larger true exponents

    - same-sign float bit patterns order like unsigned integers

    For normalized numbers, stored exponents `00000001`…`11111110` map to true exponents $-126$…$+127$.

!!! info "Why store significand + implicit 1, not the full mantissa?"
    Binary normalized form always has a leading `1`. IEEE 754 **does not store** that bit; the 23-bit significand is only the bits *after* the binary point, and you reconstruct:

    $$
    \text{mantissa} = 1 + \text{significand},\quad 0 \le \text{significand} < 1
    $$

    That buys an **extra bit of precision**: 24-bit normalized mantissas using only 23 stored bits.

!!! note "Specials reserved"
    Exponent all-0 and all-1 encode zero, denormals, $\pm\infty$, NaN — covered under [Special Numbers](#Special-Numbers). The formulas above apply only to the normalized range.

### Double Precision

C’s `double` is IEEE 754 double precision (64 bits): 1 sign + 11-bit exponent (bias $1023$) + 52-bit significand. Larger significand → better accuracy; range roughly $2.0\times 10^{-308}$ to $2.0\times 10^{308}$.

!!! tip "Handy converter"
    The web app: [IEEE-754 Floating Point Converter](https://www.h-schmidt.net/FloatConverter/IEEE754.html), for converting between decimal numbers and their IEEE 754 single-precision floating point format.

## Special Numbers

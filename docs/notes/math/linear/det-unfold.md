---
date: 2025-11-20 15:40:15
title: 行列式展开
permalink: 
publish: true
---

# 行列式展开

## 定义

在学[三阶行列式展开](det.md#三阶行列式)时，有提到“逐层展开”的概念。

$$
D = a_{i1}A_{i1} + a_{i2}A_{i2} + \cdots + a_{in}A_{in}
$$

其中 $A_{ij}$ 为元素 $a_{ij}$ 的**代数余子式**:

$$
A_{ij} = (-1)^{i + j} \begin{vmatrix}
    a_{11} & \cdots & a_{1,j-1} & a_{1,j+1} & \cdots & a_{1n} \\
    \vdots & \ddots & \vdots & \vdots & \ddots & \vdots \\
    a_{i-1,1} & \cdots & a_{i-1,j-1} & a_{i-1,j+1} & \cdots & a_{i-1,n} \\
    a_{i+1,1} & \cdots & a_{i+1,j-1} & a_{i+1,j+1} & \cdots & a_{i+1,n} \\
    \vdots & \ddots & \vdots & \vdots & \ddots & \vdots \\
    a_{n1} & \cdots & a_{n,j-1} & a_{n,j+1} & \cdots & a_{nn}
\end{vmatrix}
$$

简记为:

$$
A_{ij} = (-1)^{i + j} M_{ij}
$$

$M_{ij}$ 为元素 $a_{ij}$ 的**余子式**。

上面提到的是**按行展开**，按列展开同理。

## 部分定理

- 某行（列）的元素与另一行（列）的对应元素的代数余子式乘积之和为 $0$

    $$
    \sum_{j = 1}^{n} a_{ij}A_{kj} = 0 \quad (i \not ={k})
    $$

    !!! example
        $D = \begin{vmatrix}
        3 & -5 & 2 & 1 \\
        1 & 1 & 0 & -5 \\
        -1 & 3 & 1 & 3 \\
        2 & -4 & -1 & -3
        \end{vmatrix}$，求 $3A_{31} - 5A_{32} + 2A_{33} + A_{34}$

        - 解:

            $$
            原式 = 0
            $$

- 求某一行代数余子式之和，相当于求将该行的元素全部替换成 $1$ 的行列式的值

    !!!example
        $D = \begin{vmatrix}
        3 & -5 & 2 & 1 \\
        1 & 1 & 0 & -5 \\
        -1 & 3 & 1 & 3 \\
        2 & -4 & -1 & -3
        \end{vmatrix}$，求 $A_{11} + A_{12} + A_{13} + A_{14}$

        - 解:

            $$
            \begin{align}
                原式 &= 1 \times A_{11} + 1 \times A_{12} + 1 \times A_{13} + 1 \times A_{14} \\
                &= \begin{vmatrix}
                    1 & 1 & 1 & 1 \\
                    1 & 1 & 0 & -5 \\
                    -1 & 3 & 1 & 3 \\
                    2 & -4 & -1 & -3
                \end{vmatrix} = -2 \begin{vmatrix}
                    1 & 1 & 1 & 1 \\
                    0 & 2 & 1 & 2 \\
                    0 & 0 & -1 & -6 \\
                    0 & 0 & 0 & 1
                \end{vmatrix} \\
                &= -2 \times 1 \times 2 \times -1 \times 1 = 4
            \end{align}
            $$

## 范德蒙德行列式

$$
\begin{align}
D = \begin{vmatrix}
    1 & 1 & \cdots & 1 \\
    x_1 & x_2 & \cdots & x_n \\
    x_1^2 & x_2^2 & \cdots & x_n^2 \\
    \vdots & \vdots & \ddots & \vdots \\
    x_1^{n-1} & x_2^{n-1} & \cdots & x_n^{n-1} \\
\end{vmatrix} = \prod_{1 \leq j < i \leq n} (x_i - x_j)
\end{align}
$$

!!! example
    $D = \begin{vmatrix}
    1 & 1 & 1 & 1 \\
    1 & 2 & 3 & 4 \\
    1 & 4 & 9 & 16 \\
    1 & 8 & 27 & 64 \\
    \end{vmatrix} = (4 - 3)(4 - 2)(4 - 1)(3 - 2)(3 - 1)(2 - 1) = 12$

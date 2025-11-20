---
date: 2025-11-20 23:25:02
title: 线性方程组
permalink: 
publish: true
---

# 线性方程组

## 齐次线性方程组

### 定义

形如下式的线性方程组称为**齐次线性方程组**:

$$
\begin{cases}
a_{11}x_1 + a_{12}x_2 + \cdots + a_{1n}x_n = 0 \\
a_{21}x_1 + a_{22}x_2 + \cdots + a_{2n}x_n = 0 \\
\quad \quad \quad \quad \quad \quad \quad \vdots \\
a_{n1}x_1 + a_{n2}x_2 + \cdots + a_{nn}x_n = 0
\end{cases}
$$

可简记作 $Ax = 0$。使用矩阵表示可记为:

$$
A = \begin{pmatrix}
a_{11} & a_{12} & \cdots & a_{1n} \\
a_{21} & a_{22} & \cdots & a_{2n} \\
\vdots & \vdots & \ddots & \vdots \\
a_{n1} & a_{n2} & \cdots & a_{nn}
\end{pmatrix}, \quad x = \begin{pmatrix}
x_1 \\
x_2 \\
\vdots \\
x_n
\end{pmatrix}
$$

### 解齐次线性方程组

解一个齐次线性方程组，通常可分为三个步骤:

1. 判断方程组是否有非零解

2. 求解向量 $\mathbb{x} = (x_1, x_2, \cdots, x_n)^T$

3. 表示通解

!!! example
    求解齐次线性方程组的通解: $\begin{cases}
        3x_1 - 6x_2 - 4x_3 + x_4 = 0 \\
        x_1 - 2x_2 + 2x_3 - x_4 = 0 \\
        2x_1 - 4x_2 - 6x_3 + 2x_4 = 0 \\
        x_1 - 2x_2 + 7x_3 - 3x_4 = 0
    \end{cases}$

    - 解:

        依题可得线性方程组的系数矩阵为 $A = \begin{pmatrix}
            3 & -6 & -4 & 1 \\
            1 & -2 & 2 & -1 \\
            2 & -4 & -6 & 2 \\
            1 & -2 & 7 & -3
        \end{pmatrix}$

        对 $A$ 进行初等行变换, 化简至行最简形矩阵:

        $$
        \begin{pmatrix}
            1 & -2 & 0 & -\frac{1}{5} \\
            0 & 0 & 1 & -\frac{2}{5} \\
            0 & 0 & 0 & 0 \\
            0 & 0 & 0 & 0
        \end{pmatrix}
        $$

        可得 $R(A) = 2 < 4$，故方程组有无穷多解，且基础解系含 $4 - 2 = 2$ 个线性无关的解向量:

        $$
        \begin{cases}
            x_1 - 2x_2 - \frac{1}{5}x_4 = 0 \\
            x_3 - \frac{2}{5}x_4 = 0 \\
        \end{cases} \Rightarrow \begin{cases}
            x_1 = 2x_2 + \frac{1}{5}x_4 \\
            x_3 = \frac{2}{5}x_4 \\
        \end{cases}
        $$

        令 $x_2 = 1, x_4 = 0$，可得 $x_1 = 2, x_3 = 0$，故 $\alpha_1 = (2, 1, 0, 0)^T$

        令 $x_2 = 0, x_4 = 1$，可得 $x_1 = \frac{1}{5}, x_3 = \frac{2}{5}$，故 $\alpha_2 = (\frac{1}{5}, 0, \frac{2}{5}, 1)^T$

        故方程组的通解为:

        $$
        x = k_1 \alpha_1 + k_2 \alpha_2 = k_1 (2, 1, 0, 0)^T + k_2 (\frac{1}{5}, 0, \frac{2}{5}, 1)^T
        $$

        !!! tip
            - 基础解系中，$x_n$ 的系数与系数矩阵的行最简行矩阵的每行元素一一对应

            - 最终要表示的 $x_n$ 是首非零元所在列的向量（这里是 $x_1$ 和 $x_3$），其余的变量（这里是 $x_2$ 和 $x_4$）称为**自由变量**

            - 自由变量可以取任意值，但不能全为 $0$

            - 不同的解向量**线性无关**，因此自由变量通常取 $1$ 和 $0$ 的组合，即形如**单位向量**的形式

## 非齐次线性方程组

---
date: 2025-11-22 15:45:02
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

    系数矩阵的秩 $R(A)$ 与未知量个数 $n$ 的关系决定了方程组是否有非零解：
    
    - 若 $R(A) = n$，则方程组只有零解

    - 若 $R(A) < n$，则方程组有无穷多解

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
        x = k_1 \alpha_1 + k_2 \alpha_2 = k_1 (2, 1, 0, 0)^T + k_2 (\frac{1}{5}, 0, \frac{2}{5}, 1)^T \quad k_1, k_2 \in \mathbb{R}
        $$

        !!! tip
            - 基础解系中，$x_n$ 的系数与系数矩阵的行最简行矩阵的每行元素一一对应

            - 最终要表示的 $x_n$ 是首非零元所在列的向量（这里是 $x_1$ 和 $x_3$），其余的变量（这里是 $x_2$ 和 $x_4$）称为**自由变量**

            - 自由变量可以取任意值，但不能全为 $0$

            - 不同的解向量**线性无关**，因此自由变量通常取 $1$ 和 $0$ 的组合，即形如**单位向量**的形式

## 非齐次线性方程组

### 定义

形如下式的线性方程组称为**非齐次线性方程组**:

$$
\begin{cases}
a_{11}x_1 + a_{12}x_2 + \cdots + a_{1n}x_n = b_1 \\
a_{21}x_1 + a_{22}x_2 + \cdots + a_{2n}x_n = b_2 \\
\quad \quad \quad \quad \quad \quad \quad \vdots \\
a_{n1}x_1 + a_{n2}x_2 + \cdots + a_{nn}x_n = b_n
\end{cases}
$$

与[齐次线性方程组](#定义)相比就是常数项不全为 $0$。简记作 $Ax = b$。

### 解非齐次线性方程组

解一个非齐次线性方程组的步骤大致与[齐次线性方程组](#解齐次线性方程组)相同，但是多一个**求非齐次特解**的步骤。

判定方程组解的情况的方法如下:

- 若 $R(A) \neq R(A\ |\ \beta)$，则方程组无解

- 若 $R(A) = R(A\ |\ \beta) = n$，则方程组有唯一解

- 若 $R(A) = R(A\ |\ \beta) < n$，则方程组有无穷多解

其中 $R(A)$ 为系数矩阵的秩，$R(A\ |\ \beta)$ 为增广矩阵的秩。

在非齐次线性方程组有无穷解的情况下，通解为**对应齐次线性方程组的通解与非齐次特解的和**。

!!! example
    求解非齐次线性方程组的通解: $\begin{cases}
        x_1 + x_2 - x_3 - x_4 = 1 \\
        2x_1 + x_2 + x_3 + x_4 = 4 \\
        4x_1 + 3x_2 - x_3 - x_4 = 6 \\
        x_1 + 2x_2 - 4x_3 - 4x_4 = -1
    \end{cases}$

    - 解:

        依题可得线性方程组的增广矩阵为 $(A\ |\ \beta)$:

        $$
        (A\ |\ \beta) = \left(\begin{array}{cccc|c}
            1 & 1 & -1 & -1 & 1 \\
            2 & 1 & 1 & 1 & 4 \\
            4 & 3 & -1 & -1 & 6 \\
            1 & 2 & -4 & -4 & -1
        \end{array}\right)
        $$

        对 $(A\ |\ \beta)$ 进行初等行变换, 化简至行最简形矩阵得:

        $$
        \left(\begin{array}{cccc|c}
            1 & 0 & 2 & 2 & 3 \\
            0 & 1 & -3 & -3 & 2 \\
            0 & 0 & 0 & 0 & 0 \\
            0 & 0 & 0 & 0 & 0
        \end{array}\right)
        $$

        可得 $R(A) = R(A\ |\ \beta) = 2 < 4$，故方程组有无穷多解，且其对应齐次线性方程组的通解含 $4 - 2 = 2$ 个线性无关的解向量:

        $$
        \begin{cases}
            x_1 + 2x_3 + 2x_4 = 0 \\
            x_2 - 3x_3 - 3x_4 = 0 \\
        \end{cases} \Rightarrow \begin{cases}
            x_1 = -2x_3 - 2x_4 \\
            x_2 = 3x_3 + 3x_4 \\
        \end{cases}
        $$

        令 $x_3 = 1, x_4 = 0$，可得 $x_1 = -2, x_2 = 3$，故 $\alpha_1 = (-2, 3, 1, 0)^T$

        令 $x_3 = 0, x_4 = 1$，可得 $x_1 = -2, x_2 = 3$，故 $\alpha_2 = (-2, 3, 0, 1)^T$

        又有特解 $\beta = (3, -2, 0, 0)^T$

        故通解为:

        $$
        X = k_1 \alpha_1 + k_2 \alpha_2 + \beta = k_1 (-2, 3, 1, 0)^T + k_2 (-2, 3, 0, 1)^T + (3, -2, 0, 0)^T \quad k_1, k_2 \in \mathbb{R}
        $$

        !!! tip
            - 特解可以由方程组增广矩阵行最简形矩阵的最后一列直接得到，但注意行列之间一一对应的关系，例如有以下行最简形矩阵:

                $$
                \left(\begin{array}{cccc|c}
                    1 & 0 & 2 & 2 & 3 \\
                    0 & 1 & -3 & -3 & 2 \\
                    0 & 0 & 0 & 1 & 2 \\
                    0 & 0 & 0 & 0 & 0
                \end{array}\right)
                $$

                则特解为 $(3, -2, 0, 2)^T$，而不是 $(3, -2, 2, 0)^T$，因为第四列是 $x_4$ 的系数。

## 例题

1. 方程组 $\begin{cases}
    (1 + \lambda)x_1 + x_2 + x_3 = 0 \\
    x_1 + (1 + \lambda)x_2 + x_3 = 3 \\
    x_1 + x_2 + (1 + \lambda)x_3 =\lambda 
\end{cases}$，当 $\lambda$ 取何值时，方程组 $1)$ 有唯一解；$2)$ 无解； $3)$ 有无穷多解，并求其通解。

    解:

    依题可得线性方程组的增广矩阵为 $(A\ |\ \beta)$:

    $$
    (A\ |\ \beta) = \left(\begin{array}{ccc|c}
        1 + \lambda & 1 & 1 & 0 \\
        1 & 1 + \lambda & 1 & 3 \\
        1 & 1 & 1 + \lambda & \lambda
    \end{array}\right)
    $$

    化**阶梯形**:

    $$
    \left(\begin{array}{ccc|c}
        1 & 1 & 1 + \lambda & \lambda \\
        0 & \lambda & -\lambda & 3 - \lambda \\
        0 & 0 & -\lambda(3 + \lambda) & (1 - \lambda)(3 + \lambda)
    \end{array}\right)
    $$

    $1)$ 有唯一解时，$R(A) = R(A\ |\ \beta) = 3$，即 $-\lambda(3 + \lambda) \neq 0 \Rightarrow \lambda \neq 0$ 且 $\lambda \neq -3$

    $2)$ 无解时，$R(A) \neq R(A\ |\ \beta)$，即 $\begin{cases}
        -\lambda(3 + \lambda) = 0 \\
        (1 - \lambda)(3 + \lambda) \neq 0
    \end{cases}$ $\Rightarrow \lambda = 0$

    $3)$ 有无穷多解时，$R(A) = R(A\ |\ \beta) < 3$，即 $\begin{cases}
        -\lambda(3 + \lambda) = 0 \\
        (1 - \lambda)(3 + \lambda) = 0
    \end{cases}$ $\Rightarrow \lambda = -3$

    代入 $\lambda = -3$ 得:

    $$
    \left(\begin{array}{ccc|c}
        1 & 1 & -2 & -3 \\
        0 & -3 & 3 & 6 \\
        0 & 0 & 0 & 0
    \end{array}\right) \rightarrow \left(\begin{array}{ccc|c}
        1 & 0 & -1 & -1 \\
        0 & 1 & -1 & -2 \\
        0 & 0 & 0 & 0
    \end{array}\right)
    $$

    得其对应齐次线性方程组的基础解系 $\begin{cases}
        x_1 - x_3 = 0 \\
        x_2 - x_3 = 0
    \end{cases} \Rightarrow \begin{cases}
        x_1 = x_3 \\
        x_2 = x_3
    \end{cases}$

    令 $x_3 = 1$，得解向量 $\alpha = (1, 1, 1)^T$

    对于该非齐次线性方程组，又有特解 $\beta = (-1, -2, 0)^T$

    故通解为:

    $$
    X = k \alpha + \beta = k (1, 1, 1)^T + (-1, -2, 0)^T \quad k \in \mathbb{R}
    $$

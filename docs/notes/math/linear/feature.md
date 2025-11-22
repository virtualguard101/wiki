---
date: 2025-11-22 17:22:25
title: 相似矩阵
permalink: 
publish: true
---

# 相似矩阵

## 求特征值与特征向量

求一个矩阵的特征向量大致可分为两步:

1. 求特征值 $\lambda_i$ （通过特征多项式 $|A - \lambda_i E| = 0$ 求解）

2. 求 $(A - \lambda_i E)x = 0$ 的基础解系（将 $(A - \lambda_i E)$ 看作一个系数矩阵，$(A - \lambda_i E)x = 0$ 其实就是一个[齐次线性方程组](equa-group.md#齐次线性方程组)）

### 例题

1. 求矩阵 $A = \begin{pmatrix}
    3 & -1 \\
    -1 & 3
\end{pmatrix}$ 的特征值

    解:

    依题可得矩阵 $A$ 的**特征多项式**为:

    $$
    \begin{align}
        |A - \lambda E| &= \begin{vmatrix}
        \begin{pmatrix}
            3 & -1 \\
            -1 & 3
        \end{pmatrix} - \lambda \begin{pmatrix}
            1 & 0 \\
            0 & 1
        \end{pmatrix}
    \end{vmatrix} = \begin{vmatrix}
        3 - \lambda & -1 \\
        -1 & 3 - \lambda
    \end{vmatrix} \\
    &= (3 - \lambda)^2 - (-1)^2 = (\lambda - 4)(\lambda - 2) = 0
    \end{align}
    $$

    解得 $A$ 的特征值为 $\lambda_1 = 4$, $\lambda_2 = 2$.

2. 求矩阵 $A = \begin{pmatrix}
    2 & 0 & 0 \\
    1 & 2 & -1 \\
    1 & 0 & 1
\end{pmatrix}$ 的特征值和特征向量

    解:

    $$
    |A - \lambda E| = \begin{vmatrix}
        2 - \lambda & 0 & 0 \\
        1 & 2 - \lambda & -1 \\
        1 & 0 & 1 - \lambda
    \end{vmatrix}
    $$

    [按行（列）展开](det-unfold.md)得:

    $$
    \begin{align}
    原式 &= (2 - \lambda)(-1)^{1 + 1} \begin{vmatrix}
        2 - \lambda & -1 \\
        0 & 1 - \lambda
    \end{vmatrix} \\
    &= (2 - \lambda)^{2}(1 - \lambda) = 0
    \end{align}
    $$

    解得 $A$ 的特征值为 $\lambda_1 = 1$, $\lambda_2 = \lambda_3 = 2$.

    - $\lambda_1 = 1$ 时，解 $(A - E)x = 0$

        $$
        A - E = \begin{pmatrix}
            1 & 0 & 0 \\
            1 & 1 & -1 \\
            1 & 0 & 0
        \end{pmatrix} \rightarrow \begin{pmatrix}
            1 & 0 & 0 \\
            0 & 1 & -1 \\
            0 & 0 & 0
        \end{pmatrix}
        $$

        得 $\begin{cases}
            x_1 = 0 \\
            x_2 - x_3 = 0
        \end{cases}$

        令 $x_3 = 1 \Rightarrow x_1 = 0, x_2 = 1$，得解向量 $\alpha_1 = (0, 1, 1)^T$

        故 $\lambda_1 = 1$ 对应的全部特征向量为 $k_1(0, 1, 1)^T \quad (k_1 \neq 0)$

    - $\lambda_2 = \lambda_3 = 2$ 时，解 $(A - 2E)x = 0$

        $$
        A - 2E = \begin{pmatrix}
            0 & 0 & 0 \\
            1 & 0 & -1 \\
            1 & 0 & -1
        \end{pmatrix} \rightarrow \begin{pmatrix}
            1 & 0 & -1 \\
            0 & 0 & 0 \\
            0 & 0 & 0
        \end{pmatrix}
        $$

        得 $x_1 - x_3 = 0$

        令 $x_2 = 1, x_3 = 0 \Rightarrow x_1 = 0$，得解向量 $\alpha_2 = (0, 1, 0)^T$

        令 $x_2 = 0, x_3 = 1 \Rightarrow x_1 = 1$，得解向量 $\alpha_3 = (1, 0, 1)^T$

        故 $\lambda_2 = \lambda_3 = 2$ 对应的全部特征向量为 $k_2(0, 1, 0)^T + k_3(1, 0, 1)^T$ ($k_2, k_3$ 不全为 $0$)

## 相似对角化

---
date: 2025-10-09 23:47:00
title: 矩阵的初等变换
permalink: 
publish: true
---

# 矩阵的初等变换

> [矩阵](matrix.md)

## 矩阵方程

设 $A$, $B$ 均为可逆矩阵

常见的方程都可以转化为以下几种基本形式:

- $AX = C$

    矩阵两边同时**左乘** $A^{-1}$ 即可, 即:

    $$
    A^{-1}AX = A^{-1}C
    $$

    故解为 $EX = A^{-1}C$, 即 

    $$
    X = A^{-1}C
    $$

!!! warning
    注意 $A$ 和 $A^{-1}$ 的顺序, 且**不得将矩阵置于分母**：

    !!! failure
        $$
        X = \frac{C}{A}
        $$

        这是一个典型错误。==$A^{-1} \not ={\frac{1}{A}}$，不存在后者这个概念==。

- $XA = C$

    同理，对于这个形式，矩阵两边同时**右乘** $A^{-1}$ 即可, 即:

    $$
    XAA^{-1} = CA^{-1}
    $$

    故解为 $EX = CA^{-1}$, 即 

    $$
    X = CA^{-1}
    $$

- $AXB = C$

    对于这个形式，矩阵两边同时**左乘** $A^{-1}$ 加**右乘** $B^{-1}$ 即可, 即:

    $$
    A^{-1}AXBB^{-1} = A^{-1}CB^{-1}
    $$

    故解为 $EXE = A^{-1}CB^{-1}$, 即 

    $$
    X = A^{-1}CB^{-1}
    $$

!!! example

    1. 解矩阵方程 $AX = 2X + B$, 其中 $A = \begin{pmatrix}
        4 & 0 & 0 \\
        0 & 1 & -1 \\
        0 & 1 & 4
    \end{pmatrix}$, $B = \begin{pmatrix}
        3 & 6 \\
        1 & 1 \\
        2 & -3
    \end{pmatrix}$.

        - 解:
    
            将方程变形为 $AX - 2X = B$, 即 $(A - 2E)X = B$

            又 $A - 2E = \begin{pmatrix}
                2 & 0 & 0 \\
                0 & -1 & -1 \\
                0 & 1 & 2
            \end{pmatrix}$, $|A- 2E| = -2 \not = 0$, 故 $A - 2E$ 可逆

            等式两侧同时乘以 $(A - 2E)^{-1}$, 化简得 $X = (A - 2E)^{-1}B$.

            又有 $(A - 2E)^{-1} = \begin{pmatrix}
                \frac{1}{2} & 0 & 0 \\
                0 & -2 & -1 \\
                0 & 1 & 1 
            \end{pmatrix}$

            故 $X = (A - 2E)^{-1}B = \begin{pmatrix}
                \frac{1}{2} & 0 & 0 \\
                0 & -2 & -1 \\
                0 & 1 & 1 
            \end{pmatrix} \begin{pmatrix}
                3 & 6 \\
                1 & 1 \\
                2 & -3
            \end{pmatrix} = \begin{pmatrix}
                \frac{3}{2} & 3 \\
                -4 & 1 \\
                3 & -2
            \end{pmatrix}$

## 初等变换

### 定义

初等变换分为**初等行变换**和**初等列变换**。有三种初等变换:

- 交换两行(列)

    $$
    \begin{pmatrix}
        R_i \\
        R_j
    \end{pmatrix} \xrightarrow{r_i \leftrightarrow r_j} \begin{pmatrix}
        R_j \\
        R_i
    \end{pmatrix}
    $$

- 某行(列)乘以非零常数 $k$

    $$
    \begin{pmatrix}
        R_i \\
        R_j
    \end{pmatrix} \xrightarrow{kr_i} \begin{pmatrix}
        kR_i \\
        R_j
    \end{pmatrix}
    $$

- 某行(列)乘以非零常数 $k$ 加到另一行(列)

    $$
    \begin{pmatrix}
        R_i \\
        R_j
    \end{pmatrix} \xrightarrow{r_i + kr_j} \begin{pmatrix}
        R_i + kR_j \\
        R_j
    \end{pmatrix}
    $$

### 行阶梯形矩阵

判断的一个简单方法: **画楼梯**

- 阶梯线下方全为 $0$

- 竖线每次只经过一个数

- 横线可经过多个数

### 行最简形矩阵

在行阶梯行矩阵的基础上新增如下几点:

- 每行的**首非零元**（最靠近竖线的数）为 $1$

- 首非零元所在列的其余元素为 $0$

### 标准形

若矩阵的左上角可分离出一个单位矩阵，且其他元素均为 $0$，则称该矩阵为标准形。简记作：

$$
\begin{pmatrix}
    E_r & O \\
    O & O
\end{pmatrix}_{m \times n}
$$

!!! example
    注意标准形不一定是方阵以下矩阵都是标准形：

    $\begin{pmatrix}
        1 & 0 & 0 \\
        0 & 1 & 0 \\
        0 & 0 & 0
    \end{pmatrix}$, $\begin{pmatrix}
        1 & 0 & 0 & 0 \\
        0 & 1 & 0 & 0 \\
        0 & 0 & 1 & 0
    \end{pmatrix}$, $\begin{pmatrix}
        1 & 0 & 0 & 0 & 0 \\
        0 & 1 & 0 & 0 & 0\\
        0 & 0 & 1 & 0 & 0\\
        0 & 0 & 0 & 0 & 0
    \end{pmatrix}$

### 初等变换的应用

最主要的应用就是将矩阵化为行阶梯形矩阵或行最简形矩阵:

```
普通矩阵 -> 行阶梯形矩阵 -> 行最简形矩阵 -> 标准形
```

向行阶梯形矩阵或行最简形矩阵的变换过程可遵循**从左向右逐列进行**的原则，不易出错。

若只将矩阵变换至行阶梯形矩阵，则**结果不唯一**，但若进一步转换至行最简形矩阵，则**结果唯一**。

## 初等矩阵

### 定义

单位矩阵经过一次初等变换后得到的新矩阵称为初等矩阵。所以三种初等变换就对应着三种初等矩阵:

- 交换第 $i$ 行和第 $j$ 行(列)，记作 $E(i, j)$

    $$
    E(1, 2) = \begin{pmatrix}
        0 & 1 & 0 \\
        1 & 0 & 0 \\
        0 & 0 & 1
    \end{pmatrix}
    $$

- 第 $i$ 行(列)乘以非零常数 $k$，记作 $E(i(k))$

    $$
    E(2(k)) = \begin{pmatrix}
        1 & 0 & 0 \\
        0 & k & 0 \\
        0 & 0 & 1
    \end{pmatrix}
    $$

- 第 $j$ 行(第 $i$ 列)乘以非零常数 $k$ 加到第 $i$ 行(第 $j$ 列)，记作 $E(ij(k))$

    $$
    E(23(k)) = \begin{pmatrix}
        1 & 0 & 0 \\
        0 & 1 & k \\
        0 & 0 & 1
    \end{pmatrix}
    $$

### 性质

- 初等矩阵的行列式均不为 $0$

    - $|E(i, j)| = -1$, $|E(i(k))| = k$, $|E(ij(k))| = 1$

    - ==故初等矩阵**均可逆**, 且有其逆矩阵为同类型的初等矩阵==:

        - $E(i, j)^{-1} = E(i, j)$

        - $E(i(k))^{-1} = E(i(\frac{1}{k}))$

        - $E(ij(k))^{-1} = E(ij(-k))$

- 初等矩阵的转置矩阵仍为同类型的初等矩阵

    - $E(i, j)^T = E(i, j)$

    - $E(i(k))^T = E(i(k))$

    - $E(ij(k))^T = E(ji(k))$

### 初等矩阵与初等变换的关系

设 $A$ 为 $m \times n$ 矩阵, 则有:

- 对 $A$ 进行一次初等行变换, 相当于用同类型的 $m$ 阶初等矩阵左乘 $A$

    - $A \xrightarrow{r_i \leftrightarrow r_j} E(i, j)A$

    - $A \xrightarrow{kr_i} E(i(k))A$

    - $A \xrightarrow{r_i + kr_j} E(ij(k))A$

- 同理，对 $A$ 进行一次初等列变换, 相当于用同类型的 $n$ 阶初等矩阵右乘 $A$

    - $A \xrightarrow{c_j \leftrightarrow c_k} AE(j, k)$

    - $A \xrightarrow{kc_j} AE(j(k))$

    - $A \xrightarrow{c_j + kc_k} AE(jk(k))$


## 矩阵的秩

### 最高阶非零子式

在 $m \times n$ 矩阵 $A$ 中, 任取 $k$ 行 $k$ 列, 位于这些行列交叉处的 $k^2$ 个元素, 不改变其位置次序所构成的 $k$ 阶**行列式**, 称为矩阵 $A$ 的 $k$ 阶子式.

若 $A$ 中存在一个不等于零的 $r$ 阶子式, 且所有 $r + 1$ 阶子式（如果有的话）全为零, 则称 $D$ 为矩阵 $A$ 的最高阶非零子式, 阶数 $r$ 称为矩阵 $A$ 的秩, 记作 $r(A)$, 且有$r(A) = 0$ 当且仅当 $A = O$, 即零矩阵的秩为 $0$.

!!! abstract "秩的定义"
    ==$r(A) = n$ $\Longleftrightarrow$ $A$ 至少有一个 $n$ 阶子式不等于 $0$ 且所有 $n + 1$ 阶子式全为零 $0$==

    !!! tip
        不存在 $r + 1$ 阶子式不等于 $0$ 且所有 $r + 2$ 阶子式（若有）全为零的情况, 从[行列式按行(列)展开的内容](det.md#三阶行列式)中不难看出, 若 $r + 1$ 的阶子算式全为零, 即为 $r + 2$ 的代数余子式全为零, 而行列式按行(列)展开后, 每一项都包含一个代数余子式, 它们全为零, 故 $r + 2$ 阶子式必全为零.

### 性质

- $0 \leq r(A) \leq \min\{m, n\}$

- $r(A) = r(A^T)$

- 若 $A$ 为 $n$ 阶方阵:

    - ==$A$ 满秩 $\Longleftrightarrow$ $r(A) = n$ $\Longleftrightarrow$ $|A| \not ={0}$ $\Longleftrightarrow$ $A$ 可逆 $\Longleftrightarrow$ $A$ 的行最简形矩阵为单位矩阵==

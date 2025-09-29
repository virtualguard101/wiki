# 矩阵

## 常用类型

- **$m \times n$ 矩阵**

    由 $m \times n$ 个元素 $a_{ij}$ 排列而成.

    $$
    \begin{pmatrix}
        a_{11} & a_{12} & \cdots & a_{1n} \\
        a_{21} & a_{22} & \cdots & a_{2n} \\
        \vdots & \vdots & \ddots & \vdots \\
        a_{m1} & a_{m2} & \cdots & a_{mn}
    \end{pmatrix}
    $$

    记作 $(a_{ij})$ 或 $(a_{ij})_{m \times n}$, 也可使用大写字母表示, 如 $A_{m \times n}$.

    - 特别地, $m = n$, 即行列相等时, 矩阵称为 **$n$ 阶方阵**

- **零矩阵**

    矩阵元素 $a_{ij}$ 皆为 $0$ 的矩阵, 记作 $O$.

- **对角矩阵**

    除对角线外的元素均为 $0$ 的矩阵称为对角矩阵, 记作 $diag(a_1, a_2, \cdots, a_n)$, 即

    $$
    diag(a_1, a_2, \cdots, a_n) = 
    \begin{pmatrix}
        a_1 & 0 & \cdots & 0 \\
        0 & a_2 & \cdots & 0 \\
        \vdots & \vdots & \ddots & \vdots \\
        0 & 0 & \cdots & a_n
    \end{pmatrix}
    $$

    - 特别地, 当 $a_1 = a_2 = \cdots = a_n = 1$ 时, 称为 **单位矩阵**, 记作 $E_n$:

        $$
        E_n = 
        \begin{pmatrix}
            1 & 0 & \cdots & 0 \\
            0 & 1 & \cdots & 0 \\
            \vdots & \vdots & \ddots & \vdots \\
            0 & 0 & \cdots & 1
        \end{pmatrix}
        $$

- **行(列)矩阵**

    只有一行或一列的矩阵被称为行(列)矩阵/向量

    $$
    A = (a_1, a_2, \cdots, a_n)
    $$

    $$
    B = \begin{pmatrix}
        b_1 \\
        b_2 \\
        \vdots \\
        b_n
    \end{pmatrix}
    $$

## 运算

### 线性运算

#### 加法

!!! warning
    只有两个矩阵为**同型矩阵**时, 才能进行加法运算.

直接把各个元素对应相加即可.

设有同型矩阵 $A = (a_{ij})_{m \times n}$, $B = (b_{ij})_{m \times n}$, 则

$$
A + B = (a_{ij} + b_{ij})_{m \times n}
$$

- 矩阵加法满足以下运算律

    - **交换律**: $A + B = B + A$

    - **结合律**: $(A + B) + C = A + (B + C)$

    - $A + O = A$

#### 数乘

和加法类似, 数乘就是把矩阵的每个元素都乘上一个数.

设有矩阵 $A = (a_{ij})_{m \times n}$, 数 $\lambda$, 则有

$$
\lambda A = A \lambda = (\lambda a_{ij})_{m \times n}
$$

- 矩阵加法满足以下运算律

    - **交换率**

    - **结合律**: $(\lambda \mu) A = \lambda (\mu A)$

    - **分配率**: 

        - $(\lambda + \mu) A = \lambda A + \mu A$

        - $\lambda (A + B) = \lambda A + \lambda B$

### 矩阵乘法

#### 定义

==矩阵乘法本质上是"行与列的对应关系"==.

有矩阵 $A = (a_{ik})_{m \times t}$, $B = (b_{kj})_{t \times n}$, 则有 $C = (c_{ij})_{m \times n}$, 称为矩阵 $A$ **左乘** 矩阵 $B$(或 $B$ 右乘 $A$)**之积**, 记作

$$
C = AB
$$

其中

$$
c_{ij} = \sum_{k = 1}^{t} a_{ik}b_{kj} = a_{i1}b_{1j} + a_{i2}b_{2j} + \cdots + a_{it}b_{tj} \quad \quad (i = 1, 2, \cdots, m; j = 1, 2, \cdots, n)
$$

!!! warning
    这里注意 $A$ 的行数与 $B$ 的列数必须是一致的

只看公式可能不太好理解, 下面看几个例子

!!! example
    1. 设 $A = \begin{pmatrix}
        a_{11} & a_{12} & a_{13} \\
        a_{21} & a_{22} & a_{23}
    \end{pmatrix}$, $B = \begin{pmatrix}
        b_{11} & b_{12} \\
        b_{21} & b_{22} \\
        b_{31} & b_{32}
    \end{pmatrix}$, 则有

        $$
        AB = \begin{pmatrix}
            a_{11} & a_{12} & a_{13} \\
            a_{21} & a_{22} & a_{23}
        \end{pmatrix} \begin{pmatrix}
            b_{11} & b_{12} \\
            b_{21} & b_{22} \\
            b_{31} & b_{32}
        \end{pmatrix} = \begin{pmatrix}
            a_{11}b_{11} + a_{12}b_{21} + a_{13}b_{31} & a_{11}b_{12} + a_{12}b_{22} + a_{13}b_{32} \\
            a_{21}b_{11} + a_{22}b_{21} + a_{23}b_{31} & a_{21}b_{12} + a_{22}b_{22} + a_{23}b_{32}
        \end{pmatrix}
        $$
    
    2. 设 $A = (a, b, c)$, $B = \begin{pmatrix}
        d \\
        e \\
        f
    \end{pmatrix}$, 则有

        $$
        AB = (a, b, c) \begin{pmatrix}
            d \\
            e \\
            f
        \end{pmatrix} = ad + be + cf
        $$

        $$
        BA = \begin{pmatrix}
            d \\
            e \\
            f
        \end{pmatrix} (a, b, c) = \begin{pmatrix}
            da & db & dc \\
            ea & eb & ec \\
            fa & fb & fc
        \end{pmatrix}
        $$

    3. 求解 $(x_1, x_2, x_3) \begin{pmatrix}
        a_{11} & a_{12} & a_{13} \\
        a_{21} & a_{22} & a_{23} \\
        a_{31} & a_{32} & a_{33}
    \end{pmatrix} \begin{pmatrix}
        x_1 \\
        x_2 \\
        x_3
    \end{pmatrix}$

        $$
        \begin{align}
            \text{原式} & = (x_1, x_2, x_3) \begin{pmatrix}
                a_{11}x_1 + a_{12}x_2 + a_{13}x_3 \\
                a_{21}x_1 + a_{22}x_2 + a_{23}x_3 \\
                a_{31}x_1 + a_{32}x_2 + a_{33}x_3
            \end{pmatrix} \\
            & = x_1(a_{11}x_1 + a_{12}x_2 + a_{13}x_3) + x_2(a_{21}x_1 + a_{22}x_2 + a_{23}x_3) + x_3(a_{31}x_1 + a_{32}x_2 + a_{33}x_3) \\
            & = a_{11}x_1^2 + a_{12}x_1x_2 + a_{13}x_1x_3 + a_{21}x_2x_1 + a_{22}x_2^2 + a_{23}x_2x_3 + a_{31}x_3x_1 + a_{32}x_3x_2 + a_{33}x_3^2 \\
            & = a_{11}x_1^2 + a_{22}x_2^2 + a_{33}x_3^2 + (a_{12} + a_{21})x_1x_2 + (a_{13} + a_{31})x_1x_3 + (a_{23} + a_{32})x_2x_3 \\
        \end{align}
        $$
    
简单来说就是, ==左矩阵第 $i$ 行的元素与右矩阵第 $j$ 列对应元素相乘后求和，得到结果矩阵的第 $(i, j)$ 个元素==, **左矩阵有几行, 结果就有几行; 右矩阵有几列, 结果就有几列**.


#### 运算律

从上面的第二个例子不难看出, **矩阵乘法不满足交换律**.

- $(AB)C = A(BC)$

- $(\lambda A)B = \lambda (AB)$

- $A(B + C) = AB + AC$

- $(A + B)C = AC + BC$

- 对于单位矩阵 $E_n$, 有

    $$
    A_{m \times n}E_{n} = A_{m \times n}
    $$

    $$
    E_{n}A_{m \times n} = A_{m \times n}
    $$

    即

    $$
    AE = EA = A
    $$

    !!! example
        设 $A = \begin{pmatrix}
            a_{11} & a_{12} & a_{13} \\
            a_{21} & a_{22} & a_{23}
        \end{pmatrix}$, $E_3 = \begin{pmatrix}
            1 & 0 & 0 \\
            0 & 1 & 0 \\
            0 & 0 & 1
        \end{pmatrix}$, $E_2 = \begin{pmatrix}
            1 & 0 \\
            0 & 1
        \end{pmatrix}$, 则有

        $$
        AE_3 = \begin{pmatrix}
            a_{11} & a_{12} & a_{13} \\
            a_{21} & a_{22} & a_{23}
        \end{pmatrix} \begin{pmatrix}
            1 & 0 & 0 \\
            0 & 1 & 0 \\
            0 & 0 & 1
        \end{pmatrix} = \begin{pmatrix}
            a_{11} & a_{12} & a_{13} \\
            a_{21} & a_{22} & a_{23}
        \end{pmatrix} = A
        $$

        $$
        E_2A = \begin{pmatrix}
            1 & 0 \\
            0 & 1
        \end{pmatrix} \begin{pmatrix}
            a_{11} & a_{12} & a_{13} \\
            a_{21} & a_{22} & a_{23}
        \end{pmatrix} = \begin{pmatrix}
            a_{11} & a_{12} & a_{13} \\
            a_{21} & a_{22} & a_{23}
        \end{pmatrix} = A
        $$

### 矩阵的幂

设 $A$ 为 $n$ 阶**方阵**, 则有:

$$
A^{0} = E
$$

$$
A^{n} = \underbrace{A \cdot A \cdot \cdots A}_{\text{n 个}}
$$


矩阵的幂运算满足以下运算率 $(k \in \mathbb{Z}, n \in \mathbb{N^{+}})$:

- $A^{n_1 + n_2} = A^{n_1} A^{n_2}$

- $(A^{n_1})^{n_2} = A^{n_1 n_2}$

- $(kA)^{n} = k^{n} A^{n}$

!!! warning
    由于矩阵乘法不满足交换律, 故有以下结论:

    $$
    (AB)^{2} \not ={A^{2} B^{2}}
    $$

    将左右两边分别展开对比一下就知道了:

    $$
    \begin{align}
        (AB)^{2} & = AB \cdot AB \\
        A^{2} B^{2} & = AA \cdot BB \\
    \end{align}
    $$

    不难发现中间两项 $A$ $B$ 相乘的顺序不同. ==但且仅当矩阵 $A$ $B$ 可交换时, 方可像实数一样进行幂运算==.

!!! exmaple
    1. 设 $A = \begin{pmatrix}
        1 \\
        -1 \\
        2
    \end{pmatrix}$, $B = \begin{pmatrix}
        3 & 1 & -2
    \end{pmatrix}$, 求 $(AB)^{n}$.

        - 解:

            $$
            AB = \begin{pmatrix}
                1 \\
                -1 \\
                2
            \end{pmatrix} \begin{pmatrix}
                3 & 1 & -2
            \end{pmatrix} = \begin{pmatrix}
                3 & 1 & -2 \\
                -3 & -1 & 2 \\
                6 & 2 & -4
            \end{pmatrix}
            $$

            $$
            BA = \begin{pmatrix}
                3 & 1 & -2
            \end{pmatrix} \begin{pmatrix}
                1 \\
                -1 \\
                2
            \end{pmatrix} = 3 - 1 - 4 = -2
            $$

            故有

            $$
            \begin{align}
                \text{原式} & = A \cdot \underbrace{BABABA}_{\text{n-1组}} \cdots B \\
                & = (-2)^{n - 1} AB \\
                & = (-2)^{n - 1} \begin{pmatrix}
                    3 & 1 & -2 \\
                    -3 & -1 & 2 \\
                    6 & 2 & -4
                \end{pmatrix}
            \end{align}
            $$
        
    2. 设 $A = \begin{pmatrix}
        2 & 4 & -6 \\
        1 & 2 & -3 \\
        4 & 8 & -12
    \end{pmatrix}$, 求 $A^{100}$.

        - 解:

            观察易发现, $A$ 的行(列)成比例, $R(n) = 1$[^1]

            令 $A = \begin{pmatrix}
                2 \\
                1 \\
                4
            \end{pmatrix} \begin{pmatrix}
                1 & 2 & -3
            \end{pmatrix} = \alpha \beta^{T}$

            则有

            $$
            \beta^{T} \alpha = \begin{pmatrix}
                1 & 2 & -3
            \end{pmatrix} \begin{pmatrix}
                2 \\
                1 \\
                4
            \end{pmatrix} = 2 + 2 - 12 = -8
            $$

            故

            $$
            \begin{align}
                \text{原式} & = \alpha \cdot \underbrace{\beta^{T}\alpha\beta^{T}\alpha\beta^{T}\alpha}_{\text{99 组}} \cdots \beta^{T} \\
                & = (-8)^{99} \alpha\beta^{T} \\
                & = - 8^{99} \begin{pmatrix}
                    2 & 4 & -6 \\
                    1 & 2 & -3 \\
                    4 & 8 & -12
                \end{pmatrix}
            \end{align}
            $$


[^1]: 这里指[矩阵的秩](), 会在初等变换中学到
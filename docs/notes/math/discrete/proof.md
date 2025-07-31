# 证明

>[CS70 Note 2 | UC Berkeley](https://www.eecs70.org/assets/pdf/notes/n2.pdf)

在科学领域，人们通过实验积累数据来断言某个命题的正确性，而数学则追求更高层次的确定性——数学证明能确保命题必然为真，且在某种程度上类似于计算机程序。

学习证明的目标是学会针对不同的定理给出清晰简洁的证明，本节内容将通过观察不同的证明实例来学习不同的证明方法并达成这一目标。

## 直接证明法（*Direct Proof*）

1. 对于任意整数 $a$, $b$, $c$，如果 $a\ |\ b$[^1] 且 $a\ |\ c$，则 $a\ |\ (b+c)$

    !!! review
        设 $P(x, y) =$ "$x\ |\ y$"，则上述命题等价于

        $$
        (\forall a, b, c \in \mathbb{Z})(P(a, b) \land P(a, c) \Rightarrow P(a, b+c))
        $$
    
    从高层次来看，直接证明的步骤如下：

    对于每个 $x$，我们要证明的命题均具有 $P(x) \Rightarrow Q(x)$ 的形式。直接证明的方式首先假设 $P(x)$ 对某个通用 $x$ 值成立，最终通过一系列蕴含关系得出 $Q(x)$ 的结论：

    !!! success inline "直接证明法"

        目标：证明 $P \Rightarrow Q$

        方法：假设 $P$ 成立

        .....

        因此 $Q$ 得证
    
    - 关于该定理的证明如下：

        设 $a\ |\ b$ 且 $a\ |\ c$，即存在整数 $q_1$ 和 $q_2$ 使得 $b = aq_1$ 且 $c = aq_2$。

        于是有 $b + c = aq_1 + aq_2 = a(q_1 + q_2)$。

        由于整数集 $\mathbb{Z}$ 对加法封闭[^2]，可得 $(q_1 + q_2) \in \mathbb{Z}$，故 $a\ |\ (b+c)$ 得证。

    !!! tip
        在上述的证明中，我们并没有限定 $a$, $b$, $c$ 的具体取值，故该证明适用于任意整数，也就对应了 *review* 中的 $(\forall a, b, c \in \mathbb{Z})$ 

2. 设 $0 < n < 1000$ 为整数。若 $n$ 的各位数字之和能被 $9$ 整除，则 $n$ 也能被 $9$ 整除。

    !!! review
        该命题等价于

        $$
        (\forall n \in \mathbb{Z}^{+})(n <1000) \Rightarrow (n \text{的各位数字之和能被 9 整除} \Rightarrow n \text{能被 9 整除})
        $$

  我们的证明思路是：首先假设对于任意 $n$ 值，其各位数字之和能被 $9$ 整除，然后通过一系列推导得出 $n$ 本身也能被 $9$ 整除的结论。

  - 证明如下：

    令 $n = 100a + 10b + c$。假设 $n$ 的各位数字之和能被 $9$ 整除，即

    $$
    \exists k \in \mathbb{Z}\ \text{使得}\ a+b+c = 9k\ \ \ \ \ (1)
    $$

    在等式 $(1)$ 两侧同时加上 $99a + 9b$，可得

    $$
    100a + 10b + c = n = 9k + 99a + 9b = 9(k + 11a + b)
    $$

    故 定理$2$ 得证。

3.（定理$2$ 的逆定理）设 $0 < n < 1000$ 为整数。若 $n$ 能被 $9$ 整除，则 $n$ 的各位数字之和也能被 $9$ 整除。

  - 证明如下：

    $$
    n \text{能被} 9 \text{整除} \Rightarrow \exists l \in \mathbb{Z}\ \text{使得}\ n = 9l
    $$

    $$
    \hspace{3cm} \Rightarrow 100a + 10b + c = 9l
    $$

    $$
    \hspace{4.8cm} \Rightarrow 99a + 9b + (a + b + c) = 9l
    $$

    $$
    \hspace{4.4cm} \Rightarrow a + b + c = 9l - 99a - 9b
    $$

    $$
    \hspace{4.5cm} \Rightarrow a + b + c = 9(l - 11a - b)
    $$

    $$
    \hspace{7.9cm} \Rightarrow \exists k = l - 11a - b \in \mathbb{Z}\ \text{使得}\ a + b + c = 9k
    $$

    故 定理$3$ 得证。

!!! important
    从 定理$2$ 与 定理$3$ 的证明可以得出：**当且仅当**整数 $n$ 本身能被 $9$ 整除时，$n$ 的各位数字之和也能被 $9$ 整除，即 定理2 与 定理3 在逻辑上等价。

    ==当需要证明等价关系 $P \Leftrightarrow Q$ 时，务必分别证明 $P \Rightarrow Q$（充分性） 和 $Q \Rightarrow P$（必要性）==

## 逆否命题证明法（*Proof by Contraposition*）


[^1]: 对于整数 $a$ 和 $b$，当且仅当存在整数 $q$ 使得 $b = aq$ 时，我们称 $a$ 整除 $b$，记作 ==$a\ |\ b$==

[^2]: 求和运算或两个整数的乘积仍是整数，即整数集在加法或乘法运算下封闭。自然数集在加法和乘法运算下同样具有封闭性
# 集合 & 数学符号与命题逻辑

## 集合

>[CS70 Note 0 | UC Berkeley](https://www.eecs70.org/assets/pdf/notes/n0.pdf)

**集合（*set*）**是明确定义的对象组合，这些对象称为集合的**元素**或**成员**，可以是任何事物。

### 基数

==**基数（*cardinality*）**是指集合中不同元素的数量==。假设有一个集合 $A = {\{1, 2, 3, 4, 5\}}$，其基数就是它的元素数量$5$，记作：

$$
|A| = 5
$$

一个集合的元素个数可能是$0$，此时这个集合就是一个空集，用符号 $\varnothing$ 或 $\{\}$ 表示。

### 子集与真子集

设集合 $A$ 中的所有元素都属于集合 $B$，则称 ==$A$ 是 $B$ 的**子集（*subset*）**==，记作:

$$
A \subseteq B
$$

或称 ==$B$ 是 $A$ 的**超集（*superset*）**==，记作:

$$
B \supseteq A
$$

特别地，若集合 $B$ 中还包含 $A$ 中不存在的元素，则称 ==$A$ 是 $B$ 的**真子集（*proper subset*）**==，记作 ==$A \subset B$==。

以下是关于集合的几个基本性质:

  - 空集是任何非空子集 $A$ 的**真子集**：$\forall A \subseteq \mathbb{U}$, $\varnothing \subset A$ ($A \not ={\varnothing}$)

  - 空集是任意集合 $B$ 的**子集**：$\forall B \subseteq \mathbb{U}$, $\{\} \subseteq B$

  - 任意集合 $A$ 都是其自身的子集：$\forall A \subseteq \mathbb{U}$, $A \subseteq A$

### 交集与并集

集合 $A$ 与集合 $B$ 的**交集（*intersection*）**，指包含同时属于二者的元素的集合，记作：

$$
A \cap B
$$

若两个集合存在关系 $A \cap B = \varnothing$，则称二者**互斥（*disjoint*）**。

集合 $A$ 与集合 $B$ 的**并集（*union*）**，指包含所有属于二者的元素的集合，记作：

$$
A \cup B
$$

例如，设 $A$ 是所有正偶数的集合，$B$ 是所有正奇数的集合，则 $A$ 与 $B$ 的交集就是空集，并集则是正整数集。

即 

$$
(\exists A = \{x \in \mathbb{N}^{+}\ |\ \exists k \in \mathbb{N}^{+}, x = 2k\},\ B = \{x \in \mathbb{N}^{+}\ |\ \exists k \in \mathbb{N}^{+}, x = 2k - 1\})(A \cap B = \varnothing \land A \cup B = \mathbb{N}^{+})
$$

下面是关于交集与并集的几个性质：

- $A \cap B = B \cap A$

- $A \cup B = B \cup A$

- $A \cap \varnothing = \varnothing$

- $A \cup \varnothing = A$

### 差集

集合 $A$ 中集合 $B$ 的**相对补集（*relative complement*）**，或称为 $A$ 与 $B$ 的**差集（*set difference*）**，记作：

$$
B - A
$$

或

$$
B \setminus A
$$

指 ==属于 $B$ 但不属于 $A$ 的元素组成的集合==，即：

$$
B \setminus A = \{x\ |\ x\in B,\ x\not \in A\}
$$

例如，实数集与有理数集的差集就是无理数集：$\mathbb{R} \setminus \mathbb{Q}$

!!! warning inline end
    ️注意差集运算不满足交换律：

    $$
    B \setminus A \not = A \setminus B
    $$

以下是关于差集的几个重要性质：

- $A \setminus A = \varnothing$

- $A \setminus \varnothing = A$

- $\varnothing \setminus A = \varnothing$

### 笛卡尔积与幂集

#### 笛卡尔积

两个集合 $A$ 和 $B$ 的**笛卡尔积（*Cartesian product*）**，也被成为**叉积（*cross product*）**，记作：

$$
A \times B
$$

==是由所有由 $A$ 与$B$ 中的元素组成的**有序对**的集合==，其中第一个分量为 $A$ 的元素，第二个分量为 $B$ 的元素，即：

$$
A \times B = \{(a, b)\ |\ a \in A,\ b \in B\}
$$

例如，设 $A = \{1, 3, 5\}$ ，$B = \{u, v\}$，则：

$$
A \times B = \{(1, u), (1, v), (3, u), (3, v), (5, u), (5, v)\}
$$

对于两个自然数集的叉积，则有：

$$
\mathbb{N} \times \mathbb{N} = \{(0, 0), (1, 0), (0, 1), (1, 1), (2, 0), ...\}
$$

表示所有自然数对构成的集合。

#### 幂集

给定集合 $S$，其**幂集（*power set*）**记作

$$
\wp(S)
$$

==指 $S$ 的所有子集构成的集合==，即：

$$
\wp(S) = \{T\ |\ T \subseteq S\}
$$

例如，设集合 $A = \{1, 2, 3\}$，则

$$
\wp(A) = \{\varnothing, \{1\}, \{2\}, \{3\}, \{1, 2\}, \{1, 3\}, \{2, 3\}, \{1, 2, 3\}\}
$$

!!! tip "幂集基数定理"
    对于任意**有限集合** $S$，若 $|S| = k$，则 $|\wp(S)| = 2^k$，即：

    $$
    (\forall S \subseteq \mathbb{U})(\exists k \in \mathbb{N})(|S| = k \rightarrow |\wp(S)| = 2^k)
    $$

## 数学符号与命题逻辑

>[CS70 Note 1 | UC Berkeley](https://www.eecs70.org/assets/pdf/notes/n1.pdf)

为了能够流畅、熟练地处理数学陈述，我们有必要理解数学语言的基础框架以及一些常用的数学符号。

### 求和与求积

对于书写大量项的和或积，有一种紧凑的表达方式，即**求和（$\sum$）**与**求积（$\prod$）**符号。

对于多项式 $\mathcal{f}(m) + \mathcal{f}(m+1) + ... + \mathcal{f}(n)$，我们可以写作：

$$
\sum_{i=m}^n \mathcal{f}(i)
$$

同理，对于$\mathcal{f}(m) \cdot \mathcal{f}(m+1) ... \mathcal{f}(n)$，可简写作：

$$
\prod_{i=m}^n \mathcal{f}(i)
$$

### 命题逻辑

**命题（*proposition*）**是陈述数学定理的一个基础构件，定义上，它是一个 ==非真即假的陈述句==。

例如，以下陈述皆为命题：

  - $5$ 是有理数

  - $x^2 + 2x +1 > 1$

  - *virtualguard101* 是一个飞舞

而下列陈述则不能被定义为命题：

  - $\sqrt{5} + \sqrt{5}$ [无法定义真假]

  - $x^2 + 2x +1 = 1$ [$x$ 是多少?]

  - 他是大佬  [他是谁?]

==命题不应包含**概念模糊**的术语。==

#### 逻辑连接词与命题形式

==命题可以通过逻辑连接词组合成更复杂的陈述。==

设存在命题变量 $P$、$Q$（如可令$P =$ "$5$是有理数"），则连接这些命题最简单的方式就是使用“与”、“或”、“非”等逻辑连接词。

- **合取（*conjunction*）**: $P ∧ Q$（$P$ 且/与 $Q$，当且仅当 $P$ 与 $Q$ 同时为真时为真）

- **析取（*disjunction*）**: $P ∨ Q$（$P$ 或 $Q$，当 $P$ 和 $Q$ 中至少有一个为真时为真）

- **否定（*negation*）**: $\neg P$（非 $P$，当 $P$ 为假时为真）

!!! note inline end "排中律"
    对于任意命题 $P$，==要么其为真，要么其否定 $\neg P$ 为真，但二者不会同时为真==：

    $$
    \phi(x) ∨ \neg \phi(x)
    $$

==这类带有变量的陈述被称为**命题形式（*propostiotn forms*）**==

根据**排中律（*law of the excluded middle*）**可得，无论命题 $P$ 的真值如何，$P \vee \neg P$ 恒为真。像这样 ==真值恒为真的命题形式，我们称其为**重言式（*tautology*）**==；反之，像 $P \wedge \neg P$ 这样 ==恒为假的命题形式，则被称为**矛盾式（*contradiction*）**==

在分析命题形式可能取值的过程中，**真值表（*truth table*）**是一个直观高效的工具，其与函数表相同：列出所有可能的输入变量，并给出对应的输出值。

例如否定的真值表：

| $P$ | $\neg P$ |
|:-:|:-:|
|$T$|$F$|
|$F$|$T$|

- **蕴含（*implication*）**: $P \Rightarrow Q$（$P$ 蕴含 $Q$，如果 $P$，那么 $Q$）

    蕴含是最重要且微妙的命题形式。在定义中，$P$ 是蕴含的**前提（*hypothesis*）**，$Q$ 则是**结论（*conclusion*）**

    <!-- [ ] 蕴含实例与真值表 -->

### 量词与括号逻辑规则

#### 量词及其作用域规则

$\forall$ 是**全称量词（*universal quantifier*）**，表示“对于所有”；$\exists$ 是**存在量词（*existential quantifier*）**，表示“存在...（条件）”

在数学逻辑表达式中，常使用括号 $()$、$[]$ 来限定量词的作用域。简单的命题通常遵循以下结构：

$$
(\text{quantifier}\ \text{value}\ \text{domain})(\text{proposition})
$$

例如，有以下命题

$$
(\forall x \in \mathbb{R})(x^2 \geqslant 0)
$$

该命题用自然语言表述即：对于任意实数 $x$，$x^2 \geqslant 0$ 均成立。

- 第一个括号用于定义量词的 ==作用域==，即变量 $x$ 及其定义域

- 第二个括号用于写入量词所 ==约束的命题==，即 $x^2 \geqslant 0$ 这个命题


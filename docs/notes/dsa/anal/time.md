# 算法时间复杂度

>[大话数据结构【溢彩加强版】](https://zh.z-library.sk/book/21866019/61284b/%E5%A4%A7%E8%AF%9D%E6%95%B0%E6%8D%AE%E7%BB%93%E6%9E%84%E6%BA%A2%E5%BD%A9%E5%8A%A0%E5%BC%BA%E7%89%88.html){target="_blank"}
>
>[时间复杂度 | Hello 算法](https://www.hello-algo.com/chapter_computational_complexity/time_complexity/){target="_blank"}


在评估一个算法的效率时，我们的第一反应通常是这个算法处理一定数量的任务需要多少时间；然而，准确计算出一个程序在不同设备上的运行时间是复杂且不现实的，因此我们需要一个通用的方法来衡量算法的运行效率。

## 定义

时间复杂度量化分析的不是算法的运行时间，而是 ==算法运行时长随着其处理的数据量的增加而增长的**趋势**==。

### 函数渐近上界与算法的渐进时间复杂度

==算法时间复杂度分析本质上是计算算法在处理特定问题规模（这个规模我们通常会假定其无穷大）所需“操作数量”的**函数的渐进上界**==，它具有明确的数学定义：

设算法的操作数量是一个关于输入数据大小 $n$ 的函数，记作 $T(n)$，则有定义

!!! important "函数渐近上界"
    若存在正实数 $c$ 和 实数 $n_0$，使得对于对于所有的 $n > n_0$，均有 $T(n) < c \cdot f(n)$，则可认为 $f(n)$ 给出了 $T(n)$ 的一个渐进上界，记作：
    
    $$
    T(n) = O(f(n))
    $$

在数学与计算机科学中，常使用形似 $O(f(n))$ 的形式来表示一个算法的时间复杂度，称为 ==大 $O$ 记法==，是一个**渐进上界**；其中 $f(n)$ 是关于问题规模 $n$ 的某个函数，==通常是一个系数为 $1$ 的**单项式**==。

### 推算 $O(f(n))$

一般分两步可推算出一个算法的时间复杂度：

1. 构造操作数函数 $T(n)$

    其中在构造时可以**忽略操作函数各项的系数以及常数项**，例如有以下程序：

    ```py
    def func(n: int) -> None:
      a = 1     # +1
      a = n + 1 # +1
      
      for i in range(5*n + 1):
        # +5n + 1
        print(n)
      
      for i in range(2 * n):
        for j in range(n + 1):
          # +2n(n + 1)
          print(n)
    ```

    像在注释中这样完全统计上述程序的操作数，则有：

    $$
    \begin{aligned}
      T(n) & = 2 + (5n + 1) + 2n(n + 1) \newline
      & = 2n^2 + 7n + 3
    \end{aligned}
   $$

    但若采用上面提到的技巧，构造的过程就会简单很多：

    ```py
    def func(n: int) -> None:
      a = 1     # 忽略
      a = n + 1 # 忽略
      
      for i in range(5*n + 1):
        # +n
        print(n)
      
      for i in range(2 * n):
        for j in range(n + 1):
          # +n*n
          print(n)
    ```

    即

    $$
    T(n) = n^2 + n
    $$

2. 判断渐进上界

    在数学上我们知道，当一个单调递增的一元函数的自变量（这里就是 $n$）趋于无穷大时，则该函数的**最高阶**在函数递增中发挥主导作用，==故时间复杂度由我们在上一步构造的函数 $T(n)$ 中最高阶的项决定，其他项可忽略==。

    求解一个函数的最高阶本质上就是一个数学问题了，这里不再展开。

## 常见类型

设输入数据大小为 $n(n \in \mathbb{N}^{+})$，则有以下常见类型（增长趋势从左往右从低到高）：

$$
\begin{aligned}
  O(1) < O(\log n) < O(n) < O(n\log n) < O(n^2) < O(2^n) < O(n!) < O(n^n) \newline
  \text{常数阶} < \text{对数阶} < \text{线性阶} < \text{线性对数阶} < \text{平方阶} < \text{指数阶} < \text{阶乘阶} < \text{超指数阶}
\end{aligned}
$$

### 常数阶 $O(1)$

常数阶的操作数与输入数据量无关，即不随输入数据大小的变化而增大，始终为一个常数。

如普通的赋值语句：
```py
def assign(n: int) -> int:
    res = n # 常数阶
    return res
```

!!! warning
    需要注意的是，常数阶的定义是**操作数量与输入数据大小无关**，因此即便一个程序的输入数据大小很大（必须是一个常量），如下面的例子：
    ```py
    def sum_to_const(n: int) -> int:
        """Sum from 0 with step n, size times."""
        count = 0
        size = 10000
        for _ in range(size):
            count += n
        return count
    ```
    这是一个求和函数，用于将输入数据`n`相加`size`次。
    
    虽然我们在编写程序时可以将`size`设置得很大，但在程序运行时，无论输入数据的大小如何，求和的操作次数永远只执行`size`次，即**不随输入数据大小的变化而增大**，因此上面示例的时间复杂度只是一个**常数阶**。

### 线性阶 $O(n)$

线性阶的操作数与输入数据大小 $n$ 呈**线性相关**，常以单层循环的形式出现：

```py
def for_linear(n: int) -> int:
    sum = 0 
    for _ in range(n):
        count += 1
    return sum
```

线性阶算法常出现在[**线性表**](https://www.geeksforgeeks.org/dsa/introduction-to-linear-data-structures/)的遍历中；在这中情景下，输入数据一般为待遍历线性表的长度（或大小）:
```py
def throughout_arr(nums: list[int]) -> int:
    count = 0
    for num in nums:
        count += num
    return count
```

### 平方阶 $O(n^2)$

平方阶的操作数可以看作是输入数据大小 $n$ 的一个二次函数，通常出现在**嵌套循环**中。

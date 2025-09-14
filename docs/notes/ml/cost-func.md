# 成本函数概述

> [Machine Learning | Coursera](https://www.coursera.org/specializations/machine-learning-introduction)

!!! abstract
    简单来说，==**成本函数（*Cost Function*）**是用于衡量模型函数对训练数据的拟合程度的一个**指标函数**==，记作:

    $$
    J(\theta)
    $$

    在线性回归中也可记作

    $$
    J(w, b)
    $$

## 成本函数公式

在机器学习中，需要根据不同的应用场景选择不同的成本函数。

在线性回归中，最常用的成本函数是[均方误差函数](https://www.geeksforgeeks.org/maths/mean-squared-error/)[^1]，即对训练样本中所有预测值与目标值的差的平方求和后求算术平均值:

$$
J(\theta) = \frac{1}{m} \sum_{i=1}^{m}(\hat{y}^{(i)} - y^{(i)})^2
$$

或：

$$
J(w, b) = \frac{1}{m} \sum_{i=1}^{m}(f_{w, b}(x^{(i)}) - y^{(i)})^2
$$

按照惯例，机器学习领域使用的成本函数实际上会除以 $2m$，即:

$$
J(w, b) = \frac{1}{2m} \sum_{i=1}^{m}(f_{w, b}(x^{(i)}) - y^{(i)})^2
$$

额外的除以 $2$ 只是为了让我们后续的一些计算看起来更整洁，但无论你是否包含这个除以 $2$ 的步骤，成本函数仍然有效，==将其看作一个系数即可==。

## 成本函数 vs 模型函数

简单来说，模型函数是预测数据关于输入数据的函数，==而成本函数是**模型参数关于拟合程度**的函数==。

基于成本函数的定义与作用我们不难得出，在训练过程中，==当成本函数的值最小时，对应的模型参数是最优的（拟合程度最好的）==:

$$
\text{Objective} \Rightarrow \text{minimize}_{\theta} J(\theta)
$$


[^1]: [Cost Function in Linear Regression | GeeksForGeeks](https://www.geeksforgeeks.org/machine-learning/what-is-the-cost-function-in-linear-regression/)
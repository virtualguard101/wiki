---
date: 2025-10-18 16:34:46
title: 过拟合问题与正则化
permalink: 
publish: true
---

# 过拟合问题与正则化


## 模型拟合度

在机器学习中，模型拟合度是指模型对**训练数据**的拟合程度。

!!! warning
    注意这里说的是**训练数据**，而非**测试数据**。

    - 前者是用于训练模型的数据，是一个**已知的数据集**，==作为学习算法的**输入**，其对应的**真实标签**（ground truth）是已知的，模型函数对训练数据的**预测值**与**真实标签**之间的差异，就是我们要最小化的损失函数==

    - 后者是来自同一数据分布但**未参与训练**的数据，用于评估模型的**泛化能力**，其真实标签在评估时是已知的（用于计算测试误差）

    理解这二者的区别是理解过拟合问题的基础。

从模型拟合度的角度来看，我们可以将模型拟合度分为以下三种情况：

- **<span style="color: blue;">欠拟合（*Underfitting*）</span>**

    欠拟合是指模型无法很好地拟合训练数据，通常是由于模型过于简单或训练数据不足。欠拟合的模型在训练数据和测试数据上表现都很差。

    以我们之前在学习[模型表示法](model-repr.ipynb#model-function)时所举的[就业率预测模型](regression.md#训练集)的例子为例，当时我们使用的是一个**一元线性回归模型**，从数据集的可视化来看，该模型显然是欠拟合的。

- **<span style="color: green;">最佳拟合（*Best Fit*）</span>**

    最佳拟合是指模型能够很好地拟合训练数据，通常是由于模型复杂度适中或训练数据充足。最佳拟合的模型在训练数据和测试数据上表现都很好。

- **<span style="color: red;">过拟合（*Overfitting*）</span>**

前两者在前面的学习中或多或少都会有所体会，相对较好理解。下面着重学习记录第三者的概念。

## 过拟合问题

在初学者眼中，拟合度或许是越高越好，但事实并非如此。

!!! example
    下面通过模型函数可视化的方式分别举一个回归与分类的例子:

    - 回归

        下图对某个数据集使用一个一元线性回归模型进行拟合，可以看到模型并没有很好地拟合数据，这就是欠拟合:
        ![欠拟合-回归](underfitting_demo1.jpg)

        而将模型函数的最高阶提高至 $4$ 阶后，可以看出模型很好地拟合了数据（与红色虚线基本吻合），这就是最佳拟合:
        ![最佳拟合-回归](bestfit_demo1.jpg)

        但随着最高阶数的继续升高，可以看出模型虽然更好地拟合了训练数据，即穿过了更多的数据点，但不难发现在本应该接近 $y=0$ 的区域，模型却出现了剧烈的波动，这就是过拟合的一种表现:
        ![过拟合-回归](overfit_demo1.jpg)
    
    - 分类同理

        ![欠拟合-分类](underfit_demo2.jpg)

        ![最佳拟合-分类](bestfit_demo2.jpg)

        ![过拟合-分类](overfit_demo2.jpg)


通过以上例子，就不难理解过拟合问题的本质，即会导致模型在训练数据上表现良好，而在测试数据上表现较差，即模型的**泛化能力较差**。

!!! tip "泛化能力"
    泛化能力是指模型对未知数据的预测能力。可通过一个有意思的例子理解其概念:
    
    想象一下，你是一个学生，如果只是死记硬背课本上的例题，在考试时遇到稍微变化的新题目就会束手无策。机器学习模型也是如此：
    
    - **训练数据** = 课本例题（已知答案）

    - **测试数据** = 考试新题（需要推理能力）

    - **泛化能力** = 举一反三的能力
    
    一个具有良好泛化能力的模型，就像是一个真正理解了知识本质的学生，能够处理各种变化的情况。

这里注意到还有一个可供调节的参数 $\lambda$，这就所谓的**正则化参数**，与接下来要学习的**正则化**相关。

## 正则化

### 什么是正则化

正则化是一种**用于解决过拟合问题**的技术。它通过在成本函数中添加一个正则化项，来约束模型的复杂度。

!!! abstract
    正则化本质上就是在原始成本函数基础上添加一个**复杂度惩罚项**，形成新的目标函数：

    $$
    J(\theta) = L(\theta) + \lambda \cdot R(\theta)
    $$

    其中:

    - $\lambda$ 是正则化参数，控制正则化强度

    - $L(\theta)$ 是原始成本函数

    - $R(\theta)$ 是正则化项

!!! tip "正则化项的作用机制"
    正则化项是一个**惩罚项**，用于惩罚模型的复杂度：
    
    - **$\lambda = 0$**：不使用正则化，模型完全依赖训练数据拟合

    - **$\lambda$ 增大**：正则化强度增强，模型复杂度被约束，效果相当于减少模型的参数数量

    - **$\lambda$ 过大**：可能导致欠拟合，模型过于简单
    
    以在过拟合中提到的学生的例子为例，把 $\lambda$ 想象成"学习时的约束条件"：

    - 没有约束（$\lambda = 0$）→ 学生可能过度学习，死记硬背

    - 适度约束（$\lambda$ 适中）→ 学生学会举一反三，真正理解

    - 过度约束（$\lambda$ 过大）→ 学生学得太浅，连基础都掌握不好

### 数学模型与代码实现

基于上面的概念，我们得知正则化本质上就是在原始成本函数基础上添加一个**复杂度惩罚项**形成新的目标函数，故其通用的数学模型可用如下公式表示：

$$
J(\theta) = L(\theta) + \lambda \cdot R(\theta)
$$

其中:

- $\lambda$ 是正则化参数，控制正则化强度

- $L(\theta)$ 是原始成本函数

- $R(\theta)$ 是正则化项

下面分别以线性回归与逻辑回归为例，给出它们成本函数的正则化形式与代码实现:

#### 正则化线性回归的成本函数

$$
J(\overrightarrow{w}, b) = \frac{1}{2m} \sum_{i=1}^{m} (f_{\overrightarrow{w}, b}(\overrightarrow{x}^{(i)}) - y^{(i)})^2 + \frac{\lambda}{2m} \cdot R(\overrightarrow{w})
$$

其中:

- $f_{\overrightarrow{w}, b}(\overrightarrow{x}^{(i)})$ 是模型函数:

    $$
    f_{\overrightarrow{w}, b}(\overrightarrow{x}^{(i)}) = \overrightarrow{w} \cdot \overrightarrow{x}^{(i)} + b
    $$

- $R(\overrightarrow{w})$ 是正则化项:

    $$
    R(\overrightarrow{w}) = \sum_{j=1}^{n} w_j^2
    $$

    加入这一项会促使梯度下降算法减小模型的参数，从而避免过拟合。

代码实现如下:

```py
def compute_cost_linear_reg(X, y, w, b, lambda_ = 1):
    """
    Computes the cost over all examples
    Args:
      X (ndarray (m,n): Data, m examples with n features
      y (ndarray (m,)): target values
      w (ndarray (n,)): model parameters  
      b (scalar)      : model parameter
      lambda_ (scalar): Controls amount of regularization
    Returns:
      total_cost (scalar):  cost 
    """

    m  = X.shape[0]
    n  = len(w)
    cost = 0.
    for i in range(m):
        f_wb_i = np.dot(X[i], w) + b                                   #(n,)(n,)=scalar, see np.dot
        cost = cost + (f_wb_i - y[i])**2                               #scalar             
    cost = cost / (2 * m)                                              #scalar  
 
    reg_cost = 0
    for j in range(n):
        reg_cost += (w[j]**2)                                          #scalar
    reg_cost = (lambda_/(2*m)) * reg_cost                              #scalar
    
    total_cost = cost + reg_cost                                       #scalar
    return total_cost                                                  #scalar
```

#### 正则化逻辑回归的成本函数

$$
J(\overrightarrow{w}, b) = \frac{1}{m} \sum_{i=1}^{m} [ -y^{(i)} \log(f_{\overrightarrow{w}, b}(\overrightarrow{x}^{(i)})) - (1 - y^{(i)}) \log(1 - f_{\overrightarrow{w}, b}(\overrightarrow{x}^{(i)}))] + \frac{\lambda}{2m} \cdot R(\overrightarrow{w})
$$

其中:

- $f_{\overrightarrow{w}, b}(\overrightarrow{x}^{(i)})$ 是模型函数:

    $$
    f_{\overrightarrow{w}, b}(\overrightarrow{x}^{(i)}) = \sigma(\overrightarrow{w} \cdot \overrightarrow{x}^{(i)} + b)
    $$

- $R(\overrightarrow{w})$ 是正则化项:

    $$
    R(\overrightarrow{w}) = \sum_{j=1}^{n} w_j^2
    $$

代码实现如下:

```py
def compute_cost_logistic_reg(X, y, w, b, lambda_ = 1):
    """
    Computes the cost over all examples
    Args:
    Args:
      X (ndarray (m,n): Data, m examples with n features
      y (ndarray (m,)): target values
      w (ndarray (n,)): model parameters  
      b (scalar)      : model parameter
      lambda_ (scalar): Controls amount of regularization
    Returns:
      total_cost (scalar):  cost 
    """

    m,n  = X.shape
    cost = 0.
    for i in range(m):
        z_i = np.dot(X[i], w) + b                                      #(n,)(n,)=scalar, see np.dot
        f_wb_i = sigmoid(z_i)                                          #scalar
        cost +=  -y[i]*np.log(f_wb_i) - (1-y[i])*np.log(1-f_wb_i)      #scalar
             
    cost = cost/m                                                      #scalar

    reg_cost = 0
    for j in range(n):
        reg_cost += (w[j]**2)                                          #scalar
    reg_cost = (lambda_/(2*m)) * reg_cost                              #scalar
    
    total_cost = cost + reg_cost                                       #scalar
    return total_cost                                                  #scalar
```

## 带正则化的梯度下降

### 数学模型

$$
\begin{aligned}
\frac{\partial J(\theta)}{\partial \theta_j} &= \frac{\partial L(\theta)}{\partial \theta_j} + \lambda \cdot \frac{\partial R(\theta)}{\partial \theta_j} \\
&= \frac{1}{m} \sum_{i=1}^{m} (f_{\theta}(\overrightarrow{x}^{(i)}) - y^{(i)}) \cdot x_j^{(i)} + \lambda \cdot \frac{1}{m} \sum_{i=1}^{m} w_j \\
&= \frac{1}{m} \sum_{i=1}^{m} (f_{\theta}(\overrightarrow{x}^{(i)}) - y^{(i)}) \cdot x_j^{(i)} + \frac{\lambda}{m} \cdot w_j
\end{aligned}
$$

常数项 $b$ 不参与正则化，故其梯度下降公式与原来保持一致:

$$
\begin{aligned}
\frac{\partial J(\theta)}{\partial b} &= \frac{\partial L(\theta)}{\partial b} \\
&= \frac{1}{m} \sum_{i=1}^{m} (f_{\theta}(\overrightarrow{x}^{(i)}) - y^{(i)})
\end{aligned}
$$

迭代公式:

$$
\begin{aligned}
\theta_j &= \theta_j - \alpha \cdot \frac{\partial J(\theta)}{\partial \theta_j} \\
b &= b - \alpha \cdot \frac{\partial J(\theta)}{\partial b}
\end{aligned}
$$

在先前的学习我们知道，[线性回归模型](linear-grad-desent.ipynb)与[逻辑回归模型](logistic-grad-desent.ipynb)的梯度下降几乎没有差异，仅在 $f_{\theta}(\overrightarrow{x}^{(i)})$ 有所不同:

- 对于线性回归模型而言，$f_{\theta}(\overrightarrow{x}^{(i)})$ 为:

    $$
    f_{\overrightarrow{w}, b}(\overrightarrow{x}^{(i)}) = \overrightarrow{w} \cdot \overrightarrow{x}^{(i)} + b
    $$

- 对于逻辑回归模型而言，$f_{\theta}(\overrightarrow{x}^{(i)})$ 为:

    $$
    f_{\overrightarrow{w}, b}(\overrightarrow{x}^{(i)}) = \sigma(\overrightarrow{w} \cdot \overrightarrow{x}^{(i)} + b)
    $$

在上面的数学表达式中:

- $m$ 为训练集中训练样本的数量

- $f_{\theta}(\overrightarrow{x}^{(i)})$ 为模型的预测值，$y^{(i)}$ 为目标值

### 代码实现

- 线性回归模型

    ```py
    def compute_gradient_linear_reg(X, y, w, b, lambda_): 
        """
        Computes the gradient for linear regression 
        Args:
        X (ndarray (m,n): Data, m examples with n features
        y (ndarray (m,)): target values
        w (ndarray (n,)): model parameters  
        b (scalar)      : model parameter
        lambda_ (scalar): Controls amount of regularization
        
        Returns:
        dj_dw (ndarray (n,)): The gradient of the cost w.r.t. the parameters w. 
        dj_db (scalar):       The gradient of the cost w.r.t. the parameter b. 
        """
        m,n = X.shape           #(number of examples, number of features)
        dj_dw = np.zeros((n,))
        dj_db = 0.

        for i in range(m):                             
            err = (np.dot(X[i], w) + b) - y[i]                 
            for j in range(n):                         
                dj_dw[j] = dj_dw[j] + err * X[i, j]               
            dj_db = dj_db + err                        
        dj_dw = dj_dw / m                                
        dj_db = dj_db / m   
        
        for j in range(n):
            dj_dw[j] = dj_dw[j] + (lambda_/m) * w[j]

        return dj_db, dj_dw
    ```

- 逻辑回归模型

    ```py
    def compute_gradient_logistic_reg(X, y, w, b, lambda_): 
        """
        Computes the gradient for linear regression 
    
        Args:
        X (ndarray (m,n): Data, m examples with n features
        y (ndarray (m,)): target values
        w (ndarray (n,)): model parameters  
        b (scalar)      : model parameter
        lambda_ (scalar): Controls amount of regularization
        Returns
        dj_dw (ndarray Shape (n,)): The gradient of the cost w.r.t. the parameters w. 
        dj_db (scalar)            : The gradient of the cost w.r.t. the parameter b. 
        """
        m,n = X.shape
        dj_dw = np.zeros((n,))                            #(n,)
        dj_db = 0.0                                       #scalar

        for i in range(m):
            f_wb_i = sigmoid(np.dot(X[i],w) + b)          #(n,)(n,)=scalar
            err_i  = f_wb_i  - y[i]                       #scalar
            for j in range(n):
                dj_dw[j] = dj_dw[j] + err_i * X[i,j]      #scalar
            dj_db = dj_db + err_i
        dj_dw = dj_dw/m                                   #(n,)
        dj_db = dj_db/m                                   #scalar

        for j in range(n):
            dj_dw[j] = dj_dw[j] + (lambda_/m) * w[j]

        return dj_db, dj_dw  
    ```

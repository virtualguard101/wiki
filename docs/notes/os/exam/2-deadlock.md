---
date: 2025-10-24 21:45:33
title: 死锁
permalink: 
publish: true
---

# 死锁

## 什么是死锁

<strong>死锁（*Deadlock*）</strong>是操作系统中的一个经典问题，指的是两个或多个进程因为互相等待对方释放资源而永远阻塞的状态。形象地说，就是两个或多个进程在等待对方手里的资源，而对方也在等待对方手里的资源，从而形成了一个死循环。

## 死锁产生的原因

- 竞争不可抢占资源

- 竞争可消耗性资源

- 进程推进顺序不当

## 死锁的必要条件

死锁的发生需要同时满足以下四个条件：

- 互斥条件

- 请求并保持条件

- 不可剥夺条件

- 循环等待条件

## 死锁避免

### 系统安全状态

指系统能按照某种进程推进顺序为某个进程 $P_i$ 分配其所需资源，使得每个进程都能顺利完成；这个推进顺序称为**安全序列**。

安全序列可能不止一个，但只要能找出一个安全序列，系统就是安全的。

### 银行家算法

之所以叫"银行家算法"，是因为该算法最早用于银行贷款问题的解决。银行在放贷前，需要检查能否找到一个顺序让所有客户都还清贷款，如果能，这次安全放贷；否则拒绝放贷。

### 数据结构描述

- `Available[m]`: 当前系统各类资源可用数量

- `Max[n][m]`: 进程 $i$ 对资源 $j$ 的最大需求量

- `Allocation[n][m]`: 进程 $i$ 已分配的各类资源数量

- `Need[n][m]`: 进程 $i$ 还需的各类资源数量

其中 `Need[i][j] = Max[i][j] - Allocation[i][j]`

### 检查流程

1. 初始化

   `Work = Available`: 当前可用资源

   `Finish[i] = false`: 所有进程未完成

2. 寻找可执行的进程
   找到一个 `Finish[i] == false` 且 `Need[i] <= Work` 的进程 $P_i$
   
3. 如果找到

   `Work = Work + Allocation[i]`: 进程完成后释放资源

   `Finish[i] = true`: 进程已完成

   重复步骤 2
   
4. 如果所有 `Finish[i] == true`

   系统处于安全状态，存在安全序列；否则，系统处于不安全状态

```py
def banker_algorithm(processes, resources, available, max_need, allocation):
    """
    银行家算法的安全性检查
    """
    n = len(processes)  # 进程数
    m = len(resources)  # 资源种类数
    
    # 计算 Need 矩阵
    need = [[max_need[i][j] - allocation[i][j] 
             for j in range(m)] for i in range(n)]
    
    # 初始化
    work = available.copy()
    finish = [False] * n
    safe_sequence = []
    
    # 寻找安全序列
    while len(safe_sequence) < n:
        found = False
        for i in range(n):
            if not finish[i]:
                # 检查 Need[i] <= Work
                if all(need[i][j] <= work[j] for j in range(m)):
                    # 进程可以执行
                    work = [work[j] + allocation[i][j] for j in range(m)]
                    finish[i] = True
                    safe_sequence.append(processes[i])
                    found = True
                    break
        
        if not found:
            # 无法找到可执行进程，系统不安全
            return False, []
    
    return True, safe_sequence
```

### 资源请求处理

当进程 `P_i` 请求资源 `Request[i]` 时：

1. 检查合法性

   当 `Request[i] > Need[i]` 时，拒绝（请求超过需要量）
   
2. 检查可用性

   当 `Request[i] > Available` 时，等待（资源不足）
   
3. 尝试分配（临时）

   `Available = Available - Request[i]`

   `Allocation[i] = Allocation[i] + Request[i]`

   `Need[i] = Need[i] - Request[i]`
   
4. 安全性检查

   如果系统安全，则批准分配（保持不变）；否则，撤销分配（回滚），拒绝请求，进程等待

```py
# 资源请求处理
def request_resources(process_id, request, available, need, allocation):
    """
    处理进程的资源请求
    """
    m = len(request)
    
    # 1. 检查请求合法性
    if any(request[j] > need[process_id][j] for j in range(m)):
        return False, "Request exceeds need"
    
    # 2. 检查资源可用性
    if any(request[j] > available[j] for j in range(m)):
        return False, "Insufficient resources, need to wait"
    
    # 3. 尝试分配（模拟）
    temp_available = [available[j] - request[j] for j in range(m)]
    temp_allocation = [allocation[process_id][j] + request[j] 
                       for j in range(m)]
    temp_need = [need[process_id][j] - request[j] for j in range(m)]
    
    # 4. 安全性检查（需要调用上面的 banker_algorithm）
    # 如果安全，则正式分配；否则撤销
    
    return True, "Allocation successful"
```

!!! example
    假设一个操作系统中有 3 个进程（P0, P1, P2）和 3 种资源（A=10, B=5, C=7）。

    初始状态如下：
    <table>
    <thead>
    <tr>
    <th style="text-align: center;">进程</th>
    <th style="text-align: center;">Max<br>A B C</th>
    <th style="text-align: center;">Allocation<br>A B C</th>
    <th style="text-align: center;">Need<br>A B C</th>
    <th style="text-align: center;">Available<br>A B C</th>
    </tr>
    </thead>
    <tbody>
    <tr>
    <td style="text-align: center;">P0</td>
    <td style="text-align: center;">7 5 3</td>
    <td style="text-align: center;">0 1 0</td>
    <td style="text-align: center;">7 4 3</td>
    <td style="text-align: center;" rowspan="3">3 3 2</td>
    </tr>
    <tr>
    <td style="text-align: center;">P1</td>
    <td style="text-align: center;">3 2 2</td>
    <td style="text-align: center;">2 0 0</td>
    <td style="text-align: center;">1 2 2</td>
    </tr>
    <tr>
    <td style="text-align: center;">P2</td>
    <td style="text-align: center;">9 0 2</td>
    <td style="text-align: center;">3 0 2</td>
    <td style="text-align: center;">6 0 0</td>
    </tr>
    </tbody>
    </table>

    1. 求出 Need 矩阵

        $$
        Need = Max - Allocation = \begin{pmatrix}
            7 & 4 & 3 \\
            1 & 2 & 2 \\
            6 & 0 & 0
        \end{pmatrix}
        $$

    2. 设置 Work 向量

        初始值为 $Available: (3, 3, 2)$

        然后遍历 $Need$ 矩阵，找到一个 `Need[i] <= Work` 的进程 $P_i$，然后执行该进程，并更新 $Work$

        $$
        Work = Work + Allocation[i]
        $$

        比如 $Need[1] = (1, 2, 2) <= (3, 3, 2)$，执行 $P_1$ 后，更新 $Work$ 为 $(3, 3, 2) + (2, 0, 0) = (5, 3, 2)$

    3. 重复步骤 2，直到所有进程都执行完毕

    4. 如果所有进程都执行完毕，则系统处于安全状态，否则系统处于不安全状态

        这里可以得到安全序列 $\{P1, P2, P0\}$

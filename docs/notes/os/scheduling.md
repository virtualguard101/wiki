---
date: 2025-10-23 01:00:51
title: 处理机调度
permalink: 
publish: true
---

# 处理机调度

## 处理机调度层次

### 高级调度

高级调度又称为**作业调度**或**长程调度**。其主要功能是根据某种算法，决定将外存上处于后备队列中的哪些作业调入内存，为它们创建进程、分配必要资源，并放入就绪队列。

简单来说，==高级调度用于决定哪些**作业**可以进入内存运行==。

高级调度主要用于**多道批处理系统**，分时系统与实时系统不设置高级调度。

### 中级调度

中级调度又称**内存调度**，其主要目的是提高内存利用率和系统吞吐量，改善系统性能。

为实现这一目的，中级调度需要完成两项工作（“对换”功能）：

- 将暂不运行的进程调至外存等待

- 将存于外存上急需运行的进程调入内存运行

### 低级调度

低级调度也称为**进程调度**或**短程调度**。其主要功能是按照某种算法，==决定就绪队列中的哪个**进程（或[内核级线程](process.md#内核支持线程)）**获得处理机资源==。

低级调度是操作系统中**最为活跃的调度**，因此其算法设计的好坏直接影响到系统的性能。

多道批处理系统、分时系统、实时系统均有应用低级调度。

## 处理机调度算法

### 调度算法的目标

#### 共同目标

- **资源利用率**: 使系统中的处理机和其他所有资源都尽可能地**保持忙碌**状态

- **公平性**: 确保每个进程都能获得合理的CPU时间，避免某些进程**饥饿**

    !!! info "饥饿"
        饥饿（*starvation*）是指进程因为某种原因**长时间无法获得所需资源（特别是CPU时间）**，导致无法继续执行的现象

- **平衡性**: 根据资源使用情况，可将系统中的进程划分为**计算密集型**与**I/O密集型**。调度算法应尽可能保持系统资源使用的平衡性，从而满足第一条目标。

    !!! info "计算密集型与I/O密集型进程"
        - **计算密集型进程**：需要大量CPU计算资源的进程，如科学计算、图像处理等

        - **I/O密集型进程**：需要大量I/O操作的进程，如文件读写、网络通信等

- **策略强制执行**: 对于所制定的策略（包括安全策略等），只要需要，必须予以准确地执行，即使会造成某些工作的延迟

#### 部分评价指标

- CPU利用率

    $$
    \text{CPU利用率} = \frac{\text{CPU有效工作时间}}{\text{CPU有效工作时间} + \text{CPU空闲等待时间}}
    $$

- 周转时间

    从作业提交到系统开始到作业完成的时间间隔。

    - ==**平均周转时间**: 所有作业的周转时间之和与作业个数之比==

        $$
        T = \frac{1}{n} \sum_{i=1}^{n} T_i
        $$

    - **带权周转时间**: 权值为作业周转时间 $T_i$ 与系统为之服务时间 $T_s$ 之比

        $$
        T_{W_i} = \frac{T_i}{T_s}
        $$

    - ==**平均带权周转时间**: 所有作业的带权周转时间之和与作业个数之比==

        $$
        T_{W} = \frac{1}{n} \sum_{i=1}^{n} T_{W_i} = \frac{1}{n} \sum_{i=1}^{n} \frac{T_i}{T_s}
        $$

- 响应时间: 从作业提交到首次产生响应的时间间隔。

- 等待时间（进程调度）: 进程在就绪队列中等待处理机的时间之和。

#### 批处理系统的目标

- 平均周转时间短

- 系统吞吐量高

- 处理机利用率高

#### 分时系统的目标

- 响应时间短

- 均衡性

#### 实时系统的目标

- 保证满足截止时间的要求

- 保证可预测性

### 调度算法

#### 概述

调度算法按照服务对象可分为**作业调度算法**与**进程调度算法**，分别对应[前文](#处理机调度层次)提到的高级调度与低级调度。

常见的作业调度算法有：

- 先来先服务（FCFS）

- 短作业优先（SJF）

- 优先级调度（PR）

- 最高响应比优先（HRRN）

常见的进程调度算法有：

- 先来先服务（FCFS）

- 短作业优先（SJF）

- 优先级调度（PR）

- 时间片轮转（RR）

- 多级队列（MQ）

- 多级反馈队列（MLFQ）

- 公平调度（Fair）

- 公平共享调度（Fair Share）

#### 先来先服务

##### 定义

<strong>先来先服务（*First Come First Served, FCFS*）</strong>调度算法是最简单的调度算法，既可以用于作业调度，也可以用于进程调度。顾名思义，其基本思想是按照作业到达的先后顺序进行调度。

```cpp
// 伪代码示例
void FCFS_Scheduler() {
    while (!ready_queue.empty()) {
        Process current = ready_queue.front();  // 取队首进程
        ready_queue.pop();
        
        execute_process(current);  // 执行到完成
    }
}
```

##### 特点与优缺点

1. 非抢占式调度：一旦进程开始执行，就会一直运行到完成

2. 按到达时间排序：严格按照进程到达就绪队列的时间顺序进行调度

3. 简单公平：实现简单，对所有进程一视同仁

- 优点

    - 实现简单：逻辑清晰，易于理解和实现

    - 公平性：所有进程按到达顺序获得服务

    - 无饥饿现象：每个进程最终都会被执行

- 缺点

    - 护航效应：短进程可能被长进程阻塞

        !!! info "护航效应"
            护航效应（*convoy effect*）是指长进程会阻塞短进程的执行，导致短进程的响应时间变长。

            想象一下，如果有一个执行时间很长的进程排在队列前面，后面所有进程都要等待它完成。就像高速公路上的慢车，会拖慢整条车流的速度。

    - 平均等待时间长：特别是当短进程排在长进程后面时

    - 响应时间差：不适合交互式系统

!!! example
    假设有三个进程：

    - 进程A：到达时间0，执行时间3

    - 进程B：到达时间1，执行时间1

    - 进程C：到达时间2，执行时间2

    使用先来先服务调度算法，甘特图（Gantt Chart）如下：

    ```
    时间轴: 0----1----2----3----4----5----6
    进程A:  [==============]
    进程B:       [----------====]
    进程C:            [----------=========]
    ```
    
    性能指标：

    - 进程A：等待时间 $0$，周转时间 $3$

    - 进程B：等待时间 $2$，周转时间 $3$

    - 进程C：等待时间 $2$，周转时间 $4$

    **平均等待时间**: $\frac{0+2+2}{3} = 1.33$

    **平均周转时间**: $\frac{3+3+4}{3} = 3.33$

#### 短作业优先

##### 定义

顾名思义，<strong>短作业优先（*Short Job First, SJF*）</strong>以作业（或进程）执行时间的长短来决定调度的优先级，时间越短，优先级越高。

SJF 既可以用于作业调度，也可以用于进程调度

- 针对作业调度，SJF 从后备队列中选择若干估计运行时间最短的作业，将它们调入内存运行

- 针对进程调度，SJF 关联到每个进程下次运行的CPU区间长度，调度最短的进程执行

    - 另外，针对进程调度，SJF 有两种模式:

        - **非抢占式SJF**: 一旦进程开始执行，就会一直运行到完成

        - **抢占式SJF（Shortest Remaining Time First, SRTF）**: 进程执行一段时间后，如果新的进程进入就绪队列，且新进程的执行时间比当前进程的剩余执行时间短，则新进程会抢占当前进程，当前进程会重新进入就绪队列

```cpp
// 非抢占式SJF调度算法
void nonPreemptiveSJF(vector<Process>& processes) {
    int n = processes.size();
    int currentTime = 0;
    vector<bool> completed(n, false);
    
    cout << "Non-preemptive SJF scheduling order:\n";
    
    for (int i = 0; i < n; i++) {
        // 找到当前时间已到达且未完成的最短作业
        int shortestIndex = -1;
        int shortestTime = INT_MAX;
        
        for (int j = 0; j < n; j++) {
            if (!completed[j] && 
                processes[j].arrivalTime <= currentTime && 
                processes[j].burstTime < shortestTime) {
                shortestTime = processes[j].burstTime;
                shortestIndex = j;
            }
        }
        
        if (shortestIndex == -1) {
            // 没有进程到达，等待下一个进程到达
            int nextArrival = INT_MAX;
            for (int j = 0; j < n; j++) {
                if (!completed[j]) {
                    nextArrival = min(nextArrival, processes[j].arrivalTime);
                }
            }
            currentTime = nextArrival;
            i--; // 重新尝试
            continue;
        }
        
        // 执行选中的进程
        Process& p = processes[shortestIndex];
        p.completionTime = currentTime + p.burstTime;
        p.turnaroundTime = p.completionTime - p.arrivalTime;
        p.waitingTime = p.turnaroundTime - p.burstTime;
        
        cout << "Process P" << p.id << " execution time: " << currentTime 
             << " - " << p.completionTime << endl;
        
        currentTime = p.completionTime;
        completed[shortestIndex] = true;
    }
}
```

```cpp

// 抢占式SJF调度算法
void preemptiveSJF(vector<Process>& processes) {
    int n = processes.size();
    int currentTime = 0;
    int completed = 0;
    
    // 初始化剩余时间
    for (auto& p : processes) {
        p.remainingTime = p.burstTime;
    }
    
    cout << "Preemptive SJF scheduling order:\n";
    
    while (completed < n) {
        // 找到当前时间已到达且剩余时间最短的进程
        int shortestIndex = -1;
        int shortestTime = INT_MAX;
        
        for (int i = 0; i < n; i++) {
            if (processes[i].remainingTime > 0 && 
                processes[i].arrivalTime <= currentTime && 
                processes[i].remainingTime < shortestTime) {
                shortestTime = processes[i].remainingTime;
                shortestIndex = i;
            }
        }
        
        if (shortestIndex == -1) {
            // 没有进程可执行，跳到下一个到达时间
            int nextArrival = INT_MAX;
            for (int i = 0; i < n; i++) {
                if (processes[i].remainingTime > 0) {
                    nextArrival = min(nextArrival, processes[i].arrivalTime);
                }
            }
            currentTime = nextArrival;
            continue;
        }
        
        Process& p = processes[shortestIndex];
        
        // 检查是否有新进程到达并可能抢占
        bool preempted = false;
        for (int i = 0; i < n; i++) {
            if (processes[i].arrivalTime == currentTime + 1 && 
                processes[i].remainingTime < p.remainingTime) {
                // 新进程到达且更短，当前进程被抢占
                cout << "Process P" << p.id << " preempted, execution time: " 
                     << currentTime << " - " << currentTime + 1 << endl;
                p.remainingTime -= 1;
                currentTime++;
                preempted = true;
                break;
            }
        }
        
        if (!preempted) {
            // 执行到完成
            cout << "Process P" << p.id << " execution time: " << currentTime 
                 << " - " << currentTime + p.remainingTime << endl;
            
            currentTime += p.remainingTime;
            p.remainingTime = 0;
            p.completionTime = currentTime;
            p.turnaroundTime = p.completionTime - p.arrivalTime;
            p.waitingTime = p.turnaroundTime - p.burstTime;
            completed++;
        }
    }
}
```

##### 特点与优缺点

对于平均等待时间而言，SJF是最优的（对一组指定的进程而言），它给出了最短的平均等待时间。

- 优点

    - 平均等待时间最短：数学上可证明SJF能给出最优解

    - 系统吞吐量高：短作业快速完成，释放资源

    - 简单直观：逻辑清晰，易于理解

- 缺点

    - 长作业饥饿：长作业可能永远得不到执行

    - 需要预知时间：实际中很难准确预测执行时间

    - 不公平：对长作业用户不友好

!!! example
    假设有四个进程:

    | 进程 | 到达时间 | 执行时间 |
    |:----:|:--------:|:--------:|
    | A    | 0        | 5        |
    | B    | 1        | 4        |
    | C    | 2        | 2        |
    | D    | 3        | 3        |

    - 使用非抢占式SJF调度算法，甘特图如下：

        ```
        时间轴: 0----1----2----3----4----5----6----7----8----9----10----11----12----13----14
        进程A:  [========================]
        进程B:       [------------------------------====================]
        进程C:            [---------------=========]
        进程D:                 [-----------------------------------------==================]
        ```

        性能指标:

        - 进程A: 等待时间 $0$，周转时间 $7$

        - 进程B: 等待时间 $6$，周转时间 $10$

        - 进程C: 等待时间 $3$，周转时间 $5$

        - 进程D: 等待时间 $8$，周转时间 $11$

        **平均等待时间**: $\frac{0+6+3+8}{4} = 4.25$

        **平均周转时间**: $\frac{7+10+5+11}{4} = 8.25$

    - 若使用抢占式SJF调度算法，则甘特图如下：

        ```
        时间轴: 0----1----2----3----4----5----6----7----8----9----10----11----12----13----14
        进程A:  [=========----------===============]
        进程B:       [--------------------------------------------=========================]
        进程C:            [=========]
        进程D:                 [-------------------===============]
        ```

        性能指标:

        - 进程A: 等待时间 $2$，周转时间 $7$

        - 进程B: 等待时间 $9$，周转时间 $13$

        - 进程C: 等待时间 $0$，周转时间 $2$

        - 进程D: 等待时间 $4$，周转时间 $7$

        **平均等待时间**: $\frac{2+9+0+4}{4} = 3.75$

        **平均周转时间**: $\frac{7+13+2+7}{4} = 7.25$

#### 优先级调度

##### 定义

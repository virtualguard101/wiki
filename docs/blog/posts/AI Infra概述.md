---
title: AI Infra概述
date: 2026-02-23 16:00:00
excerpt: 去年11月份在CS的学习生涯中遭遇了瓶颈，加上连续遭遇生理与心理上的双重打击，消沉了一段时间。考虑到接下来学业方面大概率以推进11408为主，在研究与工程方面上决定尽可能寻找一个贴近计算机基础学科的方向。经过一段时间的观察与思考，截至写这篇文章时，准备将AI Infra作为日后的主要研究方向.
cover:
categories: 
  - Projects
tags:
  - AI Infra
  - Blog
authors:
  - virtualguard101
mermaid: true
---

**去年11月份在CS的学习生涯中遭遇了瓶颈，加上连续遭遇生理与心理上的双重打击，消沉了一段时间。考虑到接下来学业方面大概率以推进11408为主，在研究与工程方面上决定尽可能寻找一个贴近<i>计算机基础学科</i>的方向。经过一段时间的观察与思考，截至写这篇文章时，准备将<i>AI Infra</i>作为日后的主要研究方向**。

AI Infra（AI Infrastructure, AI基础设施）技术栈[^1]，是支撑现代大模型训练、微调、推理、服务化部署和AI Agent运行的整套软硬件体系。它不像传统后端服务那样“搭几台服务器装个k8s”就行，而是高度依赖计算效率、成本控制、稳定性和弹性。

AI Infra 并非单一技术模块，而是通过硬件与软件的深度协同，构建起支撑 AI 大模型任务全流程的技术底座，其核心特征在于“垂直整合”，从物理硬件到上层工具，各环节形成闭环，确保 AI 计算高效、稳定落地[^2]。

<!-- more -->

## AI Infra技术栈分层

自底向上，AI Infra 可分为**硬件层**和**软件层**，软件层又可分为**资源调度&管理层**、**编译&计算架构**、**模型训练&推理框架**、**第三方框架**、**大模型&应用层**、**数据&存储层**等。若系统庞大，还会设置**观测/运维层**以方便对系统进行监控与维护。

```
应用层（LLM / CV / ASR）
        ↓
推理引擎 / 训练框架
        ↓
通信库 + 调度器
        ↓
Kubernetes + 容器
        ↓
OS + 驱动
        ↓
GPU / Network / Storage
```

### 硬件层

![](https://pica.zhimg.com/80/v2-8bc58636edd071cb09538ac7071367c6_1440w.webp?source=2c26e567)

硬件层面虽然看似简单，但是却是AI Infra领域投入成本最大的部分，是 AI Infra 的“骨架”。

如上图[^2]，其主要模块可以根据职能划分为**AI芯片（计算）**、**存储系统（存储）**、**高性能网卡（通信）**。

形成一个AI集群，需要合理组合这些硬件模块，并利用软件层中的**IaaS（Infrastructure as a Service）**实现对资源的高效管理与调度。

### 软件层

![](https://picx.zhimg.com/80/v2-8f9bbcc77dba850c42d36d6c15610b2a_1440w.webp?source=2c26e567)

软件层主要负责高效处理数据流动和资源管理与调度，AI Infra 的 “神经中枢”。可参考云计算[^3]中的架构层次将其划分为如下几个层次:

- **IaaS（Infrastructure as a Service, 基础设施即服务）层**: 聚焦*资源落地*，整合分散的计算、存储和网络资源，满足 AI 任务对海量数据的存储与快速读取需求，核心解决“计算、通信、存储”三大底层需求。除了后端所熟知的容器化技术（[Docker](https://www.docker.com/)等）、分布式调度框架（[Kubernetes](https://kubernetes.io/)等）外，还有网络层（Interconnect & Cluster Network）的分布式训练与通信技术（[Horovod](https://github.com/horovod/horovod)、[NCCL](https://github.com/NVIDIA/nccl)、[Gloo](https://github.com/facebookincubator/gloo)等）；存储层（Storage Layer）的分布式存储技术（[Ceph](https://github.com/ceph/ceph)、[Lustre](https://github.com/lustre/lustre)、[MinIO](https://github.com/minio/minio)等）。

- **PaaS（Platform as a Service, 平台即服务）层**: 聚焦*硬件衔接与模型开发*，负责编译上层代码、优化核心算子、将底层细节封装起来，提供模型搭建与训练的基础工具，从而提高算力利用率、降低底层基础门槛。如底层算子加速库（[NVIDIA cuDNN](https://github.com/NVIDIA/cudnn)、[TensorFlow XLA](https://github.com/tensorflow/tensorflow/tree/master/tensorflow/compiler/xla)、[RAPIDS](https://github.com/rapidsai/rapids)等）；深度学习框架（[PyTorch](https://pytorch.org/)、[TensorFlow](https://www.tensorflow.org/)、[Jax](https://github.com/google/jax)等）；推理加速框架（[NVIDIA TensorRT](https://github.com/NVIDIA/TensorRT)、[vLLM](https://github.com/vllm-project/vllm)、[ONNX Runtime](https://github.com/microsoft/onnxruntime)等）。

- **SaaS（Software as a Service, 软件即服务）层**: 聚焦*AI任务的“高效执行”*，而非通用应用。核心包含推理服务，如 [Triton Inference Server](https://github.com/triton-inference-server/server)，实现模型部署后的低延迟、高并发响应，支持动态批处理、模型动态加载；分布式并行框架，如 [DeepSpeed](https://github.com/microsoft/DeepSpeed)、[Megatron-LM](https://github.com/NVIDIA/Megatron-LM)、VeRL 通过数据并行、张量并行等技术，拆分大规模训练任务，适配多卡/多节点集群，解决单设备算力不足问题，直接支撑 AI 任务的落地执行[^2]。

- **Maas（Model as a Service, 模型即服务）层**: *AI 领域特有的中间层，衔接 SaaS 层与终端用户*，核心提供模型托管（存储、管理预训练模型、微调后模型）、模型版本、轻量化微调与 API 调用服务，让用户无需关注底层框架与硬件，直接通过接口调用模型能力，是*大模型能力普惠化*的关键环节，填补了 “模型开发” 与 “业务应用” 间的空白[^2]。

!!! tip "一些前沿方向"
    - 异构计算与编译优化

      - [TVM](https://github.com/apache/tvm): 开源的机器学习编译器，支持将高效计算图部署到不同硬件上，优化加速.

      - [MLIR](https://github.com/llvm/mlir): LLVM 提供的多层次中间表示（MLIR），适用于编译与优化AI计算.

    - Serverless AI

      - [FaaS](https://github.com/openfaas/faas): 提供一个Serverless框架，支持快速部署机器学习模型，优化推理延迟.

## AI Infra的发展历程

> [AI Infra 发展历程-有没有大佬帮我解释一下AI Infra到底是干啥的？| 知乎](https://www.zhihu.com/question/4023337465/answer/1950623317519242011?share_code=wOgLUTuVp9MB&utm_psn=2009324012581458495)

## AI Infra依赖的基础学科[^4][^5]

> *斜体标注为11408考察内容*

- **计算机科学与技术**

    - **<i>计算机体系结构（Computer Architecture）</i>**

        - 基础理论: 处理器设计、内存层次结构、缓存优化、并行计算架构等

        - 关联: 硬件层（如 GPU、TPU、NPU）设计及优化、内存层次等。

        - 代表技术栈: H100/B200/Blackwell架构、RoCEv2、InfiniBand、Chiplet

    - **<i>操作系统（Operating System）</i>**

        - 基础理论: 进程调度、内存管理、I/O 管理、文件系统等

        - 关联: AI Infra依赖操作系统（属软件层IaaS）来进行资源调度与管理，尤其是在容器化和虚拟化环境中的资源隔离和调度（例如 Kubernetes 和容器）。操作系统中的优化技术直接影响到 AI 训练时的效率和稳定性。

        - 代表技术栈: Ubuntu（Linux）、容器化技术（Docker、Containerd、Kubernetes）、SLURM、Flux、Volcano

    - **<i>计算机网络（Computer Networking）</i>**

        - 基础理论: 网络协议、数据通信、网络拓扑等

        - 关联: 分布式训练依赖高速、低延迟的网络环境，如 InfiniBand、RDMA 等。网络优化对数据传输和模型参数同步至关重要。

        - 代表技术栈: RoCEv2、Ultra Ethernet、NCCL优化、SHARP

    - **并行与分布式计算（Parallel & Distributed Computing）**

        - 基础理论: 分布式计算、负载均衡、容错性、消息队列、通信原语优化等

        - 关联: 大规模分布式训练、分布式文件系统（如 Ceph、Lustre）和分布式数据库的架构设计都依赖分布式系统的理论。高效的分布式计算可大幅度提升训练速度。

        - 代表技术栈: Megatron、DeepSpeed、FSDP、Colossal-AI、vLLM PagedAttention

    - **数据库管理（Database Management Systems）**

        - 基础理论: 数据库设计、查询优化、事务管理、分布式数据库等

        - 关联: AI Infra 中的数据存储（尤其是大规模数据集的存储和管理）需要强大的数据库支持。开源数据库（如 MySQL、PostgreSQL）和分布式数据库（如 Cassandra、HBase）常用于存储训练数据和模型参数。

        - 代表技术栈: MySQL、PostgreSQL、Cassandra、HBase等

    - **编译原理（Compiler Theory）**

        - 基础理论: 编译原理、语法分析、语义分析、代码生成、优化等

        - 关联: 编译优化决定资源利用是否高效，低效的优化会导致内核效率低下，同样硬件跑不出SOTA性能。

        - 代表技术栈: TorchInductor、OpenXLA、MoE路由编译优化、TVM等

- **人工智能与机器学习**
  
    - **机器学习与深度学习（Machine Learning & Deep Learning）**

        - 基础理论: 监督学习、无监督学习、强化学习、神经网络等

        - 关联: AI Infra 的核心目标是高效训练与部署机器学习和深度学习模型。所有的模型训练框架、加速工具、推理引擎等都基于机器学习与深度学习的基础理论。

    - 自然语言处理（NLP）

        - 基础理论: 语言模型、序列建模、BERT、GPT 等

        - 关联: 在大语言模型（如 GPT、BERT）的训练过程中，AI Infra 需要大规模的计算资源、存储和通信能力，这些都与 NLP 的发展息息相关。

- **数学**
  
    - **<i>线性代数（Linear Algebra）</i>**

        - 基础理论: 向量、矩阵运算、特征值分解、奇异值分解等

        - 关联: 线性代数是深度学习和AI的核心工具，模型训练过程中大量的矩阵运算依赖于线性代数。在优化算法（如梯度下降）和神经网络训练中，线性代数为数据处理提供了基础。

    - **<i>概率论与数理统计（Probability Theory & Mathematical Statistics）</i>**

        - 基础理论: 概率分布、贝叶斯推断、假设检验等

        - 关联: AI 模型的构建、优化和评估都需要统计学原理。深度学习中的优化算法（如梯度下降）和调优技巧（如正则化、早停等）都离不开统计分析。

    - **控制论&优化理论（Control Theory & Optimization Theory）**

        - 基础理论: 函数优化、梯度下降、凸优化、MoE路由、学习率调度、混合精度训练稳定性等

        - 关联: 训练过程依赖于多种优化算法。无论是深度学习的参数优化，还是分布式系统中的负载均衡、资源调度，都需要优化理论的支持。

    - **信息论（Information Theory）**

        - 基础理论: 熵、信息增益、编码理论等

        - 关联: 在大规模数据处理和深度学习模型设计中，信息论为模型压缩、数据传输和通信提供了理论支持。例如，神经网络中的量化、蒸馏技术就借鉴了信息论中的编码与压缩思想。

- **物理学**

    - **信号处理与通信（Signal Processing & Communications）**

        - 基础理论: 信号编码、解码、噪声抑制、滤波等

        - 关联: 在分布式训练中，通信效率至关重要。数据传输和模型同步需要应用信号处理理论，如压缩感知、量化、编码等技术，以优化带宽使用和减少通信开销。

    - 电路与半导体物理（Circuits & Semiconductor Physics）

        - 基础理论: 电流、电压、功率、晶体管、集成电路等

        - 关联: AI Infra 需要依赖硬件进行大规模并行计算，如 GPU 和 TPU。这些硬件的设计与工作原理需要半导体物理学、电子学等领域的支持。电路设计直接决定了计算性能与能效。

- 工程自动化

    - 自动化与控制理论（Automation & Control Theory）

        - 基础理论: 控制系统设计、反馈机制、优化控制等

        - 关联: 在 AI Infra 中，尤其是在资源调度、负载均衡和自适应学习等方面，自动化与控制理论帮助实现智能调度与自我优化。
  
    - 系统工程（Systems Engineering）

        - 基础理论: 复杂系统建模、系统集成、性能分析等

        - 关联: AI Infra 本质上是一个高度复杂的系统工程。它需要考虑各个组件的协同工作、系统性能的调优、故障容错等。系统工程的理论和方法帮助设计高效、稳定的基础设施。

综合来看，AI Infra涉及广泛的基础学科，涵盖了计算机科学、数学、物理、工程以及人工智能等领域，综合度较高。但实际依赖占比最大的是**计算机体系结构**、**并行与分布式计算**、**操作系统**这三个学科。

## 与传统Infra的关系

## 行业现状

## 开源项目参考

### 理论资料

- [AIInfra | GitHub](https://github.com/Infrasys-AI/AIInfra) - https://github.com/Infrasys-AI/AIInfra

- [AIInfra AI基础设施 - Home](https://infrasys-ai.github.io/aiinfra-docs/) - https://infrasys-ai.github.io/aiinfra-docs/


[^1]: [什么是 AI 基础设施？| IBM](https://www.ibm.com/cn-zh/think/topics/ai-infrastructure)

[^2]: [有没有大佬帮我解释一下AI Infra到底是干啥的？| 知乎解答](https://www.zhihu.com/question/4023337465/answer/1950623317519242011?share_code=A6LoAAhNcnIU&utm_psn=2009692977648395347)

[^3]: [深入高可用系统原理与设计](https://www.thebyte.com.cn/)

[^4]: [2025-2026 AI Infra技术栈全景 | Grok](https://grok.com/share/bGVnYWN5_3741cd34-6bd7-4384-9092-48959371736f)

[^5]: [AI Infra技术栈分析 | ChatGPT](https://chatgpt.com/share/699d7417-4ee0-800e-95bd-93c8e08e5901)
---
title: Todo List
icon: material/check-circle
permalink: todo
hide:
  - navigation
  - toc
---

# Todo List

## 📌 学习路线总览

```
阶段一：计算机底层基础 (6-12个月)
        ↓
阶段二：数学与信号处理基础 (3-6个月，可与阶段一并行)
        ↓
阶段三：机器学习/深度学习基础 (3-6个月)
        ↓
阶段四：计算机听觉专项 (6-12个月)
        ↓
阶段五：项目实践与竞赛 (持续)
```

---

## 1️⃣ 阶段一：计算机底层基础

### 体系结构

| 资源 | 说明 |
|------|------|
| [CMU 15-213: CSAPP](https://www.cs.cmu.edu/~213/) | 必修！计算机系统入门经典 |
| [UC Berkeley CS61C](https://cs61c.org/) | 机器结构，RISC-V架构 |
| 《深入理解计算机系统》(CSAPP) | 配套书籍 |

### 操作系统

| 资源 | 说明 |
|------|------|
| [MIT 6.S081](https://pdos.csail.mit.edu/6.828/2023/schedule.html) | xv6操作系统实验，强烈推荐 |
| [OSTEP](https://pages.cs.wisc.edu/~remzi/OSTEP/) | 操作系统导论，免费在线书籍 |

### 分布式系统

| 资源 | 说明 |
|------|------|
| [MIT 6.824](https://pdos.csail.mit.edu/6.824/) | 分布式系统经典课程 |
| 《Designing Data-Intensive Applications》(DDIA) | 数据密集型应用设计 |

### 存储系统

| 资源 | 说明 |
|------|------|
| [CMU 15-445 Database Systems](https://15445.courses.cs.cmu.edu/) | 数据库系统实现 |
| [CMU 15-721 Advanced Database](https://15721.courses.cs.cmu.edu/) | 进阶存储引擎 |

---

## 2️⃣ 阶段二：数学与信号处理基础

这是**连接底层与听觉**的关键桥梁：

| 领域 | 资源 |
|------|------|
| 线性代数 | MIT 18.06 (Gilbert Strang) |
| 概率论 | MIT 6.041 / 《概率导论》 |
| **数字信号处理 (DSP)** | [MIT 6.003 Signals and Systems](https://ocw.mit.edu/courses/6-003-signals-and-systems-fall-2011/) |
| **傅里叶变换** | 3Blue1Brown 视频讲解 |
| 音频信号处理入门 | [Audio Signal Processing for Music Applications (Coursera)](https://www.coursera.org/learn/audio-signal-processing) - Stanford/UPF 联合课程 |

---

## 3️⃣ 阶段三：机器学习/深度学习基础

| 资源 | 说明 |
|------|------|
| [Stanford CS229](https://cs229.stanford.edu/) | 机器学习基础 |
| [Andrew Ng - Deep Learning Specialization](https://www.coursera.org/specializations/deep-learning) | 深度学习专项课程 |
| [李沐《动手学深度学习》](https://d2l.ai/) | 实践导向 |
| PyTorch/TensorFlow | 至少熟练一个框架 |

---

## 4️⃣ 阶段四：计算机听觉专项

### 核心课程与资源

| 资源 | 说明 |
|------|------|
| [Stanford CS224S](https://web.stanford.edu/class/cs224s/) | Spoken Language Processing，语音处理入门经典 |
| [ISMIR Tutorials](https://ismir.net/resources/tutorials/) | Music Information Retrieval 年度教程 |
| [librosa](https://librosa.org/doc/latest/index.html) | Python 音频分析库，必学 |
| [Hugging Face Audio Course](https://huggingface.co/learn/audio-course/) | 音频深度学习实践 |
| [Speech and Language Processing](https://web.stanford.edu/~jurafsky/slp3/) | Jurafsky & Martin，NLP/语音经典教材（在线免费） |

### 音乐方向专项

| 方向 | 核心技术/资源 |
|------|---------------|
| Music Information Retrieval (MIR) | [musicinformationretrieval.com](https://musicinformationretrieval.com/) - 实践教程 |
| 音乐生成 | Magenta (Google), Jukebox (OpenAI), AudioCraft (Meta) |
| 音乐转录 | Onsets and Frames, MT3 |
| 音乐推荐 | Spotify Research 论文 |
| 音频合成 | WaveNet, Diffusion Models for Audio |

### 重要开源项目

建议阅读源码：

- **Kaldi** / **ESPnet** - 语音识别框架
- **Fairseq** - 序列到序列模型（含音频）
- **Whisper** (OpenAI) - 多语言语音识别
- **AudioCraft** (Meta) - 音频/音乐生成
- **Demucs** (Meta) - 音源分离
- **Spleeter** (Deezer) - 音源分离

---

## 5️⃣ 相关竞赛

### 音频/语音方向

| 竞赛 | 说明 | 时间 |
|------|------|------|
| [DCASE Challenge](https://dcase.community/) | 声音事件检测/分类，学术圈权威 | 每年，通常3-7月 |
| Interspeech Challenge | 语音处理顶会附属竞赛 | 每年跟随会议 |
| [MIREX](https://www.music-ir.org/mirex/wiki/MIREX_HOME) | MIR 领域权威评测 | 每年 |
| Kaggle 音频竞赛 | 不定期，如 BirdCLEF, RFCX | 持续关注 |

### 算法/系统方向

| 竞赛 | 说明 |
|------|------|
| ACM-ICPC / XCPC | 算法竞赛，提升编程基础 |
| PingCAP TiDB Hackathon | 分布式数据库实践 |
| OceanBase 数据库大赛 | 存储系统方向 |

---

## 6️⃣ 学习建议

### 底层 → 听觉的衔接点

- 实时音频处理需要深入理解操作系统调度、内存管理
- 大规模音频检索需要分布式系统与存储系统知识
- 音频编解码涉及体系结构优化（SIMD指令等）

### 项目建议

- 用 C/C++ 实现一个简单的音频播放器（底层）
- 用 Python + librosa 实现音乐节拍检测（信号处理）
- 用 PyTorch 实现一个简单的语音分类模型（深度学习）
- 复现一篇 MIR 领域论文（综合能力）

### 关注的会议/期刊

- **ISMIR** (Music Information Retrieval)
- **ICASSP** (信号处理顶会)
- **Interspeech** (语音处理)
- **NeurIPS/ICML** 的音频相关 workshop

---

## 7️⃣ 推荐阅读

1. [The Scientist and Engineer's Guide to DSP](https://www.dspguide.com/) - 免费在线 DSP 教材，非常适合入门
2. [Music Information Retrieval: An Introductory Survey](https://www.ee.columbia.edu/~dpwe/pubs/Casey08-mir.pdf) - MIR 领域综述
3. [A Tutorial on Audio Recognition](https://arxiv.org/abs/2303.18033) - 音频识别综合教程 (2023)
4. [Awesome Audio/Speech/Music Processing](https://github.com/faroit/awesome-python-scientific-audio) - GitHub 资源汇总

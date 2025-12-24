# Library Management System For Curriculum Design

## Overview

It's my OS Curriculum Design (Proposition Design) for the Operating System Course in Fujian University of Technology.

For training my C programming engineering skills, I decide to seperate the source code as a multi-file structure so that more in line with the scene of **production environment**.

For convinent to submit, I also create a copy as a singal file.

## Build and Run

The project can be built use `make`:

```bash
cd wiki/code/misc/os/library
make
./library
```

Or

```bash
make build && make run
```

Use `make clean` to clean the build artifacts:

```bash
make clean
```

For singal file version, you can use `make singal`:

```bash
make singal
./singal
```

## How it Works

![](seq.drawio.png)

```mermaid
flowchart TB
    subgraph Parent["父进程 (图书馆)"]
        P1[启动图书馆<br>显示馆藏信息]
        P2[创建 Pipe 管道]
        P3[Fork 子进程]
        P4[从管道读取消息]
        P5{解析消息类型}
        P6[处理查询请求 S<br>返回图书信息]
        P7[处理借阅请求 B<br>更新库存]
        P8[等待子进程结束<br>显示最终馆藏]
    end

    subgraph Child["子进程 (用户)"]
        C1[初始化随机种子]
        C2[创建 4 个查询线程]
        C3[创建 2 个借阅线程]
        C4[等待所有线程完成]
        C5[关闭管道写端<br>退出进程]
    end

    subgraph Threads["线程操作"]
        T1["查询线程 (x4)<br>pthread_rwlock_rdlock"]
        T2["借阅线程 (x2)<br>pthread_rwlock_wrlock"]
        T3[随机选择图书]
        T4[通过管道发送消息<br>格式: 类型:线程ID:书名]
    end

    P1 --> P2 --> P3
    P3 -->|父进程| P4
    P3 -->|子进程| C1

    C1 --> C2 --> C3 --> C4 --> C5

    C2 --> T1
    C3 --> T2
    T1 --> T3 --> T4
    T2 --> T3

    T4 -->|"Pipe 通信"| P4
    P4 --> P5
    P5 -->|"S (查询)"| P6
    P5 -->|"B (借阅)"| P7
    P6 --> P4
    P7 --> P4
    C5 -.->|"子进程结束"| P8
```

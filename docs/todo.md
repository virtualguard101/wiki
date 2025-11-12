---
date: 2025-11-06 19:59:55
title: Todo List
permalink: 
publish: false
hide:
- navigation
---

```mermaid
stateDiagram-v2
    direction LR

    CSB --> PROJECTS
    JHP --> PROJECTS
    PROJECTS --> JOB
    CSB --> Research
    Research --> DECISION
    JOB --> DECISION

    state "Computer Science Basics" as CSB {
        direction LR
        OS --> CN
        CN --> CS

        state "Operating System" as OS {
            OS408: OS Overview
            OS408 --> OSTEP
        }

        state "Computer Network" as CN {
            CN408: CN Overview
            CN408 --> CS168
        }

        state "Computer Systems" as CS {
            CSAPP
        }
    }

    state "Job Hunting Preparation" as JHP {
        direction LR
        Golang --> DSA
        DSA --> Leetcode
        Leetcode --> resume
    }

    state "Personal Projects" as PROJECTS {
        GOAL: Product/Framework
        Backend --> GOAL
        AI_Agent --> GOAL
        System --> GOAL
    }

    state "Job Hunting" as JOB {
        BI: Background Investigation
        first: First Internship
        BI --> first
    }

    state Research {
        AIDD: AI-assisted Drug Design
    }
    DECISION: 408 or Job
```


- [ ] Operating System

    - [*] Basic concepts learning: 《王道2026操作系统考研复习指导》

    - [ ] Advanced Understanding

        - [ ] [《Operating Systems: Three Easy Pieces》](https://pages.cs.wisc.edu/~remzi/OSTEP/)

- [ ] Computer Network

    - [ ] [CS 168 - Introduction to the Internet: Architecture and Protocols](https://sp25.cs168.io/)

        - [ ] [Textbook | CS 168](https://textbook.cs168.io)


- [ ] Job Related Tech Stack

    - [ ] **Golang**:

        - [Go语言圣经（中文版）](https://golang-china.github.io/gopl-zh/index.html)

        - [Go 语言中文文档](https://www.topgoer.com/)

        - [ ] [Awesome Go | A curated list of awesome Go frameworks, libraries and software](https://awesome-go.com/)

    - [ ] [bilibili Open Source Task Force | Github](https://github.com/bilibili)

    - [ ] [bilibili 校园招聘](https://jobs.bilibili.com/campus)

- [ ] Computer Systems: A Programmer's Perspective

# Curriculum Design of Data Structure

## Overview

This is a curriculum design (also a *Proposition Design*) of the data structure course in Fujian University of Technology, implemented in C language.

It contains two projects:

![](dsa_curriculum.jpg)

## How it works

### `sort.c`

```mermaid
flowchart TD
    A[开始] --> B[生成测试数据]
    B --> B1[生成已排序数据]
    B --> B2[生成逆序数据]
    B --> B3[生成基本有序数据]
    B --> B4[生成随机数据]
    
    B1 --> C1[转换为链表]
    B2 --> C2[转换为链表]
    B3 --> C3[转换为链表]
    B4 --> C4[转换为链表]
    
    C1 --> D1[直接插入排序]
    C2 --> D1
    C3 --> D1
    C4 --> D1
    
    D1 --> E1[记录比较和移动次数]
    E1 --> F1[输出结果]
    
    C1 --> D2[冒泡排序]
    C2 --> D2
    C3 --> D2
    C4 --> D2
    
    D2 --> E2[记录比较和移动次数]
    E2 --> F2[输出结果]
    
    C1 --> D3[简单选择排序]
    C2 --> D3
    C3 --> D3
    C4 --> D3
    
    D3 --> E3[记录比较和移动次数]
    E3 --> F3[输出结果]
    
    F1 --> G[结束]
    F2 --> G
    F3 --> G
```

### `operation.c`

```mermaid
flowchart TD
    A[开始] --> B[初始化链表]
    B --> C[显示菜单]
    C --> D{用户选择操作}
    
    D -->|0| E[退出程序]
    D -->|1| F1[按位置插入]
    D -->|2| F2[头插法插入]
    D -->|3| F3[尾插法插入]
    D -->|4| F4[按位置删除]
    D -->|5| F5[按值删除]
    D -->|6| F6[按位置查找]
    D -->|7| F7[按值查找]
    D -->|8| F8[计数/获取长度]
    D -->|9| F9[输出链表]
    D -->|10| F10[清空链表]
    D -->|其他| G[提示无效选择]
    
    F1 --> H[执行操作]
    F2 --> H
    F3 --> H
    F4 --> H
    F5 --> H
    F6 --> H
    F7 --> H
    F8 --> H
    F9 --> H
    F10 --> H
    G --> C
    
    H --> I[显示操作结果]
    I --> C
    
    E --> J[销毁链表]
    J --> K[结束]
```



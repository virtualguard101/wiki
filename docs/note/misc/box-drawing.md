---
date: 2026-10-22 14:40:33
title: Box Drawing
permalink: box-drawing
publish: true
tags:
  - 杂项学习
---

# Box Drawing

整理一下在终端/Markdown中绘制线框和流程图时常用的[box-drawing字符](https://en.wikipedia.org/wiki/Box-drawing_characters), 本质上是[Unicode字符集](../csa/cs61c/Number%20Representation.md#Bits-can-represent-anything)中的一部分.

## 常用字符

| 字符 | 名称 | 作用 |
|:---:|:---|:---|
| `│` | vertical | 竖线 |
| `─` | horizontal | 横线 |
| `├` | tee-right | 向右分叉 (`|--` 的常见美化版) |
| `┤` | tee-left | 向左分叉 |
| `┬` | tee-down | 向下分叉 |
| `┴` | tee-up | 向上分叉 |
| `└` | corner-up-right | 左下转角 |
| `┌` | corner-down-right | 左上转角 |
| `┼` | cross | 十字交叉 (左右上下都连) |
| `▼` | down-arrow | 向下箭头 |
| `►` | right-arrow | 向右箭头 |


```text
tree style
A
├─ B
├─ C
└─ D

cross style
  │
──┼──
  │
```

## 输入方式

在大多数 Linux 输入法/终端中可用 `Ctrl+Shift+U`, 输入 Unicode 码点后回车或空格:

- `251c` -> `├`

- `253c` -> `┼`

- `2502` -> `│`

- `2500` -> `─`

- `2514` -> `└`

但最稳妥的方法仍是常用字符复制粘贴:

```text
├ └ │ ─ ┬ ┴ ┤ ┼ ▼ ►
```

## 对齐建议

1. 放在代码块里 (```text), 确保等宽字体渲染.

2. 图内节点尽量用英文短词, 中文说明放到图外文字中, 可减少中英文宽度差导致的错位.

3. 同一张图固定一种风格, 例如分叉统一用 `├`/`└`, 少用 `┼`.

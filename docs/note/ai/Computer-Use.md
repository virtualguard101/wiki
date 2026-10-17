---
date: 2026-09-23 16:24:52
title: Computer Use
permalink: cua
publish: true
tags:
  - 人工智能
  - Agent
---

# Computer Use

> [Computer use tool | Claude Platform](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool)
>
> [Computer-Using Agent | OpenAI](https://openai.com/index/computer-using-agent/)
>
> [Browser | Cursor Docs](https://cursor.com/docs/agent/tools/browser)
>
> [Cloud Agent capabilities | Cursor Docs](https://cursor.com/docs/cloud-agent/capabilities)
>
> [Computer use and desktop sharing | Cursor Docs](https://cursor.com/docs/cloud-agent/self-hosted/computer-use)

**Computer Use** 是让 agent 像人一样操作图形界面的一种技术: 看屏幕, 点按钮, 敲键盘, 再根据新画面决定下一步.

大量软件只提供窗口和网页, 这个界面就是现成的操作面. 一轮任务是一条闭环: 截图或界面结构送进模型, 模型输出点击, 输入, 滚动, 执行器做完再把新画面送回去.

部署时通常把"想"和"手"拆开. 模型负责决定下一步, 另一台机器或一个进程负责真正移动鼠标.

IDE 内的浏览器工具操作网页; 托管 Cloud Agent 在隔离虚拟机里控制整台桌面; 自托管 worker 把推理留在 Cursor 云端, 用一条出站连接在自己的 Mac 或 Linux 上点击和截图.

## 闭环

1. **观察**: 拿到当前屏幕的截图, 或一份界面结构.

2. **决定**: 模型输出下一个动作, 例如单击某个坐标, 或点某个页面元素.

3. **执行**: 旁边的执行器移动鼠标, 敲键, 滚动. 模型本身不直接碰操作系统.

4. **核对**: 把新画面送回模型. 画面没有按预期变化, 就换一种点法, 或把控制权交给人.

动作词汇很窄: 移动, 单击, 双击, 右键, 拖拽, 滚动, 输入文字, 按快捷键, 等待.

## 两种观察

| 材料 | 模型看到什么 | 动作怎么落 | 适合 |
| --- | --- | --- | --- |
| 像素 | 整屏截图 | 坐标, 例如点 `(x, y)` | 任何有画面的软件 |
| 结构 | 浏览器 DOM, 或系统无障碍树 | 点这个元素 | 网页, 以及做了无障碍支持的应用 |

像素路线覆盖面大. 小按钮, 弹窗, 分辨率变化都容易点偏. 结构路线命中更稳, 覆盖面限于能导出节点的界面.

Anthropic 把截图和鼠标键盘做成 [Messages API 上的一组客户端工具](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool). 模型返回 `screenshot`, `left_click`, `type` 这类调用, 循环由调用方在自己的环境里执行, 所以能接到容器, 虚拟机或远程桌面. OpenAI 的 [Computer-Using Agent](https://openai.com/index/computer-using-agent/) 同样吃像素, 出虚拟键鼠, 先以 Operator 的形式做网页任务. 2026 年常见的做法是混合: 终端, 编辑器, 浏览器元素工具能完成的步骤走这些工具; 窗口应用, 安装向导, 视觉验收才落到像素桌面.

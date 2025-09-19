# 操作系统模型

> [数学视角的操作系统-操作系统 (2025 春) | Yanyan's Wiki](https://jyywiki.cn/OS/2025/lect4.md)

## 应用视角下的操作系统

<div class="text-center-container" style="text-align: center;">
    <strong>程序 = 状态机</strong>
</div>

==即将程序抽象为一个**有限状态自动机**==。

- **状态**：栈帧中的变量（局部变量）和PC（*Process Computer*, 程序计数器）

- **初始状态**：`main(argc, argv)`

    即 `main` 函数被调用时的状态，==此时栈帧包含命令行参数(`argc`、`argv`)，PC指向`main`函数的入口

- **状态迁移**

    - 执行“当前栈帧PC“的语句

        即执行当前PC指向的指令，更新栈帧中的变量和PC

    - `syscall`（系统调用语句）

        可通过`syscall`与操作系统交互，可能改变程序状态

## 数学视角下的操作系统

<div class="text-center-container" style="text-align: center;">
    <strong>🚧前方施工中🚧</strong>
</div>

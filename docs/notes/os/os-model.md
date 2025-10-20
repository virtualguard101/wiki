# 操作系统简易模型

> [数学视角的操作系统-操作系统 (2025 春) | Yanyan's Wiki](https://jyywiki.cn/OS/2025/lect4.md)

一旦把操作系统、应用程序当做 “数学对象” 处理，那么我们图论、数理逻辑中的工具就能被应用于处理程序，甚至可以用图遍历的方法证明程序的正确性[^1]。

## 应用视角下的操作系统

<div class="text-center-container" style="text-align: center;">
    <strong>操作系统 = 对象 + API</strong>
</div>

<div class="text-center-container" style="text-align: center;">
    <strong>程序 = 状态机</strong>
</div>

==即将程序抽象为一个**有限状态自动机**==。

- **状态**：栈帧中的变量（局部变量）和PC（*Process Computer*, 程序计数器）

- **初始状态**：`main(argc, argv)`

    即 `main` 函数被调用时的状态，==此时栈帧包含命令行参数(`argc`、`argv`)，PC指向`main`函数的入口==

- **状态迁移**

    - 执行“当前栈帧PC“的语句

        即执行当前PC指向的指令，更新栈帧中的变量和PC

    - `syscall`（系统调用语句）

        可通过`syscall`与操作系统交互，可能改变程序状态

## 数学视角下的操作系统

<div class="text-center-container" style="text-align: center;">
    <strong>操作系统 = 状态机的管理者</strong>
</div>

- 可同时容纳多个“程序状态机”

    - ==程序状态机 $\Rightarrow$ 进程==

        - **程序内计算**：选一个程序（进程）执行一步

            ==即操作系统的调度功能——决定哪个进程在什么时候运行==

        - **系统调用**：创建新状态机、退出状态机、打印字符.....

            - 这是状态机改变系统状态的唯一方式

## 操作系统模型（Python实现）

!!! abstract
    操作系统的基本模型包含以下要素:

    - [进程](process.md)

    - 系统调用

    - ==上下文切换==

    - ==调度==

    其实现难点在于后两个要素，即如何在**进程之间来回切换**？如何实现“在单个CPU上并发运行多个程序”的效果？

!!! quote
    *源代码为蒋炎岩老师在[数学视角的操作系统-操作系统 (2025 春)](https://jyywiki.cn/OS/2025/lect4.md)所公开的**操作系统模型-Python实现**，下面是我在AI辅助学习下的个人解读（~~根据答案推过程这一块~~），感兴趣可自行前往拜读*

这是 AI 分析后给出的架构图
```bash
  OS类
  ├── 进程列表 (procs)
  ├── 缓冲区 (buffer)
  └── 主循环 (run)
      │
      ├── 随机调度器
      │   └── current = random.choice(procs)
      │
      ├── 进程执行器
      │   └── current.step()
      │       └── 返回: (syscall, args)
      │
      └── 系统调用处理器
          ├── read: 返回随机位
          ├── write: 写入缓冲区
          └── spawn: 创建新进程

  Process类 (进程)
  ├── _func: 生成器对象 (保存状态)
  ├── retval: 系统调用返回值
  └── step(): 执行一步
      └── 通过 yield 发出系统调用

  用户代码转换
  sys_read() → yield "read", ()
  sys_write(s) → yield "write", (s)
  sys_spawn(fn, args) → yield "spawn", (fn, args)
```

### 元素

从上面两个视角的分析，不难建模出这样**一种（类）**"简易的操作系统"：

- 只具有三个**系统调用**

    === "`os-model.py`"
    ```py
    SYSCALL = [
        'read', 'write', 'spawn'
    ]
    ```
    其中：

    - `read` 用于读取一个随机位的值并返回（0/1）

    - `write` 用于向缓冲区写入字符串`s`

    - `spawn` 用于创建一个新的状态机（进程）`f`

- 一个与适配于该“操作系统”的进程模型（`Process`辅助类）

### 设计理念

==核心思想是**进程建模为状态机（Python生成器）**==

- **进程 = 生成器函数**：每个进程都是一个[Python生成器](https://stackoverflow.com/questions/1756096/understanding-generators-in-python)，可以暂停和恢复执行

- **状态保存**：生成器的局部变量、程序计数器等状态自动保存在生成器对象中

- **协作式多任务**：通过`yield`实现进程主动让出CPU控制权

### 进程模型（`Process`类）

=== "`os-model.py`"

    ```py
    class Process:
        '''A "freezed" state machine. 
        The state (local variables, program counters, etc.) 
        are stored in the generator object.

        Attributes:
            _func: The generator function.
            retval: The return value of the last system call,
            which is set by the OS's main loop.
        '''
        def __init__(self, func, *args):
            """`func` should be a generator function. 
            Calling func(*args) returns a generator object.
            """
            self._func = func(*args) # Create generator objects
            self.retval = None # The return value system call of system call

        def step(self):
            '''Resume the process with OS-written return value,
            until the next system call is issued.
            '''
            syscall, args, *_ = self._func.send(self.retval)
            self.retval = None
            return syscall, args
    ```

- ==进程是一个"冻结"的状态机==

- ==状态（局部变量、程序计数器等）存储在生成器对象中==

- `_func`：存储生成器对象，包含进程的所有状态

- `retval`：存储上次系统调用的返回值，由操作系统主循环（`while self.procs`）设置，初始状态为空（`None`）

- ⭐`step()`：恢复进程执行直到下一个系统调用

    - ==使用`send(self.retval)`恢复生成器执行，并接受系统调用信息==

        - `syscall`为系统调用名称

        - `args`为系统调用参数

        - `*_`表示忽略其他返回值

    - 清空返回值

    - 返回系统调用名称和参数

### ⭐系统构造

#### 构造函数

=== "`os-model.py`"

    ```py
    def __init__(self, src):
        """This is a hack: we directly execute the source 
        in the current Python runtime--and main is thus 
        available for calling.
        """
        exec(src, globals())
        self.procs = [OS.Process(main)]
        self.buffer = ''
    ```

- `src` 即为要执行的“程序"，例如

    === "`hello.py`"

        ```py
        def main():
        x = 0
        for _ in range(10):
            b = sys_read()
            x = x * 2 + b

        sys_write(f'x = {x:010b}b')
        ```
    === "`proc.py`"

        ```py
        def Process(name):
        for _ in range(5):
            sys_write(name)

        def main():
            sys_spawn(Process, 'A')
            sys_spawn(Process, 'B')
        ```

    在执行时直接作为参数传入这个操作系统模型（`os-model.py`）

- 使用 `exec(str, globals())` 执行源码，使 `main` 函数在全局作用域中可用

- 创建进程列表 `proc`，初始包含一个调用 `main` **函数**的进程

- 初始化空缓冲区

#### ⭐主循环与进程调度

=== "`os-model.py`"

    ```py
    def run(self):
        """Real operating systems waste all 
        CPU cycles(efficiently, by putting the CPU into sleep)
        when there is no running process at the moment.
        Our model terminates if there is nothing to run.
        """
        while self.procs:

            # There is also a pointer to the "current" process in today's operating systems.
            current = random.choice(self.procs)

            try:
                # Operating systems handle interrupt and system calls, and "assign" CPU to a process.
                match current.step():
                    case 'read', _:
                        current.retval = random.choice([0, 1])
                    case 'write', s:
                        self.buffer += s
                    case 'spawn', (fn, *args):
                        self.procs += [OS.Process(fn, *args)]
                    case _:
                        assert 0

            except StopIteration:
                # The generator object terminates.
                self.procs.remove(current)

        return self.buffer
    ```

!!! tip
    这里`Python Docs`上提到了一个细节，真实的操作系统在没有进程时只会让CPU进入休眠；而我们的这个简易操作系统模型在没有进程时就会直接终止整个系统。

- `while`循环创建了一个**主循环**，使得进程列表中还有进程时就继续执行

- ==**⭐调度进程**==

    - 使用 `current` 作为指针指向当前执行的进程

    - **模拟[抢占式调度](https://rcore-os.cn/rCore-Tutorial-Book-v3/chapter3/4time-sharing-system.html)**：调用 `random` 随机选择一个进程作为当前进程

        !!! note
            - 这个模型实际上是协作式多任务，因为进程必须主动调用系统调用（yield）才能让出CPU

            - 真正的抢占式调度是操作系统强制中断进程，而这里进程是主动让出的

            - 随机选择确实模拟了抢占式调度的"不可预测性"

    - 调用 `step()` 方法，使用 `match` 语句匹配返回值，并处理对应的系统调用

    - 捕获生成器对象结束异常（进程状态终止），并从列表中移除当前（状态终止的）进程

    - 返回缓冲区 `buffer` 的内容作为程序输出

### 调用机制

#### 调用概述

使用方法为
```bash
./os-model.py [proc_simu_file (.py)]
```

=== "`os-model.py`"

    ```py
    src = Path(sys.argv[1]).read_text()
    # Hack: patch sys_read(...) -> yield "sys_read", (...)
    for syscall in OS.SYSCALLS:
        src = src.replace(f'sys_{syscall}',
                          f'yield "{syscall}", ')
    stdout = OS(src).run()
    print(stdout)
    ```

调用过程倒是不难理解，简单来说就是读取调用命令的第一个参数（即程序模拟文件 `proc_simu_file.py`）的内容，==并将系统调用的部分进行遍历替换，并**转换成 `yield` 语句**：

`sys_read(...)` → `yield` "read", (...)
`sys_write(...)` → `yield` "write", (...)
`sys_spawn(...)` → `yield` "spawn", (...)

然后再传入系统模型实例并获取输出，最后打印结果。

#### ⭐系统调用的双向通信

- 进程通过 `yield` 发出系统调用请求 (request)

- 操作系统通过 `current.retval` 返回结果 (response)

- 进程通过 `yield` 的返回值接收结果 (get)


[^1]: [数学视角的操作系统-操作系统 (2025 春) | Yanyan's Wiki](https://jyywiki.cn/OS/2025/lect4.md)
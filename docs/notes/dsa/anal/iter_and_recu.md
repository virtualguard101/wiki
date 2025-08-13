# 迭代与递归

>[迭代与递归 | Hello 算法](https://www.hello-algo.com/chapter_computational_complexity/iteration_and_recursion/){target="_blank"}
>
>[递归函数 | Composing Programs 中译版](https://composingprograms.netlify.app/1/7){target="_blank"}

在算法中，重复执行某个任务在实现某些功能时是非常常见的，通常可通过**迭代**或**递归**两种方式来实现这些重复的任务。

## 迭代

**迭代（*iteration*）**是一种重复执行某个特定任务的**控制结构**。

在迭代中，程序会在满足一定条件时**重复**执行某段代码以**更新某种状态**（这个状态本质上是一个或一系列变量的值或者某个/些**可迭代对象**的状态），直至该条件不再满足。

!!! info "可迭代对象"
    可迭代对象（*Iteratable Object*）是能够一次返回其中一个成员的对象，通常使用 `for` 循环来完成此操作，如字符串、列表、元组、集合、字典等等之类的对象都属于可迭代对象。简单来理解，任何可以循环遍历的对象都是可迭代对象。

    可迭代对象的应用几乎遍布所有高级编程语言，尤其是现代编程语言。可参考以下资料理解其概念与应用：
    
    - [Iterable object（可迭代对象）| JavaScript.INFO](https://zh.javascript.info/iterable){target="_blank"}
    - [迭代协议 | MDN Web Docs](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Iteration_protocols){target="_blank"}
    - [隐式序列 | Composing Programs 中译版](https://composingprograms.netlify.app/4/2){target="_blank"}
    - [What exactly does "iterable" mean in Python? Why isn't my object which implements `__getitem__()` an iterable? | stackoverflow](https://stackoverflow.com/questions/32799980/what-exactly-does-iterable-mean-in-python-why-isnt-my-object-which-implement){target="_blank"}

迭代**重复**操作的本质使得**循环控制结构**成为实现其最合适的方式与形式。

### `for`循环

`for`循环是最常见的迭代形式，可迭代对象的遍历通常就可通过`for`循环完成。

`for`循环适合 ==在预先知道迭代次数== 的程序中使用。

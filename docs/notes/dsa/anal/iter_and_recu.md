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

!!! tip
    `for`循环适合 ==在预先知道迭代次数== 的程序中使用。

以下面的求和程序为例：

```python
def sum(n: int) -> int:
    """Sum from 1 to n"""
    res = 0
    # iteration with for loop
    for i in range(1, n + 1):
        res += i
    return res
```
??? success "可视化运行"
    <iframe width="800" height="500" frameborder="0" src="https://pythontutor.com/iframe-embed.html#code=def%20sum%28n%3A%20int%29%20-%3E%20int%3A%0A%20%20%20%20%22%22%22Sum%20from%201%20to%20n%22%22%22%0A%20%20%20%20res%20%3D%200%0A%20%20%20%20%23%20iteration%20with%20for%20loop%0A%20%20%20%20for%20i%20in%20range%281,%20n%20%2B%201%29%3A%0A%20%20%20%20%20%20%20%20res%20%2B%3D%20i%0A%20%20%20%20return%20res%0A%0Aif%20__name__%20%3D%3D%20%22__main__%22%3A%0A%20%20%20%20x%20%3D%205%0A%20%20%20%20sum%20%3D%20sum%28x%29%0A%20%20%20%20print%28sum%29&codeDivHeight=400&codeDivWidth=350&cumulative=false&curInstr=0&heapPrimitives=nevernest&origin=opt-frontend.js&py=311&rawInputLstJSON=%5B%5D&textReferences=false"> </iframe>

对于该程序而言，迭代的应用在于不断**更新**`res`的过程，以下是描述该过程的算法流程图：

![](../../assets/dsa.assets/anal/iter_and_recu/sum.drawio.png)

### `while`循环

`while`循环与`for`循环的一个主要区别就是前者无法用于直接操作可迭代对象，但它仍然可以用于实现迭代。

还是以前面的求和函数为例，使用`while`循环实现则有：

```py
def sum(n: int) -> int:
    """Sum from 1 to n"""
    res = 0
    i = 1
    while i <= n:
        res += i
        i += 1
    return res
```
??? success "可视化运行"
    <iframe width="800" height="500" frameborder="0" src="https://pythontutor.com/iframe-embed.html#code=def%20sum%28n%3A%20int%29%20-%3E%20int%3A%0A%20%20%20%20%22%22%22Sum%20from%201%20to%20n%22%22%22%0A%20%20%20%20res%20%3D%200%0A%20%20%20%20i%20%3D%201%0A%20%20%20%20while%20i%20%3C%3D%20n%3A%0A%20%20%20%20%20%20%20%20res%20%2B%3D%20i%0A%20%20%20%20%20%20%20%20i%20%2B%3D%201%0A%20%20%20%20return%20res%0A%0Aif%20__name__%20%3D%3D%20%22__main__%22%3A%0A%20%20%20%20x%20%3D%205%0A%20%20%20%20sum%20%3D%20sum%28x%29%0A%20%20%20%20print%28sum%29&codeDivHeight=400&codeDivWidth=350&cumulative=false&curInstr=0&heapPrimitives=nevernest&origin=opt-frontend.js&py=311&rawInputLstJSON=%5B%5D&textReferences=false"> </iframe>

虽然在使用`while`循环操作可迭代对象需要更加复杂的代码，但麻烦的同时也赋予了`while`循环更高的自由度，使得其能够实现一些逻辑更加复杂的迭代。例如需要同时对两个变量进行迭代：

```py
def sum_with_product(n: int) -> int:
    """renew i twice once loop"""
    res = 0
    i = 1
    while i <= n:
        res += i
        i += 1
        i *= 2
    return res
```
??? success "可视化运行"
    <iframe width="800" height="500" frameborder="0" src="https://pythontutor.com/iframe-embed.html#code=def%20sum_with_product%28n%3A%20int%29%20-%3E%20int%3A%0A%20%20%20%20%22%22%22renew%20i%20twice%20once%20loop%22%22%22%0A%20%20%20%20res%20%3D%200%0A%20%20%20%20i%20%3D%201%0A%20%20%20%20while%20i%20%3C%3D%20n%3A%0A%20%20%20%20%20%20%20%20res%20%2B%3D%20i%0A%20%20%20%20%20%20%20%20i%20%2B%3D%201%0A%20%20%20%20%20%20%20%20i%20*%3D%202%0A%20%20%20%20return%20res%0A%0Aif%20__name__%20%3D%3D%20%22__main__%22%3A%0A%20%20%20%20x%20%3D%2010%0A%20%20%20%20sum%20%3D%20sum_with_product%28x%29%0A%20%20%20%20print%28sum%29&codeDivHeight=400&codeDivWidth=350&cumulative=false&curInstr=0&heapPrimitives=nevernest&origin=opt-frontend.js&py=311&rawInputLstJSON=%5B%5D&textReferences=false"> </iframe>

### 嵌套循环

在一些复杂场景中，可在一个循环结构中嵌套另一个循环结构来满足特定的迭代需求。最简单且经典的例子莫过于输出一个乘法口诀表：

```py
def multiplication_table() -> None:
    for i in range(1, 10):
        for j in range(1, i+1):
            print(f"{i} * {j} = {i*j}", end='\t')
        print('\n')
```
??? success "可视化运行"
    <iframe width="800" height="500" frameborder="0" src="https://pythontutor.com/iframe-embed.html#code=def%20multiplication_table%28%29%20-%3E%20None%3A%0A%20%20%20%20for%20i%20in%20range%281,%2010%29%3A%0A%20%20%20%20%20%20%20%20for%20j%20in%20range%281,%20i%2B1%29%3A%0A%20%20%20%20%20%20%20%20%20%20%20%20print%28f%22%7Bi%7D%20*%20%7Bj%7D%20%3D%20%7Bi*j%7D%22,%20end%3D'%5Ct'%29%0A%20%20%20%20%20%20%20%20print%28'%5Cn'%29%0A%0Aif%20__name__%20%3D%3D%20%22__main__%22%3A%0A%20%20%20%20multiplication_table%28%29&codeDivHeight=400&codeDivWidth=350&cumulative=false&curInstr=0&heapPrimitives=nevernest&origin=opt-frontend.js&py=311&rawInputLstJSON=%5B%5D&textReferences=false"> </iframe>

算法流程图：

![乘法口诀表输出程序](../../assets/dsa.assets/anal/iter_and_recu/multiplication_table.drawio.png)

!!! warning
    在使用循环嵌套时，每增加一层嵌套就会使得迭代操作的数量“提升一个维度”，同时减低代码的可读性，因此应尽量避免使用过深的嵌套。

## 递归

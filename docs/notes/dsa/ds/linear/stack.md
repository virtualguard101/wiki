# 栈


## 定义

==**栈（*stack*）**是限定**仅在表尾进行插入和删除操作的线性表**==。栈遵循**后进先出（*Last In First Out*，LIFO）**的特点，即最后插入的元素最先被删除。

允许插入和删除的一端称为**栈顶（*top*）**，另一端则称为**栈底（*bottom*）**:

![栈](../../../assets/dsa.assets/ds/linear/stack/stack_operations.png)
*图片来源：[栈 | Hello算法](https://www.hello-algo.com/chapter_stack_and_queue/stack/)*

栈的特殊之处在于其限制了元素插入与删除操作的可执行位置。栈的插入操作称为入栈（push），也可称为压栈、进栈等；删除操作称为出栈（pop），也可称为弹栈。将栈比作一个弹夹，同时将栈内元素比作子弹来理解栈的概念会形象得多。

!!! note
    注意栈首先是一个**线性表**，也就是说，栈的元素具有**线性关系**，即前后驱动关系。

## 栈的实现

栈的本质是一个线性表，那么基于线性表的两种基本存储逻辑，也就可以通过**顺序存储结构**与**链式存储结构**两种方式实现。

!!! tip
    这里提到的**线性表的两种基本存储逻辑**即前面学习的**顺序表**与**链表**的抽象概念。

### 顺序存储结构

栈的顺序存储结构本质上是对**线性表顺序存储结构**，即**顺序表**的简化，我们称其为**顺序栈**。

由于栈元素的数量未知，所以可以**基于动态数组实现**:

```py
class SqStack:
    """基于动态数组实现的顺序栈
    """
    def __init__(self):
        self._stack: List[Any] = []

    def size(self) -> int:
        """栈的长度
        """
        return len(self._stack)

    def is_empty(self) -> bool:
        """栈是否为空
        """
        return self.size() == 0

    def push(self, item: Any) -> None:
        """压栈操作
        """
        self._stack.append(item)

    def pop(self) -> Optional[Any]:
        """弹栈操作
        """
        if self.is_empty():
            return None
        return self._stack.pop()

    def peek(self) -> Optional[Any]:
        """获取栈顶元素
        """
        if self.is_empty():
            return None
        return self._stack[-1]
```

所有操作均未涉及循环语句，故时间复杂度均为 $O(1)$。

!!! note
    基于静态数组实现的顺序栈只需在入栈操作前添加判断栈满的逻辑即可。

### 链式存储结构

同理，栈也可基于单链表实现，称为**链栈**。

根据栈的基本概念我们知道，栈元素的删除与插入操作均在栈顶进行，因此链表的头部通常可以直接作为栈顶。

```py
class ListNode:
    """链表节点
    """
    def __init__(self, value: Any):
        self.value = value
        self.next = None

class LinkedStack:
    """基于链表实现的栈
    """
    def __init__(self):
        self._top: Optional[ListNode] = None

    def size(self) -> int:
        """栈的长度
        """
        count = 0
        current = self._top
        while current:
            count += 1
            current = current.next
        return count

    def is_empty(self) -> bool:
        """栈是否为空
        """
        return self._top is None

    def push(self, item: Any) -> None:
        """压栈操作
        """
        new_node = ListNode(item)
        new_node.next = self._top
        self._top = new_node

    def pop(self) -> Optional[Any]:
        """弹栈操作
        """
        if self.is_empty():
            return None
        popped_value = self._top.value
        self._top = self._top.next
        return popped_value

    def peek(self) -> Optional[Any]:
        """获取栈顶元素
        """
        if self.is_empty():
            return None
        return self._top.value
```

!!! note
    对于栈链而言，基本不存在栈满的情况，因为链表可以动态扩展。

### 实现对比

如果栈的使用过程中元素变化不可预料，建议使用链栈实现。链栈的动态特性使其能够灵活应对元素的频繁变化，而无需担心栈满的问题；

反之，如果栈的使用过程中元素变化较为稳定，且对性能要求较高，则可以考虑使用顺序栈实现。顺序栈在内存使用上更为紧凑，且在元素访问时具有更好的局部性。

## 典型应用

栈的引入简化了程序设计的问题，划分了不同关注层次，使得思考方位缩小，更加聚焦于我们所要解决的问题核心。

以下是栈的几个典型应用场景：

1. **表达式求值**：栈可以用于中缀表达式转后缀表达式（逆波兰表示法）以及后缀表达式的求值。

2. **函数调用管理**：程序的函数调用过程可以看作是一个栈结构，函数的参数、局部变量等信息都保存在栈帧中。

3. **撤销操作**：许多应用程序（如文本编辑器）都使用栈来实现撤销操作，用户的每一步操作都会被压入栈中，撤销时则弹出栈顶操作。

4. **深度优先搜索**：在图的遍历中，深度优先搜索（DFS）可以使用栈来实现，记录当前路径并回溯。

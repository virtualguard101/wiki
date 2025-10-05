# 队列

> *部分图片来源: [循环队列 | 大话数据结构【溢彩加强版】](https://zh.z-library.sk/book/24248731/7da759/%E5%A4%A7%E8%AF%9D%E6%95%B0%E6%8D%AE%E7%BB%93%E6%9E%84%E6%BA%A2%E5%BD%A9%E5%8A%A0%E5%BC%BA%E7%89%88.html)*

## 定义

与栈类似，**队列（*queue*）**也是一种限定插入与删除操作的**线性表**，但与栈不同的是，==其插入和删除操作被分别限制在表的两端==。其特点是**先进先出（FIFO）**，==插入操作被限制在队尾，而删除操作被限制在队头==。

![队列](queue.png)
*图片来源: [队列 | Hello算法](https://www.hello-algo.com/chapter_stack_and_queue/queue/)*

## 队列的实现

与栈同理，队列也可以基于**顺序存储结构**与**链式存储结构**两种方式实现。

### 顺序存储结构

在顺序存储结构中，我们可以使得队列的队首对应数组的第一个元素，即下标为 $0$ 的元素，删除操作就在该位置上进行。但这会导致出队效率较低，因为每次出队后都需要将后面的元素向前移动一位，时间复杂度为 $O(n)$。

队尾对应数组的最后一个元素，插入操作只需在该元素后追加元素，无需移动任何元素，时间复杂度为 $O(1)$。

#### 出队优化与假溢出

针对出队效率低的问题，我们可以通过指针来定义队首与队尾，从而避免每次出队后都需要将后面的元素向前移动；简单来说，队首不一定对应数组的第一个元素:

!!! tip "出队优化[^1]"

    实现上，我们可以使用一个变量 `front` 指向队首元素的索引，并维护一个变量 `size` 用于记录队列长度。定义 `rear` = `front` + `size` ，这个公式计算出的 `rear` 指向队尾元素之后的下一个位置。

    基于此设计，数组中包含元素的有效区间为 **[`front`, `rear` - 1]**，此时:

    - 入队操作：将输入元素赋值给 `rear` 索引处，并将 `size` 增加 1 。

    - 出队操作：只需将 `front` 增加 1，`size` 减少 1 。

    ![出队优化](queue_pop_improve.png)

但是仅仅是这样的优化在不断进行入队与出队的过程中可能会遇到所谓的**假溢出**（*false overflow*）问题。

!!! note "假溢出[^2]"
    在顺序存储结构中，假溢出是指队列虽然还有空闲空间，但由于队首元素指针已经出队，导致无法再进行入队操作:

    ![假溢出](false_overflow.png)

    将队列比作一辆公交车，假溢出现象就可比作是车的前面有位置，但后排位置却是满的；然而没有人会因为后排没位置了就选择等下班公交。

#### 循环队列

解决假溢出的方法也不难：后面满了，就从再前面开始，也就是**头尾相接的循环**。==队列的这种头尾相接的**顺序存储结构**称为**循环队列（*circular queue*）**==。

在循环队列中，我们可以使用取模运算来实现队列的循环。当 `rear` 指针到达数组末尾时，如果还有空闲空间，就将其移动到数组开头:

![循环队列](cir_queue.png)

结合上面的概念，就可以将 $a_5$ 所在的位置，即数组下标为 $4$ 的位置想象成是接在下标为 $0$ 空位前的一个“连接位”。这样就利用指针将一个“条形”的线性表连接成了一个“环形”的线性表，即循环队列。

但这样还会有一个问题：

在“首尾相接”前，队尾指针`rear`永远位于队首指针`front`的右侧，我们可以通过首尾指针的相对位置差直接判断队列是否已经处于队列满或队列空的状态；但在首尾相接后，`rear`有可能从右侧靠近`front`，也有可能从左侧靠近`front`。这种情况下，当`rear` == `front`时，究竟是队列满还是队列空呢？

解决方法有两种：

- 一是设置一个标志变量来区分空与满两种情况，这种方法相对简单——可以通过判断队列中是否有元素来改变`flag`的值:
  
    ![队列空](cir_queue_1.png)

    ![队列满](cir_queue_2.png)

- 二是为队列满的情况设置一种有别于队列空的形式:

    - 当队列空时，`rear` == `front`

    - 当队列满时，`rear`从左侧靠近`front`，但不会等于`front`，==即在`front`左侧保留一个空位==:

        ![队列满-无标识值](cir_queue_3.png)

    !!! tip "队列满判断公式"
        在这种方法中，若队列的最大容量为`capacity`，==则队列满的判断条件为`(rear + 1) % capacity == front`==，其中取余是为了整合`rear`与`front`的位置问题。

    !!! tip "队列长度计算公式"

        - 当队尾指针`rear`位于队首指针`front`的右侧时，队列长度可通过二者相减直接得出，即 `rear - front`；

        - 当`rear`位于`front`左侧时，队列即可分为两部分：

            - 数组首元素至`rear`的前半部分，即 `0 + rear`

            - `front`至数组末元素的后半部分==，即 `capacity - front`

            二者相加，即为 `rear - front + capacity`

        整合考虑两种情况，在溢出时取余，即可得出通用计算公式：`(rear - front + capacity) % capacity`

        第一种解决方法的长度计算在该计算公式的基础上设置`flag`值为 $1$ 时直接返回队列最大容量即可。

```py
class SqQueue:
    """基于数组的循环队列

    Attribute:
        _queue: 队列主体
        _front: 队首指针
        _rear: 队尾指针
        _capacity: 队列最大容量
    """
    def __init__(self, capacity: int):
        self._queue: List[Any] = [None] * capacity
        self._front: int = 0
        self._rear: int = 0
        self._capacity = capacity
    
    def length(self) -> int:
        """队列长度
        """
        return (self._rear - self._front + self._capacity) % self._capacity

    def is_empty(self) -> bool:
        """判断队列是否为空
        """
        return self._front == self._rear

    def is_full(self) -> bool:
        """判断队列是否处于队列满状态
        """
        return (self._rear + 1) % self._capacity == self._front
    
    def push(self, data: Any) -> None:
        """入队操作
        """
        if self.is_full():
            raise IndexError("The queue is full")
        self._queue[self._rear] = data
        self._rear = (self._rear + 1) % self._capacity

    def pop(self) -> Any:
        """出队操作
        """
        if self.is_empty():
            raise IndexError("The queue is empty")
        data = self._queue[self._front]
        self._front = (self._front + 1) % self._capacity
        return data
    
    def peek(self) -> Any:
        """查看队首元素但不删除
        """
        if self.is_empty():
            raise IndexError("The queue is empty")
        return self._queue[self._front]
```

### 链式存储结构

队列的链式存储结构，==本质上是一个将插入操作与删除操作分别限制早线性表头尾的**单链表**==，称为链队列。

![链队列](linked_queue.png)

```py
class LinkedNode:
    """链表节点

    Attribute:
        data: 数据域
        next: 指向下一节点的指针域
    """
    def __init__(self, data: Any):
        self.data = data
        self.next: LinkedNode | None = None

class LinkedQueue:
    """基于单链表的链队列

    Attribute:
        _front: 队首指针
        _rear: 队尾指针
    """
    def __init__(self):
        self._front: LinkedNode | None = None
        self._rear: LinkedNode | None = None
        self.length: int = 0

    def length(self) -> int:
        """获取链队列长度
        """
        return self.length

    def is_empty(self) -> bool:
        """判断链表是否为空
        """
        return not self._front
    
    def push(self, data: Any) -> None:
        """入队操作
        """
        node = LinkedNode(data)
        if self._front is None:
            self._front = node
            self._rear = node
        self._rear.next = node
        self._rear = self._rear.next
        self.length += 1

    def pop(self) -> Any:
        """出队操作
        """
        res = self.peek()
        if self.is_empty():
            raise IndexError("The queue is empty")
            return self._front.data
        self._front = self._front.next
        self.length -= 1
        return res

    def peek(self) -> LinkdedNode:
        """访问队首元素
        """
        if self.is_empty():
            raise IndexError("The queue is empty")
            return self._front.data
        return self._front.data
```

### 实现对比

- 从时间上来看，二者常用操作的时间复杂度都是 $O(1)$。

- 从空间上来看:

    - 循环队列基于定长数组实现，空间是实现分配好的，使用期间不释放，因此无论队列本身的长度多大，实际的空间占用仍是固定的，这就会造成**空间浪费**

    - 链队列尽管需要一个额外的指针域，但总体上更加灵活

总的来说，可以确定队列长度最大值的情况下，建议使用循环队列；否则使用链队列。

<!-- <div style="text-align: center">
    🚧前方施工中🚧
</div> -->

[^1]: [队列-基于数组的实现 | Hello算法](https://www.hello-algo.com/chapter_stack_and_queue/queue/#2)

[^2]: [循环队列 | 大话数据结构【溢彩加强版】](https://zh.z-library.sk/book/24248731/7da759/%E5%A4%A7%E8%AF%9D%E6%95%B0%E6%8D%AE%E7%BB%93%E6%9E%84%E6%BA%A2%E5%BD%A9%E5%8A%A0%E5%BC%BA%E7%89%88.html)
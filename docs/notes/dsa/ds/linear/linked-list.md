# 单链表

## 定义

**链表（*Linked List*）**本质上是**线性表的链式存储结构**，与顺序表不同，其通过可**非连续**的内存存储数据元素。

链表以**节点**形式组织数据，每个节点包含两个部分：

- **数据域**：存储实际数据元素的区域

- **指针域**：存储指向下一节点的地址（或引用）的区域

链表的节点通过指针连接，形成一个**链式结构**，逻辑上表现为**线性序列**。

### 逻辑结构

![链表](linkedlist_definition.png)
*图片来源：[链表 | Hello算法](https://www.hello-algo.com/chapter_array_and_linkedlist/linked_list/#42){target="_blank"}*

链表中的元素（节点）按照**一对一**的顺序关系排列；第一个节点称为**头节点**，可以不包含数据域（若存在一般也没意义）；最后一个节点称为**尾节点**，其指针通常指向“空”，即 `None`/`null`/`nullptr`。

链表的逻辑顺序由指针决定，不再依靠内存的连续性。

=== "Python"
    ```py
    from typing import Optional, Any

    class LinkedListNode:
        """链表节点类
        
        表示链表中的一个节点，包含数据域和指向下一个节点的指针。
        
        Attributes:
            object: 节点存储的数据，可以是任意类型或 None
            next: 指向下一个节点的引用，如果为 None 则表示链表结束
        """
        def __init__(self, obj: Optional[Any] = None):
            self.object: Optional[Any] = obj
            self.next: Optional['LinkedListNode'] = None
    ```
=== "C++"
    ```cpp
    /**
     *  LinkedNode is a node in a linked list.
     *  It contains a vector of integers and a pointer to the next node.
     */
    struct LinkedNode {
        std::vector<int> data;
        LinkedNode* next;

        LinkedNode(std::vector<int> data, LinkedNode* next) : data(data), next(next) {}
        LinkedNode(std::vector<int> data) : data(data), next(nullptr) {}
        LinkedNode() : data(std::vector<int>()), next(nullptr) {}
    };
    ```

## 常用操作

### 初始化

- 若一个链表头节点的指针域为“空”，则称这个链表是**空表**：

    === "Python"
        ```py
        # 创建空链表（头节点为 None）
        head = None

        # 创建包含空数据的头节点
        head = LinkedListNode(None)

        # 创建包含数据的头节点
        head = LinkedListNode(0)
        ```
    !!! warning

        注意这里传入构造函数的参数是节点的数据域，在上面的构造函数中，我们设定指针域默认为空。

- 从现有数据建立链表

    === "Python"
        ```py
        def create_linked_list(data_list):
            """从数据列表创建链表
            """
            # 创建头节点（哨兵节点）
            head = LinkedListNode(None)
            current = head
            
            # 逐个创建节点并连接
            for data in data_list:
                new_node = LinkedListNode(data)
                current.next = new_node
                current = new_node
            
            return head  # 返回头节点
        ```
    === "C++"
        ```cpp
        /*
            从现有数据建立链表
        */
        LinkedNode* initLinkedList(std::vector<int> data) {
            LinkedNode* head = new LinkedNode(data);    // 初始化头节点
            LinkedNode* current = head;
            for(int i = 1; i < data.size(); i++) {
                current->next = new LinkedNode({data[i]});
                current = current->next;
            }
            return head;
        }
        ```
 
!!! tip
    链表还可以以一种递归的形式创建与解析，详情可参考[递归对象-链表 | COMPOSING PROGRAMS 中译版](https://composingprograms.netlify.app/2/9#_2-9-1-%E7%B1%BB-%E9%93%BE%E8%A1%A8){target="_blank"}。

### 插入节点

与数组不同，由于存储非连续性的特性，在链表中插入元素是一个高效的操作。

在链表中插入节点，==只需改变待插入元素与插入位置前一个元素的**节点引用（指针）**即可==:

![链表-插入节点](linkedlist_insert_node.png)
*图片来源: [链表-插入节点 | Hello算法](https://www.hello-algo.com/chapter_array_and_linkedlist/linked_list/#2)*

=== "Python"
    ```py
    def insert(self, p: LinkedListNode):
        """在自身后插入一个链表节点

        Args:
            p ('LinkedListNode'): 待插入节点
        """
        p.next = self.next
        self.next = p
    ```
=== "C++"
    ```cpp
    /*
        @brief 在自身后插入一个节点
        @param self 参照节点
        @param node 插入节点
    */
    void insertLinkedList(LinkedNode* self, LinkedNode* node) {
        node->next = self->next;
        self->next = node;
    }
    ```

可以看出只需使待插入节点`p`的节点引用指向待插入位置的后一个节点，然后再使得前一个节点的节点引用指向`p`即可。==时间复杂度为 $O(1)$==。

### 删除节点

删除节点就更简单了，==只需改变待删除节点前一个节点的节点引用即可==:

![链表-删除节点](linkedlist_remove_node.png)

=== "Python"
    ```py
    def remove(self):
        """删除自身后的一个节点
        """
        if not self.next:
            raise IndexError(f"There has no Node next of {self.index}.")
        self.next = self.next.next
    ```
=== "C++"
    ```cpp
    /*
        @brief 删除自身后的一个节点
        @param self 参照节点
    */
    void deleteLinkedList(LinkedNode* self) {
        if (self->next == nullptr) {
            throw std::runtime_error("There has no Node next of " + std::to_string(self->data.at(0)) + ".");
        }
        self->next = self->next->next;
    }
    ```

执行删除操作后，即便待删除节点的节点引用仍然指向原来的位置，==但遍历操作已经无法访问到这个节点了==，即这个节点已经不再属于这个链表了。

与插入相同，删除操作的时间复杂度也为 $O(1)$。

### 访问节点

如此高效与灵活的插入与删除操作是有代价的，存储非连续性的特性使得链表中各节点分散在内存各处，==无法随机访问==。

想要访问链表的特定元素，只能从其头节点出发向后**遍历**，直至匹配到目标节点:

=== "Python"
    ```py
    def access(self, head: LinkedListNode, index: int) -> LinkedListNode | None:
        """访问头节点为 head 的链表中索引为 index 的节点

        Args:
            head: 待访问链表的头节点
            index: 待访问节点的索引
        """
        if index < 0:
            raise IndexError("Index out of range")
        cur = head
        for _ in range(index):
            if cur is None:
                return cur
            cur = cur.next
        return cur
    ```
=== "C++"
    ```cpp
    /*
        @brief 访问链表节点
        @param head 链表头节点
        @param index 访问节点索引
        @return 访问节点
    */
    LinkedNode* accessLinkedList(LinkedNode* head, int index) {
        if (head == nullptr) {
            throw std::runtime_error("Empty Linked List");
        }
        LinkedNode* current = head;
        for(int i = 0; i < index; i++) {
            if (current->next == nullptr) {
                throw std::runtime_error("Index out of range");
            }
            current = current->next;
        }
        return current;
    }
    ```
结合前面提到的链表的**递归性质**，也可以使用递归的方式实现:

=== "Python"
    ```py
    def access(self, head: LinkedListNode, index: int) -> LinkedListNode | None:
        """访问头节点为 head 的链表中索引为 index 的节点(递归)

        Args:
            head: 待访问链表的头节点
            index: 待访问节点的索引
        """
        if index < 0:
            raise IndexError("Index out of range")
        if index == 0 or head is None:
            return head
        return self.access(head.next, index - 1)
    ```
=== "C++"
    ```cpp
    /*
        访问链表节点 (递归)
        @param head 链表头节点
        @param index 访问节点索引
        @return 访问节点
    */
    LinkedNode* accessLinkedListWithRecu(LinkedNode* head, int index) {
        if (index ==0 || head == nullptr) {
            return head;
        }
        return accessLinkedListWithRecu(head->next, index - 1);
    }
    ```

无论是迭代还是递归，访问链表节点均需要 $O(n)$ 时间，递归还需要 $O(n)$ 的空间。

## 对比线性表

链表与线性表最本质的区别就是元素存储逻辑的区别：线性表元素需要存储在**连续的内存空间**中，而链表的元素可以**分散**在内存各处。

当表长很大时，内存可能无法提供足够大的连续空间，从而导致溢出问题，这时链表的灵活行就体现出来了；但元素操作灵活的代价就是访问效率的大打折扣。同时，由于链表的元素还需要包含节点引用，因此其对内存的占用也是远大于线性表的。

|   | 线性表 | 链表 |
|:-:|:-----:|:----:|
|访问元素| $O(1)$ | $O(n)$ |
|插入/删除元素| $O(n)$ | $O(1)$ |

## 杂项

!!! warning
    如题，本文介绍的仅仅只是最简单的链表类型，即**单向链表**，此外还有:

    - **环形链表**：令单向链表的尾节点指向头节点（首尾相接），则得到一个环形链表。在环形链表中，任意节点都可以视作头节点。

    - **双向链表**：与单向链表相比，双向链表记录了两个方向的引用。双向链表的节点定义同时包含指向后继节点（下一个节点）和前驱节点（上一个节点）的引用（指针）。相较于单向链表，双向链表更具灵活性，可以朝两个方向遍历链表，但相应地也需要占用更多的内存空间。

    ![常见链表类型](linkedlist_common_types.png)

### 应用

链表的应用十分广泛[^1]:

- 单向链表几乎是其他所有通用数据结构的实现基础（之一）

- 双向链表常用于需要快速查找前一个和后一个元素的场景

- 环形链表常用于需要周期性操作的场景，比如操作系统的资源调度


[^1]: [链表的典型应用 | Hello算法](https://www.hello-algo.com/chapter_array_and_linkedlist/linked_list/#424)
---
date: 2025-11-24 00:02:41
title: 线性表的链式表示
permalink: 
publish: true
---

# 线性表的链式表示

![](assets/linked/linked_type.webp)

## 单链表

>[单链表](../ds/linear/linked-list.md)

### 单链表的定义

![](assets/linked/linked.jpg)

```c
typedef struct LNode {
    ElemType data;      // 数据域
    struct LNode *next; // 指针域
} LNode, *LinkList;
```

最简单的单链表只包含一个**头指针**，==指向链表的第一个节点==，头指针为`NULL`时表示该链表为空。

为了操作上的方便，通常会在链表的第一个数据节点前设置一个**头节点**，其数据域通常不存放数据（也可以存放链表的长度），指针域指向第一个数据节点:

![](assets/linked/head.png)

引入头节点后，可以带来两个优点:

- 链表的第一个位置上的操作和在其他位置上的操作一致，无需特殊处理

- 无论链表是否为空，头指针都是指向头节点的非空指针，空表和非空表的处理也就得到了统一

### 单链表上基本操作的实现

#### 初始化

- 带头节点的单链表初始化

    ```c
    bool InitList(LinkList &L) {
        L = (LNode *)malloc(sizeof(LNode)); // 分配头节点
        if (L == NULL) {
            return false;
        }
        L->next = NULL; // 暂无数据节点
        return true;
    }
    ```

- 不带头节点的单链表初始化

    ```c
    bool InitList(LinkList &L) {
        L = NULL;   // 只需初始化头指针
        return true;
    }
    ```

#### 求表长

即计算链表数据节点的个数。这里注意，头节点不包含在内。

```c
int Length(LinkList L) {
    int len = 0;
    LNode *p = L->next;  // 带头节点时，L->next 指向第一个节点，因此从 L->next 开始
    while (p != NULL) {
        len++;
        p = p->next;
    }
    return len;
}
```

由于需要遍历链表，时间复杂度为 $O(n)$。

#### 按序号查找节点

从链表的第一个节点开始，顺序依次向下遍历，直至找到第`i`个节点。

```c
LNode *GetElem(LinkList L, int i) {
    int j = 0;          // 记录当前节点的序位
    LNode *p = L->next; // 指针p当前扫描到的节点
    while (p != NULL && j < i) {
        p = p->next;
        j++;
    }
    return p;
}
```

时间复杂度与求表长相同，为 $O(n)$。

#### 按值查找节点

从链表的第一个节点开始，顺序依次向下遍历比较，直至找到值为`e`的节点并返回，否则返回`NULL`。

```c
LNode *LocateElem(LinkList L, ElemType e) {
    LNode *p = L->next;
    while (p != NULL && p->data != e) {
        p = p->next;
    }
    return p;
}
```

时间复杂度为 $O(n)$。

#### 插入节点

将值为`e`的节点插入到链表的第`i`个位置。

![](assets/linked/linked_insert.png)

```c
bool ListInsert(LinkList &L, int i, ElemType e) {
    LNode *p = L;
    int j = 0;
    while (p != NULL && j < i - 1) {
        p = p->next;
        j++;
    }
    if (p == NULL) {
        return false;
    }
    LNode *s = (LNode *)malloc(sizeof(LNode));
    s->data = e;
    s->next = p->next;  // 1. 将s插入到p之后
    p->next = s;        // 2. 将p的next指向s
    return true;
}
```

注意1和2的顺序不能颠倒，否则相当于执行了`s->next = s`，显然有误，会导致链表断裂。

本算法的时间复杂度为 $O(n)$，因为需要遍历链表找到第`i`个节点；若直接指定在哪个元素后（前）插入，则时间复杂度为 $O(1)$:

```c
bool BackInsert(LNode *p, ElemType e) {
    LNode *s = (LNode *)malloc(sizeof(LNode));
    s->data = e;
    s->next = p->next;  // 将s插入到p之后
    p->next = s;
    return true;
}
```

#### 删除节点

将单链表的第`i`个节点删除。

![](assets/linked/linked_delete.jpg)

```c
bool ListDelete(LinkList &L, int i, ElemType &e) {
    LNode *p = L;
    int j = 0;
    while (p != NULL && j < i - 1) {
        p = p->next;
        j++;
    }
    if (p == NULL) {
        return false;
    }
    LNode *q = p->next;
    e = q->data;
    p->next = q->next;
    free(q);
    return true;
}
```

与插入同理，由于需要遍历查找到第`i`个节点，时间复杂度为 $O(n)$；若直接指定删除哪个元素，则时间复杂度为 $O(1)$:

```c
bool Delete(LNode *p) {
    LNode *q = (LNode *)malloc(sizeof(LNode));
    q = p->next;
    p->data = p->next->data;
    p->next = q->next;
    free(q);
    return true;
}
```

#### 头插法与尾插法

![](assets/linked/head_rear.webp)

##### 使用头插法建立单链表

该方法从空表开始，通过将节点依次插入元素的头部，从而实现链表的**逆序建立**。

```c
LinkList HeadInsert(LinkList &L) {
    LNode *s;
    int x;
    L = (LinkList)malloc(sizeof(LNode)); // 创建头节点
    L->next = NULL;
    scanf("%d", &x);
    while (x != 9999) {
        s = (LNode *)malloc(sizeof(LNode)); // 创建新节点
        s->data = x;
        s->next = L->next;
        L->next = s; // 将新节点插入到头节点之后
        scanf("%d", &x);
    }
    return L;
}
```

每次插入操作的时间复杂度都为 $O(1)$，总时间复杂度为 $O(n)$。

上面的头插法算法是链表**含有头节点**时的情况；若不带头节点，则每次插入新节点后都需要将头指针的指向更新为新节点。

##### 使用尾插法建立单链表

该方法从空表开始，通过将节点依次插入元素的尾部，从而实现链表的**顺序建立**。

```c
LinkList RearInsert(LinkList &L) {
    LNode *s;
    LNode *r = L; // r为表尾指针
    int x;
    L = (LinkList)malloc(sizeof(LNode)); // 创建头节点
    L->next = NULL;
    scanf("%d", &x);
    while (x != 9999) {
        s = (LNode *)malloc(sizeof(LNode)); // 创建新节点
        s->data = x;
        r->next = s;
        r = s; // 将r指向新的表尾节点s
        scanf("%d", &x);
    }
    r->next = NULL; // 尾节点指针置空
    return L;
}
```

这个算法设立了一个表尾指针`r`，时间复杂度与头插法相同，为 $O(n)$。

## 双链表

>[双链表](../ds/linear/double_linked.md)
>
>[双向链表的操作-双向链表和双向循环链表 | 稀土掘金@举止优雅的猩猩](https://juejin.cn/post/6844904131124002830#heading-1)

为克服单链表在访问某个节点的前驱时只能从头开始遍历的缺点，引入了**双链表**:

![](assets/linked/double_linked.awebp)

```c
typedef struct DNode {
    ElemType data;      // 数据域
    struct DNode *prior, *next; // 指针域，prior指向前驱，next指向后继
} DNode, *DLinkList;
```

### 双链表的插入操作

![](assets/linked/double_insert.awebp)

在单链表的基础上新增了一个前驱指针的操作:

```c
bool DoubleListInsert(DLinkList &L, int i, ElemType e) {
    DNode *p = L;
    int j = 0;
    while (p != NULL && j < i - 1) {
        p = p->next;
        j++;
    }
    if (p == NULL) {
        return false;
    }
    DNode *s = (DNode *)malloc(sizeof(DNode));
    s->data = e;
    s->next = p->next;
    p->next->prior = s;
    s->prior = p;
    p->next = s;
    return true;
}
```

特定节点后插:

```c
bool DoubleBackInsert(DNode *p, ElemType e) {
    DNode *s = (DNode *)malloc(sizeof(DNode));
    s->data = e;
    s->next = p->next; // 将s插入到p之后
    p->next->prior = s;
    s->prior = p;
    p->next = s; // 将p的next指向s
    return true;
}
```

其中注意带有注释的两行顺序不能颠倒，否则会丢失`*p`的后继节点。

### 双链表的删除操作

![](assets/linked/double_delete.awebp)

```c
bool DoubleListDelete(DLinkList &L, int i, ElemType &e) {
    DNode *p = L;
    int j = 0;
    while (p != NULL && j < i - 1) {
        p = p->next;
        j++;
    }
    if (p == NULL) {
        return false;
    }
    DNode *q = p->next;
    e = q->data;
    p->next = q->next;
    q->next->prior = p;
    free(q);
    return true;
}
```

删除特定节点:

```c
bool DoubleDelete(DNode *p) {
    LNode *q = (LNode *)malloc(sizeof(LNode));
    p->next = q->next;
    q->next->prior = p;
    free(q);
    return true;
```

## 循环链表

### 循环单链表

在单链表的基础上使最后一个节点的指针指向头节点，而不是`NULL`，从而形成一个环状结构，就构成了**循环单链表**:

![](assets/linked/loop_singal.png)

其基本操作与单链表基本一致，但是若操作是在表尾进行的，则需要更新新的尾节点的指针，使其指向头节点。

另外，循环单链表的判空条件是**头指针`L`是否等于头节点**，而不是是否为`NULL`。

### 循环双链表

>[双向循环链表的操作-双向链表和双向循环链表 | 稀土掘金@举止优雅的猩猩](https://juejin.cn/post/6844904131124002830#heading-9)

~~集大成者了属于是~~

![](assets/linked/loop_double.awebp)

在循环双链表中，头节点的prior还需要指向尾节点。

从上面的图示中不难看出，循环双向链表为空时，其头节点的prior域和next域都等于`L`。

# 静态链表

静态链表是用**数组描述**的链表，即**游标实现法**。

![](assets/linked/static_linked_concept.png)

![](assets/linked/static_linked.png)

## 顺序表和链表的对比

>[对比线性表-单链表](../ds/linear/linked-list.md#对比线性表)

1. 存取（读/写）方式

    - 顺序表既可以顺序存取，也可以随机存取

    - 链表只能顺序存取，即从表头开始依次顺序存取

2. 逻辑结构与物理结构

    - 采用顺序存储时，逻辑上相邻的元素在物理存储位置上也相邻

    - 采用链式存储时，逻辑上相邻的元素在物理存储位置上不一定相邻

3. 查找、插入和删除操作

    - 对于按值查找，顺序表无序时，两者的时间复杂度均为 $O(n)$

    - 有序时，顺序表可使用**折半查找（二分查找）**，时间复杂度为 $O(\log_2n)$，链表的时间复杂度为 $O(n)$

    - 对于按序号查找，顺序表支持随机访问，时间复杂度为 $O(1)$，链表只能顺序访问，时间复杂度为 $O(n)$

    - 对于插入和删除操作，顺序表平均需要移动半个表长的元素，时间复杂度为 $O(n)$，链表只需修改相关指针，时间复杂度为 $O(1)$

4. 空间分配

    - 顺序表的存储空间是静态分配的，需要预先分配足够大的空间，容易造成空间浪费

    - 链表的存储空间是动态分配的，需要的时候才分配，不会造成空间浪费，但是需要额外的指针空间来存储节点之间的逻辑关系，存储密度不大

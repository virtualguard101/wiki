/**
 * Copyright (c) 2025, vg101@smail.fjut.edu.cn
 * 在链表上实现排序
 * 功能：直接插入排序、冒泡排序、简单选择排序
 */

#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define ElemType int
#define MAX_SIZE 55

// 单链表节点结构
typedef struct LNode {
    ElemType data;
    struct LNode *next;
} LNode, *LinkList;


// 初始化单链表（带头结点）
LinkList initList(LinkList L) {
    L = (LinkList)malloc(sizeof(LNode));
    if (L == NULL) {
        printf("内存分配失败！\n");
        exit(1);
    }
    L->next = NULL;
    L->data = 0;  // 头结点存储链表长度
    return L;
}

// 获取链表长度
int getLength(LinkList L) {
    return L->data;
}

// 直接插入排序: 将链表分为已排序和未排序两部分，每次从未排序部分取出一个节点，插入到已排序部分的适当位置
int* insertSort(LinkList L) {
    // 用于记录比较和移动次数的临时变量, 0: 比较次数, 1: 移动次数
    static int counter[2] = {0, 0}; 
    
    // 重置计数器
    counter[0] = 0;
    counter[1] = 0;

    if (L->next == NULL || L->next->next == NULL) return NULL;
    
    LNode *sortedTail = L->next;  // 已排序部分的尾节点（初始为第一个节点）
    
    while (sortedTail->next != NULL) {
        LNode *p = sortedTail->next;  // 待插入的节点
        ElemType key = p->data;
        
        // 在已排序部分从头开始找插入位置
        LNode *prev = L;
        LNode *curr = L->next;
        
        while (curr != p) {
            counter[0]++;  // 比较次数+1
            if (curr->data > key) {
                break;  // 找到插入位置
            }
            prev = curr;
            curr = curr->next;
        }
        
        // 如果需要移动（插入位置不是当前位置）
        if (curr != p) {
            // 将p从原位置摘下
            sortedTail->next = p->next;
            counter[1]++;
            
            // 将p插入到prev之后
            p->next = curr;
            counter[1]++;
            prev->next = p;
            counter[1]++;
        } else {
            // 不需要移动，扩展已排序部分
            sortedTail = p;
        }
    }
    return counter;
}

// 冒泡排序: 相邻元素两两比较，如果逆序则交换数据域
int* bubbleSort(LinkList L) {
    static int counter[2] = {0, 0}; // 用于记录比较和移动次数的临时变量
    
    // 重置计数器
    counter[0] = 0;
    counter[1] = 0;

    if (L->next == NULL || L->next->next == NULL) return NULL;
    
    int n = getLength(L);
    int swapped;
    
    for (int i = 0; i < n - 1; i++) {
        swapped = 0;
        LNode *p = L->next;
        
        for (int j = 0; j < n - 1 - i; j++) {
            counter[0]++;  // 比较次数+1
            if (p->data > p->next->data) {
                // 交换数据域
                ElemType temp = p->data;
                counter[1]++;  // temp = p->data
                p->data = p->next->data;
                counter[1]++;  // p->data = p->next->data
                p->next->data = temp;
                counter[1]++;  // p->next->data = temp
                swapped = 1;
            }
            p = p->next;
        }
        
        // 如果一趟下来没有交换，说明已经有序
        if (!swapped) break;
    }
    return counter;
}

// 简单选择排序: 每次从未排序部分选择最小元素，与未排序部分的第一个元素交换
int* selectSort(LinkList L) {
    // 用于记录比较和移动次数的临时变量
    static int counter[2] = {0, 0}; 
    
    // 重置计数器
    counter[0] = 0;
    counter[1] = 0;

    if (L->next == NULL || L->next->next == NULL) return NULL;
    
    LNode *p = L->next;  // 指向未排序部分的第一个节点
    
    while (p->next != NULL) {
        LNode *minNode = p;  // 记录最小值节点
        LNode *q = p->next;
        
        // 找未排序部分的最小值
        while (q != NULL) {
            counter[0]++;  // 比较次数+1
            if (q->data < minNode->data) {
                minNode = q;
            }
            q = q->next;
        }
        
        // 如果最小值不是当前位置，交换数据
        if (minNode != p) {
            ElemType temp = p->data;
            counter[1]++;  // temp = p->data
            p->data = minNode->data;
            counter[1]++;  // p->data = minNode->data
            minNode->data = temp;
            counter[1]++;  // minNode->data = temp
        }
        
        p = p->next;
    }
    return counter;
}

// 生成已排序数据
void generateSorted(int arr[], int size) {
    for (int i = 0; i < size; i++) {
        arr[i] = i + 1;
    }
}

// 生成逆序数据
void generateReverse(int arr[], int size) {
    for (int i = 0; i < size; i++) {
        arr[i] = size - i;
    }
}

// 生成基本有序数据
void generateAlmost(int arr[], int size) {
    // 先生成有序数组
    for (int i = 0; i < size; i++) {
        arr[i] = i + 1;
    }
    // 随机交换10%的元素
    int swapCount = size / 10;
    for (int i = 0; i < swapCount; i++) {
        int idx1 = rand() % size;
        int idx2 = rand() % size;
        int temp = arr[idx1];
        arr[idx1] = arr[idx2];
        arr[idx2] = temp;
    }
}

// 生成随机序列
void generateRandom(int arr[], int size) {
    for (int i = 0; i < size; i++) {
        arr[i] = rand() % (size * 10) + 1;
    }
}

// 将数组转换为链表
LinkList transform(int arr[], int size) {
    // 创建链表并使用尾插法插入数据
    LinkList L = initList(L);
    LNode *tail = L;  // 尾指针，初始指向头结点
    
    for (int i = 0; i < size; i++) {
        LNode *newNode = (LNode *)malloc(sizeof(LNode));
        newNode->data = arr[i];
        newNode->next = NULL;
        tail->next = newNode;
        tail = newNode;  // 更新尾指针
        L->data++;  // 更新链表长度
    }
    return L;
}


int main() {
    // 已排序数据
    int sorted[MAX_SIZE];
    generateSorted(sorted, MAX_SIZE);
    // 逆序数据
    int reverse[MAX_SIZE];
    generateReverse(reverse, MAX_SIZE);
    // 基本有序数据
    int almost[MAX_SIZE];
    generateAlmost(almost, MAX_SIZE);
    // 随机数据
    srand(time(NULL)); // 设置随机种子
    int random[MAX_SIZE];
    generateRandom(random, MAX_SIZE);

    // 对不同数据进行排序并记录比较和移动次数
    int *result;

    // 直接插入排序
    LinkList L_sorted = transform(sorted, MAX_SIZE);
    result = insertSort(L_sorted);
    printf("直接插入排序 - 已排序数据: \n比较次数 = %d, 移动次数 = %d\n", result[0], result[1]);
    
    LinkList L_reverse = transform(reverse, MAX_SIZE);
    result = insertSort(L_reverse);
    printf("直接插入排序 - 逆序数据: \n比较次数 = %d, 移动次数 = %d\n", result[0], result[1]);
    
    LinkList L_almost = transform(almost, MAX_SIZE);
    result = insertSort(L_almost);
    printf("直接插入排序 - 基本有序数据: \n比较次数 = %d, 移动次数 = %d\n", result[0], result[1]);
    
    LinkList L_random = transform(random, MAX_SIZE);
    result = insertSort(L_random);
    printf("直接插入排序 - 随机数据: \n比较次数 = %d, 移动次数 = %d\n", result[0], result[1]);
    printf("\n");

    // 冒泡排序（重新创建链表）
    L_sorted = transform(sorted, MAX_SIZE);
    result = bubbleSort(L_sorted);
    printf("冒泡排序 - 已排序数据: \n比较次数 = %d, 移动次数 = %d\n", result[0], result[1]);
    
    L_reverse = transform(reverse, MAX_SIZE);
    result = bubbleSort(L_reverse);
    printf("冒泡排序 - 逆序数据: \n比较次数 = %d, 移动次数 = %d\n", result[0], result[1]);
    
    L_almost = transform(almost, MAX_SIZE);
    result = bubbleSort(L_almost);
    printf("冒泡排序 - 基本有序数据: \n比较次数 = %d, 移动次数 = %d\n", result[0], result[1]);
    
    L_random = transform(random, MAX_SIZE);
    result = bubbleSort(L_random);
    printf("冒泡排序 - 随机数据: \n比较次数 = %d, 移动次数 = %d\n", result[0], result[1]);
    printf("\n");

    // 选择排序（重新创建链表）
    L_sorted = transform(sorted, MAX_SIZE);
    result = selectSort(L_sorted);
    printf("选择排序 - 已排序数据: \n比较次数 = %d, 移动次数 = %d\n", result[0], result[1]);
    
    L_reverse = transform(reverse, MAX_SIZE);
    result = selectSort(L_reverse);
    printf("选择排序 - 逆序数据: \n比较次数 = %d, 移动次数 = %d\n", result[0], result[1]);
    
    L_almost = transform(almost, MAX_SIZE);
    result = selectSort(L_almost);
    printf("选择排序 - 基本有序数据: \n比较次数 = %d, 移动次数 = %d\n", result[0], result[1]);
    
    L_random = transform(random, MAX_SIZE);
    result = selectSort(L_random);
    printf("选择排序 - 随机数据: \n比较次数 = %d, 移动次数 = %d\n", result[0], result[1]);

    return 0;
}
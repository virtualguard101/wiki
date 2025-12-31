/**
 * Copyright (c) 2025, vg101@smail.fjut.edu.cn
 * 链表操作子系统
 * 功能：插入、删除、查找、计数、输出
 */

#include <stdio.h>
#include <stdlib.h>

#define ElemType int

// 单链表节点结构
typedef struct LNode {
    ElemType data;
    struct LNode *next;
} LNode, *LinkList;

// 初始化链表（不带头结点）
int initList(LinkList *L) {
    *L = NULL;
    return 0;
}

// 获取链表长度
int getLength(LinkList L) {
    int count = 0;
    LNode *p = L;
    while (p != NULL) {
        count++;
        p = p->next;
    }
    return count;
}

// 输出链表
void printList(LinkList L) {
    if (L == NULL) {
        printf("链表为空: []\n");
        return;
    }
    
    int len = getLength(L);
    LNode *p = L;
    int pos = 1;
    
    // 显示逻辑结构
    p = L;
    while (p != NULL) {
        printf("[%d]", p->data);
        if (p->next != NULL) printf(" -> ");
        p = p->next;
    }
    printf(" -> NULL\n");
}

// 按位置插入元素
int insertByPos(LinkList *L, int pos, ElemType e) {
    int len = getLength(*L);
    
    if (pos < 1 || pos > len + 1) {
        printf("插入位置不合法！有效范围: 1 ~ %d\n", len + 1);
        return 0;
    }
    
    // 创建新节点
    LNode *newNode = (LNode *)malloc(sizeof(LNode));
    if (newNode == NULL) {
        printf("内存分配失败！\n");
        return 0;
    }
    newNode->data = e;
    
    // 特殊情况：插入到第一个位置
    if (pos == 1) {
        newNode->next = *L;
        *L = newNode;
        return 1;
    }
    
    // 找到第 pos-1 个节点
    LNode *p = *L;
    for (int i = 1; i < pos - 1; i++) {
        p = p->next;
    }
    
    newNode->next = p->next;
    p->next = newNode;
    
    return 1;
}

// 头插法插入元素
void insertHead(LinkList *L, ElemType e) {
    LNode *newNode = (LNode *)malloc(sizeof(LNode));
    if (newNode == NULL) {
        printf("内存分配失败！\n");
        exit(1);
    }
    newNode->data = e;
    newNode->next = *L;
    *L = newNode;
}

// 尾插法插入元素
void insertTail(LinkList *L, ElemType e) {
    LNode *newNode = (LNode *)malloc(sizeof(LNode));
    if (newNode == NULL) {
        printf("内存分配失败！\n");
        exit(1);
    }
    newNode->data = e;
    newNode->next = NULL;
    
    // 特殊情况：链表为空
    if (*L == NULL) {
        *L = newNode;
        return;
    }
    
    // 找到最后一个节点
    LNode *p = *L;
    while (p->next != NULL) {
        p = p->next;
    }
    p->next = newNode;
}

// 按位置删除元素
int deleteByPos(LinkList *L, int pos, ElemType *e) {
    if (*L == NULL) {
        printf("链表为空，无法删除！\n");
        return 0;
    }
    
    int len = getLength(*L);
    if (pos < 1 || pos > len) {
        printf("删除位置不合法！有效范围: 1 ~ %d\n", len);
        return 0;
    }
    
    LNode *q;
    
    // 特殊情况：删除第一个节点
    if (pos == 1) {
        q = *L;
        *e = q->data;
        *L = q->next;
        free(q);
        return 1;
    }
    
    // 找到第 pos-1 个节点
    LNode *p = *L;
    for (int i = 1; i < pos - 1; i++) {
        p = p->next;
    }
    
    q = p->next;  // q 指向要删除的节点
    *e = q->data;
    p->next = q->next;
    free(q);
    
    return 1;
}

// 按值删除元素（删除第一个匹配的元素）
int deleteByValue(LinkList *L, ElemType e) {
    if (*L == NULL) {
        printf("链表为空，无法删除！\n");
        return 0;
    }
    
    // 特殊情况：删除的是第一个节点
    if ((*L)->data == e) {
        LNode *q = *L;
        *L = q->next;
        free(q);
        return 1;
    }
    
    // 查找要删除的节点
    LNode *p = *L;
    while (p->next != NULL) {
        if (p->next->data == e) {
            LNode *q = p->next;
            p->next = q->next;
            free(q);
            return 1;
        }
        p = p->next;
    }
    
    printf("未找到值为 %d 的元素！\n", e);
    return 0;
}

// 按位置查找元素
int findByPos(LinkList L, int pos, ElemType *e) {
    int len = getLength(L);
    
    if (pos < 1 || pos > len) {
        printf("查找位置不合法！有效范围: 1 ~ %d\n", len);
        return 0;
    }
    
    LNode *p = L;
    for (int i = 1; i < pos; i++) {
        p = p->next;
    }
    
    *e = p->data;
    return 1;
}

// 按值查找元素
int findByValue(LinkList L, ElemType e) {
    LNode *p = L;
    int pos = 1;
    while (p != NULL) {
        if (p->data == e) {
            return pos;
        }
        p = p->next;
        pos++;
    }
    return 0;  // 未找到
}

// 销毁链表
void destroyList(LinkList *L) {
    LNode *p = *L;
    while (p != NULL) {
        LNode *temp = p;
        p = p->next;
        free(temp);
    }
    *L = NULL;
}

// 显示菜单
void showMenu() {
    printf("\n================= 链表的操作子系统 =================\n");
    printf("  0. 退出程序\n");
    printf("  1. 插入元素（按位置）\n");
    printf("  2. 插入元素（头插法）\n");
    printf("  3. 插入元素（尾插法）\n");
    printf("  4. 删除元素（按位置）\n");
    printf("  5. 删除元素（按值）\n");
    printf("  6. 查找元素（按位置）\n");
    printf("  7. 查找元素（按值）\n");
    printf("  8. 计数（获取链表长度）\n");
    printf("  9. 输出链表\n");
    printf("  10. 清空链表\n");
    printf("请选择一个操作 (0-10): ");
}

int main() {
    LinkList L;
    initList(&L);
    int choice;
    int pos, value;
    ElemType e;
    int len;
    
    while (1) {
        showMenu();
        scanf("%d", &choice);
        
        switch (choice) {
            case 0:  // 退出
                destroyList(&L);
                return 0;
 
            case 1:  // 按位置插入
                printf("\n【按位置插入元素】\n");
                printf("操作前 - ");
                printList(L);
                len = getLength(L);
                printf("请输入插入位置 (1~%d): ", len + 1);
                scanf("%d", &pos);
                printf("请输入要插入的元素值: ");
                scanf("%d", &value);
                if (insertByPos(&L, pos, value)) {
                    printf("插入成功！\n");
                    printf("操作后 - ");
                    printList(L);
                }
                break;
                
            case 2:  // 头插法
                printf("\n【头插法插入元素】\n");
                printf("操作前 - ");
                printList(L);
                printf("请输入要插入的元素值: ");
                scanf("%d", &value);
                insertHead(&L, value);
                printf("插入成功！\n");
                printf("操作后 - ");
                printList(L);
                break;
                
            case 3:  // 尾插法
                printf("\n【尾插法插入元素】\n");
                printf("操作前 - ");
                printList(L);
                printf("请输入要插入的元素值: ");
                scanf("%d", &value);
                insertTail(&L, value);
                printf("插入成功！\n");
                printf("操作后 - ");
                printList(L);
                break;
                
            case 4:  // 按位置删除
                printf("\n【按位置删除元素】\n");
                printf("操作前 - ");
                printList(L);
                len = getLength(L);
                if (len == 0) break;
                printf("请输入删除位置 (1~%d): ", len);
                scanf("%d", &pos);
                if (deleteByPos(&L, pos, &e)) {
                    printf("删除成功！删除的元素值为: %d\n", e);
                    printf("操作后 - ");
                    printList(L);
                }
                break;
                
            case 5:  // 按值删除
                printf("\n【按值删除元素】\n");
                printf("操作前 - ");
                printList(L);
                len = getLength(L);
                if (len == 0) break;
                printf("请输入要删除的元素值: ");
                scanf("%d", &value);
                if (deleteByValue(&L, value)) {
                    printf("删除成功！\n");
                    printf("操作后 - ");
                    printList(L);
                }
                break;
                
            case 6:  // 按位置查找
                printf("\n【按位置查找元素】\n");
                printList(L);
                len = getLength(L);
                if (len == 0) break;
                printf("请输入查找位置 (1~%d): ", len);
                scanf("%d", &pos);
                if (findByPos(L, pos, &e)) {
                    printf("查找成功！第 %d 个位置的元素值为: %d\n", pos, e);
                }
                break;
                
            case 7:  // 按值查找
                printf("\n【按值查找元素】\n");
                printList(L);
                len = getLength(L);
                if (len == 0) break;
                printf("请输入要查找的元素值: ");
                scanf("%d", &value);
                pos = findByValue(L, value);
                if (pos > 0) {
                    printf("查找成功！元素 %d 在链表中的位置是: %d\n", value, pos);
                } else {
                    printf("未找到值为 %d 的元素！\n", value);
                }
                break;
                
            case 8:  // 计数
                printf("\n【计数 - 获取链表长度】\n");
                printf("链表长度 = %d\n", getLength(L));
                break;
                
            case 9:  // 输出链表
                printf("\n【输出链表】\n");
                printList(L);
                break;

            case 10:  // 清空链表
                printf("\n【清空链表】\n");
                printf("操作前 - ");
                printList(L);
                destroyList(&L);
                printf("链表已清空！\n");
                printf("操作后 - ");
                printList(L);
                break;

            default:
                printf("\n无效的选择, 请重新输入！\n");
        }
    }

    return 0;
}

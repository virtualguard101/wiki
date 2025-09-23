#include <iostream>
#include <vector>

/*
    链表节点类
*/
struct LinkedNode {
    std::vector<int> data;
    LinkedNode* next;

    LinkedNode(std::vector<int> data, LinkedNode* next) : data(data), next(next) {}
    LinkedNode(std::vector<int> data) : data(data), next(nullptr) {}
    LinkedNode() : data(std::vector<int>()), next(nullptr) {}
};

/*
    从现有数据初始化链表
*/
LinkedNode* initLinkedList(std::vector<int> data) {
    LinkedNode* head = new LinkedNode(data);
    LinkedNode* current = head;
    for(int i = 1; i < data.size(); i++) {
        current->next = new LinkedNode({data[i]});
        current = current->next;
    }
    return head;
}

/*
    打印链表元素
*/
void printLinkedList(LinkedNode* head) {
    LinkedNode* current = head;
    while(current != nullptr) {
        std::cout << current->data.at(0) << " ";
        current = current->next;
    }
    std::cout << std::endl;
}

/*
    @brief 在自身后插入一个节点
    @param self 参照节点
    @param node 插入节点
*/
void insertLinkedList(LinkedNode* self, LinkedNode* node) {
    node->next = self->next;
    self->next = node;
}

/*
    @brief 删除自身后的一个节点
    @param self 参照节点
*/
void removeLinkedList(LinkedNode* self) {
    if (self->next == nullptr) {
        throw std::runtime_error("There has no Node next of " + std::to_string(self->data.at(0)) + ".");
    }
    self->next = self->next->next;
}

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

/*
    查找链表节点
    @param head 链表头节点
    @param target 查找节点索引
    @return 查找节点索引
*/
int searchLinkedList(LinkedNode* head, int target) {
    LinkedNode* current = head;
    int index = 0;
    while(current != nullptr) {
        if (current->data.at(0) == target) {
            return index;
        }
        current = current->next;
    }
    return -1;
}

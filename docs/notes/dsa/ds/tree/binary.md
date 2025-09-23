# 二叉树

> [二叉树 | Hello算法](https://www.hello-algo.com/chapter_tree/binary_tree/)
>
> [Binary Tree Data Structure | GeeksForGeeks](https://www.geeksforgeeks.org/dsa/binary-tree-data-structure/)

## 定义

**二叉树（*binary tree*）**是一种非线性数据结构，代表“祖先”与“后代”之间的派生关系，体现了“一分为二”的分治逻辑。

二叉树以根节点为起点**一分为二**向下延伸。由于每个节点要么没有（只有数据域），要么有且只有两个子节点，可以用**左、右节点**分别表示这个两个子节点:

![二叉树](../../../assets/dsa.assets/ds/tree/binary/binary_tree_terminology.png)
*图片来源: [二叉树 | Hello算法](https://www.hello-algo.com/chapter_tree/binary_tree/)*

=== "Python"
    ```py
    class BinaryTreeNode:
        """二叉树节点类
        
        Attribute:
            data (Any): 节点数据域
            left ('BinaryTreeNode'): 子节点左节点引用
            right ('BinaryTreeNode'): 子节点右节点引用
        """
        def __init__(self, data: Any):
            self.data = data
            self.left: 'BinaryTreeNode' | None = None
            self.right: 'BinaryTreeNode' | None = None
    ```
=== "C++"
    ```cpp
    struct BinaryTreeNode {
        std::vector<int> val;  // 节点值
        BinaryTreeNode *left;  // 左子节点
        BinaryTreeNode *right;  // 右子节点

        // 初始化方法
        BinaryTreeNode() : val({}), left(nullptr), right(nullptr) {}
        BinaryTreeNode(std::vector<int> val) : val(val), left(nullptr), right(nullptr) {}
        BinaryTreeNode(std::vector<int> val, BinaryTreeNode *left, BinaryTreeNode *right) : val(val), left(left), right(right) {}
    };
    ```

## 常用操作

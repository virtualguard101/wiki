# 二叉树

## 定义

**二叉树（*binary tree*）**是一种非线性数据结构，代表“祖先”与“后代”之间的派生关系，体现了“一分为二”的分治逻辑。

二叉树以根节点为起点**一分为二**向下延伸。由于每个节点要么没有（只有数据域），要么有且只有两个子节点，可以用**左、右节点**分别表示这个两个子节点:

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

#include <vector>

struct BinaryTreeNode {
  std::vector<int> val;  // 节点值
  BinaryTreeNode *left;  // 左子节点
  BinaryTreeNode *right;  // 右子节点
  // 初始化方法
  BinaryTreeNode() : val({}), left(nullptr), right(nullptr) {}
  BinaryTreeNode(std::vector<int> val) : val(val), left(nullptr), right(nullptr) {}
  BinaryTreeNode(std::vector<int> val, BinaryTreeNode *left, BinaryTreeNode *right) : val(val), left(left), right(right) {}
};

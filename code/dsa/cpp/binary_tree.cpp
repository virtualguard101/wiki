#include <vector>

struct BinaryTreeNode {
  std::vector<int> data;  // 节点值
  BinaryTreeNode *left;  // 左子节点
  BinaryTreeNode *right;  // 右子节点
  // 初始化方法
  BinaryTreeNode() : data({}), left(nullptr), right(nullptr) {}
  BinaryTreeNode(std::vector<int> data) : data(data), left(nullptr), right(nullptr) {}
  BinaryTreeNode(std::vector<int> data, BinaryTreeNode *left, BinaryTreeNode *right) : data(data), left(left), right(right) {}
};

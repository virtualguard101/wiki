#include <vector>
#include <cstdlib>
#include <stdexcept>

/**
 * @brief 获取静态数组的长度
 * @param nums 静态数组
 * @param size 数组大小
 * @return 数组长度
 */
int static_array_length(int *nums, int size) {
  return size;
}

/**
 * @brief 获取动态数组的长度
 * @param nums 动态数组
 * @return 数组长度
 */
int array_length(std::vector<int> &nums) {
  return nums.size();
}

/** 
 * @brief 随机访问数组元素
 * @param nums 数组
 * @return 随机访问的元素
 */
std::vector<int> array_random_access(std::vector<int> &nums) {
  int random_index = rand() % nums.size();
  int res = nums.at(random_index);
  return {res};
}

/**
 * @brief 判断静态数组是否为空
 * @param nums 静态数组
 * @param size 数组大小
 * @return 是否为空
 */
bool static_array_is_empty(int *nums, int size) {
  int res = static_array_length(nums, size);
  return res == 0;
}

/**
 * @brief 判断动态数组是否为空
 * @param nums 动态数组
 * @return 是否为空
 */
bool array_is_empty(std::vector<int> &nums) {
  return nums.empty();
}

/**
 * @brief 判断静态数组是否为满
 * @param nums 静态数组
 * @param size 数组大小
 * @return 是否为满
 */
bool static_array_is_full(int *nums, int size) {
  return size == static_array_length(nums, size);
}

/**
 * @brief 将 num 插入 nums 的 index 处
 * @param nums 静态数组
 * @param size 数组大小
 * @param num 插入的元素
 * @param index 插入的位置
 */
void static_array_insert(int *nums, int size, int num, int index) {
  if (index < 0 || index > size) {
    throw std::out_of_range("Index out of range");
  }
  for (int i = size - 1; i > index; i--) {
    nums[i] = nums[i - 1];
  }
  nums[index] = num;
}

/**
 * @brief 将 num 插入 nums 的 index 处
 * @param nums 动态数组
 * @param num 插入的元素
 * @param index 插入的位置
 */
void array_insert(std::vector<int> &nums, int num, int index) {
  if (index < 0 || index > nums.size()) {
    throw std::out_of_range("Index out of range");
  }
  nums.push_back(0);
  for (int i = nums.size() - 1; i > index; i--) {
    nums.at(i) = nums.at(i - 1);
  }
  nums.at(index) = num;
}

/**
 * @brief 删除 nums 的 index 处的元素
 * @param nums 静态数组
 * @param size 数组大小
 * @param index 删除的位置
 */
void static_array_remove(int *nums, int size, int index) {
  if (index < 0 || index > size) {
    throw std::out_of_range("Index out of range");
  }
  for (int i = index; i < size - 1; i++) {
    nums[i] = nums[i + 1];
  }
  // 填充哨兵值
  nums[size - 1] = 0;
}

/**
* @brief 删除 nums 的 index 处的元素
* @param nums 动态数组
* @param index 删除的位置
*/
void array_remove(std::vector<int> &nums, int index) {
  if (index < 0 || index > nums.size()) {
    throw std::out_of_range("Index out of range");
  }
  for (int i = index; i < nums.size() - 1; i++) {
    nums.at(i) = nums.at(i + 1);
  }
  // 移除最后一个元素
  nums.pop_back();
}

/**
 * @brief 访问静态数组的元素
 * @param nums 静态数组
 * @param size 数组大小
 * @param index 访问的位置
 * @return 访问的元素
 */
int static_access_element(int *nums, int size, int index) {
  if (index < 0 || index > size) {
    throw std::out_of_range("Index out of range");
  }
  return nums[index];
}

/**
 * @brief 访问动态数组的元素
 * @param nums 动态数组
 * @param index 访问的位置
 * @return 访问的元素
 */
int access_element(std::vector<int> &nums, int index) {
  if (index < 0 || index > nums.size()) {
    throw std::out_of_range("Index out of range");
  }
  return nums.at(index);
}

/**
 * @brief 静态数组线性查找，根据元素查找索引
 * @param nums 静态数组
 * @param size 数组大小
 * @param target 目标元素
 * @return 目标元素的索引
 */
int static_linear_search(int *nums, int size, int target) {
  int length = static_array_length(nums, size);
  for (int i = 0; i < length; i++) {
    if (nums[i] == target) {
      return i;
    }
  }
  return -1;
}

/**
 * @brief 动态数组线性查找，根据元素查找索引
 * @param nums 动态数组
 * @param target 目标元素
 * @return 目标元素的索引
 */
int linear_search(std::vector<int> &nums, int target) {
  for (int i = 0; i < nums.size(); i++) {
    if (nums.at(i) == target) {
      return i;
    }
  }
  return -1;
}

/**
 * @brief 扩展静态数组
 * @param nums 静态数组
 * @param size 数组大小
 * @param enlarge 扩展的单位
 * @return 扩展后的数组
 */
void static_array_extend(int *nums, int size, int enlarge) {
  int new_size = size + enlarge;
  int *new_nums = new int[new_size];
  for (int i = 0; i < size; i++) {
    new_nums[i] = nums[i];
  }
  delete[] nums;
  nums = new_nums;
}

/**
 * @brief 扩展动态数组
 * @param nums 动态数组
 * @param enlarge 扩展的单位
 * @return 扩展后的数组
 */
void array_extend(std::vector<int> &nums, int enlarge) {
  nums.resize(nums.size() + enlarge);
}

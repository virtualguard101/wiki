# RAII 和智能指针

## RAII(Resource Acquisition Is Initialization)

**资源获取即初始化**(*RAII, Resource Acquisition Is Initialization*)，指将资源的生命周期与对象的生命周期绑定在一起的技术。这种技术确保资源在对象创建时获取，在对象销毁时释放，从而避免资源泄漏。

### 核心原则

- **在构造函数中获取资源**：当对象被创建时，它的构造函数负责获取所需的资源。

- **在析构函数中释放资源**：当对象被销毁时，它的析构函数负责释放之前获取的资源。

- **资源的所有权由对象管理**：资源的生命周期与对象的生命周期绑定。

### 优势

- **自动资源管理**：不需要手动释放资源，减少了忘记释放资源的风险。

- **异常安全**：即使在异常发生时，资源也能被正确释放。

- **代码简洁**：减少了资源管理的样板代码。

```cpp
class FileHandler {
private:
    FILE* file;

public:
    FileHandler(const char* filename, const char* mode) {
        file = fopen(filename, mode);
        if (!file) {
            throw std::runtime_error("Failed to open file");
        }
    }

    ~FileHandler() {
        if (file) {
            fclose(file);
        }
    }

    // 禁止复制
    FileHandler(const FileHandler&) = delete;
    FileHandler& operator=(const FileHandler&) = delete;

    // 文件操作方法
    void write(const char* data) {
        fputs(data, file);
    }
};

void processFile() {
    FileHandler handler("example.txt", "w");
    handler.write("Hello, RAII!");
    // 当 handler 离开作用域时，文件会自动关闭
}
```

- 参考阅读：[Resource Acquisition Is Initialization | GeeksForGeeks](https://www.geeksforgeeks.org/resource-acquisition-is-initialization/)

## 智能指针

智能指针是 C++ 标准库提供的实现 RAII 的模板类，用于自动管理动态分配的内存。它们确保内存在不再需要时被正确释放，从而避免内存泄漏。

STL中的主要智能指针：

- `std::unique_ptr`

    - 独占所有权的智能指针，不允许复制，但可以移动

    - 当 `unique_ptr` 被销毁时，它所指向的对象也会被销毁

```cpp
void rawPtrFn() {
    Node* n = new Node;
    // ...
    delete n;
}
/* This plan should be abandoned. */

/* Use this one! */
void rawPtrFn() {
    std::unique_ptr<Node> n(new Node);
    // ...
    // n will automatically freed.
}
```

- `std::shared_ptr`

    - 共享所有权的智能指针，允许多个 `shared_ptr` 指向同一个对象

    - 使用引用计数来跟踪有多少个 `shared_ptr` 指向同一个对象

    - 当最后一个指向对象的 `shared_ptr` 被销毁时，对象才会被销毁

!!! note
    共享指针解决了 std::unique_ptr 不能复制的限制，它通过引用计数机制确保只有当所有指向某块内存的共享指针都离开作用域后，才会释放该内存。

    ![](../../../../assets/images/cpp/share_pointer.png)

- `std::weak_ptr`

    - 弱引用，不增加引用计数

    - 用于打破 `shared_ptr` 循环引用导致的内存泄漏问题

    - 可以从 `weak_ptr` 创建 `shared_ptr`，但只有当原始对象仍然存在时才能成功

```cpp
#include <memory>
#include <iostream>

class Resource {
public:
    Resource() { std::cout << "Resource acquired\n"; }
    ~Resource() { std::cout << "Resource released\n"; }
    void use() { std::cout << "Resource used\n"; }
};

void useUniquePtr() {
    // 创建 unique_ptr
    std::unique_ptr<Resource> res = std::make_unique<Resource>();
    res->use();
    
    // 转移所有权
    std::unique_ptr<Resource> res2 = std::move(res);
    res2->use();
    
    // res 现在为 nullptr
    if (!res) {
        std::cout << "res is nullptr\n";
    }
    
    // res2 离开作用域时，Resource 会被自动释放
}

void useSharedPtr() {
    // 创建 shared_ptr
    std::shared_ptr<Resource> res1 = std::make_shared<Resource>();
    {
        std::shared_ptr<Resource> res2 = res1; // 共享所有权
        std::cout << "Reference count: " << res1.use_count() << "\n"; // 输出 2
    }
    // res2 离开作用域，引用计数减少
    std::cout << "Reference count: " << res1.use_count() << "\n"; // 输出 1
    
    // res1 离开作用域时，Resource 会被自动释放
}

void useWeakPtr() {
    std::weak_ptr<Resource> weak;
    {
        std::shared_ptr<Resource> shared = std::make_shared<Resource>();
        weak = shared;
        
        // 从 weak_ptr 创建 shared_ptr
        if (auto temp = weak.lock()) {
            temp->use();
        }
    }
    // shared 离开作用域，Resource 被释放
    
    // 尝试从 weak_ptr 创建 shared_ptr
    if (auto temp = weak.lock()) {
        temp->use();
    } else {
        std::cout << "Resource no longer exists\n";
    }
}

int main() {
    std::cout << "=== Using unique_ptr ===\n";
    useUniquePtr();
    
    std::cout << "\n=== Using shared_ptr ===\n";
    useSharedPtr();
    
    std::cout << "\n=== Using weak_ptr ===\n";
    useWeakPtr();
    
    return 0;
}
```

!!! note "为什么应该使用 `std::make_unique` 和 `std::make_shared`"
    - 最重要的原因在于当你不使用 `std::make_unique<T>` 或 `std::make_shared<T>` 时，会发生两次独立的内存分配：

        - 第一次分配：为对象 T 分配内存（通过 `new T(...)`）

        - 第二次分配：为智能指针的控制块分配内存

    - 同时还应保持一致性：

        - 如果使用了 `make_unique`，那么一定要同时使用 `make_share`

- 参考阅读：[Smart Pointers in C++ | GeeksForGeeks](https://www.geeksforgeeks.org/smart-pointers-cpp/)

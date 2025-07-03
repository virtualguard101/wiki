# CMake

**CMake**本质上可简单理解为一个`Makefile`生成器，有自己的构建语法。

- 官方教程(`v3.22`)：[CMake Tutorial](https://cmake.org/cmake/help/v3.22/guide/tutorial/index.html)

## 简单案例

### 普通构建配置

假设有以下项目结构：
```bash
.
├── build       # use for store cmake cache
├── CMakeLists.txt
├── include     # store .h file
│   ├── point.h
│   └── vector.h
├── logger      # logger program
│   ├── log.cpp
│   └── log.h
├── main.cpp    # main program
├── src         # executable file
│   ├── point.cpp
│   ├── template.py
│   └── vector.cpp
├── test        # test file
│   └── test.cpp
├── vcpkg-configuration.json
└── vcpkg.json
```

`CMakeLists.txt`如下
```bash
# 指定 CMake 的最低版本要求
cmake_minimum_required(VERSION 3.10)

# 设置项目名称与版本号
project(cgEngine VERSION 0.0.0)

# 设置 C++ 标准
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# 添加可执行文件
# 创建静态库
add_library(${PROJECT_NAME}_lib STATIC
    src/vector.cpp
    src/point.cpp
    logger/log.cpp
)

# 主可执行文件
add_executable(${PROJECT_NAME} main.cpp)
target_link_libraries(${PROJECT_NAME} PRIVATE ${PROJECT_NAME}_lib)

# 设置头文件目录
# 设置头文件目录（PUBLIC可见性）
target_include_directories(${PROJECT_NAME}_lib
    PUBLIC
    ${CMAKE_CURRENT_SOURCE_DIR}/include
    ${CMAKE_CURRENT_SOURCE_DIR}/logger)

# 添加测试目标
enable_testing()  # 启用测试功能

# 添加测试可执行文件
# 创建测试可执行文件并链接库
add_executable(test_${PROJECT_NAME} test/test.cpp)
# 主可执行文件需要包含目录
target_include_directories(${PROJECT_NAME}
    PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}/include)
target_link_libraries(test_${PROJECT_NAME} PRIVATE ${PROJECT_NAME}_lib)

# 添加测试并指定工作目录
add_test(NAME test_${PROJECT_NAME}
    COMMAND test_${PROJECT_NAME}
    WORKING_DIRECTORY ${CMAKE_BINARY_DIR})

target_link_libraries(${PROJECT_NAME}_lib PRIVATE GL glfw m)

target_link_libraries(test_${PROJECT_NAME} PRIVATE GL glfw m)
```

可通过以下命令进行测试构建/构建：
```bash
cd build
cmake ..
make
```

通过以下命令进行测试/运行主程序：
```bash
# test
make test

# main program
./cgEngine
```

通过以下命令清除构建缓存：
```bash
# in build/
rm -rf *
```

### 配合`vcpkg`进行构建

基础配置参考[vcpkg | virtualguard's note](https://note.virtualguard101.com/notes/tools/vcpkg/)

假设需要依赖`glfw3`，`CMakeLists.txt`如下

```bash
# 指定 CMake 的最低版本要求
cmake_minimum_required(VERSION 3.10)

# 设置项目名称与版本号
project(cgEngine VERSION 0.0.0)

# 设置 C++ 标准
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# 添加可执行文件
# 创建静态库
add_library(${PROJECT_NAME}_lib STATIC
    src/vector.cpp
    src/point.cpp
    logger/log.cpp
)

# 主可执行文件
add_executable(${PROJECT_NAME} main.cpp)
target_link_libraries(${PROJECT_NAME} PRIVATE ${PROJECT_NAME}_lib)

# 设置头文件目录
# 设置头文件目录（PUBLIC可见性）
target_include_directories(${PROJECT_NAME}_lib
    PUBLIC
    ${CMAKE_CURRENT_SOURCE_DIR}/include
    ${CMAKE_CURRENT_SOURCE_DIR}/logger)

# 添加测试目标
enable_testing()  # 启用测试功能

# 添加测试可执行文件
# 创建测试可执行文件并链接库
add_executable(test_${PROJECT_NAME} test/test.cpp)
# 主可执行文件需要包含目录
target_include_directories(${PROJECT_NAME}
    PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}/include)
target_link_libraries(test_${PROJECT_NAME} PRIVATE ${PROJECT_NAME}_lib)

# 添加测试并指定工作目录
add_test(NAME test_${PROJECT_NAME}
    COMMAND test_${PROJECT_NAME}
    WORKING_DIRECTORY ${CMAKE_BINARY_DIR})

# 设置链接库
target_link_libraries(${PROJECT_NAME}_lib PRIVATE 
    m
    GL 
    glfw 
)

target_link_libraries(test_${PROJECT_NAME} PRIVATE 
    m
    GL 
    glfw 
)
```

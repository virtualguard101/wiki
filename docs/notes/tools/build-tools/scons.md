# SCons

一个开源的软件构建工具，类似于 Make，但使用 Python 脚本作为配置文件。它提供了一种更现代、更灵活的方式来管理软件构建过程。

[Godot](https://godotengine.org/zh-cn/)源码就使用**SCons**进行构建

- 官网：[SCons: A software construction tool](https://scons.org/)

- 官方文档：[Current Documentation | SCons](https://scons.org/documentation.html)

- 与**CMake**的选择：[SCons or CMake instead of qmake](https://stackoverflow.com/questions/14197372/scons-or-cmake-instead-of-qmake)

但由于其构建配置基于Python，等于在构建过程中在项目源码与编译器间加入了一个Python解释器的兼容层，这对性能的依赖无疑是大于CMake/xmake等一众构建工具的。

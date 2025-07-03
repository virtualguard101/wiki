# vcpkg

**vcpkg**是微软提供并维护的一个开源的**C++包管理器**，形式上类似于Python的**pip**/**uv**等工具。

- 官方中文文档 & 教程：[vcpkg 文档](https://learn.microsoft.com/zh-cn/vcpkg/)

## 配合CMake进行使用

- 官方教程：[通过 CMake 安装和使用包](https://learn.microsoft.com/zh-cn/vcpkg/get_started/get-started?pivots=shell-bash#1---set-up-vcpkg)

适合较为轻量的项目。

使用vscode配合CMake的操作差别不大，详情可参考[在 Visual Studio Code 中通过 CMake 安装和使用包](https://learn.microsoft.com/zh-cn/vcpkg/get_started/get-started-vscode?pivots=shell-bash)

安装过程官方教程有详尽的说明，这里不再赘述。

- 初始化

通过以下命令在项目的目录中创建清单文件：
```bash
vcpkg new --application
```

该命令会在项目的根目录下创建`vcpkg.json`和`vcpkg-configuration.json`。二者的作用分别是**作为依赖项列表**及**引入[基线](https://learn.microsoft.com/zh-cn/vcpkg/reference/vcpkg-configuration-json#registry-baseline)约束**。

- 修改`CMakeLists.txt`

在`CMakeLists.txt`中添加以下内容：
```bash
find_package([your_lib] CONFIG REQUIRED)
```
表示使用第三方库的 CMake 配置文件查找该库。`REQUIRED`关键字确保在找不到包时生成错误。

如果只是使用一个库的某些组件，也可这样配置（以`Qt6`为例）：
```bash
find_package(Qt6 REQUIRED COMPONENTS Core Widgets)  # 根据需要选择组件
```
`COMPONENTS`参数用于指定需要的Qt模块。

注意`target_link_libraries`列表中也需添加引入的第三方库名。

- 创建 CMake 配置

参考[官方教程](https://learn.microsoft.com/zh-cn/vcpkg/get_started/get-started?pivots=shell-bash#4---build-and-run-the-project)配置CMake工具链。

!!! note
    `CMakeUserPresets.json` 文件会将 `VCPKG_ROOT` 环境变量设置为指向包含 `vcpkg` 本地安装的绝对路径，因此注意配置完成后将`CMakeUserPresets.json`移入`.gitignore`，以避免信息泄漏等问题。

配置完成后即可进行生成与构建运行。

## 可能遇到的问题

### 缺少依赖项

如果在运行`cmake --preset=default`的过程中出现错误，且在项目的`build/vcpkg-manifest-install.log`日志中出现类似下面的信息：
```bash
qtbase currently requires packages from the system package manager.  They
  can be installed on Ubuntu systems via sudo apt-get install '^libxcb.*-dev'
  libx11-xcb-dev libglu1-mesa-dev libxrender-dev libxi-dev libxkbcommon-dev
  libxkbcommon-x11-dev libegl1-mesa-dev.
Call Stack (most recent call first):
  scripts/ports.cmake:206 (include)
```

说明缺少依赖项，根据提示安装后删除`build`然后重新运行`cmake --preset=default`进行配置生成即可。

出现问题时可通过管道命令查看是否存在依赖缺失的问题：
```bash
cat build/vcpkg-manifest-install.log | grep apt-get
```

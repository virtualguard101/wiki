---
date: 2026-05-05 23:51:32
title: C++ Coding Style
permalink: cpp-coding-style
publish: true
tags:
  - 编程语言
  - C++
---

# C++ Coding Style

> [Bjarne Stroustrup's C++ Style and Technique FAQ](https://www.stroustrup.com/bs_faq2.html)

C++ 社区里认可度较高的风格主要有 [Google](https://google.github.io/styleguide/cppguide.html)、[LLVM](https://llvm.org/docs/CodingStandards.html)、[Mozilla](https://firefox-source-docs.mozilla.org/code-quality/coding-style/coding_style_cpp.html)、[Chromium](https://chromium.googlesource.com/chromium/src/+/main/styleguide/c++/c++.md)，以及偏“原则指导”的 [C++ Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines)

工程上最常见的组合是 [clang-format](https://clang.llvm.org/docs/ClangFormat.html) + [clang-tidy](https://clang.llvm.org/extra/clang-tidy/)。

---

## 部分 C++ Coding Style

### Google C++ Style Guide

> [Google C++ Style Guide](https://google.github.io/styleguide/cppguide.html)

- **定位**：规则详细、约束较强，强调团队协作时的一致性和可读性。

- **适合场景**：多人协作、长期维护的企业项目。

- **关键词**：规范严格、可维护优先、审查友好。

#### 命名规范

- **类型（class/struct/enum/typedef）**：`PascalCase`，如 `HttpClient`。

- **函数名**：`PascalCase`，如 `SendRequest()`。

- **变量名（局部变量/参数/成员变量）**：`snake_case`，如 `retry_count`。

- **常量名**：`kPascalCase`，如 `kDefaultTimeoutMs`。

- **宏名**：`ALL_CAPS_WITH_UNDERSCORES`，如 `MAX_BUFFER_SIZE`。

- **命名空间**：一般使用小写（必要时可下划线分词），如 `net`、`image_codec`。

### LLVM Coding Standards

> [LLVM Coding Standards](https://llvm.org/docs/CodingStandards.html)

- **定位**：简洁、统一，和 LLVM/Clang 生态契合度高。

- **适合场景**：编译器、基础设施、中大型开源项目。

- **关键词**：现代 C++、风格统一、工程实践成熟。

#### 命名规范

- **类型（class/struct/enum）**：`PascalCase`，如 `SmallVector`。

- **函数名**：`camelCase`，如 `getElementPtr()`。

- **变量名**：`camelCase`，如 `retryCount`。

- **常量名**：LLVM 中常见常量也采用 `camelCase`（具体以子项目约定为准）。

- **宏名**：`ALL_CAPS_WITH_UNDERSCORES`。

### Mozilla C++ Style

> [Mozilla C++ Style](https://firefox-source-docs.mozilla.org/code-quality/coding-style/coding_style_cpp.html)

- **定位**：历史久、工程导向明显，强调跨平台与可读性。

- **适合场景**：有历史积累的大型跨平台项目。

- **关键词**：兼容性、审查效率、稳健维护。

#### 命名规范

- **类型（class/struct/enum）**：`PascalCase`。

- **函数名**：通常使用 `camelCase`。

- **变量名**：通常使用 `camelCase`。

- **常量名**：常见 `k` 前缀或项目自定义约定（以仓库规则为准）。

- **宏名**：`ALL_CAPS_WITH_UNDERSCORES`。

### Chromium C++ Style

> [Chromium C++ Style](https://chromium.googlesource.com/chromium/src/+/main/styleguide/c++/c++.md)

- **定位**：在大规模工程实践下形成的风格体系，关注性能与安全。

- **适合场景**：超大代码库、系统级/浏览器类项目。

- **关键词**：性能、安全、可审查性。

#### 命名规范

- **类型（class/struct/enum）**：`PascalCase`。

- **函数名**：`camelCase`（和 Chromium 代码风格保持一致）。

- **变量名**：`camelCase`。

- **常量名**：常见 `k` 前缀 + `PascalCase`，如 `kMaxRetryCount`。

- **宏名**：`ALL_CAPS_WITH_UNDERSCORES`。

### C++ Core Guidelines（原则集）

> [C++ Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines)

- **定位**：更偏“怎么写出更安全、更现代的 C++”，不只是排版风格。

- **适合场景**：新项目设计、旧项目现代化重构。

- **关键词**：RAII、类型安全、资源管理、现代 C++ 思维。

#### 命名规范

- **说明**：Core Guidelines 不是“统一排版手册”，而是“现代 C++ 设计原则集”，对命名不做像 Google/LLVM 那样的强制统一。

- **实践建议**：在项目中选择一套固定命名风格并长期一致；优先保证“见名知意”与语义清晰。

- **推荐基线**（可选）：

    - 类型：`PascalCase`

    - 函数/变量：`snake_case` 或 `camelCase`（二选一，不混用）

    - 常量：`kPascalCase`

    - 宏：`ALL_CAPS_WITH_UNDERSCORES`


## Formatting Tools

### clang-format

> [clang-format](https://clang.llvm.org/docs/ClangFormat.html)

- **作用**：自动统一代码格式（缩进、换行、括号风格等）。

- **优点**：社区事实标准，和 IDE/CI 集成成熟，支持多种预设（Google/LLVM/Mozilla/Chromium）。

- **常见用法**：在仓库根目录放 `.clang-format`，提交前自动格式化。

    - 在项目根目录生成[对应风格](https://clang.llvm.org/docs/ClangFormatStyleOptions.html)的 `.clang-format`：

        ```bash
        clang-format -style=<format_option> -dump-config > .clang-format
        ```

    - 终端预览格式化结果：

        ```bash
        clang-format <file1> <file2> ...
        ```
    
    - 写入格式化：

        ```bash
        clang-format -i <file1> <file2> ...
        ```

    - 配合 [`rg`](https://github.com/burntsushi/ripgrep) 批量处理：

        ```bash
        rg --files /path -g '*.{h,hpp,cc,cpp,cxx}' -0 | xargs -0 clang-format -i
        ```


### clang-tidy

> [clang-tidy](https://clang.llvm.org/extra/clang-tidy/)

- **作用**：静态检查 + 一部分自动修复，不只是格式，还能给出现代化与安全建议。

- **优点**：可发现潜在 bug、坏味道和不推荐写法。

- **常见用法**：CI 中做质量门禁，本地配合 `-fix` 做自动修复。

建议与 clang-format 搭配使用。

### Uncrustify

> [Uncrustify](https://github.com/uncrustify/uncrustify)

- **作用**：可高度定制的格式化工具。

- **优点**：灵活度高。

- **注意**：配置复杂，上手和维护成本较高。

### AStyle (Artistic Style)

> [AStyle (Artistic Style)](https://github.com/astyle/astyle)

- **作用**：轻量格式化工具。

- **优点**：简单、易用。

- **注意**：生态和能力通常弱于 clang-format。

## Practical Suggestions

### 新项目

- 推荐：`clang-format + clang-tidy`

- 风格基线：优先从 `LLVM` 或 `Google` 预设开始，再小幅定制。

### 旧项目

- 原则：先跟随现有风格，避免一次性全仓库大改造成 review 噪音。

- 做法：按模块逐步收敛，配合 CI 慢慢统一。

### 团队协作

- 原则：把格式统一交给工具，减少“手工争论格式”。

- 做法：本地 pre-commit 自动 format + CI 检查未格式化代码。

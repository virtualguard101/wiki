---
date: 2026-05-05 23:40:32
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

### LLVM Coding Standards

> [LLVM Coding Standards](https://llvm.org/docs/CodingStandards.html)

- **定位**：简洁、统一，和 LLVM/Clang 生态契合度高。

- **适合场景**：编译器、基础设施、中大型开源项目。

- **关键词**：现代 C++、风格统一、工程实践成熟。

### Mozilla C++ Style

> [Mozilla C++ Style](https://firefox-source-docs.mozilla.org/code-quality/coding-style/coding_style_cpp.html)

- **定位**：历史久、工程导向明显，强调跨平台与可读性。

- **适合场景**：有历史积累的大型跨平台项目。

- **关键词**：兼容性、审查效率、稳健维护。

### Chromium C++ Style

> [Chromium C++ Style](https://chromium.googlesource.com/chromium/src/+/main/styleguide/c++/c++.md)

- **定位**：在大规模工程实践下形成的风格体系，关注性能与安全。

- **适合场景**：超大代码库、系统级/浏览器类项目。

- **关键词**：性能、安全、可审查性。

### C++ Core Guidelines（原则集）

> [C++ Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines)

- **定位**：更偏“怎么写出更安全、更现代的 C++”，不只是排版风格。

- **适合场景**：新项目设计、旧项目现代化重构。

- **关键词**：RAII、类型安全、资源管理、现代 C++ 思维。


## Formatting Tools

### clang-format

> [clang-format](https://clang.llvm.org/docs/ClangFormat.html)

- **作用**：自动统一代码格式（缩进、换行、括号风格等）。

- **优点**：社区事实标准，和 IDE/CI 集成成熟，支持多种预设（Google/LLVM/Mozilla/Chromium）。

- **常见用法**：在仓库根目录放 `.clang-format`，提交前自动格式化。

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

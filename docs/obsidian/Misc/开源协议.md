---
date: 2025-10-09 15:26:00
title: 开源协议
permalink: 
publish: true
---

# 开源协议

> [Choose an open source license](https://choosealicense.com/)


## MIT License

[MIT License](https://choosealicense.com/licenses/mit/) 是一种非常宽松的许可协议，允许使用者自由地使用、修改和分发软件。它是最常用的开源许可证之一，广泛应用于各种软件项目中。

### 许可内容

- 使用者可以自由地使用、修改和分发软件。

### 应用场景

基本上只要是不需要太严格限制使用者行为的软件，都可以使用 MIT License。如果没有特别的需求，一般推荐使用 MIT License，因为它**简单宽松**。

## Apache License 2.0

[Apache License 2.0](https://choosealicense.com/licenses/apache-2.0/) 与 MIT License 类似，也是**宽松**的许可协议。二者的区别在于前者的条款更长、更详细，结构化且包含更多具体规定。

### 许可内容

- 软件使用、修改和分发协议基本与 MIT License 相同，但条款更长、更详细，结构化且包含更多具体规定。

- 核心要求是保留版权声明和许可文本，还包括专利授权、免责条款和贡献者义务等。

### 应用场景

与 MIT 的简洁相比，Apache License 2.0 提供了更清晰的法律框架，适合需要明确保护的**大型项目或企业**使用。

## GNU GPLv3 & AGPLv3

### GPLv3

[GNU GPLv3](https://choosealicense.com/licenses/gpl-3.0/) 是 GNU General Public License 的第三个版本，是 GNU 通用公共许可证的缩写。它是一种[**Copyleft**许可证](https://www.pingcap.com/article/understanding-copyleft-licenses-and-their-purpose/)，要求所有修改和分发都必须包含原始许可证文本。

简单来说，GPLv3 同样允许人们几乎可以随心所欲地使用应用该协议的项目，但**禁止分发闭源版本**。

### AGPLv3

[GNU AGPLv3](https://choosealicense.com/licenses/agpl-3.0/) 则在 GPLv3 的基础上增加了**网络服务**的限制，旨在<mark>确保通过网络提供服务的软件也能触发开源义务</mark>，传染性比 GPLv3 更严格。

简单来说，AGPLv3 在 GPLv3 的基础上要求当修改版本用于提供网络服务时，必须履行开源义务。

### 应用场景

如果关心分享改进成果，或者项目就是以促进开源为目的而创建的，那么就可以考虑使用这两个协议。

### 二者对比案例

以一个web插件与应用了该插件的网站为例：

- 如果该插件是 GPLv3+:

    - 构建出来的文档和网站 可以不开源

    - 但如果项目直接引用或修改插件源码，则必须开源

- 如果该插件是 AGPLv3:

    - 若插件的代码在网站运行时被用户使用（例如前端 JS），那么网站源码必须开源；

    - 若它只是构建工具（构建后不包含 AGPL 代码），则仍可闭源。

| 情况                   | GPLv3 插件 | AGPL 插件        |
|-------------------------|:--------:|:--------------:|
| 仅用于构建（离线使用）               | ✅ 可闭源    | ✅ 可闭源          |
| 引用了插件源码（集成或修改）            | ❌ 必须开源   | ❌ 必须开源         |
| 插件代码在网页运行时被用户访问（例如 JS 部分） | ✅ 可闭源    | ❌ 必须开源（触发网络条款） |

## 非软件许可证

对我而言，最常用的的非软件许可证应该是用于**数据**、**文档**的许可证。

需要注意的是，任何开源软件许可证或媒体开放许可证（见上文）同样适用于软件文档，软件与其对应文档可采用不同的协议。

### CC-BY-4.0 & CC-BY-NC-4.0

二者都来自 [Creative Commons（知识共享组织）](https://creativecommons.org/)，都是[**知识共享许可协议**](https://creativecommons.org/share-your-work/cclicenses/)。

- [前者](https://choosealicense.com/licenses/cc-by-4.0/)允许几乎所有用途，但需注明出处和许可声明。常用于媒体资源和教育材料，是开放获取科学出版物中最常见的许可方式，但不建议用于软件

- [后者](https://choosealicense.com/licenses/cc-by-sa-4.0/)在前者的基础上要求衍生作品在相同或类似的兼容许可下分发。常用于媒体资源和教育材料。该许可的早期版本是维基百科及其他维基媒体项目的默认许可

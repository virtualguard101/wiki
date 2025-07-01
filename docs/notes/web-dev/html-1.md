# HTML

>- [使用HTML构建Web | MDN Web Docs](https://developer.mozilla.org/zh-CN/docs/Learn_web_development/Core/Structuring_content)
>
>- [MIT Web Development Crash Course](https://weblab.mit.edu/schedule)

## 基本概念

HTML（HyperText Markup Language，超文本标记语言）是一种用来告知浏览器如何组织页面的标记语言，用于定义网页结构[^1]。

![](https://developer.mozilla.org/zh-CN/docs/Learn_web_development/Core/Structuring_content/Basic_HTML_syntax/grumpy-cat-small.png)

如上图所示，这是一个**HTML元素**。HTML 由一系列的元素组成，这些元素可以用来包围或标记不同部分的内容，使其以某种方式呈现或者工作。

针对一个制作精良的网页，可将其对应的 HTML 文件分解为多个不同的**块**，在这些块中也可存在**嵌套**关系。

## 元素属性

### 属性概述

在 HTML 中，元素可以拥有**属性**。属性包含元素的额外信息，这些信息不会出现在实际的网页内容中[^2]。

!!! important

    - 一个空格，它在属性和元素名称之间。如果一个元素具有多个属性，则每个**属性之间必须由空格分隔**

    - 属性名称，后面跟着一个等于号`=`

    - 一个属性值，由一对引号`""`引起来

- *e.g.*

    ```html
    <p>A link to my <a href="https://virtualguard101.com/" title="virtualguard101's Homepage" target="_blank">homepage</a>.</p>
    ```

    在上面的例子中：

    - `href`属性声明超链接的 web 地址；

    - `title`属性为超链接声明额外的信息，当鼠标悬停在超链接上面时，这部分信息将以工具提示的形式显示；
    
    - `target`属性用于指定链接如何呈现出来，在上面的例子中，`target="_blank"` 表示将在新标签页中显示链接。

### 布尔属性




[^1]: [HTML | MDN Web Docs](https://developer.mozilla.org/zh-CN/docs/Glossary/HTML)

[^2]: [HTML 属性 | MDN Web Docs](https://developer.mozilla.org/zh-CN/docs/Learn_web_development/Core/Structuring_content/Basic_HTML_syntax#%E5%B1%9E%E6%80%A7)
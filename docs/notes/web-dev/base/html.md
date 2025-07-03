# HTML 要点

>- [使用HTML构建Web | MDN Web Docs](https://developer.mozilla.org/zh-CN/docs/Learn_web_development/Core/Structuring_content)
>
>- [MIT Web Development Crash Course](https://weblab.mit.edu/schedule)

## HTML 基本概念 & 基础

HTML（HyperText Markup Language，超文本标记语言）是一种用来告知浏览器如何组织页面的标记语言，用于定义网页结构[^1]。

![](https://developer.mozilla.org/zh-CN/docs/Learn_web_development/Core/Structuring_content/Basic_HTML_syntax/grumpy-cat-small.png)

如上图所示，这是一个**HTML元素**。HTML 由一系列的元素组成，这些元素可以用来包围或标记不同部分的内容，使其以某种方式呈现或者工作。

针对一个制作精良的网页，可将其对应的 HTML 文件分解为多个不同的**块**，在这些块中也可存在**嵌套**关系。基于 HTML 的设计理念，可简单将其理解为一个**高度嵌套的模块**[^4]。

### HTML 文档结构基础

>可参考[HTML 基础 | MDN Web Docs](https://developer.mozilla.org/zh-CN/docs/Learn_web_development/Getting_started/Your_first_website/Creating_the_content)

## HTML 元素属性

### 属性概述

在 HTML 中，元素可以拥有**属性**。属性包含元素的额外信息，这些信息不会出现在实际的网页内容中[^2]。

!!! important

    - 一个空格，它在属性和元素名称之间。如果一个元素具有多个属性，则每个**属性之间必须由空格分隔**

    - 属性名称，后面跟着一个等于号`=`

    - 一个属性值，由一对引号`""`引起来

- *e.g.*

    !!! tip inline end
        Markdown 文档在渲染时兼容 HTML 语法，因此在右侧可以直接将示例中的 HTML 代码块的实际渲染效果展示出来

    ```html
    <p>A link to my <a href="https://virtualguard101.com/" title="virtualguard101's Homepage" target="_blank">homepage</a>.</p>
    ```
    >实际效果：
    >
    ><p>A link to my <a href="https://virtualguard101.com/" title="virtualguard101's Homepage" target="_blank">homepage</a>.</p>

    在上面的例子中：

    - `href`属性声明超链接的 web 地址；
    !!! note
        属性`href`含义是**超文本引用**(**h**ypertext **ref**erence)

    - `title`属性为超链接声明额外的信息，当鼠标悬停在超链接上面时，这部分信息将以工具提示的形式显示；
    
    - `target`属性用于指定链接如何呈现出来，在上面的例子中，`target="_blank"` 表示将在新标签页中显示链接。

### 布尔属性

在 HTML 中，布尔属性是一种特殊的属性类型，它们要么存在（表示true），要么不存在（表示false）。布尔属性只能有一个值，这个值通常与属性名相同或者为空字符串；也可以不需要赋值，仅仅是属性的存在与否就决定了它们的状态。

- *e.g.*

    ```html
    <!-- 使用被赋值的 disabled 属性来防止终端用户输入文本到输入框中 -->
    <input type="text" disabled="disabled" />

    <!-- 使用无赋值的 disabled 属性禁用按钮 -->
    <button  disabled>Unavailable Button</button>

    <!-- 下面这个输入框不包含 disabled 属性，所以用户可以向其中输入 -->
    <input type="text" />
    ```
    >实际效果：
    >
    ><!-- 使用被赋值的 disabled 属性来防止终端用户输入文本到输入框中 -->
    ><input type="text" disabled="disabled" />
    >
    ><!-- 使用无赋值的 disabled 属性禁用按钮 -->
    ><button  disabled>Unavailable Button</button>
    >
    ><!-- 下面这个输入框不包含 disabled 属性，所以用户可以向其中输入 -->
    ><input type="text" />
    
### 属性参考列表

>- [HTML 属性参考 | MDN Web Docs](https://developer.mozilla.org/zh-CN/docs/Web/HTML/Reference/Attributes)

## HTML 特殊字符

在HTML中，有一些字符（如`<`、`&`等）会作为HTML语法的一部分被浏览器解释而无法被当作文本信息显示于网页中，这些字符被称为 HTML 特殊字符。这些字符需要使用特定的编码方式来表示，主要包括HTML实体（HTML Entities）。

HTML 实体引用通常有两种表示方法：

- **命名实体**: `&entityname;`

- **数字实体**: `&#number;`/`&#xhexnumber;`

命名实体引用相对较为方便记忆，因为其与自然语言相关。下表中列出了一些常见特殊字符的命名实体引用[^3]：

| 原义字符 | 等价字符引用 |
|:-------:|:-----------:|
|`<`| `&lt;` |
|`>`| `&gt;` |
|`"`| `&quot;`|
|`'`| `&apos;`|
|`&`| `amp;`|

更多关于实体引用的信息，可参考[List of XML and HTML character entity references | Wikipedia](https://en.wikipedia.org/wiki/List_of_XML_and_HTML_character_entity_references)

## HTML 元信息

>[“头”里有什么——HTML 元信息 | MDN Web Docs](https://developer.mozilla.org/zh-CN/docs/Learn_web_development/Core/Structuring_content/Webpage_metadata)

以一个 HTML 文档为例：
```html
<!doctype html>
<html lang="zh-CN">
  <head>
    <meta charset="utf-8" />
    <title>Test Page</title>
  </head>
  <body>
    <p>Test message</p>
  </body>
</html>
```

在上面的示例中，由`<head></head>`包围的元素就是该 HTML 文档的**头部**，头部中包含的`<meta>`元素就是**元数据**

## 在 HTML 中应用 CSS 和 JavaScript

>[在 HTML 中应用 CSS 和 JavaScript | MDN Web Docs](https://developer.mozilla.org/zh-CN/docs/Learn_web_development/Core/Structuring_content/Webpage_metadata#%E5%9C%A8_html_%E4%B8%AD%E5%BA%94%E7%94%A8_css_%E5%92%8C_javascript)

1. CSS

    在 HTML 中应用 CSS 一般有两种方式：

    - 直接插入 CSS 规则集

        ```html
        <style>
            .example {
                property: value;
                property: value;
            }
        </style>

        <section>
            <div class="example">
                something here.....
            </div>
        </section>
        ```

    - 链接 CSS 文件

        ```html
        <link rel="stylesheet" href="path/to/style.css">
        <section>
            <div class="example">
                something here.....
            </div>
        </section>
        ```
        在这个方式中，`<link>`元素的`rel`属性表明这是样式表；`href`则表明了样式表文件的路径

2. JavaScript

    有多种方法可以在 HTML 上加载 JS，但对于现代浏览器而言，最可靠的方法还是在 HTML 中使用`<script>`元素：
    ```html
    <script src="path/to/script.js" defer></script>
    ```

    上面的示例中，`defer`属性表示向浏览器声明**在解析完成 HTML 后再加载 JavaScript**，可根据实际情况决定是否添加这个属性。


[^1]: [HTML | MDN Web Docs](https://developer.mozilla.org/zh-CN/docs/Glossary/HTML)

[^2]: [HTML 属性 | MDN Web Docs](https://developer.mozilla.org/zh-CN/docs/Learn_web_development/Core/Structuring_content/Basic_HTML_syntax#%E5%B1%9E%E6%80%A7)

[^3]: [实体引用：在 HTML 中包含特殊字符 | MDN Web Docs](https://developer.mozilla.org/zh-CN/docs/Learn_web_development/Core/Structuring_content/Basic_HTML_syntax#%E5%AE%9E%E4%BD%93%E5%BC%95%E7%94%A8%EF%BC%9A%E5%9C%A8_html_%E4%B8%AD%E5%8C%85%E5%90%AB%E7%89%B9%E6%AE%8A%E5%AD%97%E7%AC%A6)

[^4]: [Intro to HTML/CSS | MIT Web Lab](https://docs.google.com/presentation/d/1z7mrIg_M6pn828sbvcJ5XjiK3xpgjC-n1lihA4B-yzM/edit?slide=id.g4c1383710a_0_0#slide=id.g4c1383710a_0_0)
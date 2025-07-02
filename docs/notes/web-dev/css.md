# CSS 要点

## CSS 基本概念 & 基础

CSS(Cascading Style Sheet, 层叠样式表)是一门**样式表语言**，用于选择性地为 HTML 元素添加样式，可简单理解为用来告诉浏览器如何组织网页外观的**规则描述列表**。

### CSS 规则集

在 CSS 中，单个模块的 CSS 规则列表称为该 CSS 的一个**规则集**(*ruleset* or *rule*)。规则集是 CSS 的基本组成单位，其基本结构如下：

```css
selector {
  /* declarations list */
  properties: property value;
  properties: property value;

  /* more declarations... */
}
```

可以看出主要分为四个元素：**选择器(Selector)**、**声明(Declaration)**、**属性(Properties)**、**属性值(Property value)**。

关于各个部分的详细描述可参考[CSS 规则集详解 | MDN Web Docs](https://developer.mozilla.org/zh-CN/docs/Learn_web_development/Getting_started/Your_first_website/Styling_the_content#css_%E8%A7%84%E5%88%99%E9%9B%86%E8%AF%A6%E8%A7%A3)

- 这里简要记录一下**选择器**的分类及其在开发场景下的应用：

    假设这里有一个 HTML 片段：
    ```html
    <h1>Head</h1>
    <div>
      <p>
        Hello!
      </p>
    </div>
    <div class="info">Information</div>
    ```
    现在我们想要使用 CSS 来制定如何修饰其中的元素`Information`，那么可以通过一下 CSS 代码实现：
    ```css
    .info {
      color: red;
      font-family: Arial;
      font-size: 24pt;
    }
    ```
    在这里，选择器`.info`依赖 HTML 的**类(class)**进行元素选择，因此这个选择器就称为**类选择器**。

    同理，如果我们将上面 HTML 中的`class`属性替换为`id`：
    ```html
    <h1>Head</h1>
    <div>
      <p>
        Hello!
      </p>
    </div>
    <div id="info">Information</div>
    ```
    那么对应地，CSS 中的选择器就要替换为**ID选择器**：
    ```css
    #info {
      color: red;
      font-family: Arial;
      font-size: 24pt;
    }
    ```

    !!! info "ID vs Class"
        在 HTML 中，一个元素只能拥有一个 ID，而可以拥有多个类；  
        同时，在一个 HTML 中，每个 ID 都是是独一无二的，而一个相同的类可以同时用于多个元素。这涉及到 CSS 的层级问题，关于这部分内容，可参考[Specificity | HTML Dog](https://www.htmldog.com/guides/css/intermediate/specificity/)

        实际应用中，类的应用要比 ID 频繁得多，因此尽可能在 CSS 中使用类选择器[^1]

    除了**类选择器**和**ID选择器**外，CSS 还支持多个不同类型的选择器，更多信息可参考[不同类型的选择器 | MDN Web Docs](https://developer.mozilla.org/zh-CN/docs/Learn_web_development/Getting_started/Your_first_website/Styling_the_content#%E4%B8%8D%E5%90%8C%E7%B1%BB%E5%9E%8B%E7%9A%84%E9%80%89%E6%8B%A9%E5%99%A8)

### 设计理念

CSS 的设计理念基于 HTML，因此其布局也是基于所谓的**盒子模型**[^2]。


[^1]: [Intro to HTML/CSS | MIT Web Lab](https://docs.google.com/presentation/d/1z7mrIg_M6pn828sbvcJ5XjiK3xpgjC-n1lihA4B-yzM/edit?slide=id.g6cf79318c7_0_26#slide=id.g6cf79318c7_0_26)

[^2]: [CSS：一切皆盒子 | MDN Web Docs](https://developer.mozilla.org/zh-CN/docs/Learn_web_development/Getting_started/Your_first_website/Styling_the_content#css%EF%BC%9A%E4%B8%80%E5%88%87%E7%9A%86%E7%9B%92%E5%AD%90)
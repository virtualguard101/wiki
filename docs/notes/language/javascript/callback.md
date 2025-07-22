# 回调函数简单应用

合理地使用回调函数能够提高**代码的复用性**以及使得代码的**抽象接口**更加优雅，**抽象**的概念可以简单概括成"When `something` happens, do `something`"[^1]

## 数据批量处理

**回调函数与数组结合使用可用于批量处理一组数据：**

```js
const modify = (originData, transformFunc) => {
  const modifiedData = [];
  for (let i = 0; i < originData.length; i++) {
    modifiedData.push(transformFunc(originData[i]))
  }
  return modifiedData;
};

const transform = (origins) => {
  // some transform operate
};

const array = [1, 2, 3, 4, 5];
const modified = modify(array, transform);
```

## 数组方法与回调函数

### `map(...)`

可将回调函数传入`map()`方法中，==以调用该方法的数组对象为源数据、传入的回调函数为数据模板==，创建新的数据集：
```js
const num = [1, 2, 3, 4, 5];

const double = num.map((origin) => {
  return origin * 2;
});
// double = [2, 4, 6, 8, 10]
```

- 计算面积
  ```js
  const rectangles = [
    {width: 2, height: 4},
    {width: 3, height: 6},
    {width: 4, height: 8},
    {width: 5, height: 10},
  ];

  const areas = rectangles.map((rect) => {
    return rect.width * rect.height;
  });
  //areas = [8, 18, 32, 50]
  ```

### `filter(...)`

使用`filter()`方法，可将筛选函数作为回调函数传入其中，==以调用该方法的数组对象为源数据、传入的回调函数为筛选条件==，筛选并创建新的数据集：
```js
const value = [-1, 2, -3, 4, -5];

const positive = value.filter((num) => {
  return num > 0;
});
// positive = [2, 4]
```

- 筛选面积
  ```js
  const rectangles = [
    {width: 2, height: 4},
    {width: 3, height: 6},
    {width: 4, height: 8},
    {width: 5, height: 10},
  ];

  const filteredRectangles = rectangles.filter((rect) => {
    return rect.width * rect.height > 25;
  });
  // filteredRectangles = [{width: 4, height: 8}, {width: 5, height: 10}]
  ```

## 在Web开发中的应用

回调函数在Web开发中无处不在，是实现 ==[异步](https://developer.mozilla.org/zh-CN/docs/Glossary/Asynchronous)编程== 和 ==事件驱动编程== 的核心机制。

下面列举几个简单的的例子：

!!! note
    下面的三个事件处理中，事件监听方法中第二个参数（回调函数）的`event`是这个回调函数的参数，因为只有这一个参数，故采用不加括号的写法以保持代码简洁；若回调函数中需要传入多个参数或没有参数传入，则必须携带括号

- DOM事件处理：
  ```js
  // 点击事件
  document.getElementById('submitBtn').addEventListener('click', event => {
      console.log('表单提交按钮被点击');
      event.preventDefault(); // 阻止默认行为
  });

  // 表单提交事件
  document.getElementById('myForm').addEventListener('submit', event => {
      event.preventDefault();
      validateForm(function(isValid) {
          if (isValid) {
              console.log('表单验证通过');
              submitForm();
          } else {
              console.log('表单验证失败');
          }
      });
  });

  // 鼠标事件
  document.addEventListener('mouseover', event => {
      if (event.target.classList.contains('tooltip-trigger')) {
          showTooltip(event.target);
      }
  });
  ```

- HTTP通信

    以下是一个典型的RESTful API接口，用于评论系统的数据获取功能：
    ```js
    // HTTP GET接口
    router.get("/comment", (request, response) => {
      // 1. 定义GET路由，路径为 /comment
      Comment.find({ parent: request.query.parent }).then((comments) => {
        // 2. 使用Comment模型查询数据库
        // 3. 查询条件：parent字段等于请求参数中的parent值
        // 4. 使用Promise处理异步查询结果
        response.send(comments)
        // 5. 将查询结果发送给客户端
      });
    });
    ```

- 动画与视觉效果

    滚动懒加载和渐变动画效果：
    ```js
    // 事件监听器
    document.addEventListener("DOMContentLoaded", () => {
      //获取目标元素
      const elems = document.querySelectorAll(".scroll-fade");
      // 创建交叉观察器
      const io = new IntersectionObserver((entries, observer) => {
        // 观察器回调函数
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            // 图片懒加载逻辑
            const el = entry.target;
            const img = el.querySelector("img[data-src]");
            if (img && img.dataset.src) {
              img.src = img.dataset.src;
              delete img.dataset.src;
            }
            // 触发动画效果
            el.classList.add("in-view");
            observer.unobserve(el);
          }
        });
        // 观察器配置
      }, { threshold: 0.2 });
      // 开始观察
      elems.forEach(el => io.observe(el));
    });
    ```


[^1]: [JS Cont: Callback Functions, Map, Filter | MIT Web Docs](https://docs.google.com/presentation/d/1fr1uVNiVwQjfb0ORcSpYVzpin7HgGGtM4O2JaPHuITs/edit?slide=id.g2ab7bc3906d_0_73#slide=id.g2ab7bc3906d_0_73)
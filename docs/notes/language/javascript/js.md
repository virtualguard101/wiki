---
date: 2025-07-20 09:52:00
title: JavaScript入门要点
permalink: 
publish: true
---

# JavaScript 入门要点

>[什么是JavaScript? | MDN Web Docs](https://developer.mozilla.org/zh-CN/docs/Learn_web_development/Core/Scripting/What_is_JavaScript)
>
>[Intro to JS | MIT WebLab](https://docs.google.com/presentation/d/14eJA-Zn6UOA0NaMHCbNCGFC_xzBNRLqJN6QsT5kuaK4/edit?slide=id.p#slide=id.p)
>
>[JSchallenger](https://www.jschallenger.com/dashboard/)

## 数据类型与运算符

JavaScript 有`Boolean`、`Number`、`String`、`Null`、`Undefined`5种原始数据类型；运算符除`===`（严格相等）外基本与 Python 等编程语言相通，可参考[Intro to JS | MIT Web Lab](https://docs.google.com/presentation/d/14eJA-Zn6UOA0NaMHCbNCGFC_xzBNRLqJN6QsT5kuaK4/edit?slide=id.g2acc0371921_0_8#slide=id.g2acc0371921_0_8)

在计算机语言中，严格相等通常意义上指：

!!! tip inline end
    因此在开发实践中，推荐优先使用`===`进行数据比较

- 值相等

- 数据类型相同

在 JavaScript 中，进行比较操作前[JS引擎](https://developer.mozilla.org/zh-CN/docs/Glossary/Engine/JavaScript)会首先判断二者的数据类型是否相同。若使用`==`比较两个数据是否相等，且二者的数据类型不相同时，**JS会先隐式地将二者转换为相同的数据类型再行数值比较**；而使用`===`时，JS引擎则**不会进行类型转换**。

### `null` vs `undefined`

| | `null` | `undefined` |
|:-|:-|:-|
|含义|人为赋值的“空值”|未赋值的默认值|
|类型|`object`（历史遗留的 bug）|`undefined`|
|`==` 比较|`null == undefined` → `true`|同上|
|`===` 比较|`null === undefined` → `false`|同上|
|典型出现场景|手动置空：`let x = null`|1. 变量声明未赋值2. 函数无 `return`3. 对象不存在的属性4. 形参未传|
|使用建议|明确“无值”时手动使用|让 JS 自动表示“缺失”|

```js
let name;
let name = {};
// currently, 'name' is 'undefined'

name = virtualguard101
// and has now been assigned to a value

name = null;
// this explicitly 'empty' the variable
```

简单来说，`undefined`指 ==声明但还未赋值的变量==，通常是系统给对象自动分配的空位；

`null`指的就是 ==没有数值的变量==，通常是人为分配的空壳。

## 基本语法 & 数据结构

JavaScript 代码基本与其他主流编程语言（如 [C++](../cpp/cs106l/00-type-structure.md)、[Java](../java/intro.md)等）相通，代码块以大括号`{}`进行分隔

### 变量声明

在声明变量时，JavaScript提供了三个关键字可供使用：`var`、`let`、`const`。下面是三者的对比：

| | var | let | const |
|:-|:-|:-|:-|
|作用域|函数级|块级|块级|
|[变量提升](https://developer.mozilla.org/zh-CN/docs/Glossary/Hoisting)|✅ 提升并初始化为 `undefined`|❌ 不提升，存在[暂时性死区，TDZ](https://stackoverflow.com/questions/33198849/what-is-the-temporal-dead-zone)|❌ 同 let|
|重复声明|✅ 允许|❌ 禁止|❌ 禁止|
|重新赋值|✅ 允许|✅ 允许|❌ 声明后不可重新赋值|
|声明时必须初始化|❌ 不必|❌ 不必|✅ 必须立即初始化|
|全局绑定|✅ 会成为 [`window` 属性](https://developer.mozilla.org/zh-CN/docs/Web/API/Window/window)|❌ 不会|❌ 不会|
|循环中的闭包|常见陷阱（共享同一变量）|每次迭代独立作用域|同 let，但值不可改变|

简单来说，`var`是早期的变量声明关键字，作用域较大、在使用时易出错；`let`声明的变量是具有块级安全的“`var`变量”；`const`是用于保证所声明变量不可变的关键字，具有最高的安全性，==但是对象属性仍然可变==。

在开发实践中，通常优先使用`const`以确保程序数据的安全性与可靠性。

### `console.log()` & `alert()`

在 web 开发中，我们通常使用`console.log()`将信息输出到浏览器控制台上[^1]。

`alert()`则用于在浏览器界面中弹出一个带有指定信息的通知窗口[^2]。

### 数组

在 JavaScript 中，单个数组支持多数据类型共存，即**混合类型数组**。访问数组元素的方式与大多数支持数组数据结构的编程语言相同，采用下标引索访问：
```js
// initialize
let arr = ["virtual", "guard", 101, true];

// access
console.log(arr[2]); // output 101

// replace
arr[3] = false;
```

同时，在JS中，数组的大小类似C++中的`vector`，是可变的。可通过一些原生的方法实现：
```js
// remove and return the element from end
arr.pop()

// add to end
arr.push("virtualguard101@gmail.com")
```
更多有关数组的方法可参考[JavaScript 内置对象：Array | MDN Web Docs](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects/Array)

### for循环

在 JavaScript 中，for循环有两种形式可用：

- 一种是与大多数编程语言通用的 ==条件for循环==：

    ```js
    const information = [101, "virtualguard", "virtualguard101@gmail.com", true]

    for (let i = 0; i < information.length; i++) {
        const info = information[i];
        console.log(info);
    }
    ```

- 还有一种被称为 ==`for...of...`==，在形式上类似于C++与Java中的[Foreach 语句](https://www.geeksforgeeks.org/cpp/g-fact-40-foreach-in-c-and-java/)

    ```js
    const information = [101, "virtualguard", "virtualguard101@gmail.com", true]

    for (const info of information) {
        const info = information[i];
        console.log(info);
    }
    ```

## 对象(`Object`)

>[Object | MDN Web Docs](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects/Object)

入门阶段，可将一个JS对象简单理解为一个`name: value`的 ==键值对集合==[^3]。形式上类似Python的字典(dict)：

### 访问属性

JavaScript 提供了两种方式访问一个对象的属性：
```js
const person = {
    name: "virtualguard",
    id: 101
    email: "virtualguard101@gmail.com"
};

const name = person.name;
const id = person.id;
```

### 对象解构

对象解构是一种简化操作，形式上有些类似于C++中的[结构化绑定](../cpp/cs106l/01-init-reference.md#结构化绑定)，相比较上面的访问方式，可一次性获取对象的多个属性：
```js
const person = {
    name: "virtualguard",
    id: 101
    email: "virtualguard101@gmail.com"
};

const { name, id } = person;
```

### 对象引用

在 JavaScript 中，一个对象本质上是一个指向某个内存空间的引用(或指针)，这些内存空间中储存的就是对应对象的数据。因此，尽管两个对象可能具有完全相同的属性值，使用`===`(严格相等)对它们进行比较时也会返回`false`：

```js
let person1 = {
    name: "virtualguard",
    id: 101
};

let person2 = {
    name: "virtualguard",
    id: 101
};

person1 === person2;    // false
```

!!! tip inline end
    以上说法对数组也适用

因为在JS引擎看来，`person2`相较于`person1`是一个新的对象，它们的数据储存在内存中的不同位置。

### 对象拷贝

针对对象、数组等**可迭代对象**的拷贝，仅仅使用`=`赋值是不行的：
```js
let arr = [1, 2, 3];
// don't code like this
let copy = arr;
```
在 JavaScript 中，对于对象和数组等可迭代对象，直接使用赋值操作符（`=`）进行拷贝并不会创建一个新的对象或数组，而是创建了一个引用。这意味着对“拷贝”所做的任何修改都会影响到原始对象或数组，因为它们实际上指向的是同一个内存地址。

正确且便捷的方式（也可手动创建一个新对象并将旧对象的属性逐一复制过去）是使用 ==`...`(Spread Operator, 扩展运算符)==：
```js
let arr = [1, 2, 3];
// shallow copy of arr
let copy = [...arr];

let obj = {
    name: "virtualguard",
    code: 101,
    email: "virtualguard101@gmail.com"
};
// shallow copy of obj
let cppy = { ...obj };
```

!!! warning
    上面所讨论的皆为对象的**浅拷贝**，这意味着如果对象或数组中包含嵌套的对象或数组，那么嵌套的部分仍然是引用，而不是独立的副本。如果需要创建深拷贝，可以使用其他方法，如 `JSON.parse(JSON.stringify(obj))` 或递归拷贝等

## 函数

[常规函数](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Guide/Functions)的语法与大多数主流**动态类型编程语言**并没有什么区别。JavaScript 采用`function`关键字声明或定义函数。

### 箭头函数

在 JavaScript 中，有一种特殊的函数表达方式，其结构大致如下：

!!! note inline end
    箭头函数除了左侧包含`return`语句的原始写法，还有一种不含`return`语句的简单写法：
    ```js
    const functionName = (parameters) => (parameters);
    ```

```js
(parameters) => {
    // function body
}

// or with full structure
const functionName = (parameters) => {
    // function body
    return parameters;
};
```
它被形象地称为[**箭头函数**](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Functions/Arrow_functions)，是 ES6（ECMAScript 2015）引入的一种新的函数语法，它提供了一种更简洁的方式来写函数表达式。

关于箭头函数与常规函数的区别，可以参考[这篇文章](https://www.geeksforgeeks.org/javascript/difference-between-regular-functions-and-arrow-functions/)

### 回调函数

JavaScript 支持[回调函数](https://developer.mozilla.org/zh-CN/docs/Glossary/Callback_function)，即作为参数传入其他函数的函数。下面是一个简单的例子：
```js
const timeoutInfo = () => {
    console.log("Procees time out");
};
setTimeout(timeoutInfo, 5000);

// or pass the function body directly
setTimeout(
    () => {
        console.log("Procees time out");
    },
    5000
);
```

在上面的例子中，`setTimeout`函数是JavaScript中的一个定时器函数，用于在指定的毫秒数后执行一个函数。它接受两个参数：第一个参数是要执行的函数（即回调函数），第二个参数是延迟的时间（以毫秒为单位）。

!!! warning
    若采用第一种向函数传入回调函数名的方式，则必须填入的是函数名本身（在上面的例子中就是`timeoutInfo`），而不是`timeoutInfo()`，否则传入的就是回调函数的返回值（这里是`undefined`），而不是它本身

## 类

>[类 | MDN Web Docs](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Classes)

JavaScript 也支持面向对象编程。定义类的语法形式类似C++：
```js
class Rectangle {
    constructor(width, height) {
        this.width = width;
        this.height = height;
    }

    getArea() {
        return this.width * this.height;
    };
}

class Square extends Rectangle {
    constructor(side) {
        super(side, side);
    };
}

const rect = new Rectangle(4, 6);
const squa = new Square(5);
console.log(rect.getArea());    // 24
console.log(squa.getArea());    // 25
```


[^1]: [Intro to JS | MIT Web Lab](https://docs.google.com/presentation/d/14eJA-Zn6UOA0NaMHCbNCGFC_xzBNRLqJN6QsT5kuaK4/edit?slide=id.ga9ff0d6df4_0_34#slide=id.ga9ff0d6df4_0_34)

[^2]: [Intro to JS | MIT Web Lab](https://docs.google.com/presentation/d/14eJA-Zn6UOA0NaMHCbNCGFC_xzBNRLqJN6QsT5kuaK4/edit?slide=id.ga9ff0d6df4_0_502#slide=id.ga9ff0d6df4_0_502)

[^3]: [Intro to JS | MIT Web Lab](https://docs.google.com/presentation/d/14eJA-Zn6UOA0NaMHCbNCGFC_xzBNRLqJN6QsT5kuaK4/edit?slide=id.gb1ce1181a2_0_81#slide=id.gb1ce1181a2_0_81)
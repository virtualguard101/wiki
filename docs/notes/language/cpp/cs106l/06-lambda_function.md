# `lambda`表达式

## 定义

在Python中，`lambda`表达式**函数式编程**中起到了极大的简化作用。自C++11起，C++也引入了`lambda`表达式，增强了C++的函数式编程能力。

`lambda`表达式是一种匿名函数**对象**，可在需要在需要函数功能的地方直接定义和使用，而无需单独定义一个函数。

`lambda`表达式是**内联的**、**匿名的**函数，能够知晓于其处于相同作用域的变量。

```cpp
auto var = [capture-clause] (auto param) -> return_type { /* function_body */ }
/*                ^              ^              */
/*       outside parameters  func parameters    */
```

**e.g.**：
```cpp
int limit = 5;
auto lessThanFive = [limit] (int n) {
    return n < limit;
};

lessThanFive(6);  // False
```

## 捕获列表（`[capture-clause]`）

```cpp
[]              // captures nothing
[limit]         // captures limit by value
[&limit]        // captures limit by reference
[&limit, upper] // captures limit by reference, upper by value
[&, limit]      // captures everything except limit by reference
[&]             // captures everything by reference
[=]             // captures everything by value
```

## 应用 & 杂项

`lambda`表达式的计算成本很低，可提高程序的运行效率。

>   - 需要一个简短的函数或需要在函数中访问局部变量时，可使用`lambda`表达式
>
>   - 若需要使用更复杂的逻辑或重载功能，可使用**函数指针**

!!! note "函数指针"
    - 和其他指针共享操作接口，即可像其他指针一样进行处理

    - 可作为变量/参数在函数或模板函数中传递

    - 可像函数一样被调用

### `lambda`表达式作为谓词传递

```cpp
template<typename InputIt, typename UniPred>
int count_occurrences(InputIt begin, InputIt end, UniPred pred) {
    int count = 0;
    for (auto iter = begin; iter != end; ++iter) {
        if (pred(*iter)) { count++; }
    }
    return count;
}

int main() {
    int limit = 5;
    auto moreThanFive = [limit] (int n) {
        return n > limit;
    }

    std::vector<int> nums = {3, 5, 7, 9, 11, 13};

    count_occurrences(nums.begin(), nums.end(), moreThanFive)  // returns 4
}
```

在上面的示例中，`InputIt`是输入的迭代器类型；`UniPred`是一个一元谓词类型（**函数指针**/**函数对象**/**Lambda表达式**），用于判断元素是否满足条件。

模板函数`count_occurrences`的功能是遍历从`begin`到`end`的所有元素；对每个元素，调用`pred`谓词判断是否满足条件，如果满足条件，计数器 count 增加；最后返回计数器的值。

!!! note "谓词函数(Predicate Functions)"
    - 任何返回`bool`值的函数都属于谓词函数

    - 谓词函数可以是**一元**或**多元**的，即单参数的或多参数的

### 函数对象/函子(Function Object/Functor)

在**函数式编程**中，这是一个十分重要的模块。

在C++中，函数对象和函子是同一个概念，指通过**重载了`operator()`运算符**的类实现的技术。这项技术使得该类能够创建用户自定义功能的**闭包**，其实例能够像函数一样使用，从而提供更加灵活的函数式编程方式。

!!! note "闭包(Closure)"
    函数对象的单一实例化形式，能够捕获并保持对其所在作用域中变量的引用，即使该作用域已经执行完毕。可简单理解为**一个会记住其周围环境（词法作用域）并访问其中变量的函数，即使这个函数在这个环境外调用**。

    在C++中，**闭包**通常就通过`lambda`表达式实现。


```cpp
class factor {
public:
    int operator() (int arg) const {
        return num + arg;    // parameters and function body
    }
private:
    int num;    // capture clause
};

int num = 0;
auto lambda = [&num] (int arg) {
    num += ara;
};
lambda(5);
```

- `factor`是一个函数对象，对于捕获变量`num`，由于其是`factor`的私有变量，是不可变的，故这个函数对象仅仅提供了一个**只读**的加法操作

- `lambda`表达式则通过**引用捕获**提供了一个可以修改捕获变量的操作，即对捕获变量`num`的累加。这就是一个典型的**闭包**

### `std::function<return_type(param_types)> func;`

到目前为止，我们已经讨论了`lambda`表达式、函数指针以及函数对象。

在C++中，STL提供了一个通用的函数类型`std::function<return_type(param_types)>`，称为**标准函数**。以上讨论的三个东西都可以转换为标准函数。

标准函数占用的资源会比函数指针与`lambda`表达式多，运行开销也更大。

### 虚拟函数（`virtual`）

- [Virtual Function in C++ | GeeksForGeeks](https://www.geeksforgeeks.org/virtual-function-cpp/)

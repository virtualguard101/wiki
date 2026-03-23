---
date: 2025-05-08 00:26:00
title: C++流
permalink: 
publish: true
tags:
  - 编程语言
  - C++
  - CS106L
---

# C++流

在C++中，流(`stream`)是一个十分重要的概念，它是**I/O（Input/Output, 输入输出）的一般抽象**，表示数据的流动方向和方式。

!!! note

    抽象（Abstractions）通常为各种操作提供一个统一的**接口（Interface）**。在这里，`stream`就是**数据读写**的接口。

## 标准输入输出流

最常用的标准输入输出流就是`cin`和`cout`了，他们工作时分别从控制台读取数据和向控制台输出数据。

在标准输入输出流中，还有两个输出流：

- `cerr`：**标准错误输出流**，用于输出错误信息。与`cout`的不同在于不会被缓冲，会立即输出

- `clog`：**标准日志输出流**，用于输出非关键日志信息。与`cerr`类似，但会进行缓冲

更多信息可参考[Difference between cerr and clog | GeeksForGeeks](https://www.geeksforgeeks.org/difference-between-cerr-and-clog/)

### `std::cin`/`std::cout`

```cpp
#include <iostream>

int main() {
    double pi;
    std::cin >> pi;
    // verify the value of pi
    std::cout << pi << '\n';

    return 0;
}
```
编译并执行上述cpp程序，我们在终端输入`3.14`，终端最终返回`1.57`。

这里就会有一个疑问：从终端读取的数据显然是数据的**字符表示形式**，而程序中的`pi`是`double`型的，中间是否有什么处理或转换的过程呢？

答案是肯定的。作为I/O的一般抽象，`stream`允许以一种通用的方式处理来自外部的数据。

本质上，所有的`stream`都可以归为`Input stream(I)`和`Output stream(O)`中的一种。对于相同类型的输入输出流，它们在数据源/目标是互补的。在后面的章节中，我们还会详细介绍这两个流。

## 字符串流

字符串流将字符串视为流，用于在内存中处理数据，在处理多中数据类型混合的应用场景是一个高效的处理接口。

`std::stringstream`示例：

```cpp
#include <string>
#include <iostream>
#include <sstream>

void foo() {
    /// partial Bjarne Quote
    std::string initial_quote = "Bjarne Stroustrup C makes it easy to shoot yourself in the foot"; 
    
    /// create a stringstream
    std::stringstream ss(initial_quote);
    // another way to insert 'initial_quote'
    // std::stringstream ss;
    // ss << initial_quote;
    
    /// data destinations
    std::string first;
    std::string last;
    std::string language, extracted_quote;
        
    ss >> first >> last >> language >> extracted_quote;
    std::cout << first << " " << last << " said this: "<< language << " " << extracted_quote << std::endl;
}

int main() {
    foo();
    return 0;
}
```
在上面的示例中，我们为字符串变量`initial_quote`创建了一个字符串流`ss`，并通过`>>`（输出流操作符）将流数据++从原始数据移动到`first`、`last`等目的地++。这就是流的作用，即**将数据从内存中的一个地方移动到另一个地方**。将数据比作货物，流就是装载货物的货车，而创建数据流的过程就是将货物装车的操作。

但上面的程序存在一个小小的bug：

这是上述程序编译并执行的结果：
```bash
Bjarne Stroustrup said this: C makes
```
这显然不是我们预期的结果，那么为什么呢？

通过数据流，我们将变量字符串变量`initial_quote`的第一第二以及第三个单词分别从字符串流`ss`移动到了字符串变量`first`、`last`和`language`上。接下来，我们的预期是将`initial_quote`的剩余部分全部赋给`extracted_quote`，但是`>>`（输出流操作符）在读取数据时遇到空格就会停止，因此数据流只转移了一个单词。

解决方法是使用`std::getline()`：

```cpp
#include <iostream>
#include <string>
#include <sstream>

void foo() {
    /// partial Bjarne Quote
    std::string initial_quote = "Bjarne Stroustrup C makes it easy to shoot yourself in the foot";
    
    /// create a stringstream
    std::stringstream ss(initial_quote);
    
    /// data destinations
    std::string first;
    std::string last;
    std::string language, extracted_quote;
    ss >> first >> last >> language;
    std::getline(ss, extracted_quote);
    std::cout << first << " " << last << " said this: \'" << language << " " << extracted_quote + "‘" << std::endl;
    }

    
int main() {
    foo();
    return 0;
}
```

下面是`std::getline()`的定义：

```cpp
istream& getline(istream& is, std::string& str, char delim)
```
`std::getline()`读取输入流`is`，**直到遇到字符型分隔符`delim`**，并将数据存入字符串型缓存`str`中。其中`delim`的默认值为`\n`。

## 输出流

### `std::cout`

`Output Stream`用于将数据写入目标地址或外部设备，例如`std::cout`将数据写入控制台。实际操作时，我们使用操作符`<<`将数据写入输出流。

输出流的数据在加载至目标区域前会事先存储在中间缓存中：

```md
                        Buffer
double n = 5.50         -------------------------             ---------
std::cout << n;  ====>  | 5 | . | 5 | 0 |   |   |    ======>  |>_     |
                        -------------------------             |       |
                                                              ---------
```

`std::cout`输出流是**行缓冲流**。缓冲区中的数据不会显示在控制台上，直到缓冲区执行刷新（flush）操作。

### `std::endl`

`std::endl`用于提示`cout`当前数据流到达行末，需要进行换行操作。

```cpp
int main() {
    for (int i=0; i < 5; i++) {
        std::cout << i << std::endl;
    }

    return 0;
}
```
result:
```bash
0
1
2
3
4
```

如果去掉上面的`std::endl`，结果就会变成这样：
```bash
01234
```

换行的同时，`std::endl`还会提示流进行刷新（flash）操作，下面是该过程的可视化：

```md
Buffer
------------------  flash   ------------------  flash
| 1 |'\n'|   |   |   ===>   | 2 |'\n'|   |   |   ===> ......
------------------          ------------------
```

每个数在被放入流后都会立即刷新，直接输出到控制台上。使用`\n`的情况相同，详情可参考[std::endl | cppreference](https://zh.cppreference.com/w/cpp/io/manip/endl)

### 文件输出流

文件输出流用于将数据流写入文件，其具有数据类型`std::ofstream`。在实际操作中，我们使用操作符`<<`将数据流传输至文件。

下面是具体用法：

```cpp
#include <fstream>

int main() {
  /// associating file on construction
  std::ofstream ofs("hello.txt");
  if (ofs.is_open()) {
    ofs << "Hello CS106L !" << '\n';
  }
  ofs.close();
  ofs << "this will not get written";

  /* try adding a 'mode' argument to the open method, like std::ios:app
   * What happens?
   */
  ofs.open("hello.txt");
  ofs << "this will though! It’s open again";
  return 0;
}
```

要使用文件输出流，我们首先要创建一个具有类型`std::ofstream`的流。上面的示例中：  

- `ofs(hello.txt)`创建了一个指向`hello.txt`的文件输出流`ofs`

- 使用`is_open()`检查文件输出流是否打开

- 使用`<<`尝试写入数据

- 写入第一行数据后，使用`close()`关闭文件输出流

- 文件关闭后，无法向文件中写入数据

- 使用`open()`再次打开文件输出流`ofs`

- 打开文件输出流后，可继续向文件写入数据

在关闭文件输出流并进行再次打开的操作时，如不希望已写入文件的数据被覆盖，可在`open()`方法的参数中添加追加模式的标签：
```cpp
ofs.open("hello.txt", std::ios::app)
```

### 文件输入流

文件输入流用于从文件读取数据，本质与文件输出流相同。

假设有文件`input.txt`，其内容如下：

```txt
line1
line2
```
在相同路径下编译并执行以下程序：

```cpp
#include <fstream>
#include <iostream>

int main() {
  std::ifstream ifs("input.txt");
  if (ifs.is_open()) {
    std::string line;
    std::getline(ifs, line);
    std::cout << "Read from the file: " << line << '\n';
  }
  if (ifs.is_open()) {
    std::string lineTwo;
    std::getline(ifs, lineTwo);
    std::cout << "Read from the file: " << lineTwo << '\n';
  }
  return 0;
}
```
则会得到如下结果：
```bash
Read from the file: line1
Read from the file: line2
```

## 输入流

在文件流中我们简要了解了文件输入流的用法，下面我们将详细学习输入流的概念与应用。

输入流用于从目标或外部数据源读取数据，其具有数据类型`std::istream`。实际操作中，我们使用`>>`从输出流中读取数据。

### `std::cin`

与`std::cout`相同，`std::cin`也是行缓冲流。可将`std::cin`的行缓冲区理解为用户暂存数据，随后从中读取数据的区域。

需要注意的是，`std::cin`的缓冲区遇到空格时会停止接受数据。

```cpp
int main() {
    double pi;
    std::cin;
    std::cin >> pi;

    std::cout << pi << '\n';

    return 0;
}
```

在上面的示例中：

- 最开始时缓冲区为空，所以首个`std::cin`会提示用户进行输入

- 到第二个`std::cin`时，缓冲区中不为空，所以`cin`会从其中读取数据，直到遇到空格，并将数据存入变量`pi`

在日常开发中，我们通常直接将输入操作与数据流转移写在同一个语句：

```cpp
int main() {
    double pi;
    std::cin >> pi;

    std::cout << pi << '\n';

    return 0;
}
```

与在了解字符串流时遇到的一个问题类似，`std::cin`在从目标读取数据时，遇到空格就会停止读取数据：

```cpp
#include <iostream>

void cinGetlineBug() {
  double pi;
  double tao;
  std::string name;
  std::cin >> pi;
  std::cin >> name;
  std::cin >> tao;
  std::cout << "my name is : " << name << " tao is : " << tao
            << " pi is : " << pi << '\n';
}

int main() {
    cinGetlineBug();
    return 0;
}
```
```bash
3.14
Benjamin C
my name is : Benjamin tao is : 0 pi is : 3.14
```
程序甚至还未等到我们输入第三个数据就停止从控制台读取数据了。这是由于在读取第二个数据时，`cin`缓冲区不为空，因此它在读取数据时遇到空格后就立刻停止继续读取数据：

```md
Buffer
-----------------------------------
|3|.|1|4|\n|B|e|n|j|a|m|i|n| |C|\n|
-----------------------------------
                            ^
                     stop read data here
```

那么有了之前字符串流的修复经验，你可能会给出以下修复版本：

```cpp
#include <iostream>

void cinGetlineBug() {
  double pi;
  double tao;
  std::string name;
  std::cin >> pi;
  std::getline(std::cin, name);
  std::cin >> tao;
  std::cout << "my name is : " << name << " tao is : " << tao
            << " pi is : " << pi << '\n';
}

int main() {
    cinGetlineBug();
    return 0;
}
```
然而，实际的执行效果却是这样的：
```bash
3.14
Benjamin C
my name is :  tao is : 0 pi is : 3.14
```
这次甚至连第二个数据也丢失了🤯.....

事实上，第二个数据并不是“丢失了”，而是`getline()`的特性导致的：

在介绍字符串流时，我们曾介绍过`std::getline()`的定义，其中提到了，**`getline()`默认将`\n`作为字符分隔符，并在遇到它时“消耗它”并停止继续读取数据**，那么针对上面失败的修改我们可以想象出如下可视化过程：

```md
Buffer   std::cin >> pi;
-----------------------------------
|3|.|1|4|\n|B|e|n|j|a|m|i|n| |C|\n|
-----------------------------------
        ^               pi: 3.14
                || 
                \/

   std::getline(std::cin, name);
-----------------------------------
|3|.|1|4|\n|B|e|n|j|a|m|i|n| |C|\n|
-----------------------------------
           ^            pi: 3.14
                        name: ""
         std::cin >> tao;
-----------------------------------
|3|.|1|4|\n|B|e|n|j|a|m|i|n| |C|\n|
-----------------------------------
            ^^^^^^^^^^^^^^^^^^^^
The buffer is not empty, and cin try to read the part, but 'tao' is double type!
                        pi: 3.14
                        name: ""
                        tao: 🗑
```

那么应该如何修复这个问题呢？

既然`getline()`在遇到`\n`时会“消耗它”并停止读取数据，那么我们不妨在第一个`getline()`消耗`\n`后在添加一个`getline()`来读取`name`的内容：

```cpp
#include <iostream>

void cinGetline() {
  double pi;
  double tao;
  std::string name;
  std::cin >> pi;
  std::getline(std::cin, name);
  std::getline(std::cin, name);
  std::cin >> tao;
  std::cout << "my name is : " << name << " tao is : " << tao
            << " pi is : " << pi << '\n';
}

int main() {
    cinGetline();
    return 0;
}
```
这时再执行程序，bug也就被修复了：
```bash
3.14
Benjamin C
5
my name is : Benjamin C tao is : 5 pi is : 3.14
```

其可视化过程如下：

```md
Buffer   std::cin >> pi;
----------------------------------------
|3|.|1|4|\n|B|e|n|j|a|m|i|n| |C|\n| |  |
----------------------------------------
        ^               pi: 3.14
                || 
                \/

   std::getline(std::cin, name);
----------------------------------------
|3|.|1|4|\n|B|e|n|j|a|m|i|n| |C|\n| |  |
----------------------------------------
           ^            pi: 3.14
                        name: ""
                || 
                \/

   std::getline(std::cin, name);
----------------------------------------
|3|.|1|4|\n|B|e|n|j|a|m|i|n| |C|\n| |  |
----------------------------------------
                                  ^
                        pi: 3.14
                        name: "Benjamin C"
                || 
                \/

         std::cin >> tao;
----------------------------------------
|3|.|1|4|\n|B|e|n|j|a|m|i|n| |C|\n| |  |
----------------------------------------
                                   ^
The stream now is empty, so is going to promot user for input!
                        pi: 3.14
                        name: "Benjamin C"
                        tao: 
                || 
                \/

         std::cin >> tao;
----------------------------------------
|3|.|1|4|\n|B|e|n|j|a|m|i|n| |C|\n|5|\n|
----------------------------------------
                                       ^
                        pi: 3.14
                        name: "Benjamin C"
                        tao: 5(double)
```

事实上，在实际应用的过程中，由于`cin`和`getline()`解析数据的方式有所差异，我们并不会在一个场景内同时使用二者。但确有需求的话，像上面的操作也是可行的，但还是不建议这样做。

## Assignment1: SimpleEnroll

这次作业要求学生补全实现三个函数，用于实现`CSV`文件的数据处理，考验学生对**文件输入输出流**的掌握程度。作业难度不算大，同时还涉及了一小部分容器部分的知识点（虽然但是容器部分比较常用的也就`std::vector`）

作业个人实现：[CS106L-Assignments](https://github.com/virtualguard101/cs106l-assignments/blob/main/assignment1/main.cpp)


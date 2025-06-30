---
title: Academic
icon: material/pencil-ruler
date: 2025-04-13 09:05:18
---

!!! Note 
    计算机理论类资源汇总归档，收录计算机基础课程资料、基础理论、进阶理论资料以及计算机领域的学术资料，**用于记录个人的CS基础学习路线**

    1.**课程模块**主要由`教材（电子书/网页文档）`、`幻灯片`、`课程主页（网址）`、`csdiy课程信息页`、`课程录播视频`五个要素组成，由于不同课程的差异以及资源碎片化的特性，上述五个要素一般不会同时出现，当然，也有可能你可以在一个汇总性的要素中找到其他的要素。各个要素会按照我个人认为的权重进行排序。例如，在CS61A中，精读课程的部分内容**对我来说**是合理的，那么我便将`课程主页`、`csdiy课程信息页`这类汇总性较强的要素排在前面；而对于CS106L而言，仅仅需要阅读课程教材及幻灯片就能很大程度上掌握课程的主要内容，以及当下我只希望快速通读一下这个课程的主要内容，那么我就将`教材`与`幻灯片`置前。  

    2.**进阶理论**：大部分进阶理论不是处于**技术闭源**的状态就是只能通过原始学术论文了解，该模块的内容除去部分科普性的资料，大部分是晦涩难懂的。但可以肯定的是，所有的进阶理论都有它们对应的基础依赖。

## 课程/基础理论

### 学习社区/学习资源集群

#### csdiy（CS自学指南）
>北大学长基于自己的自学历程打造的教科书级别的自学指南，在github上有超60k的star。项目中云集了全球各个顶尖大学的计算机开源课程，及其附属资料。不过由于课程更迭，有些课程的附属资料会出现缺失的情况，但评论区里总会有大佬为课程内容做资源备份，所以在搜集课程资料时，搭配评论区食用更佳。

- 中文版网址：[CS自学指南](https://csdiy.wiki/)

- 英文版网址：[csdiy](https://csdiy.wiki/en)

- github仓库：[cs-self-learning | PKUFlyingPig](https://github.com/PKUFlyingPig/cs-self-learning)

#### w3school
>国外一个专为程序员打造的技术栈学习平台，内容分为`HTML & CSS`、`Data Analytics`、`JavaScript`、`Web Building`、`Backend`五大模块，主要讲解各个技术栈使用的编程语言的**基础语法**或**技术框架基础**。各教程采用**文档型**的方法将各技术栈的特性逐个列出，并加以简化描述。形式上类似于国内的[菜鸟教程](https://www.runoob.com/)，但前者在内容上更加精简，适合用于在毫无基础的情况下速通技术栈的常用基础特性。

- 网址：[w3school](https://www.w3schools.com/)

#### tutorials point
>形式上与[菜鸟教程](https://www.runoob.com/)、[w3school](https://www.w3schools.com/)没有区别，但涵盖的技术种类比前两者都要丰富，甚至还有数学模块。与w3school一样为境外资源。

- 网址：[Tutorial on Technical and Non Technical Subjects](https://www.tutorialspoint.com/index.htm)

#### GeekForGeeks
>基本同上

- 网址：[GeekforGeeks](https://www.geeksforgeeks.org/)


### 编程入门

#### MIT-missing-semester: The Missing Semester of Your CS Education
>**课程简述**：课程主要传授在大学课堂上几乎不会涉及但对于cs学习无比重要的工具或零散知识点。例如shell、Git（版本控制）等

- 课程网址/教程：[The Missing Semester of Your CS Education](https://missing.csail.mit.edu/)

- 课程中文网址/教程：[计算机教育中缺失的一课](https://missing-semester-cn.github.io/)

- csdiy课程信息页：[MIT-Missing-Semester | csdiy](https://csdiy.wiki/%E7%BC%96%E7%A8%8B%E5%85%A5%E9%97%A8/MIT-Missing-Semester/)

- ~~pass~~

#### CS61A: Structure and Interpretation of Computer Programs
>**课程简述**：伯克利CS61系列的第一门课程，使用python作为课程的编程语言。强调抽象，让学生掌握用程序来解决实际问题，而不关注底层的硬件细节。oop（面向对象编程）入门利器。

- 课程官方网址：[CS61A | UC Berkeley](https://cs61a.org/)

- 往期课程页面备份：[Fall 2024 | hqhq1025](https://hqhq1025.github.io/cs61a-24fa-backup/)

- 课程教材：[Composing Programs](https://www.composingprograms.com/)

- 课程教材中译：[COMPOSING PROGRAMS](https://composingprograms.netlify.app/)

- csdiy课程信息页：[CS61A: Structure and Interpretation of Computer Programs | csdiy](https://csdiy.wiki/%E7%BC%96%E7%A8%8B%E5%85%A5%E9%97%A8/Python/CS61A/)

- ~~half pass 【py-oop】~~
- pass 【Functional Programming】【SQL】

#### C++ Tutorial - w3school
>**课程简述**：这个就没什么好说的了，就是单纯的**文档型教程**，与国内的[菜鸟教程](https://www.runoob.com)类似，但在重点讲解上显然要精简得多。对C++的各种特性毫无概念时可以参考这个教程，可以在短时间内建立起对C++的初步了解，随后即可通过**CS106L**深入了解C++的各种特性及其运用。

- 课程网址：[C++ Tutorial | w3school](https://www.w3schools.com/cpp/default.asp)

- ~~pass~~

#### CS106L: Standard C++ Programming
>**课程简述**：这门课会深入到很多标准 C++ 的特性和语法，让你编写出高质量的 C++ 代码。例如 auto binding, uniform initialization, lambda function, move semantics，RAII 等技巧。这门课并不难，但是信息量很大，需要在之后的开发实践中反复巩固，因此正好适合正在钻研C++工程的我。

- 官方教材：[CS106L-Textbook](https://cs106l.github.io/textbook/)

- 课程资料备份1（幻灯片等）：[Winter 2024 | JiNanPiWang](https://github.com/JiNanPiWang/CS106L)
- 课程资料备份2：[Winter 2025 | Gkbinqi](https://github.com/Gkbinqi/CS106L)

- csdiy课程信息页：[CS106L: Standard C++ Programming | csdiy](https://csdiy.wiki/%E7%BC%96%E7%A8%8B%E5%85%A5%E9%97%A8/cpp/CS106L/)

- 课程官方网址：[CS106L: Standard C++ Programming | Stanford University](https://web.stanford.edu/class/cs106l/)

- ~~pass~~


### 数据结构与算法

#### Hello 算法
>动画图解、一键运行的数据结构与算法教程。支持 Python, Java, C++, C, C#, JS, Go, Swift, Rust, Ruby, Kotlin, TS, Dart 代码。

- 教程网址：[Hello 算法](https://www.hello-algo.com/)

- 项目仓库：[hello-algo](https://github.com/krahets/hello-algo)

#### *CS106B/X: Programming Abstractions in C++
>**课程简述**：CS106系列的另一部分课程，专注于算法与抽象。B与X的教材均为[Programming Abstractions in C++](https://web.stanford.edu/dept/cs_edu/resources/textbook/)，其中CS106X的[课程网站](https://web.stanford.edu/class/cs106x/)整理有[课程讲义](https://web.stanford.edu/class/cs106x/handouts.html)。不过这个课程的资源较为分散，对于学习的话更适合用于入门阅读参考。如果想要系统地学习数据结构与算符的内容的话，建议去看[CS61B](https://csdiy.wiki/%E6%95%B0%E6%8D%AE%E7%BB%93%E6%9E%84%E4%B8%8E%E7%AE%97%E6%B3%95/CS61B/)或[Algorithms I & II](https://csdiy.wiki/%E6%95%B0%E6%8D%AE%E7%BB%93%E6%9E%84%E4%B8%8E%E7%AE%97%E6%B3%95/Algo/)

- CS106X课程讲义：[Handouts | CS106X: Programming Abstractions in C++](https://web.stanford.edu/class/cs106x/handouts.html)

- CS106B课程主页：[CS106B: Programming Abstractions](https://web.stanford.edu/class/cs106b/)

- csdiy课程信息页：[Stanford CS106B/X: Programming Abstractions in C++ | csdiy](https://csdiy.wiki/%E7%BC%96%E7%A8%8B%E5%85%A5%E9%97%A8/cpp/CS106B_CS106X/)



## 进阶理论

### 工程理论

#### GPU工作原理
>**模块简述**：GPU是现代计算机上一个重要的处理模块，主要用于诸如图形学计算、深度学习等对并行计算性能要求较高的计算领域。需要注意的是，**GPU**与人们口中常说的**显卡**是两个概念，前者是一个处理芯片，后者是一个完整、独立的计算机部件。
>
>**基础依赖**：**计算机体系结构**、**计算机组成原理**

- 相关文章1：[计算机组成原理——GPU图像处理器 | 云物互联](https://www.cnblogs.com/jmilkfan-fanguiju/p/11825032.html)

- 相关视频1：[内存与显存的区别 | Redknot-乔红](https://www.bilibili.com/video/BV1SGXsYxESV/?spm_id_from=333.1245.0.0&vd_source=bf4f387b9668a681bfdcd3b4b0a3b4ee)  
**Note**：该视频内容主要介绍了GPU数据传输技术、显存（GDDR：Graphics Doule Data Rate SDRAM，图形双倍数据速率同步动态随机存取储存器）技术与传统内存（DDR：Doule Data Rate SDRAM，双倍数据速率同步动态随机存取储存器）技术的区别

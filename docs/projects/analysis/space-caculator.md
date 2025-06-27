---
draft: true
title: SpaceCaculator：Python3面向对象简单应用
categories:
  - 编程语言
abbrlink: 27707
date: 2025-03-16 14:48:10
cover: https://i.imgur.com/rsm0tiV.png
tags: 
  - Projects
  - Python
---

## 导言

学习了cs61a的有关python面向对象的课程（函数式编程没有去细看，本文内容也与之无关），对面向对象的思想有了更加深刻的理解，特别是在多态对象的统一接口思想上，其在实现上主要运用了python对象系统的**继承**及**组合**机制（详情可以参考cs61a的[课程资料](https://csdiy.wiki/%E7%BC%96%E7%A8%8B%E5%85%A5%E9%97%A8/Python/CS61A/)）。当然，不是只有python才具有继承与组合机制，几乎所有的面向对象语言都支持继承与组合。

将上面的思想与数学中立体几何的各种定义结合起来，就有了下面这个项目👇 

项目网址：[Space Calculator](https://github.com/virtualguard101/space-calculator) 

本文主要结合cs61a的课程思想，通过核心代码简要解读一下这个项目的实现框架，针对语法及代码细节不作展开，详情可结合本文自行阅读源码，核心代码位于项目根目录下的/src/space.py 

---
## 多态对象

**一个数据对象可能由不止一种有用的表示，我们也许会想要设计能够处理多种表示形式的系统**。这是cs61a对多态对象系统的表述。在构建一个对象时，我们可以从多个角度来描述构建该对象所需要的属性，从而使这个对象有多种表示形态。 

举一个简单的例子，一个向量在空间中的表示通常有**坐标表示**和**分解表示（通常是正交分解）**两种形式，前者在代数运算上具有极大的方便，后者在几何意义的表示上具有优势。因此在构造一个向量时，我们就可以通过两种方式进行构造： 

```py
class VectorWithPoint(VectorOperation):
    '''Vector represent with point.'''
    branch = 'geometry'

    def __init__(self, point_start: Point, point_end: Point):
        super().__init__()
        self.point_s = point_start
        self.point_e = point_end 

    def __repr__(self):
        super().__init__()
        return f'Vector({self.point_s.name}{self.point_e.name}) == {VectorWithCoordinate((self.point_e.x - self.point_s.x), (self.point_e.y - self.point_s.y), (self.point_e.z - self.point_s.z))}'

    def __str__(self):
        return f'{self.point_s.name.upper()}->{self.point_e.name.upper()}'


class VectorWithCoordinate(VectorOperation):
    '''Vector represent with coordinate.'''
    branch = 'algebra'

    def __init__(self, x, y, z):
        super().__init__()
        self.x = x 
        self.y = y 
        self.z = z 

    def __repr__(self):
        return f'Vector({self.x}i + {self.y}j + {self.z}k)'

    def __str__(self):
        return f'({self.x}, {self.y}, {self.z})'
```

通过上面的py代码中，我们可以通过**几何元素（点）**和**代数元素（坐标）**两种形态来构造和表示一个向量对象，从而为我们后续的可能需要的操作作铺垫。 

---
## 组合、继承与对象接口

### 继承与组合

继承是面向对象编程中一个强大的机制，它允许一个子类从其所继承的父类**继承**属性和方法。我们通过将计算结果为基类（父类）的表达式放在类名后面的括号中来指定继承。

```py
class VectorOperation:
    '''The operation interface for vector which represent with coordinate or point in space.'''

class VectorWithPoint(VectorOperation):
    '''Vector represent with point.'''

class VectorWithCoordinate(VectorOperation):
    '''Vector represent with coordinate.'''
```

在上面的代码中，类`VectorWithCoordinate`、`VectorWithPoint`均继承于`VectorOperation`。 

对于类的继承，我们通常以`is-a`即**xx是一个xx**来描述子类与父类之间的关系，从上面的例子来看就是**几何形态向量**与**坐标形态向量**都是一个**向量**（所以从定义角度来看，`VectorOperation`应该改为`Vector`）。

在面向对象中，还有一个概念称为类的**组合**，以`has-a`即**xx有一个xx**来描述二者的关系。举一个简单的例子：

```py
class Lessons:
    def __init__(self, name, teacher, grade):
        self.name = name
        self.teacher = teacher
        self.grade = grade

class Students:
    def __init__(self, name, id):
        self.name = name
        self.id = id
        self.lesson = Lessons('python-oop', 'cs61a', 4.0)
    def __repr__(self):
        return f'name: {self.name} id: {self.id} \ 
                 lesson: {self.lesson.name}'
```

在上面的代码中，我们定义了两个类：`Lessons`和`Students`，其中`Students`的构造函数中将`Lessons`的一个实例作为一个属性，用上面的关系来说明就是**学生有一门课程**。在面向对象编程中，**组合**相比起**继承**更加灵活，因为后者所定义的类与类之间的关系是**静态**的，前者反之。 

在这个项目中，我们对组合的运用同样无处不在。在数学关系上，各个概念之间的关系是确定的，不需要动态调整，因此我们在这里更加倾向于使用继承来描述类于类之间的关系；而在定义操作各个数学元素的运算概念时，组合灵活的优势就能得到极大的发挥。定义运算的地方和方法就是下文将要重点介绍的对象。 

---
### 对象共享接口

~~你已经对继承和组合的概念有了初步的了解，现在来手搓一个计算器吧🤓👆~~ 

通过上一节，对继承和组合有了一定的了解后，是时候将其运用于实际项目中了。 

为了内容能够同时涵盖**组合**与**继承**，我们选取源码中概念综合度相对较高的平面操作模块为例展开解读。 
整个平面模块的代码如下： 

```py
class PlaneOperation:
    '''The operation interface for plane which represent with geometrical represent or algebraic represent in space.'''
    type_tag = 'plane'

    @property
    def normal_vector(self) -> VectorWithCoordinate:
        if self.branch == 'geometry':
            vector_a = VectorWithPoint(self.point_1, self.point_2)
            vector_b = VectorWithPoint(self.point_1, self.point_3)
            return vector_a.cross_product(vector_b)
        elif self.branch == 'algebra':
            return VectorWithCoordinate(self.A, self.B, self.C)

    def normal_vec_repr(self):
        assert isinstance(self, PlaneWithGeo), '''A point argument is required, while the object dosen't have.'''
        return f'{self.normal_vector.x}(x-{self.point_1.x}) + {self.normal_vector.y}(y-{self.point_1.y}) + {self.normal_vector.z}(z-{self.point_1.z}) = 0'

    def general_repr(self):
        if self.branch == 'geometry':
            self.constant = self.point_1.x*self.normal_vector.x + self.point_1.y*self.normal_vector.y + self.point_1.z*self.normal_vector.z
        return f'{self.normal_vector.x}x + {self.normal_vector.y}y + {self.normal_vector.z}z + {self.constant} = 0'

    def intercept_repr(self):
        if self.normal_vector.x == 0:
            self.a = 0
        else:
            self.a = -(self.constant/self.normal_vector.x)
        if self.normal_vector.y == 0:
            self.b = 0
        else:
            self.b = -(self.constant/self.normal_vector.y)
        if self.normal_vector.z == 0:
            self.c = 0
        else:
            self.c = -(self.constant/self.normal_vector.z)
        
        if self.branch == 'geometry':
            self.constant = self.point_1.x*self.normal_vector.x + self.point_1.y*self.normal_vector.y + self.point_1.z*self.normal_vector.z
        return f'x/{self.a} + y/{self.b} + z/{self.c} = 1'

    def angle(self, other: VectorOperation) -> list:
        cos_a = (self.normal_vector.quantity_product(other.normal_vector)) / self.normal_vector.magnitude * other.normal_vector.magnitude
        angle = acos(cos_a)
        return [cos_a, f'{angle/pi}pi']

    def is_vertical(self, other: VectorOperation) -> bool:
        return self.angle(other)[0] == 0

    def is_parallel(self, other: VectorOperation) -> bool:
        return self.normal_vector.cross_product(other.normal_vector).magnitude == 0

    def distance_to_plane(self, point: Point) -> float:
        assert isinstance(point, Point), ''
        A = self.normal_vector.x
        B = self.normal_vector.y
        C = self.normal_vector.z
        x0 = point.x; y0 = point.y; z0 = point.z
        return fabs(A*x0 + B*y0 + C*z0 + self.constant) / self.normal_vector.magnitude

    def point_at_plane(self, point: Point) -> bool:
        return self.normal_vector.x * point.x + self.normal_vector.y * point.y + self.normal_vector.z * point.z + self.constant == 0


class PlaneWithGeo(PlaneOperation):
    '''Plane construct by geometrical elements.'''
    branch = 'geometry'

    def __init__(self, point_1: Point, point_2: Point, point_3: Point):
        super().__init__()
        self.point_1 = point_1
        self.point_2 = point_2
        self.point_3 = point_3

    @property
    def constant(self):
        return -(self.normal_vector.x*self.point_1.x + 
                 self.normal_vector.y*self.point_1.y +
                 self.normal_vector.z*self.point_1.z)

    def __repr__(self):
        return f'Plane({super().normal_vec_repr()})'
    
    def __str__(self):
        return f'{PlaneOperation.type_tag}-{self.point_1.name}{self.point_2.name}{self.point_3.name}'


class PlaneWithAlg(PlaneOperation):
    '''Plane construct by algebraic elements.'''
    branch = 'algebra'

    def __init__(self, A, B, C, constant):
        super().__init__()
        self.A = A
        self.B = B
        self.C = C
        self.constant = constant

    def __repr__(self):
        return f'Plane({super().general_repr()})'

    def __str__(self):
        return f'{PlaneOperation.type_tag}: {super().general_repr()}'
```

看似很长，将其拆分来看并辅以课程思想实则非常简单。 

快速过一遍源码，不难看出`PlaneWithGeo`与`PlaneWithAlg`均*继承*于`PlaneOperation`。现在我们将注意力转移到`PlaneOperation`上，注意到这个类的定义中并没有构造器，只有一些方法。这些方法所定义的就是针对平面的操作或运算，我们暂时忽略这些实现的细节，着眼于整个`PlaneOperation`与其派生类（子类）的继承关系。 

不难发现同属“平面”的两种形态的运算定义**共享**于它们共同的父类，用上一节所提到的关系说明就是**几何形态平面和代数形态平面都是平面**。同时，这里我们可以可以换一个角度理解，根据前句提到的关系，我们也可以说**几何形态的平面与代数形态的平面都可以通过一个统一的接口相互地进行操作与运算**，因为它们都是**平面**。而我们就把这个统一的接口（这里即`PlaneOperation`）称为继承于它的多态对象的**共享接口**。 

从整个平面操作模块内部来看，我们定义了平面的多态，并且在他们的父类中定义了操作平面的共享接口。现在，我们将目光放在第一个子类的构造器上，可以看出我们在构造时传入了`Point`类的实例作为`PlaneWithGeo`的实例属性，其在数学上的定义就是*三点确定一个平面*，在**组合**关系上，我们就可以将其描述为**平面上有三个点**。 

## 总结

在这篇文章中，我们介绍了python面向对象编程中**继承**与**组合**的机制，通过一个简易项目分析了其在对象抽象的运用。以上分析为个人学习理解，尚有不足之处，系统性的知识还请参考cs61a的[课程note](https://www.composingprograms.com/pages/27-object-abstraction.html#multiple-representations)。 

---

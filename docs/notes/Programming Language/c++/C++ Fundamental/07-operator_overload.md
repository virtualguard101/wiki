# 运算符重载

*该笔记基于课程CS106L的学习，用于记录一些cpp的重要特性以及先前不曾了解的cpp特性。*

## 成员函数运算符重载

在用户自定义类中，我们可以像定义函数一样定义运算符，也可以像函数重载一样对运算符进行重载操作。

对于在前面章节中定义的`Student`类：
```cpp
class Student {
public:
    Student(String name, long int id, int age);
    void setName(String name);
    String getName() const;
    long int getID() const;
    int getAge() const;

private:
    using String = std::string;
    String _name;
    long int _id;
    int _age;
};
```
我们可以为其定义一个`<`运算符以进行排序：
```cpp
class Student {
public:
    Student(String name, long int id, int age);
    void setName(String name);
    String getName() const;
    long int getID() const;
    int getAge() const;
    bool operator < (const Student& rhs) const;

private:
    using String = std::string;
    String _name;
    long int _id;
    int _age;
};
```

```cpp
bool Student::operator<(const Student& rhs) {
    return age < rhs.age;
}
```
在上面的实现中，由于我们处于成员函数中，默认情况下`age`指的就是`this->age`，即`Student`的成员变量。

在进行重载运算符操作时通常有两种情形：

- 成员函数
    - 在用户自定义类中进行声明

    - 允许使用成员对象（`this->`）

- 非成员函数
    - 重载运算符定义在任何类之外

    - 对象两侧（左值(lhs)/右值(rhs)）均为参数

## 非成员函数运算符重载

非成员函数运算符重载允许我们为自定义类型定义运算符，使得这些类型的行为类似于内置类型。非成员函数运算符重载通常用于定义二元运算符（如 `+`、`-`、`*`、`/` 等），这些运算符需要访问两个操作数。

## `friend`关键字

`friend`关键字用于声明**友元函数**。

友元函数指不是一个类成员函数却能够访问类的私有变量的函数，通常用于实现类之间的协作，或者实现某些功能时需要访问类的内部数据。

## 实际应用

以空间向量的定义为例：

```cpp
#include <iostream>
#include <cmath>
#include <random>
#include <limits>
#include <cassert>


#pragma once
class Vector3 {
public:
    // 数据成员
    float x, y, z;  // 添加成员变量声明
    
    // 构造方法
    Vector3();
    Vector3(float x, float y, float z);
    explicit Vector3(float scalar);

    // 运算符重载
    Vector3 operator+(const Vector3& rhs) const;
    Vector3 operator-(const Vector3& rhs) const;
    Vector3 operator*(float scalar) const;
    Vector3 operator/(float scalar) const;

    Vector3& operator+=(const Vector3& rhs);
    Vector3& operator-=(const Vector3& rhs);
    Vector3& operator*=(float scalar);
    Vector3& operator/=(float scalar);

    // 向量运算
    float dot(const Vector3& rhs) const;
    Vector3 cross(const Vector3& rhs) const;

    // 向量归一化
    Vector3 normalized() const;
    void normalize();

    // 长度计算
    float length() const;
    float lengthSquared() const;

    // 投影和反射
    Vector3 projectOnto(const Vector3& target) const;
    Vector3 reflect(const Vector3& normal) const;

    // 比较操作
    bool isZero(float epsilon = 1e-6f) const;
    bool operator==(const Vector3& rhs) const;

    // 静态方法
    static Vector3 Zero();
    static Vector3 One();
    static Vector3 UnitX();
    static Vector3 UnitY();
    static Vector3 UnitZ();
    static Vector3 Random(float min = -1.0f, float max = 1.0f);

    // 友元函数
    friend std::ostream& operator<<(std::ostream& os, const Vector3& vec);
    friend Vector3 operator*(float scalar, const Vector3& vec);
    
protected:
    std::string type_tag = "vector";

};
```

```cpp
#include "vector.h"

// 构造方法
Vector3::Vector3() : x(0), y(0), z(0) {}
Vector3::Vector3(float x, float y, float z) : x(x), y(y), z(z) {}
Vector3::Vector3(float scalar) : x(scalar), y(scalar), z(scalar) {}

// 运算符重载
Vector3 Vector3::operator+(const Vector3& rhs) const {
    return Vector3(x + rhs.x, y + rhs.y, z + rhs.z);
}

Vector3 Vector3::operator-(const Vector3& rhs) const {
    return Vector3(x - rhs.x, y - rhs.y, z - rhs.z);
}

Vector3 Vector3::operator*(float scalar) const {
    return Vector3(x * scalar, y * scalar, z * scalar);
}

Vector3 Vector3::operator/(float scalar) const {
    assert(scalar != 0 && "Division by zero");
    return *this * (1.0f / scalar);
}

// 复合赋值运算符
Vector3& Vector3::operator+=(const Vector3& rhs) {
    x += rhs.x;
    y += rhs.y;
    z += rhs.z;
    return *this;
}

Vector3& Vector3::operator-=(const Vector3& rhs) {
    x -= rhs.x;
    y -= rhs.y;
    z -= rhs.z;
    return *this;
}

Vector3& Vector3::operator*=(float scalar) {
    x *= scalar;
    y *= scalar;
    z *= scalar;
    return *this;
}

Vector3& Vector3::operator/=(float scalar) {
    assert(scalar != 0 && "Division by zero");
    return *this *= (1.0f / scalar);
}

// 向量运算
float Vector3::dot(const Vector3& rhs) const {
    return x * rhs.x + y * rhs.y + z * rhs.z;
}

Vector3 Vector3::cross(const Vector3& rhs) const {
    return Vector3(
        y * rhs.z - z * rhs.y,
        z * rhs.x - x * rhs.z,
        x * rhs.y - y * rhs.x
    );
}

// 归一化方法
Vector3 Vector3::normalized() const {
    float len = length();
        if (len <= std::numeric_limits<float>::epsilon()) {
            return Vector3::Zero();
        }
        return *this / len;
}

void Vector3::normalize() {
    if (float len = length(); len > std::numeric_limits<float>::epsilon()) {
        x /= len;
        y /= len;
        z /= len;
    }
}

// 长度计算
float Vector3::length() const {
    return std::sqrt(lengthSquared());
}

float Vector3::lengthSquared() const {
    return x*x + y*y + z*z;
}

// 投影和反射
Vector3 Vector3::projectOnto(const Vector3& target) const {
    float lenSq = target.lengthSquared();
        if (lenSq < std::numeric_limits<float>::epsilon()) {
            return Vector3::Zero();
        }
        float scale = dot(target) / lenSq;
        return target * scale;
}

Vector3 Vector3::reflect(const Vector3& normal) const {
    return *this - normal * (2.0f * dot(normal));
}

// 比较操作
    bool Vector3::isZero(float epsilon) const {
        return std::abs(x) < epsilon && 
               std::abs(y) < epsilon && 
               std::abs(z) < epsilon;
}

bool Vector3::operator==(const Vector3& rhs) const {
    return std::abs(x - rhs.x) < 1e-6f &&
           std::abs(y - rhs.y) < 1e-6f &&
           std::abs(z - rhs.z) < 1e-6f;
}

// 静态方法
Vector3 Vector3::Zero() { return Vector3(0, 0, 0); }
Vector3 Vector3::One() { return Vector3(1, 1, 1); }
Vector3 Vector3::UnitX() { return Vector3(1, 0, 0); }
Vector3 Vector3::UnitY() { return Vector3(0, 1, 0); }
Vector3 Vector3::UnitZ() { return Vector3(0, 0, 1); }

Vector3 Vector3::Random(float min, float max) {
    static std::mt19937 gen(std::random_device{}());
    std::uniform_real_distribution<float> dist(min, max);
    return Vector3(dist(gen), dist(gen), dist(gen)).normalized();
}

// 友元函数实现
std::ostream& operator<<(std::ostream& os, const Vector3& vec) {
    os << "(" << vec.x << ", " << vec.y << ", " << vec.z << ")";
    return os;
}

Vector3 operator*(float scalar, const Vector3& vec) {
    return vec * scalar;
}
```

## 约定俗成的规则

- 保持代码的易读性

- 重载后的运算符定义应当与对应的算术运算具有一定的相似性

- 当操作意义不明确时，不妨为其起一个合适的名称

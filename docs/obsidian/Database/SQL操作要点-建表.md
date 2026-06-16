---
date: 2026-06-08 23:46:51
title: SQL操作要点-建表
permalink: create
publish: true
tags:
  - 数据库系统
---

# 建表

## 登录数据库管理系统

这里用的是MySQL。

```bash
mysql -u root -p
```

成功登录后可通过 `show databases;` 查看当前所有数据库。

## 建库

```sql
create database testDB charset utf8mb4 collate utf8mb4_general_ci;
```

`charset` 用于指定字符集，`collate` 指定排序规则，这里是 `utf8mb4_general_ci`，表示使用 `utf8mb4` 字符集，排序规则为 `general_ci`。

!!! info "字符集与排序方式"
    **字符集**（*Character Set*）字符集是数据库中允许存储哪些字符以及如何将字符转换为二进制数据的一套规则。它决定了你能在表中写入什么文字（比如英文、中文、日文、emoji 等）。`utf8mb4` 是 MySQL 推荐的字符集，支持几乎所有语言字符和 emoji 表情（每个字符最多 4 字节），是 UTF-8 的完整实现。
    
    **排序方式**（Collation / 排序规则）指同一字符集下，比较和排序字符的具体规则。它决定了执行 ORDER BY、GROUP BY、=、> 等操作时，字符如何比较大小、是否区分大小写、是否区分重音等。utf8mb4_general_ci：通用规则，不区分大小写（'A' = 'a'），排序速度较快，适合大多数中文/英文场景。你是一个DBA，现在正在设计“大学生选课系统”。创建数据库时，要求既能存储中文和生僻汉字，又能存储emoji表情，且排序时不区分大小写。

## 删库

```sql
drop database testDB;
```

DROP DATABASE是一个DDL（数据定义语言）操作，它不可回滚，也没有事务保护。一旦执行，数据会立即被永久移除，不进入回收站。如果没有备份，数据将几乎无法恢复。因此，在生产环境中，执行此命令需要极高的权限和极其谨慎的确认，稍有不慎就会导致“删库跑路”的灾难性后果。

## 建表

- 建表 ``Student`

    ```sql
    create table if not exists `Student` (
      `id` int not null auto_increment comment '学生编号（自增主键）',
      `name` varchar(50) not null comment '学生姓名',
      `student_no` varchar(20) not null comment '学号',
      `sex` enum('男', '女') default null comment '性别',
      primary key (`id`)
    ) engine=innodb default charset=utf8mb4 collate=utf8mb4_general_ci comment='学生表';
    ```

    - `id` 所在行中，`auto_increment` 表示该列自增，每次插入新行时，该列的值会自动加1；同时，后面的 `primary key` 表示该列为主键。

    - `not_null` 表示为某列添加**非空约束**。

    - `comment '...'` 表示为该列添加注释。

    - `engine=innodb` 表示显式指定存储引擎为 InnoDB，这是 MySQL 默认的存储引擎，也是最常用的存储引擎。

- 建表 `Course`

    ```sql
    create table if not exists `Course` (
      `course_id` int not null auto_increment comment '课程ID，自增主键',
      `course_name` varchar(100) not null comment '课程名称',
      `credit` tinyint unsigned not null comment '学分（整数）',
      primary key (`course_id`)
    ) engine=innodb default charset=utf8mb4 collate=utf8mb4_general_ci comment='课程表';
    ```

- 建表 `Enrollment`

    ```sql
    create table if not exists `Enrollment` (
      `enroll_id` int not null auto_increment comment '选课ID（自增主键）',
      `student_no` varchar(20) not null comment '学号',
      `course_id` int not null comment '课程ID',
      `grade` decimal(5,2) default null comment '成绩',
      primary key (`enroll_id`),
      key `idx_student_no` (`student_no`),
      key `idx_course_id` (`course_id`),
      constraint `fk_enrollment_student` foreign key (`student_no`) references `Student` (`student_no`) on delete restrict on update cascade,
      constraint `fk_enrollment_course` foreign key (`course_id`) references `Course` (`course_id`) on delete restrict on update cascade
    ) engine=innodb default charset=utf8mb4 collate=utf8mb4_general_ci comment='选课表';
    ```

    - `enroll_id` 所在行中，`auto_increment` 表示该列自增；`primary key` 表示该列为主键。

    - `grade` 使用 `decimal(5,2)` 存储成绩，最多两位小数；`default null` 表示未录入成绩时可为空。

    - `key` 为列建立索引，加快按学号或课程 ID 查询。

    - `foreign key ... references` 建立外键，关联 `Student` 与 `Course` 表；`on delete restrict` 表示有关联记录时不可删除，`on update cascade` 表示主表 ID 更新时同步更新。

    !!! warning
        直接运行这个建表代码会出现如下错误：

        ```bash
        ERROR 6125 (HY000): Failed to add the foreign key constraint. Missing unique key for constraint 'fk_enrollment_student' in the referenced table 'student'
        ```
        
        这是因为在父表 `Student` 中，被外键引用的列 `student_no` 缺少索引。

        MySQL 要求被引用的列（即父表中被 FOREIGN KEY 引用的列）必须拥有一个索引（可以是 PRIMARY KEY、UNIQUE KEY 或普通 KEY），否则无法创建外键约束。

        可先使用以下命令为 `student_no` 列添加索引再运行建表代码：

        ```sql
        alter table `Student` 
        add unique index `sid_index`(`student_no`) using btree;
        ```

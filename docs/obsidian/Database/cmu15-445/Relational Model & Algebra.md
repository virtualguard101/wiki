---
date: 2026-04-20 15:41:38
title: Relational Model & Algebra
permalink: relation-model-and-algebra
publish: true
tags:
  - 数据库系统
  - CMU15-445
---

# Relational Model & Algebra

> [Slide - #01: Relational Model & Algebra | CMU 15-445/645](https://15445.courses.cs.cmu.edu/spring2026/slides/01-relationalmodel.pdf)
>
> [Notes - #01: Relational Model & Algebra | CMU 15-445/645](https://15445.courses.cs.cmu.edu/spring2026/notes/01-relationalmodel.pdf)

## Database Background

### Database Management System (DBMS)

> [数据库管理系统 - 数据库系统的基本概念](../数据库系统的基本概念.md#数据库管理系统)

### Data Models

- A *data model*（[**数据模型**](../数据模型.md)） is a collection of concepts for describing the data in a database, which contains the rules that define the types of things that could exist and how they relate.

- A *schema*（[**模式**](../数据库系统结构.md#模式)） is a description of a particular collection of data, using a given data model. This defines the structure of database for a data model.

### Some Data Models

- *Relational*（**关系型**）-> Most DBMS use this model

- *Key-Value*（**键值型**）-> Simple Apps / Caches

- *Graph*（**图数据库型**）-> NoSQL

- *Document / JSON / XML / Object* -> NoSQL

- *Wide-Column / Column-family* -> NoSQL

- *Array (Vector, Matrix, Tensor)* -> ML / Science

- *Hierarchical*（**层次型**）

- *Network*（**网状型**）

- *Semantic*（**语义型**）

- *Entity-Relationship*（**实体关系**）

## Relational Model

> [关系模型](../关系模型.md)

Three concepts of relational model:

- *Structure*（**结构**）: The definition of relations and their contents independent of their physical representation.

- *Integrity*（**完整性**）: Ensure the database’s contents satisfy certain constraints.

- *Manipulation*（**操作**）: Declarative API for accessing and modifying a database's contents via relations (sets).

!!! tip "Data Independent"
    > [数据库系统结构](../数据库系统结构.md)

    Isolate the user/application from low-level data representation. The user only worries about high-level application logic.

    DBMS optimizes the layout according to operating environment, database contents, and workload.

    ![](assets/relation-model-and-algebra/1.png)

### Some basic concepts

- *Relation*（[**关系**](../关系模型.md#关系)）: Unordered sets that contain the relationship of attributes that represent entities.

    ![](assets/relation-model-and-algebra/2.png)

- *Tuple*（[**元组**](../关系模型.md#元组)）: Set of attribute values(aka its domain) in the relation.

    - Values are (normally) **atomic/scalar**.

    - The special value `NULL` is a member of every domain (if allowed).

- *Primary Key*（[**主码**](../关系模型.md#主码)）: The **unique identifier** for each tuple in the relation.

    ![](assets/relation-model-and-algebra/3.png)

    !!! info
        Some DBMSs will automatically create an internal primary key if a table does not define one.

        DBMS can auto-generation unique primary keys via an [identity column](https://en.wikipedia.org/wiki/Identity_column):

        - IDENTITY (SQL Standard)

        - SEQUENCE (PostgreSQL / Oracle)

        - AUTO_INCREMENT (MySQL)

- *Foreign Key*（**外码**）: The identifier that specifies that an attribute from one relation maps to a tuple in another relation.

    ![](assets/relation-model-and-algebra/4.png)

    ![](assets/relation-model-and-algebra/5.png)

- *Constraints*（**约束**）: Rules that ensure the data in the database is accurate and consistent.

## Relational Algebra

### Data Manipulation Language (DML)

*Data Manipulation Language*（**DML**, **数据操作语言**）, which refers to the API that a DBMS exposes to applications to store and retrieve information from a database.

There are two types of DML:

- *Procedural*（**过程式**）: The query specifies the (high-level) execution strategy the DBMS should use to find the desired result based on sets / bags.

    !!! example
        Use a `for` loop to scan all records and count how many records are there to retrieve the number of records in the table.

- *Non-Procedural (Declarative)*（**声明式**）: The query specifies only what data is wanted and not how to find it.

    !!! example
        Use SQL `SELECT COUNT(*) FROM artist` to count how many records are there in the table.

!!! tip "Why Procedural <=> Relational Algebra, Declarative <=> Relational Calculus?"
    In CMU 15-445, this mapping is not just terminology:

    - **Procedural DML** corresponds to **Relational Algebra (关系代数)**: emphasize **how** to derive results by composing operators (selection, projection, join, union, difference, etc.).

    - **Non-Procedural (Declarative) DML** corresponds to **Relational Calculus (关系演算)**: emphasize **what** result properties are desired, without specifying execution steps.

    - Under safe/tractable conditions, relational algebra and relational calculus are equivalent in expressive power (same query class, viewed from two angles).

    - SQL is written in a mostly declarative style (calculus-like), while the optimizer translates SQL into relational-algebra-style logical plans (and then physical execution plans).

### Relational Algebra Operators

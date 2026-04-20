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

## Database Background

### Database Management System (DBMS)

> [数据库管理系统 - 数据库系统的基本概念](../数据库系统的基本概念.md#数据库管理系统)

### Data Models

- A *data model*（[**数据模型**](../数据模型.md)） is a collection of concepts for describing the data in a database, which contains the rules that define the types of things that could exist and how they relate.

- A *schema*（[**模式**](../数据库系统结构.md#模式)） is a description of a particular collection of data, using a given data model. This defines the structure of database for a data model.

### Some Data Models

- *Relational*（**关系模型**）-> Most DBMS use this model

- *Key-Value*（**键值模型**）-> Simple Apps / Caches

- *Graph*（**图模型**）-> NoSQL

- *Document / JSON / XML / Object* -> NoSQL

- *Wide-Column / Column-family* -> NoSQL

- *Array (Vector, Matrix, Tensor)* -> ML / Science

- *Hierarchical*

- *Network*

- *Semantic*

- *Entity-Relationship*（**实体关系**）

## Relational Model

> [关系模型](../关系模型.md)

Three concepts of relational model:

- *Structure*（**结构化**）: The definition of relations and their contents independent of their physical representation.

- *Integrity*（**完整性**）: Ensure the database’s contents satisfy certain constraints.

- *Manipulation*（**可操作性**）: Declarative API for accessing and modifying a database's contents via relations (sets).

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

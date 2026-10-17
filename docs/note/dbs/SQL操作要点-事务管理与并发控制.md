---
date: 2026-06-25 21:52:09
title: SQL事务管理与并发控制
permalink: sql-transaction-concurrency
publish: true
tags:
  - 数据库系统
---

# 事务管理与并发控制

事务把一组 SQL 操作打包成一个**逻辑工作单元**：要么全部成功提交，要么全部撤销。DBMS 通过事务实现并发控制与故障恢复[^1]，保证多用户同时访问时数据仍然正确。

!!! tip
    本笔记以 **MySQL + InnoDB** 为主。InnoDB 支持事务；MyISAM 等存储引擎通常不支持事务。

---

## 事务

### 事务的概念和作用

**事务**（*Transaction*）是用户定义的一个数据库操作序列，这些操作要么**全部执行**，要么**全部不执行**。

典型场景：

- **转账**：A 账户扣款 + B 账户加款，必须同时成功或同时失败

- **下单**：扣库存 + 写订单 + 写支付记录，不能只完成其中一步

- **批量更新**：多条 `UPDATE`/`INSERT` 需要保持中间状态对外不可见

事务的作用可以概括为：

- **保证数据一致性**：避免“只做了一半”的脏状态

- **简化错误处理**：出错时 `rollback` 即可回到事务开始前

- **支持并发访问**：配合锁与隔离级别，协调多用户同时读写

### 创建事务

事务的基本模式：

```sql
-- 开启事务
start transaction;
-- 或 begin;

-- 一组 SQL 操作
update account set balance = balance - 100 where id = 1;
update account set balance = balance + 100 where id = 2;

-- 全部成功则提交
commit;

-- 若中途出错则回滚
-- rollback;
```

- 使用 `begin`

    ```sql
    begin;
    -- 事务操作
    commit;
    ```

- 使用 `start transaction`

    ```sql
    start transaction;
    -- 事务操作
    commit;
    ```

`start transaction` 还支持在开启时指定事务属性：

```sql
start transaction read only;
start transaction read write;
start transaction isolation level read committed;
start transaction isolation level repeatable read;
```

!!! tip "`begin` vs `start transaction`"
    | | `begin` | `start transaction` |
    | --- | --- | --- |
    | 是否标准 SQL | 不是标准，MySQL 特有 | 是 |
    | 是否支持修饰符 | 不支持 | 支持 `read only`、`isolation level` 等 |
    | 歧义性 | 有歧义（也可能是[存储过程](SQL操作要点-函数与存储过程.md#存储过程)的代码起始） | 语义明确，专用于事务 |

!!! info "autocommit"
    MySQL 默认 `autocommit = 1`：每条 SQL 自动作为一个事务并立即提交。需要显式事务时，应先 `start transaction` 或 `set autocommit = 0`。

### 事务的 ACID 特性

| 特性 | 英文 | 含义 |
|:---:|:---:|:---|
| **原子性** | Atomicity | 事务中的操作要么全部完成，要么全部不做 |
| **一致性** | Consistency | 事务前后，数据库从一个合法状态变到另一个合法状态（满足完整性约束） |
| **隔离性** | Isolation | 并发事务之间相互隔离，互不不当干扰 |
| **持久性** | Durability | 事务一旦 `commit`，结果永久保存，即使系统故障也不丢失 |

!!! tip
    - **原子性**主要靠 `commit` / `rollback` 和日志（undo log）实现

    - **隔离性**靠锁 + MVCC + 隔离级别实现（见下文）

    - **持久性**靠 redo log 等机制实现

### 事务的回滚

`rollback` 用于撤销当前事务中尚未提交的修改：

```sql
start transaction;

update book_info set price = price - 10 where id = 1;
-- 发现条件写错，撤销本次事务内的所有修改
rollback;
```

也可以使用**保存点**（Savepoint）只回滚到事务中的某个中间位置：

```sql
start transaction;

update book_info set price = 90 where id = 1;
savepoint sp1;

update book_info set price = 80 where id = 2;
rollback to sp1;  -- 只撤销 id=2 的修改，保留 id=1 的修改

commit;
```

!!! warning
    - `rollback` 只能撤销**当前事务内、尚未提交**的修改

    - 已 `commit` 的数据不能靠 `rollback` 恢复，需要备份或借助日志恢复

    - 部分 **DDL**（如 `drop table`）在 MySQL 中会**隐式提交**，无法与后续 DML 放在同一事务里回滚

### 事务隔离级别

多个事务并发执行时，若隔离不足，可能出现：

| 问题 | 含义 | 典型场景 |
|:---:|:---|:---|
| **脏读** | 读到另一个事务**尚未提交**的数据 | A 未提交就改了余额，B 读到了这个临时值 |
| **不可重复读** | 同一事务内两次读同一行，结果不同 | A 两次查询间，B 修改并提交了该行 |
| **幻读** | 同一事务内两次按条件查询，行数不同 | A 两次 `SELECT` 间，B 插入并提交了符合条件的新行 |

SQL 标准定义了 4 种隔离级别：

| 隔离级别 | 脏读 | 不可重复读 | 幻读 |
|:---:|:---:|:---:|:---:|
| READ UNCOMMITTED | 可能 | 可能 | 可能 |
| READ COMMITTED | 不可能 | 可能 | 可能 |
| REPEATABLE READ | 不可能 | 不可能 | 可能* |
| SERIALIZABLE | 不可能 | 不可能 | 不可能 |

\* MySQL InnoDB 在默认的 `REPEATABLE READ` 下，通过 **MVCC + 间隙锁** 在很大程度上避免了幻读。

查看与设置隔离级别：

```sql
-- 查看当前会话隔离级别
select @@transaction_isolation;

-- 设置当前会话隔离级别
set session transaction isolation level read committed;
```

!!! tip
    MySQL InnoDB 的默认隔离级别是 **REPEATABLE READ**。多数业务场景下无需修改；需要更强一致性时可考虑 `SERIALIZABLE`，但并发性能会下降。

---

## 并发控制

并发控制解决的核心问题：**多个事务同时读写同一数据时，如何保证正确性**。DBMS 主要依赖**锁机制**和**隔离级别**来协调。

### 表级锁

**表级锁**（Table Lock）锁住整张表。

- **优点**：实现简单，加锁/释放锁开销小

- **缺点**：并发度低——只要有一个事务写表，其他事务对该表的读写都可能被阻塞

MySQL 中 MyISAM 主要使用表级锁。InnoDB 在特殊场景下也可能对表加锁，但日常开发中更常见的是行级锁。

```sql
-- 显式对表加锁（了解即可，生产环境慎用）
lock tables book_info read;
-- 查询操作...
unlock tables;

lock tables book_info write;
-- 读写操作...
unlock tables;
```

### 行级锁

**行级锁**（Row Lock）只锁定被访问的**行**（或索引记录），不同行可由不同事务并发访问。

- **优点**：并发度高，适合 OLTP 场景

- **缺点**：实现复杂，锁管理开销更大

InnoDB 默认使用行级锁，通常无需手动加锁；执行 `UPDATE` / `DELETE` / 带锁的 `SELECT` 时，引擎会自动对涉及的行加锁。

按锁的兼容性关系，常分为：

| 锁类型 | 别名 | 作用 | 兼容性 |
|:---:|:---:|:---|:---|
| **共享锁** | S 锁、读锁 | 允许读，阻止他人写 | 多个事务可同时持有同一行的 S 锁 |
| **排他锁** | X 锁、写锁 | 阻止他人读和写 | 同一行同一时刻只能有一个 X 锁 |

显式加锁查询示例：

```sql
start transaction;

-- 共享锁：允许他人读，不允许他人写
select * from book_info where id = 1 lock in share mode;

-- 排他锁：不允许他人读和写
select * from book_info where id = 1 for update;

commit;
```

!!! tip "何时用 `for update`"
    - 先读后写、且读到的值会影响后续更新时（如检查库存后再扣减），常用 `select ... for update` 防止并发下超卖

    - 只读且允许他人同时读时，可用 `lock in share mode`

    - 必须在事务内使用（`start transaction` 之后），否则锁会立即释放

### 死锁

**死锁**：两个或多个事务互相等待对方释放锁，形成循环等待。

```text
事务 A：锁住行 1 → 等待行 2
事务 B：锁住行 2 → 等待行 1
```

InnoDB 会自动检测死锁，并**回滚其中一个事务**（通常回滚代价较小的一方）。应用层应做好重试逻辑，并尽量：

- 按**固定顺序**访问多张表/多行，减少交叉加锁

- 缩短事务持有锁的时间

- 避免在事务中做耗时外部调用（如 HTTP 请求）

---

!!! abstract
    | 操作 | 语句 |
    |:---|:---|
    | 开启事务 | `start transaction;` 或 `begin;` |
    | 提交 | `commit;` |
    | 回滚 | `rollback;` |
    | 保存点 | `savepoint sp1;` / `rollback to sp1;` |
    | 查看隔离级别 | `select @@transaction_isolation;` |
    | 排他锁查询 | `select ... for update;` |
    | 共享锁查询 | `select ... lock in share mode;` |

[^1]: [DBMS提供的数据控制功能 - 数据库系统的特点与组成](数据库系统的特点与组成.md#DBMS提供的数据控制功能)
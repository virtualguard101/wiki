---
date: 2026-06-16 17:17:59
title: SQL操作要点-视图
permalink: view
publish: true
tags:
  - 数据库系统
---

# 视图

视图是一个虚拟表，其数据来源于基表，本身不存储实际数据。使用视图可以隐藏基表中的敏感字段，例如对普通用户屏蔽身份证号、手机号等。通过视图可以简化复杂查询，例如将多表连接、聚合计算封装成视图，用户只需查询视图即可。

可通过以下sql语句创建视图：

```sql
create [or replace] view view_name [(column_list)]
as select_statement
[with [cascaded | local] check option];
```

- `or replace`：如果视图已存在，则替换它。

- `column_list`：为视图列指定别名（可选）。

- `select_statement`：定义视图数据的 SELECT 语句，决定视图包含哪些列、来自哪些表及筛选条件。

- `with [cascaded | local] check option`：对可更新视图，确保修改符合视图条件。

!!! example
    比如现在希望为普通读者实现受限图书查询功能，创建一个视图 `v_book_for_reader`，只允许读者看到书籍id、书名、作者、书架位置和书本是否借出。确保读者无法查看出版社、价格等敏感字段。则可以使用以下代码：

    ```sql
    create view v_book_for_reader as
    select book_id, book_name, author, shelf_location, state
    from book
    where state = 0;
    ```

## `case`表达式

管理员需要查看借阅记录，并直接显示“是否逾期”。

现在有以下sql代码：

```sql
create view v_borrow_overdue as
select 
  borrow_id,
  book_id,
  reader_id,
  borrow_date,
  due_date,
  actual_return_date,
  case 
    when actual_return_date is null and due_date < curdate() then '逾期'
    when actual_return_date is null then '借出中'
    else '已还'
    end as status
from borrow
```

针对这种组合条件，就可以使用`case`表达式来实现。

!!! tip
    视图中的计算列（如 CASE 表达式）不会占用物理存储空间，因为它们是计算出来的，而不是存储在数据库中的。但由于计算是实时进行的，因此在数据量较大时，可能会影响查询性能；同时，表达式可能会阻碍索引使用，导致扫描更多的行。

## 结合`join`使用

若现在有如下需求：

图书馆管理员需要查看每一笔借阅记录的详细信息，包括：

- 借阅编号（borrow_id）

- 书名（book_name）

- 读者姓名（name）

- 借书日期（borrow_date）

- 应还日期（due_date）

- 实际归还日期（actual_return_date）

这些信息分别存储在三张表中：

- 借阅记录在 borrow 表（包含 book_id, reader_id 外键）

- 图书名称在 book 表

- 读者姓名在 reader 表

那么就可以使用 `join` 将三张表连接起来：

```sql
create view v_borrow_detail as
select
  b.borrow_id,
  bk.book_name,
  r.name as reader_name,
  b.borrow_date,
  b.due_date,
  b.actual_return_date
from borrow b
join book bk
  on b.book_id = bk.book_id
join reader r
  on b.reader_id = r.reader_id;
```

- `create view v_borrow_detail as` 创建视图，将多表连接封装为虚拟表。

- `from borrow b` 以借阅表为主表；`join book bk` 和 `join reader r` 分别通过 `book_id`、`reader_id` 关联图书表与读者表。

- `select` 列出所需字段，其中 `r.name AS reader_name` 为读者姓名取别名，避免列名冲突。

- 创建后可直接 `select * from v_borrow_detail` 查询借阅明细，无需每次手写 `join`。

!!! tip "查询优化"
    当数据量达到百万级时，每次查询该视图的速度都很慢，可以通过在 borrow 表的 book_id 和 reader_id 上分别创建普通索引，并确保 book 表和 reader 表的主键索引已存在。

## 数据脱敏

数据脱敏是视图的一个重要应用场景。

根据《个人信息保护法》要求，管理员查询读者列表时，不应看到完整的身份证号和手机号，只需看到部分信息以便核对即可。因此需要通过视图对敏感字段进行脱敏处理。因此，可以使用以下代码对 `reader` 表进行脱敏处理：

```sql
create view v_reader_safe as
select 
  reader_id,
  name,
  concat(left(phone, 3), '****', right(phone, 4)) AS phone_masked,
  concat(left(id_card, 6), '****', right(id_card, 2)) AS id_card_masked,
  card_level,
  card_status
from reader;
```

- `create view v_reader_safe as` 创建脱敏视图，对外只暴露处理后的读者信息。

- `left(phone, 3)` 取手机号前 3 位，`right(phone, 4)` 取后 4 位；`concat(..., '****', ...)` 将中间替换为星号，如 `138****5678`。

- `id_card_masked` 同理，保留身份证前 6 位与后 2 位，中间用 `****` 遮盖。

- `reader_id`、`name`、`card_level`、`card_status` 等非敏感字段原样显示。

!!! tip "视图脱敏 vs. 应用层脱敏"
    - 视图脱敏在数据库层使用函数处理敏感字段，数据访问控制更强、一致性更好，但是输出是“掩码后的结果”，因此通用性受限，且可能影响查询与索引。

    - 应用层脱敏则通过应用程序从数据库查出完整数据后，在代码中对字段进行隐藏处理。

    当系统需要多客户端/多服务复用同一种安全展示规则、且希望把“敏感字段的保护”前移到数据库层以降低人为疏漏风险时，则视图脱敏最合适。

## 视图的性能风险

- 多表 JOIN 的重复开销：每次查询视图都会重新执行所有连接操作。例如 v_borrow_detail 涉及 borrow、book、reader 三表连接，即使只查一条记录，也可能需要扫描大量行才能完成连接。

- 聚合计算的实时重算：若视图中包含 GROUP BY、COUNT、SUM 等聚合，每次查询都会全量重新聚合。在高并发场景下，这会急剧消耗 CPU 和 I/O 资源。

- 嵌套视图的展开爆炸：视图嵌套视图时，MySQL 会逐层展开，可能生成包含大量派生表的复杂执行计划，导致索引失效、中间结果集膨胀。

- 无法利用缓存：视图查询结果不被缓存（除非使用应用层或查询缓存，但 MySQL 8.0 已移除查询缓存），相同查询的重复执行无法受益于中间结果复用。

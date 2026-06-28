---
date: 2026-06-28 23:12:44
title: SQL查询
permalink: select
publish: true
tags:
  - 数据库系统
---

## 查询

假设有表：

- `book.sql`

    ```sql
    SET NAMES utf8mb4;
    SET FOREIGN_KEY_CHECKS = 0;

    -- ----------------------------
    -- Table structure for book
    -- ----------------------------
    DROP TABLE IF EXISTS `book`;
    CREATE TABLE `book`  (
      `book_id` int NOT NULL AUTO_INCREMENT COMMENT '图书编号（唯一标识）',
      `book_name` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '书名',
      `isbn` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT 'ISBN号（国际标准书号）',
      `author` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '作者',
      `summary` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL COMMENT '简介',
      `publisher_id` int NULL DEFAULT NULL COMMENT '出版社编号（外键）',
      `state` tinyint(1) NOT NULL DEFAULT 0 COMMENT '状态：0-在馆，1-已借出',
      `shelf_location` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '书架位置（馆藏位置标识）',
      `price` decimal(10, 2) NULL DEFAULT NULL COMMENT '定价（单位：元）',
      `purchase_price` decimal(10, 2) NOT NULL DEFAULT 0.00 COMMENT '购入价（单位：元）',
      `storage_location` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '存储位置（如密集书库、备用库等）',
      `publish_date` date NULL DEFAULT NULL COMMENT '出版日期',
      `entry_date` date NOT NULL COMMENT '入库日期',
      PRIMARY KEY (`book_id`) USING BTREE,
      INDEX `idx_book_name`(`book_name`) USING BTREE,
      INDEX `idx_author`(`author`) USING BTREE,
      INDEX `fk_book_publisher`(`publisher_id`) USING BTREE,
      CONSTRAINT `fk_book_publisher` FOREIGN KEY (`publisher_id`) REFERENCES `publisher` (`publisher_id`) ON DELETE RESTRICT ON UPDATE CASCADE
    ) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '图书信息表' ROW_FORMAT = Dynamic;

    -- ----------------------------
    -- Records of book
    -- ----------------------------
    .....
    ```

- `borrow.sql`

    ```sql
    SET NAMES utf8mb4;
    SET FOREIGN_KEY_CHECKS = 0;

    -- ----------------------------
    -- Table structure for borrow
    -- ----------------------------
    DROP TABLE IF EXISTS `borrow`;
    CREATE TABLE `borrow`  (
      `borrow_id` int NOT NULL AUTO_INCREMENT COMMENT '借阅编号（主键）',
      `book_id` int NOT NULL COMMENT '图书编号（外键）',
      `reader_id` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '借书证号（外键）',
      `borrow_date` date NOT NULL COMMENT '借出日期',
      `due_date` date NOT NULL COMMENT '应还书日期',
      `actual_return_date` date NULL DEFAULT NULL COMMENT '实际归还日期（NULL表示未还）',
      PRIMARY KEY (`borrow_id`) USING BTREE,
      INDEX `reader_id`(`reader_id`) USING BTREE,
      INDEX `idx_borrow_date`(`borrow_date`) USING BTREE,
      INDEX `idx_overdue`(`due_date`, `actual_return_date`) USING BTREE,
      INDEX `idx_book_reader`(`book_id`, `reader_id`) USING BTREE,
      CONSTRAINT `borrow_ibfk_1` FOREIGN KEY (`book_id`) REFERENCES `book` (`book_id`) ON DELETE RESTRICT ON UPDATE CASCADE,
      CONSTRAINT `borrow_ibfk_2` FOREIGN KEY (`reader_id`) REFERENCES `reader` (`reader_id`) ON DELETE RESTRICT ON UPDATE CASCADE
    ) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '借阅信息表' ROW_FORMAT = Dynamic;

    -- ----------------------------
    -- Records of borrow
    -- ----------------------------
    .....
    ```

- `reader.sql`

    ```sql
    SET NAMES utf8mb4;
    SET FOREIGN_KEY_CHECKS = 0;

    -- ----------------------------
    -- Table structure for reader
    -- ----------------------------
    DROP TABLE IF EXISTS `reader`;
    CREATE TABLE `reader`  (
      `reader_id` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '借书证号（主键）',
      `name` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '姓名',
      `gender` char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '性别：M-男，F-女',
      `phone` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '电话号码',
      `id_card` varchar(18) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '身份证号（唯一）',
      `card_level` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT '普通' COMMENT '借书证等级（如普通、高级、VIP）',
      `card_date` date NOT NULL COMMENT '办卡日期',
      `card_status` tinyint(1) NOT NULL DEFAULT 0 COMMENT '借书卡状态：0-正常，1-禁用',
      `max_borrow_limit` int NOT NULL DEFAULT 5 COMMENT '最大可借总数（根据等级设定）',
      PRIMARY KEY (`reader_id`) USING BTREE,
      UNIQUE INDEX `id_card`(`id_card`) USING BTREE,
      UNIQUE INDEX `idx_id_card`(`id_card`) USING BTREE,
      INDEX `idx_phone`(`phone`) USING BTREE
    ) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '读者信息表' ROW_FORMAT = Dynamic;

    -- ----------------------------
    -- Records of reader
    -- ----------------------------
    .....
    ```

### 简单按列查询

比如想要查询所有图书的图书编号和书名：

```sql
select book_id, book_name from book;
```

### 指定显示顺序

在上面例子的基础上要求*升序*排列查询结果：

```sql
select book_id, book_name from book order by book_id asc;
```

即使用字段 `order by` 显式指定排列顺序。

默认就是升序，若希望降序，则使用 `order by book_id desc`。

### 条件查询

#### `where` 字段

若希望查询当前在馆（state = 0）的图书，显示：书名、作者、书架位置，并按“入库日期”从新到旧排序，那么就需要先得到“当前在馆”的图书，并显示对应的列，最后降序：

```sql
select book_name, author, shelf_location from book where state = 0 order by entry_date desc;
```

#### 组合条件

在图书馆借阅系统中，需要定期检查哪些读者存在逾期未还的图书，以便进行催还或罚款处理。

若逾期未还定义为：当前日期（`CURDATE()`）已经超过了应还日期（`due_date`），并且该借阅记录尚未归还（`actual_return_date` 为 `NULL`）。现在希望从 [`borrow`](#查询) 表中筛选出所有逾期未还的完整借阅记录，并按逾期天数从大到小排序。其中，逾期天数的计算方法为 `DATEDIFF(CURDATE(), due_date)`。则可以使用以下代码：

```sql
select * from borrow
where due_date < curdate() and actual_return_date is null
order by datediff(curdate(), due_date) desc;
```

- `where due_date < curdate()` 筛选应还日期早于今天的记录，即已逾期。

- `and actual_return_date is null` 进一步限定尚未归还（实际归还日期为空）。

- `order by datediff(curdate(), due_date) desc` 按逾期天数降序排列，逾期最久的排在最前。

- `curdate()` 返回当前日期；`datediff(日期1, 日期2)` 计算两日期相差的天数。

#### 其他常用字段

- `limit`：限制查询结果的行数。`limit 50` 表示只返回前50行；`limit 10, 20` 表示从第11行开始返回20行。

- `offset`：跳过前几行。`offset 10` 表示跳过前10行。

- `offset` 和 `limit` 一起使用，可以实现分页查询。`limit 10 offset 20` 表示从第21行开始返回10行。

- `interval` 运算符：用于计算日期或时间间隔。`interval 1 day` 表示1天、`interval 1 hour` 表示1小时，以此类推。比如 `date_sub(curdate(), interval 1 day)` 表示当前1天前的日期。

- 聚合函数

    ![](assets/create/1.jpg)

- `like`：模糊匹配。`like '%张%'` 表示匹配包含“张”的任意字符串；`like '张%'` 表示匹配以“张”开头的任意字符串；`like '%张'` 表示匹配以“张”结尾的任意字符串。

- `_` 通配符：匹配单个任意字符。`like '张_'` 表示匹配以“张”开头，后面跟着一个任意字符的任意字符串。

### 连接查询

当所需信息分散在多个表中时，需要用**连接查询**（`JOIN`）按关联字段把行拼在一起。常见写法是在 `FROM` 后列出多张表，用 `ON` 指定连接条件；也可在 `WHERE` 中写等值条件（旧式写法，不推荐）。

![](assets/create/2.jpg)

!!! tip
    - 连接条件应写在 `ON` 中；`WHERE` 用于对连接后的结果进一步过滤。

    - 多表存在同名列时，必须用 `表名.列名` 或别名限定，如 `bk.book_id`。

    - 连接字段最好有索引（如外键列），否则大表连接时性能会明显下降。

#### 内连接

**内连接**（`INNER JOIN`，可简写为 `JOIN`）只返回两表在连接条件上**都能匹配**的行，不匹配的行会被丢弃。

例如，查询每条借阅记录对应的书名和读者姓名，需要把 [`borrow`](#查询) 分别与 [`book`](#查询)、[`reader`](#查询) 关联：

```sql
select b.borrow_id, bk.book_name, r.name, b.borrow_date, b.due_date
from borrow b
inner join book bk on b.book_id = bk.book_id
inner join reader r on b.reader_id = r.reader_id;
```

- `b`、`bk`、`r` 是**表别名**，便于引用列并避免歧义。
- `on b.book_id = bk.book_id` 表示按图书编号关联借阅表与图书表。
- 若某本书从未被借出，或某位读者没有借阅记录，这些行不会出现在结果中。

#### 左连接

**左连接**（`LEFT JOIN`）保留**左表全部行**；右表找不到匹配时，右表列以 `NULL` 填充。

例如，列出所有图书及其借阅次数（含从未被借出的书）：

```sql
select bk.book_id, bk.book_name, count(br.borrow_id) as borrow_count
from book bk
left join borrow br on bk.book_id = br.book_id
group by bk.book_id, bk.book_name;
```

- 左表是 `book`，因此每本书至少出现一行。
- 从未被借出的书，`borrow_count` 为 `0`（`count(br.borrow_id)` 不计 `NULL`）。

又如，查询所有读者及其最近一次借阅日期（含从未借书的读者）：

```sql
select r.reader_id, r.name, max(br.borrow_date) as last_borrow_date
from reader r
left join borrow br on r.reader_id = br.reader_id
group by r.reader_id, r.name;
```

#### 右连接

**右连接**（`RIGHT JOIN`）与左连接对称：保留**右表全部行**，左表无匹配时填充 `NULL`。

```sql
select bk.book_name, br.borrow_date
from book bk
right join borrow br on bk.book_id = br.book_id;
```

效果上等价于把 `book` 与 `borrow` 的位置对调后写 `LEFT JOIN`。实际开发中更常用 `LEFT JOIN`，右连接较少见。

#### 全外连接

**全外连接**（`FULL OUTER JOIN`）返回两表所有行：能匹配的拼在一起，不能匹配的以 `NULL` 补全。MySQL **不直接支持** `FULL OUTER JOIN`，可用 `LEFT JOIN` 与 `RIGHT JOIN` 的 `UNION` 模拟：

```sql
select bk.book_id, bk.book_name, br.borrow_id
from book bk
left join borrow br on bk.book_id = br.book_id
union
select bk.book_id, bk.book_name, br.borrow_id
from book bk
right join borrow br on bk.book_id = br.book_id;
```

#### 多表连接与筛选

连接后仍可配合 `WHERE`、`ORDER BY` 等子句。例如，查询当前逾期未还记录及对应书名、读者姓名：

```sql
select br.borrow_id, bk.book_name, r.name,
       datediff(curdate(), br.due_date) as overdue_days
from borrow br
inner join book bk on br.book_id = bk.book_id
inner join reader r on br.reader_id = r.reader_id
where br.due_date < curdate() and br.actual_return_date is null
order by overdue_days desc;
```

### 参数化查询

参数化查询（Parameterized Query）是一种将 SQL 语句中的可变数据（如用户输入）用占位符代替，然后在执行时通过参数传递实际值的编程方式。这种方式可以防止恶意输入改变 SQL 语句的结构，从而有效避免 SQL 注入攻击。

## 插入数据

### 插入单行数据

```sql
insert into `book` (`book_name`, `author`, `publisher_id`, `state`, `shelf_location`, `price`, `purchase_price`, `storage_location`, `publish_date`, `entry_date`)
values ('MySQL教程', '张三', 1, 0, 'A1-101', 50.00, 40.00, '密集书库', '2026-01-01', '2026-01-01');
```

### 插入多行数据

```sql
insert into `book` (`book_name`, `author`, `publisher_id`, `state`, `shelf_location`, `price`, `purchase_price`, `storage_location`, `publish_date`, `entry_date`)
values ('MySQL教程', '张三', 1, 0, 'A1-101', 50.00, 40.00, '密集书库', '2026-01-01', '2026-01-01'),
('MySQL教程', '张三', 1, 0, 'A1-101', 50.00, 40.00, '密集书库', '2026-01-01', '2026-01-01'),
.....
('MySQL教程', '张三', 1, 0, 'A1-101', 50.00, 40.00, '密集书库', '2026-01-01', '2026-01-01');
```

## `explain`语句

`EXPLAIN` 用于查看 MySQL **如何执行**一条查询，包括是否走索引、预计扫描多少行等，是分析查询效率的常用手段。

### 对比示例

假设有以下建表代码：

- `book_info.sql`

    ```sql
    CREATE TABLE book_info (
      auto_id INT PRIMARY KEY AUTO_INCREMENT COMMENT '自增主键',
      id VARCHAR(10) NOT NULL COMMENT '图书业务ID',
      sn VARCHAR(13) COMMENT '序列号',
      isbn VARCHAR(13) COMMENT '国际标准书号',
      name VARCHAR(100) NOT NULL COMMENT '书名',
      price DECIMAL(10,2) COMMENT '价格',
      author VARCHAR(100) COMMENT '作者',
      cate_text VARCHAR(50) COMMENT '分类文本',
      market_price DECIMAL(10,2) COMMENT '市场价',
      has_stock TINYINT COMMENT '是否有库存（0/1）',
      cate_id INT COMMENT '分类ID',        
      cate_name VARCHAR(50) COMMENT '分类名称'
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='图书信息表';
    ```

- book_info2.sql

    ```sql
    CREATE TABLE book_info2 LIKE book_info;
    INSERT INTO book_info2 SELECT * FROM book_info;

    CREATE INDEX idx_name ON book_info(name);
    CREATE INDEX idx_author ON book_info(author);
    ```

分别运行这两段代码，得到两个表 `book_info` 和 `book_info2`（在表一的基础上创建并添加索引）。

`book_info` 在 `name` 列上建有索引，而 `book_info2` 没有：

```sql
explain select * from book_info where name = '纳兰容若词传';
explain select * from book_info2 where name = '纳兰容若词传';
```

两条语句的查询条件相同，但执行计划可能差异很大。

### 结果字段说明

| 字段 | 含义 |
| --- | --- |
| `type` | 访问类型，反映扫描方式。`ref` 表示通过索引查找；`ALL` 表示全表扫描 |
| `possible_keys` | 可能用到的索引 |
| `key` | 实际使用的索引；为 `NULL` 表示未使用索引 |
| `rows` | 预计扫描的行数。有索引时通常很小，全表扫描时接近表总行数 |
| `filtered` | 按 `WHERE` 条件过滤后，预计剩余行数占扫描行数的百分比，最大为 100 |
| `Extra` | 额外信息，如出现 `Using where` 表示在存储引擎返回结果后还需用条件进一步过滤 |

### 对比结论

- **`book_info`（有索引）**：`type` 通常为 `ref`，`key` 显示实际索引名，`rows` 较小。

- **`book_info2`（无索引）**：`type` 为 `ALL`，`key` 为 `NULL`，`rows` 接近全表行数。

索引能显著减少扫描行数，查询越快。编写或优化 `WHERE` 条件时，可用 `EXPLAIN` 检查是否真正使用了预期索引。


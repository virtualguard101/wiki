---
date: 2026-06-25 20:38:46
title: SQL函数与存储过程
permalink: sql-func-procedure
publish: true
tags:
  - 数据库系统
---

# 函数与存储过程

## 函数

**函数**接收输入、返回一个值，可在 `SELECT` 表达式中直接使用。MySQL 内置了大量**系统函数**，也支持编写**用户自定义函数**。

### 常用系统函数

#### 日期函数

| 函数 | 作用 | 示例 |
| --- | --- | --- |
| `CURDATE()` | 当前日期 | `CURDATE()` → `2026-06-25` |
| `NOW()` | 当前日期时间 | `NOW()` |
| `DATEDIFF(d1, d2)` | 两日期相差天数（`d1 - d2`） | `DATEDIFF('2026-06-25', '2026-01-01')` → `175` |
| `DATE_ADD(d, INTERVAL n DAY)` | 日期加 n 天 | `DATE_ADD(CURDATE(), INTERVAL 30 DAY)` |

查询尚未归还图书的借阅期限（天数）：

```sql
select reader_id, borrow_date, due_date,
    datediff(due_date, borrow_date) as borrow_days
from borrow
where actual_return_date is null;
```

#### 字符串函数

| 函数 | 作用 |
| --- | --- |
| `CONCAT(s1, s2, ...)` | 拼接字符串 |
| `LEFT(str, n)` / `RIGHT(str, n)` | 取左/右 n 个字符 |
| `LENGTH(str)` / `CHAR_LENGTH(str)` | 字节长度 / 字符个数 |
| `UPPER(str)` / `LOWER(str)` | 转大写 / 小写 |
| `REPEAT(str, n)` | 重复字符串 n 次 |

拼接读者信息、截取字段：

```sql
select concat(name, '(', reader_id, ')') as reader_info,
    length(id_card) as id_len,
    upper(left(name, 1)) as first_char
from reader limit 5;
```

`CONCAT` 也常用于**数据脱敏**，例如姓名只留首字、电话只显示前 3 位和后 4 位：

```sql
select
    concat(left(name, 1), repeat('*', char_length(name) - 1)) as masked_name,
    concat(left(phone, 3), '****', right(phone, 4)) as masked_phone
from reader;
```

#### 数学函数

| 函数 | 作用 | 示例 |
| --- | --- | --- |
| `ROUND(x, d)` | 四舍五入到 d 位小数 | `ROUND(3.1415, 2)` → `3.14` |
| `CEIL(x)` / `FLOOR(x)` | 向上 / 向下取整 | `CEIL(2.3)` → `3` |
| `ABS(x)` | 绝对值 | `ABS(-5)` → `5` |

计算逾期罚金时，可用 `DATEDIFF` 得到天数，再乘以单价；需要保留两位小数时用 `ROUND`：

```sql
select borrow_id,
    round(datediff(curdate(), due_date) * 0.2, 2) as fine_preview
from borrow
where actual_return_date is null and due_date < curdate();
```

#### 加密函数

`SHA2(str, len)` 计算 SHA-2 哈希值，`len` 可取 `224`、`256`、`384`、`512`。密码不应明文存储，入库时计算哈希，登录时用相同算法比较：

```sql
-- SHA-256 结果为 64 位十六进制，password_hash 列需至少 CHAR(64)
alter table login modify password_hash char(64) null comment '密码哈希';

insert into login (user_id, phone, password_hash, state, last_login_time)
values ('R20240001', '13812345678', sha2('SecPasswd123', 256), 0, now());

select * from login
where user_id = 'R20240001' and password_hash = sha2('SecPasswd123', 256);
```

列类型修改见[建表笔记中的 `ALTER`](SQL操作要点-建表.md#修改表结构)。

### 用户自定义函数

当系统函数无法满足需求时，可编写**用户自定义函数**（UDF），把常用计算逻辑封装起来复用。

### 创建函数

以根据借书证号查询电话为例：

```sql
delimiter $$
drop function if exists get_reader_phone$$
create function get_reader_phone(p_reader_id varchar(20) character set utf8mb4 collate utf8mb4_0900_ai_ci)
returns varchar(15)
reads sql data
begin
    declare v_phone varchar(15);
    select phone into v_phone from reader where reader_id = p_reader_id;
    return v_phone;
end$$
delimiter ;

select get_reader_phone('R20240011');
```

再写一个返回办卡日期的函数：

```sql
delimiter $$
drop function if exists get_reader_card_date$$
create function get_reader_card_date(p_reader_id varchar(20) character set utf8mb4 collate utf8mb4_0900_ai_ci)
returns date
reads sql data
begin
    declare v_card_date date;
    select card_date into v_card_date from reader where reader_id = p_reader_id;
    return v_card_date;
end$$
delimiter ;

select get_reader_card_date('R20240011');
```

- `RETURNS`：声明返回值类型。

- `READS SQL DATA`：声明函数只读取数据、不修改数据（MySQL 创建函数时的特性声明）。

- `DECLARE`：声明局部变量；`SELECT ... INTO` 把查询结果赋给变量。

- `RETURN`：返回结果。

!!! tip "`DELIMITER` 指令"
    `DELIMITER` 是 **MySQL 客户端指令**（不是标准 SQL），用于临时修改语句结束符。

    函数体内部含有多个 `;`，若仍用 `;` 作结束符，客户端会在第一个 `;` 处截断语句。因此：

    1. `delimiter $$`：把结束符改为 `$$`

    2. `drop function ...$$`、`create function ... end$$`：每条语句都以 `$$` 结束

    3. `delimiter ;`：恢复默认结束符

    在 Python、JDBC 等程序中提交函数定义时，通常**不需要**写 `DELIMITER`，直接整段发送即可。

!!! warning "排序规则（collation）需与表列一致"
    若函数参数与表列比较时报错：

    ```
    Illegal mix of collations (utf8mb4_0900_ai_ci,IMPLICIT) and (utf8mb4_general_ci,IMPLICIT)
    ```

    说明参数默认 collation 与表列不同。应在参数上显式指定与表列相同的 collation，例如：

    ```sql
    p_reader_id varchar(20) character set utf8mb4 collate utf8mb4_0900_ai_ci
    ```

### 在 Python 中调用函数

```python
import pymysql

conn = pymysql.connect(
    host='localhost',
    user='root',
    password='123456',
    database='libraryDB',
)
cursor = conn.cursor()
reader_id = 'R20240011'
cursor.execute(f"SELECT get_reader_card_date('{reader_id}')")
result = cursor.fetchone()[0]
print(result)  # 如 2024-01-20
cursor.close()
conn.close()
```

---

# 存储过程

默认情况下，MySQL 禁止函数执行会修改数据的 SQL 语句。如果函数内部包含 `INSERT`、`UPDATE`、`DELETE` 等语句，创建时会报错（除非设置了 `log_bin_trust_function_creators=1`，但即使创建成功，执行时也可能产生警告或错误）。这是为了保持函数的「纯粹性」，确保在 SQL 表达式中调用函数不会产生副作用。

如果需要对数据库进行修改操作（更新、插入、删除），或者批量处理，应使用**存储过程（`PROCEDURE`）**。

函数可以在 SQL 语句中用 `SELECT` 直接调用，而存储过程必须使用 `CALL` 调用。

## 创建存储过程

创建存储过程的语法与创建函数类似，但使用 `PROCEDURE` 关键字，且无需 `RETURNS` 子句。参数可用 `IN`（输入）、`OUT`（输出）、`INOUT`（输入输出）修饰。

### 示例一：按姓名模糊查询读者（返回结果集）

```sql
delimiter $$
drop procedure if exists get_reader_by_name$$
create procedure get_reader_by_name(in p_name varchar(20) character set utf8mb4 collate utf8mb4_0900_ai_ci)
begin
    select
        reader_id,
        name,
        concat(left(phone, 3), '****', right(phone, 4)) as phone,
        concat(left(id_card, 6), '****', right(id_card, 2)) as id_card
    from reader
    where name like concat('%', p_name, '%')
    limit 20;
end$$
delimiter ;

call get_reader_by_name('张');
```

### 示例二：批量更新逾期罚金

业务规则：

1. 未归还且已逾期：罚金 = 逾期天数 × 0.2 元/天
2. 已归还且逾期：罚金 = 逾期天数 × 0.2 元/天
3. 其他情况：罚金为 0

```sql
alter table borrow
add column fine_amount decimal(10, 2) not null default 0.00 comment '逾期罚金（元）';
```

存储过程：

```sql
delimiter $$
drop procedure if exists update_borrow_fine$$
create procedure update_borrow_fine()
begin
    -- 情况1：未归还且已逾期
    update borrow
    set fine_amount = datediff(curdate(), due_date) * 0.2
    where actual_return_date is null
      and due_date < curdate();

    -- 情况2：已归还且逾期
    update borrow
    set fine_amount = datediff(actual_return_date, due_date) * 0.2
    where actual_return_date is not null
      and actual_return_date > due_date;

    -- 情况3：未逾期，罚金置 0
    update borrow
    set fine_amount = 0.00
    where (actual_return_date is not null and actual_return_date <= due_date)
       or (actual_return_date is null and due_date >= curdate());
end$$
delimiter ;

call update_borrow_fine();
```

查看有罚金的记录：

```sql
select borrow_id, reader_id, due_date, actual_return_date, fine_amount
from borrow
where fine_amount > 0;
```

## 调用与管理

```sql
-- 调用存储过程
call get_reader_by_name('张');
call update_borrow_fine();

-- 查看已有存储过程
show procedure status where db = 'libraryDB';

-- 查看定义
show create procedure get_reader_by_name;

-- 删除
drop procedure if exists get_reader_by_name;
```

## 函数与存储过程的区别

| | 自定义函数 | 存储过程 |
| --- | --- | --- |
| 调用方式 | `SELECT get_reader_phone('R20240011')` | `CALL get_reader_by_name('张')` |
| 返回值 | 必须有 `RETURNS` | 无固定返回值，可返回结果集或用 `OUT` 参数 |
| 能否修改数据 | 默认禁止 `INSERT`/`UPDATE`/`DELETE` | 可以 |
| 典型用途 | 在查询中计算一个值 | 多步业务逻辑、批量更新 |

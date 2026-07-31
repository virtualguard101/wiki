---
date: 2026-06-29 01:53:50
title: SQL触发器与事件调度
permalink: trigger
publish: true
tags:
  - 数据库系统
---

# 触发器与事件调度

**触发器**（Trigger）在特定表发生 `INSERT`、`UPDATE` 或 `DELETE` 时**自动执行**一段 SQL，常用于维护关联数据、写入审计日志等。

**事件调度器**（Event Scheduler）则按预定时间**周期性或一次性**执行 SQL，类似数据库内置的定时任务（可类比Linux的[cron](../Tools/linux/Linux定时任务.md)）。

---

## 触发器

### 概念

触发器绑定在某张表上，当满足触发时机的事件发生时，DBMS 自动调用触发器体中的语句，**无需应用层显式调用**。

典型的应用场景：

- 借书时自动把图书状态改为“已借出”，还书时改回“在馆”

- 插入/修改/删除前做合法性校验（如借书数量上限）

- 记录数据变更历史到审计表

!!! warning "慎用触发器"
    触发器逻辑隐藏在数据库内部，调试和排查问题较困难；多表、多层触发器还可能引发连锁更新。能在应用层清晰表达的业务规则，优先放在应用代码中；确需保证“无论谁改表都生效”时，再考虑触发器。

### 语法要点

```sql
create trigger 触发器名
{ before | after } { insert | update | delete }
on 表名 for each row
触发器体;
```

| 要素 | 说明 |
| --- | --- |
| `BEFORE` / `AFTER` | 在语句**执行前**还是**执行后**触发 |
| `INSERT` / `UPDATE` / `DELETE` | 监听的操作类型 |
| `FOR EACH ROW` | 行级触发器：受影响每一行执行一次（MySQL 仅支持行级） |
| `NEW` | 插入或更新后的新行（`INSERT`、`UPDATE` 可用） |
| `OLD` | 更新或删除前的旧行（`UPDATE`、`DELETE` 可用） |

同一表、同一时机、同一事件类型**只能有一个**触发器。例如不能有两个 `BEFORE INSERT ON borrow`。

### 应用案例

#### 借书时更新图书状态

业务规则：新增借阅记录时，将对应图书的 `state` 设为 `1`（已借出）。

```sql
delimiter $$
drop trigger if exists tr_borrow_insert$$
create trigger tr_borrow_insert
after insert on borrow
for each row
begin
    update book set state = 1 where book_id = new.book_id;
end$$
delimiter ;
```

插入借阅记录后，触发器自动执行：

```sql
insert into borrow (book_id, reader_id, borrow_date, due_date)
values (1001, 'R20240011', curdate(), date_add(curdate(), interval 30 day));
```

#### 还书时恢复图书状态

业务规则：当 `actual_return_date` 从 `NULL` 变为非空时，把图书 `state` 改回 `0`（在馆）。

```sql
delimiter $$
drop trigger if exists tr_borrow_return$$
create trigger tr_borrow_return
after update on borrow
for each row
begin
    if old.actual_return_date is null and new.actual_return_date is not null then
        update book set state = 0 where book_id = new.book_id;
    end if;
end$$
delimiter ;
```

- `OLD` / `NEW` 区分更新前后的行。

- 用 `IF` 限定仅在“完成还书”时更新，避免修改其他字段时误触发。

#### 借书前校验可借数量

业务规则：读者当前未还图书数不得超过 `max_borrow_limit`。可在**插入借阅记录之前**检查，不满足则中断操作：

```sql
delimiter $$
drop trigger if exists tr_borrow_check_limit$$
create trigger tr_borrow_check_limit
before insert on borrow
for each row
begin
    declare v_current int;
    select count(*) into v_current
    from borrow
    where reader_id = new.reader_id and actual_return_date is null;
    if v_current >= (
        select max_borrow_limit from reader where reader_id = new.reader_id
    ) then
        signal sqlstate '45000'
            set message_text = '已达最大借阅数量，无法继续借书';
    end if;
end$$
delimiter ;
```

- `BEFORE INSERT` 在记录写入前执行；`SIGNAL` 抛出错误，整个 `INSERT` 失败。

- 应用层也应做同样校验，触发器作为数据库侧的**最后一道防线**。

### 查看与管理

```sql
-- 查看当前库的触发器
show triggers from libraryDB;

-- 查看定义
show create trigger tr_borrow_insert;

-- 删除
drop trigger if exists tr_borrow_insert;
```

---

## 事件调度器

### 概念

**事件**（Event）在指定时间**执行一次**，或按固定间隔**重复执行**预定义的 SQL常配合[存储过程](SQL操作要点-函数与存储过程.md#存储过程)处理复杂逻辑。

时间调度器典型的应用场景：

- 每天凌晨批量更新逾期罚金

- 定期清理过期临时数据

- 定时生成统计快照

事件由 MySQL **事件调度器**线程驱动；默认可能未开启，需显式启用。

### 启用调度器

```sql
-- 查看是否开启（ON / OFF）
show variables like 'event_scheduler';

-- 当前会话或全局启用（需相应权限）
set global event_scheduler = on;
```

若重启后需保持开启，在 `my.cnf` 的 `[mysqld]` 段加入 `event_scheduler=ON`。

### 应用案例

#### 每天更新逾期罚金

[存储过程 `update_borrow_fine`](SQL操作要点-函数与存储过程.md#批量更新逾期罚金) 已实现罚金计算逻辑。可创建事件，每天凌晨 2 点自动调用：

```sql
drop event if exists ev_daily_update_fine;

create event ev_daily_update_fine
on schedule every 1 day
starts timestamp(current_date + interval 1 day) + interval 2 hour
on completion preserve
enable
comment '每日凌晨 2 点更新借阅逾期罚金'
do
    call update_borrow_fine();
```

| 子句 | 含义 |
| --- | --- |
| `EVERY 1 DAY` | 每 1 天执行一次 |
| `STARTS ...` | 首次执行时间（示例为次日 02:00） |
| `ON COMPLETION PRESERVE` | 事件执行完毕后保留定义（默认 `NOT PRESERVE` 会删除一次性事件） |
| `ENABLE` / `DISABLE` | 创建时即启用或禁用 |
| `DO` | 要执行的语句（单条 SQL 或 `BEGIN ... END` 块） |

#### 仅执行一次的任务

例如，在指定时间点执行一次性维护：

```sql
create event ev_one_time_archive
on schedule at '2026-07-01 03:00:00'
on completion not preserve
do
    delete from borrow
    where actual_return_date is not null
      and actual_return_date < date_sub(curdate(), interval 5 year);
```

- `AT '日期时间'`：只在该时刻执行一次。
- `ON COMPLETION NOT PRESERVE`：执行完成后自动删除事件定义。

#### 带条件的周期任务

每周一统计上周新增借阅数，写入统计表（需先建表）：

```sql
create table if not exists borrow_weekly_stats (
    stat_date date primary key comment '统计周起始日（周一）',
    borrow_count int not null comment '当周借阅次数'
);

delimiter $$
drop event if exists ev_weekly_borrow_stats$$
create event ev_weekly_borrow_stats
on schedule every 1 week
starts (current_date - interval weekday(current_date) day) + interval 1 week + interval 8 hour
on completion preserve
enable
comment '每周一 08:00 统计上周借阅量'
do
begin
    insert into borrow_weekly_stats (stat_date, borrow_count)
    select
        curdate() - interval weekday(curdate()) day - interval 7 day,
        count(*)
    from borrow
    where borrow_date >= curdate() - interval weekday(curdate()) day - interval 7 day
      and borrow_date < curdate() - interval weekday(curdate()) day
    on duplicate key update borrow_count = values(borrow_count);
end$$
delimiter ;
```

### 查看与管理

```sql
-- 查看事件列表
show events from libraryDB;

-- 查看定义
show create event ev_daily_update_fine;

-- 临时禁用 / 重新启用
alter event ev_daily_update_fine disable;
alter event ev_daily_update_fine enable;

-- 修改执行计划
alter event ev_daily_update_fine
on schedule every 1 day
starts current_timestamp + interval 1 day;

-- 删除
drop event if exists ev_daily_update_fine;
```

### 触发器与事件的区别

| | 触发器 | 事件 |
| --- | --- | --- |
| 触发方式 | 表上的 `INSERT`/`UPDATE`/`DELETE` | 时间表（`AT` / `EVERY`） |
| 是否需外部调用 | 否，随 DML 自动执行 | 否，由调度器按点执行 |
| 典型场景 | 行级联动、校验、审计 | 批处理、定时统计、清理 |
| 默认状态 | 创建后即生效 | 依赖 `event_scheduler` 为 `ON` |

两者都可与[存储过程](SQL操作要点-函数与存储过程.md#存储过程)配合：触发器/事件的 `DO` 或过程体中 `CALL` 过程，把复杂逻辑集中维护。

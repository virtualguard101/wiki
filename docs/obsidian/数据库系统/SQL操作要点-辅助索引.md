---
date: 2026-06-25 15:40:19
title: SQL辅助索引
permalink: view
publish: true
tags:
  - 数据库系统
---

# 辅助索引

## 什么是辅助索引

**辅助索引**（Secondary Index，又称二级索引）是在主键之外额外建立的索引。

- **主键索引**：决定数据的物理存储顺序，每张表只能有一个。

- **辅助索引**：维护「索引列值 → 主键值」的映射，使按非主键列查询时能快速定位行，而不必全表扫描。

在 InnoDB 中，辅助索引的叶子节点存的是主键值；找到主键后，还需回表到聚簇索引读取完整行（称为**回表**）。

## 创建辅助索引

### 何时创建

适合为以下列建辅助索引：

- 经常出现在 `WHERE`、`JOIN ON`、`ORDER BY` 中的列

- 区分度较高（不同值较多）的列——如书名、作者、ISBN

- 数据量较大、全表扫描代价明显的表

不宜盲目建索引：索引会占用额外存储，且 `INSERT` / `UPDATE` / `DELETE` 时需同步维护索引，写入会变慢。列区分度极低（如性别、是否上架）或很少用于查询的列，通常不必单独建索引。

### 基本语法

```sql
create index idx_<column_name> on <table_name>(<column_name>);
```

命名习惯：以 `idx_` 为前缀，后接列名，便于在 `EXPLAIN` 的 `key` 字段中识别。

### 示例

以 [`book_info`](SQL操作要点-查询.md#explain语句) 表为例，为书名和作者列分别建索引：

```sql
create index idx_name on book_info(name);

create index idx_author on book_info(author);
```

建好后，可用[`EXPLAIN`语句](SQL操作要点-查询.md#explain语句)验证查询是否走了索引。

## 复合索引

若查询条件经常同时涉及多列，可建**复合索引**（多列索引）：

```sql
create index idx_cate_author on book_info(cate_id, author);
```

复合索引遵循**最左前缀原则**：索引 `(cate_id, author)` 能加速 `WHERE cate_id = ?` 或 `WHERE cate_id = ? AND author = ?`，但单独 `WHERE author = ?` 通常用不上该索引。

!!! info "复合索引与B+树"
    复合索引之所以能够支持对索引中最左边一列或左边连续多列的查询，根本原因在于[B+树](../数据结构与算法/408/B树和B+树.md#B树的基本概念)的排序规则。

    复合索引的索引项是按照定义顺序进行排序的：

    - 首先按第一列（`cate_id`）排序；

    - 当第一列相同时，再按第二列（`author`）排序；

    - 以此类推。

    因此，所有索引项在逻辑上是有序的，形成一个类似于“先按作者分组，每组内再按分类排序”的结构。

## 查看与删除

```sql
-- 查看表上所有索引
show index from book_info;

-- 删除索引
drop index idx_name on book_info;
```

## 辅助索引对查询性能的影响

以在[查询](SQL操作要点-查询.md)中提到的 [`book_info`和`book_info2`](SQL操作要点-查询.md#explain语句) 为例，使用以下python脚本测试索引对查询性能的影响：

```python
import pymysql
import time


DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '123456',
    'database': 'libraryDB',
    'charset': 'utf8mb4'
}

BOOK_NAMES = ['数据结构（C语言版）', '纳兰容若词传', '汉字的战争', '成长']

def test_table(table_name: str) -> float:
    """对指定表依次查询4本书，返回总耗时（秒）"""
    conn = pymysql.connect(**DB_CONFIG)
    cursor = conn.cursor()
    start = time.perf_counter()
    for name in BOOK_NAMES:
        sql = f"SELECT * FROM {table_name} WHERE name = %s"
        cursor.execute(sql, (name,))
        rows = cursor.fetchall()
        # 可选：打印每个查询返回的行数（便于验证）
        print(f"  {name} -> {len(rows)} 行")
    elapsed = time.perf_counter() - start
    cursor.close()
    conn.close()
    return elapsed


def main():
    print("测试书名列表：")
    for name in BOOK_NAMES:
        print(f"  - {name}")
    print("\n--- 测试 book_info (有索引) ---")
    time_idx = test_table("book_info")
    print(f"总耗时: {time_idx:.6f} 秒")
    print("\n--- 测试 book_info2 (无索引) ---")
    time_no_idx = test_table("book_info2")
    print(f"总耗时: {time_no_idx:.6f} 秒")

    if time_no_idx > 0:
        print(f"\n性能对比：有索引比无索引快 {time_no_idx / time_idx:.2f} 倍")

if __name__ == "__main__":
    main()
```

在Linux系统下运行结果如下：

![](assets/view/1.png)

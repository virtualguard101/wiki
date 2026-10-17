---
date: 2026-09-15 10:32:09
title: MongoDB操作要点
permalink: mongodb-overview
publish: true
tags:
  - 数据库系统
---

# MongoDB操作要点

> [MongoDB Manual](https://www.mongodb.com/docs/manual/)
>
> [mongosh](https://www.mongodb.com/docs/mongodb-shell/)
>
> [Aggregation Pipeline](https://www.mongodb.com/docs/manual/core/aggregation-pipeline/)

对应 Wiki 里 [建表](SQL操作要点-建表.md) / [查询](SQL操作要点-查询.md) / [辅助索引](SQL操作要点-辅助索引.md) / [视图](SQL操作要点-视图.md) / [事务](SQL操作要点-事务管理与并发控制.md) 的 Mongo 一侧, 文档模型、CRUD、索引、聚合, 以及和 MySQL 并存时的一致性.

!!! info "示例环境"
    MongoDB 7 跑在 Docker Compose 里, 宿主端口 **27018** 映射到容器 27017, 已启用认证. MySQL 仍在本机 3306. 映射到 27018 是为了避开本机可能占用的默认 27017.

    两库**没有**跨引擎外键. 关联靠同名字段 (`user_id` / `course_id` / `enrollment_id` / `section_id`), 由应用层对齐.

| [SQL操作要点](SQL操作要点-建表.md) | 本文对应 |
| --- | --- |
| [登录 / 建库 / 建表](SQL操作要点-建表.md) | 连接、逻辑库、集合 |
| [查询 / 连接](SQL操作要点-查询.md) | `find`、投影、数组、`$lookup` |
| [辅助索引](SQL操作要点-辅助索引.md) | 单字段、复合、唯一、文本、TTL |
| [视图](SQL操作要点-视图.md) | 聚合管道 (按需物化; 示例未建 view) |
| [事务与锁](SQL操作要点-事务管理与并发控制.md) | 单文档原子性; 跨 MySQL 用 Outbox, 而不是 XA |

## MongoDB 与文档模型

**MongoDB**是面向文档的 DBMS. 数据按**BSON**文档存放, 默认不强制列结构, 和[关系模型](关系模型.md)里「先声明表结构再插行」不同. 在[逻辑模型](逻辑模型.md)的谱系里, 它更接近灵活的文档 / 对象侧, 而不是二维表.

可以按三层来记, 和 MySQL 大致对应:

| MongoDB | MySQL 近似 |
| --- | --- |
| 逻辑库 (Database) | 数据库 |
| **集合** (*Collection*) | 表 |
| **文档** (*Document*) | 一行, 但字段可嵌套、可多少不一 |

适合放进 Mongo 的, 通常是半结构化、嵌套、读时希望一次拿全的数据 (进度断点、嵌套评论、课件元数据). 需要行锁、外键、严格约束的 (选课容量、余额、加密成绩) 仍放 MySQL.

## 登录

[建表](SQL操作要点-建表.md#登录数据库管理系统)一侧用 `mysql -u root -p`. Mongo 一侧用交互式 Shell **mongosh**. 示例不依赖本机 PATH 里的 `mongosh`, 而是进容器执行:

```bash
docker compose exec mongodb mongosh -u edu_mongo -p EduMongo@2026Strong --authenticationDatabase edu_platform edu_platform
```

本机 Compass / `mongosh` 用 URI. 密码里的 `@` 必须写成 `%40`, 否则 URI 解析会把用户名和主机拆错:

```bash
mongodb://edu_mongo:EduMongo%402026Strong@localhost:27018/edu_platform?authSource=edu_platform
```

- `-u` / `-p`: 用户名与密码.

- `--authenticationDatabase edu_platform`: **认证库**. 用户存在哪个库, 登录就填哪个. 业务用户建在 `edu_platform` 上, 不能填 `admin` (`mongoAdmin` 才在 `admin`).

- 命令末尾的 `edu_platform`: 登录后的默认逻辑库, 相当于 MySQL 的 `USE edu_platform`.

成功后可查看逻辑库与集合:

```javascript
show dbs
db.getName()
show collections
db.getCollectionNames()
```

`show dbs` 只列出**已有数据**的库; 空库可能不出现, 用 `db.getSiblingDB('edu_platform')` 仍可切换过去.

## 建库

MongoDB 没有必须先执行的 `CREATE DATABASE`. 向某逻辑库写入第一份数据时, 库会被创建.

```javascript
const edu = db.getSiblingDB('edu_platform');
```

- `getSiblingDB`: 在当前连接上切换逻辑库, 不必断开重连.

- 逻辑库名示例与 MySQL 相同, 都叫 `edu_platform`, 只是引擎不同, 不要理解成「同一个物理库」.

!!! warning
    删除逻辑库不可回滚: `db.dropDatabase()` 会删掉当前库的集合与数据, 和 MySQL 的 [`DROP DATABASE`](SQL操作要点-建表.md#删库) 一样没有事务保护. 生产环境权限应只授业务库的 `readWrite`, 不要把 `dropDatabase` 交给应用账号. 示例业务用户 `edu_mongo` 只有 `edu_platform` 的读写.

## 集合

**集合** (*Collection*) 对应 MySQL 的表, 但**默认无固定列结构**. 同一集合里, 文档字段可以多少不一. 约束主要靠应用层; 需要服务端校验时, 可以给集合加可选的 **JSON Schema validator** (一份 JSON Schema, 插入 / 更新时按它检查文档形状, 类似弱化版的列约束 + `CHECK`).

### 显式创建

```javascript
const edu = db.getSiblingDB('edu_platform');

edu.createCollection('learning_progress');
edu.createCollection('discussion_posts');
edu.createCollection('course_materials');
```

示例脚本 `mongodb/01_init_collections.js` 会先判断集合是否已存在, 再 `createCollection`, 避免重复执行报错.

### 隐式创建

第一次 `insertOne` / `insertMany` 时, 若集合不存在会自动建集合. 索引则不会按业务语义自动建好, 仍应显式 `createIndex`.

### 集合 vs 表

| | MySQL 表 | MongoDB 集合 |
| --- | --- | --- |
| 结构 | 建表时声明列、类型、NULL、默认值 | 默认可变; 每份文档自己带字段 |
| 主键 | `PRIMARY KEY` | 每份文档必有 `_id` (默认 ObjectId) |
| 外键 | `FOREIGN KEY` | 无跨集合外键; 用同名字段引用 |
| 改结构 | [`ALTER TABLE`](SQL操作要点-建表.md#修改表结构) | 一般不改「表结构」, 而是更新文档字段 |

示例把「半结构化、嵌套、高频写」放进 Mongo: 视频元数据、学习进度断点、嵌套评论、通知、考试快照、评价、作业附件. 选课容量、余额、加密成绩仍在 MySQL.

## 文档

### BSON 与 `_id`

**文档**是 **BSON** (*Binary JSON*): 外表像 JSON, 实际是二进制编码, 额外支持 `Date`、`ObjectId`、二进制等类型. 不要把日期存成字符串, 否则 TTL、按时间排序会失效.

每份文档必须有 `_id`. 不指定时, 驱动会生成 **ObjectId** (12 字节, 含时间戳, 集合内唯一), 相当于表的主键, 但**不是**跨库关联键.

### 嵌入 vs 引用

文档可以嵌套子文档和数组. 两种组织方式:

- **嵌入** (*embedding*): 把相关数据写进同一份文档, 一次 `find` 拿全. 适合「总是一起读、一起改」且体积可控的树, 比如帖子下的评论.

- **引用** (*referencing*): 只存对方的 id (示例里常是与 MySQL 相同的整型业务键). 适合跨集合、跨引擎, 或子文档会无限增长的情况.

选择嵌入而不是多表自连接: 评论层级不固定, [关系模型](关系模型.md) 要多次 [JOIN](SQL操作要点-查询.md#连接查询); 嵌套数组一次 `find` 就能拿到帖子树. 代价是单文档不能无限涨 (BSON 文档上限 16 MB), 示例规模足够.

### 示例

示例核心文档是学习进度, 一份选课对应一份进度 (与 MySQL `enrollments.enrollment_id` 一对一):

```javascript
db.learning_progress.insertOne({
  enrollment_id: 1001,
  user_id: 15,
  course_id: 2,
  sections: [
    { section_id: 11, watched_sec: 320, completed: false, last_position_sec: 320 }
  ],
  overall_percent: 12,
  updated_at: new Date()
});
```

- `enrollment_id`: 跨库关联键, 不是 Mongo 主键. 主键仍是 `_id`.

- `sections`: 数组内嵌小节断点. 断点续学按选课一次读出, 避免把每小节拆成多张 MySQL 进度表再 JOIN.

课件把视频、字幕、PDF 嵌在同一文档里 (一次读取):

```javascript
db.course_materials.insertOne({
  course_id: 1,
  section_id: 1,
  type: 'video',
  title: 'C1-S1',
  video: {
    resolution: '1080p',
    duration_sec: 600,
    url: 'https://cdn.example.com/c1/s1.mp4',
    signed_url_ttl_sec: 600
  },
  subtitle_path: '/subs/c1_s1.vtt',
  materials: [
    { kind: 'pdf', title: '课件', path: '/pdf/c1_s1.pdf' }
  ],
  created_at: new Date()
});
```

`video.url` 库中存模板地址; 短签防盗链在业务层签发, 字段 `signed_url_ttl_sec` 只记录建议 TTL.

嵌套评论示例 (讨论区):

```javascript
db.discussion_posts.insertOne({
  course_id: 1,
  user_id: 20,
  title: '事务隔离级别',
  content: '关于隔离级别的讨论, 关键词: 事务 索引 安全',
  parent_id: null,
  comments: [
    {
      comment_id: 'c1',
      user_id: 21,
      content: '回复 1',
      created_at: new Date(),
      replies: [
        { comment_id: 'c1_1', user_id: 20, content: '嵌套回复', created_at: new Date() }
      ]
    }
  ],
  like_count: 0,
  created_at: new Date()
});
```

## 增删改

对应 SQL 的 `INSERT` / `UPDATE` / `DELETE` ([查询](SQL操作要点-查询.md#插入数据) 一文里也写了插入).

### 插入

```javascript
db.notifications.insertOne({
  user_id: 10,
  type: 'system',
  title: '选课成功',
  body: '已选中数据库原理',
  read: false,
  created_at: new Date()
});

db.notifications.insertMany([
  { user_id: 10, type: 'announce', title: '公告 1', body: '...', read: false, created_at: new Date() },
  { user_id: 10, type: 'dm', title: '私信', body: '...', read: false, created_at: new Date() }
]);
```

`insertMany` 默认有序: 中途失败则后面的不再插入. 种子脚本 `mongodb/03_seed.js` 用 `insertMany` 灌课件、进度、讨论等.

### 更新

按 `enrollment_id` 更新断点. 点运算符写嵌套字段; `sections.$` 是**位置运算符**, 表示「查询条件命中的那一个数组元素」:

```javascript
db.learning_progress.updateOne(
  { enrollment_id: 1001, 'sections.section_id': 11 },
  {
    $set: {
      'sections.$.watched_sec': 400,
      'sections.$.last_position_sec': 400,
      updated_at: new Date()
    }
  }
);
```

- `$set`: 只改列出的字段, 其余保留.

- `sections.$`: 匹配到数组中满足查询条件的那一个元素.

选课同步进度时, 可使用**upsert** (*update + insert*): 有则覆盖, 无则插入, 保证 Outbox 重试不产生第二份进度文档:

```javascript
db.learning_progress.updateOne(
  { enrollment_id: 1001 },
  {
    $set: {
      enrollment_id: 1001,
      user_id: 15,
      course_id: 2,
      sections: [],
      overall_percent: 0,
      updated_at: new Date()
    }
  },
  { upsert: true }
);
```

Python 中对应 `python/enroll_cross_db.py` 的 `update_one(..., upsert=True)`. MySQL 里没有这一条「按关联键幂等写入」的单语句等价物, 通常要先 `SELECT` 再 `INSERT` / `UPDATE`, 或依赖唯一键冲突.

```javascript
db.notifications.updateMany(
  { user_id: 10, read: false },
  { $set: { read: true } }
);
```

### 删除

```javascript
db.learning_behavior_logs.deleteMany({ user_id: 10 });
db.course_materials.deleteOne({ course_id: 1, section_id: 1 });
```

初始化脚本里用 `_demo: true` 插入样例再 `deleteMany({ _demo: true })`, 避免把说明用文档留在业务集合里.

!!! warning
    `deleteMany({})` 会清空整个集合. 种子脚本开头对多个集合 `deleteMany({})` 仅用于示例重灌, 生产禁止对业务集合裸跑空条件删除.

## 查询

对应 [SQL查询](SQL操作要点-查询.md)中的 `SELECT` / `WHERE` / `ORDER BY`.

### 简单查询

```javascript
db.learning_progress.find({ enrollment_id: 1001 })
db.notifications.find({ user_id: 10 }).sort({ created_at: -1 }).limit(8)
db.course_reviews.find({ course_id: 1 }).sort({ rating: -1 })
```

- `find` 返回**游标** (*cursor*), 在 `mongosh` 里会自动迭代打印; 在驱动里要自己遍历或转成列表.

- `sort({ created_at: -1 })`: `-1` 降序, `1` 升序.

- `limit(8)`: 对应 SQL `LIMIT 8`.

只取一条:

```javascript
db.learning_progress.findOne({ enrollment_id: 1001 })
```

### 投影

第二个参数指定返回哪些字段 (`0` 排除, `1` 包含). `_id` 默认返回, 不要时显式关掉. 对应 SQL 的「只 `SELECT` 需要的列」:

```javascript
db.learning_progress.find(
  { user_id: 10 },
  { enrollment_id: 1, overall_percent: 1, _id: 0 }
)
```

示例工作台拉进度百分比时只投这两列, 避免把整个 `sections` 数组拉到浏览器.

### 条件

```javascript
db.course_reviews.find({ course_id: 1, rating: { $gte: 4 } })
db.notifications.find({ user_id: 10, read: false })
db.learning_progress.find({ enrollment_id: { $in: [1001, 1002, 1003] } })
```

同一对象里并列的键是 **AND**; 需要 OR 时用 `$or: [ {...}, {...} ]`.

| 操作符 | 含义 | SQL 近似 |
| --- | --- | --- |
| `$eq` / 直接写值 | 等于 | `=` |
| `$gte` / `$lte` | 大于等于 / 小于等于 | `>=` / `<=` |
| `$in` | 属于集合 | `IN (...)` |
| `$ne` | 不等于 | `<>` |
| `$exists` | 字段是否存在 | 无直接对应 (文档模型里字段可缺) |

### 嵌套与数组

点号进入子文档; 数组里「只要有一个元素满足」即可匹配:

```javascript
db.course_materials.find({ 'video.resolution': '1080p' })
db.learning_progress.find({ 'sections.section_id': 11 })
```

### 计数

```javascript
db.learning_progress.countDocuments({ course_id: 2 })
db.discussion_posts.estimatedDocumentCount()
```

- `countDocuments`: 带条件、精确.

- `estimatedDocumentCount`: 走元数据, 快, 但不接受过滤条件. 工作台总览用估计值即可.

### 文本检索

讨论区在 `title`、`content`、`comments.content` 上建了**文本索引**后, 可用 `$text` 做关键词检索 (SQL 侧近似 `LIKE`, 但走倒排, 不是逐字符扫描):

```javascript
db.discussion_posts.find({ $text: { $search: '事务 索引' } })
```

!!! warning
    MongoDB 自带文本索引对中文几乎按单字 / 空白切, 不能当成专业搜索引擎. 示例只要求「有全文索引方案」; 答辩时说明这一局限. `default_language: 'none'` 是为了关掉英语词干, 避免把中文字段按英文停用词处理.

## 聚合与「连接」

Mongo 没有 MySQL 那种可更新 [视图](SQL操作要点-视图.md), 也没有跨引擎 `JOIN`. 集合之间用**聚合管道**; 跨 MySQL 的拼接放在应用层 (Flask / Python).

### 管道

**聚合管道** (*Aggregation Pipeline*) 是一串阶段: 上一阶段的输出是下一阶段的输入, 有点像 Unix 管道, 也像 `WHERE` → `GROUP BY` → `ORDER BY` 拆开写.

按课程统计评价均分:

```javascript
db.course_reviews.aggregate([
  { $match: { course_id: { $in: [1, 2, 3] } } },
  { $group: { _id: '$course_id', avg_rating: { $avg: '$rating' }, n: { $sum: 1 } } },
  { $sort: { avg_rating: -1 } }
])
```

- `$match`: 过滤, 对应 `WHERE`, 应尽量放在管道前部以便走索引.

- `$group`: 对应 `GROUP BY`. `_id` 是分组键; `'$rating'` 表示「取字段 `rating` 的值」.

- `$sort`: 对应 `ORDER BY`.

需要把这条管道存成可查询对象时, 才考虑 `createView`. 示例未建 Mongo 视图, 学生课表仍用 MySQL 视图 `v_student_courses`.

### `$lookup`

在同一 Mongo 库内按字段做类似 [左连接](SQL操作要点-查询.md#左连接) 的拼表. 示例进度与课件都在 Mongo 时可以用; **不能** `$lookup` MySQL 的 `courses` 表.

```javascript
db.learning_progress.aggregate([
  { $match: { user_id: 10 } },
  {
    $lookup: {
      from: 'course_materials',
      localField: 'course_id',
      foreignField: 'course_id',
      as: 'materials'
    }
  }
])
```

`as: 'materials'` 会在每份进度文档上多一个数组字段, 装匹配到的课件. 一对多时数组可有多份; 一对零时是空数组.

示例学生课表仍查 MySQL 视图 `v_student_courses`; 续学只按 `enrollment_id` 查 `learning_progress`. 两库结果由 `python/cross_db_report.py` 或演示工作台在内存里按 ID 对齐.

嵌套评论若不用嵌入、改成 `parent_id` 邻接表, 才需要 `$graphLookup` (沿引用递归). 示例主路径是嵌入数组, 一般不必递归.

## 索引

对应 [SQL辅助索引](SQL操作要点-辅助索引.md). Mongo 默认在 `_id` 上有唯一索引, 相当于主键索引; 业务查询要另建.

不宜盲目建索引: 占用空间, 且插入 / 更新要维护索引. 示例只为实际查询路径建.

### 基本语法

```javascript
db.collection.createIndex({ 字段: 1 })        // 1 升序, -1 降序
db.collection.getIndexes()
db.collection.dropIndex('索引名')
```

示例 `mongodb/02_indexes.js` 中的关键索引:

```javascript
const edu = db.getSiblingDB('edu_platform');

edu.learning_progress.createIndex({ enrollment_id: 1 }, { unique: true });
edu.learning_progress.createIndex({ user_id: 1, course_id: 1 });
edu.learning_progress.createIndex({ updated_at: -1 });

edu.course_materials.createIndex({ course_id: 1, section_id: 1 });
edu.course_materials.createIndex({ 'video.url': 1 });

edu.discussion_posts.createIndex({ course_id: 1, created_at: -1 });
edu.discussion_posts.createIndex(
  { title: 'text', content: 'text', 'comments.content': 'text' },
  { name: 'idx_discussion_fulltext', default_language: 'none' }
);

edu.notifications.createIndex({ user_id: 1, created_at: -1 });
edu.notifications.createIndex({ user_id: 1, read: 1 });

edu.assignment_attachments.createIndex({ enrollment_id: 1, uploaded_at: -1 });
edu.assignment_attachments.createIndex({ expire_at: 1 }, { expireAfterSeconds: 0 });
```

- `unique: true`: `enrollment_id` 与 MySQL 选课一对一, 重复插入会报错; 配合 upsert 保证重试幂等.

- `{ course_id: 1, created_at: -1 }`: **复合索引**. 按课程拉帖子并按时间倒序, 符合[最左前缀](SQL操作要点-辅助索引.md#复合索引) —— 先等值 `course_id`, 再排序 `created_at`.

- 点号 `'video.url'`: 对嵌套字段建索引.

- `{ expire_at: 1 }, { expireAfterSeconds: 0 }`: **TTL 索引** (*Time To Live*). 后台线程按文档里的时间字段删除过期文档. `0` 表示以字段时间为准, 不再额外加秒. 示例用来清理作业附件元数据.

复合索引 `{ user_id: 1, course_id: 1 }` 能加速:

- `{ user_id: 10 }`

- `{ user_id: 10, course_id: 2 }`

单独 `{ course_id: 2 }` 通常用不上该索引 (没有最左的 `user_id`). 这与 MySQL 复合索引同一原则.

### 查看是否走索引

对应 SQL 的 [`EXPLAIN`](SQL操作要点-查询.md#explain语句):

```javascript
db.learning_progress.find({ enrollment_id: 1001 }).explain('executionStats')
```

关注 `winningPlan.stage`: `IXSCAN` 表示走索引, `COLLSCAN` 表示集合扫描 (类似 MySQL `EXPLAIN` 里的 `ALL`). `executionStats.totalDocsExamined` 过大说明条件没落到索引上.

## 用户与权限

Compose 首次空 volume 时会建两个用户:

- `mongoAdmin` (认证库 `admin`): 管理用户, 对应 MySQL 的 `root` 一类

- `edu_mongo` (`edu_platform.readWrite`): 应用 / Compass / pymongo

手工环境备用脚本: `mongodb/00_security_users.js`. 业务程序不要用 `mongoAdmin`.

```javascript
use edu_platform
db.getUsers()
```

对应 MySQL 的 `edu_app` / `edu_readonly` / `edu_backup` 分权: Mongo 侧应用账号只授一个库的读写.

## 事务与跨库一致性

对应 [SQL事务管理与并发控制](SQL操作要点-事务管理与并发控制.md). 先分清三件事: 单文档原子、同库多文档事务、跨 MySQL 的最终一致. 示例真正用到的是第一件和第三件.

### 单文档原子性

一次 `updateOne` / `findOneAndUpdate` 对**同一文档**是原子的. 更新 `sections.$` 某个小节断点, 不会出现「只写了一半字段」的中间态. 这是文档模型的默认承诺, 不依赖事务 API.

示例进度、通知、评价都按文档粒度更新, 一般不需要多文档事务.

### 多文档事务

Mongo 4+ 支持会话内多文档事务, 语义接近 InnoDB 的 `START TRANSACTION` ... `COMMIT`. 前提是**副本集** (*replica set*, 多节点复制; 单机也可配成单节点副本集) 或分片集群. 独立 `standalone` 进程上这段代码会失败.

```javascript
const session = db.getMongo().startSession();
session.startTransaction();
try {
  const edu = session.getDatabase('edu_platform');
  edu.learning_progress.updateOne({ enrollment_id: 1001 }, { $set: { overall_percent: 50 } });
  edu.notifications.insertOne({ user_id: 15, title: '进度更新', created_at: new Date() });
  session.commitTransaction();
} catch (e) {
  session.abortTransaction();
  throw e;
} finally {
  session.endSession();
}
```

示例**没有**把选课容量扣减放到这段事务里: 容量在 MySQL `sp_enroll_student` 的 [`FOR UPDATE`](SQL操作要点-事务管理与并发控制.md#行级锁) 里完成.

### 跨 MySQL 没有 XA

**XA** 是两阶段提交的分布式事务协议, 要求所有参与者都实现同一套 prepare / commit. 无法在一个 `commit` 里同时提交 InnoDB 与 MongoDB.

示例用 **Outbox** (事务性发件箱): 先在 MySQL 事务里把「待同步」写成一行, 提交成功后再写 Mongo; 失败可按这行重试. 这是**最终一致**, 不是跨引擎 [ACID](SQL操作要点-事务管理与并发控制.md#事务的-ACID-特性).

```mermaid
sequenceDiagram
    participant App as 应用
    participant MySQL
    participant Mongo

    App->>MySQL: 行锁校验容量, 写 enrollments
    App->>MySQL: 写 Outbox PENDING
    MySQL-->>App: COMMIT
    App->>Mongo: upsert learning_progress
    App->>MySQL: 回写 mongo_progress_id, Outbox COMPLETED
```

步骤展开:

1. MySQL 事务内: 行锁校验容量 → 写 `enrollments` → 写 `cross_db_sync_tasks(PENDING)` → `COMMIT`

2. 应用层按 `enrollment_id` upsert `learning_progress`

3. 回写 `enrollments.mongo_progress_id`, Outbox 标 `COMPLETED`

4. 失败则标 `FAILED`, `python/retry_cross_db.py` 重试

候补 (`候补中`) 不写 Mongo 进度. 题目里的「跨库事务」在实现上要这么讲.

!!! warning
    不要在答辩里把 `startTransaction` 说成「选课和进度一起原子提交」. 选课成功而 Mongo 短暂落后, 是 Outbox 的预期状态, 用重试补齐, 而不是两库一起 `ROLLBACK`.

## 备份与导入

`mongodump` 导出 BSON 归档, 对应 `mysqldump` 的角色, 但格式不是 SQL 文本:

```bash
docker compose exec -T mongodb mongodump -u mongoAdmin -p MongoAdmin@2026Strong --authenticationDatabase admin --db edu_platform --archive > data/backups/edu_mongo.dump
```

生成数据用 jsonl + `mongoimport` (`scripts/load_generated_data.ps1`). `--drop` 会先清空再导入, 仅限示例重灌.

## 命令速查

!!! abstract
    | 操作 | 语句 |
    | --- | --- |
    | 切换逻辑库 | `db.getSiblingDB('edu_platform')` |
    | 建集合 | `db.createCollection('learning_progress')` |
    | 插入 | `insertOne` / `insertMany` |
    | 查询 | `find` / `findOne`, `.sort().limit()` |
    | 投影 | `find(filter, { field: 1, _id: 0 })` |
    | 更新 / 幂等写 | `updateOne(..., { upsert: true })` |
    | 删除 | `deleteOne` / `deleteMany` |
    | 计数 | `countDocuments` / `estimatedDocumentCount` |
    | 聚合 | `aggregate([{ $match }, { $group }, { $sort }])` |
    | 库内连接 | `$lookup` |
    | 建索引 | `createIndex({ enrollment_id: 1 }, { unique: true })` |
    | 文本索引 | `createIndex({ title: 'text', content: 'text' })` |
    | TTL | `createIndex({ expire_at: 1 }, { expireAfterSeconds: 0 })` |
    | 执行计划 | `find(...).explain('executionStats')` |
    | 列表 | `show collections` / `getIndexes()` |

示例脚本对照: `mongodb/01_init_collections.js` 建集合, `02_indexes.js` 建索引, `03_seed.js` 灌文档; 应用写入见 `python/enroll_cross_db.py`.

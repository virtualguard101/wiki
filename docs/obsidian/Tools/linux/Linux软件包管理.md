---
date: 2026-06-16 14:47:35
title: Linux软件包管理
permalink: linux-app-pkg
publish: true
tags:
  - 工具
  - Linux
---

# Linux软件包管理

在创建这篇笔记近期，Arch Linux AUR（Arch User Repository, 用户仓库）发生了[软件包投毒事件](https://www.archlinuxcn.org/active-aur-malicious-packages-incident/)，关于恶意代码的详细分析可以参考[这篇文章](https://ioctl.fail/preliminary-analysis-of-aur-malware/)。

[供应链投毒](https://zh.wikipedia.org/zh-cn/%E4%BE%9B%E5%BA%94%E9%93%BE%E6%94%BB%E5%87%BB)在现在已经不是什么稀奇事了，本次安全事件只要在更新或安装软件包时对所有的 PKGBUILD 和安装脚本变更进行仔细审查即可有效规避风险。

由于Arch Linux是我目前的主力操作系统[^1]，借助此次事件，也深入学习一下 Linux 软件包管理要点与原理，以及在Arch Linux上，如何审查第三方软件包的安全性。

## 软件包管理器

**软件包管理器**（[*Package manager*](https://en.wikipedia.org/wiki/Package_manager)），也叫**软件包管理系统**（*Package management system*），是操作系统用来安装、升级、卸载、查询软件的一整套机制，包括包格式、依赖解析、仓库、以及命令行/图形界面工具。

得益于其统一的、可追踪、可回滚的软件生命周期管理操作接口，用户能够不必考虑依赖关系、彻底卸载的繁琐操作等问题。

### 常见的Linux发行版软件包管理器

各包管理器的命令功能大体相通，下面是各个包管理器常用命令的对照表。

| Action | [APT](https://en.wikipedia.org/wiki/APT_(software)) | [DNF](https://en.wikipedia.org/wiki/DNF_(software)) | [Pacman](https://en.wikipedia.org/wiki/Arch_Linux#Pacman) | [Zypper](https://en.wikipedia.org/wiki/Zypper) | [Portage](https://en.wikipedia.org/wiki/Portage_(software)) | [WinGet](https://en.wikipedia.org/wiki/Windows_Package_Manager) | [Homebrew](https://en.wikipedia.org/wiki/Homebrew_(package_manager)) | [Nix](https://en.wikipedia.org/wiki/Nix_(package_manager)) | [XBPS](https://en.wikipedia.org/wiki/Void_Linux) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 安装软件包 | `apt install ${PKG}` | `dnf install ${PKG}` | `pacman -S ${PKG}` | `zypper install ${PKG}` | `emerge ${PKG}` | `winget install %PKG%` | `brew install ${PKG}` | `nix-env -i ${PKG}` | `xbps-install ${PKG}` |
| 卸载软件包 | `apt remove ${PKG}` | `dnf remove ${PKG}` | `pacman -R ${PKG}` | `zypper remove ${PKG}` | `emerge -C ${PKG}` or `emerge --unmerge ${PKG}` | `winget uninstall %PKG%` | `brew uninstall ${PKG}` | `nix-env -e ${PKG}` | `xbps-remove ${PKG}` |
| 更新软件仓库 | `apt update` | — (automatic) | `pacman -Sy` | `zypper refresh` | `emerge --sync` | — (automatic) | `brew update` | `nix-channel --upgrade` | `xbps-install -S` |
| 显示可更新软件包 | `apt list --upgradable` | `dnf check-update` | `pacman -Qu` | `zypper list-updates` | `emerge -avtuDN --with-bdeps=y @world` or `emerge -u --pretend @world` | `winget upgrade` | `brew outdated` | `nix-channel --upgrade && nix-env -u && nix-collect-garbage` | `./xbps-src update-check ${PKG}` (requires void-packages repository) |
| 更新所有软件包 | `apt upgrade` | `dnf upgrade` | `pacman -Syu` | `zypper update` | `emerge -u -D --with-bdeps=y @world` | `winget upgrade --all` | `brew upgrade` | `nix-env -u && nix-collect-garbage` | `xbps-install -Su` |
| 显示未使用的依赖 | `apt autoremove --dry-run` | `dnf repoquery --unneeded` | `pacman -Qdt` | `zypper packages --unneeded` | `emerge -caD` or `emerge --depclean --pretend` | — | `brew autoremove --dry-run` | — | `xbps-remove -o` |
| 删除未使用的依赖 | `apt autoremove` | `dnf autoremove` | `pacman -Rsn $(pacman -Qdtq)` | `zypper remove -u` | `emerge --depclean` | — | `brew autoremove && brew cleanup` | `nix-collect-garbage -d` | `xbps-remove -of` |
| 删除软件包和未使用的依赖 | `apt-get remove --auto-remove ${PKG}` | `dnf remove ${PKG}` | `pacman -Rs ${PKG}` | `zypper remove -u ${PKG}` | `emerge -c ${PKG}` or `emerge --depclean ${PKG}` | `winget uninstall %PKG%` | `brew uninstall ${PKG} && brew autoremove` | `nix-env -e ${PKG} && nix-env -u` | `xbps-remove -R ${PKG}` |

更详细的信息还可参考[Arch Wiki](https://wiki.archlinux.org/title/Pacman/Rosetta)。

### Windows的软件包管理生态

Windows的官方软件包管理生态主要由Microsoft Store和Winget组成。由于Windows专注于GUI界面，因此其软件安装实际上更多采用图形化界面。本文主要整理Linux的软件包管理生态，这里只对Windows的软件包管理生态进行简要记录。

下面是几种主流的 Windows 软件包管理工具（方式）：

#### 传统安装方式

| 方式 | 说明 |
| --- | --- |
| **MSI / EXE 安装包** | 从厂商官网下载，通过图形向导安装；至今仍是 Windows 上最常见的分发方式 |
| **Microsoft Store** | 微软应用商店，主要分发 UWP / 打包应用，面向普通用户 |

这类方式**没有统一的依赖管理**，各软件各自安装、各自维护，容易出现版本冲突和残留文件。

#### 官方现代方案 — WinGet

[WinGet](https://learn.microsoft.com/zh-cn/windows/package-manager/winget/)（Windows Package Manager）是 Windows 10/11 内置的官方 CLI 包管理器，可视为微软对标 Linux `apt` / `pacman` 的尝试：

```powershell
winget search git              # 搜索软件包
winget install Git.Git         # 安装
winget upgrade --all           # 升级全部
winget uninstall Git.Git       # 卸载
```

- 仓库由微软官方维护，同时接受社区贡献

- 可与 MSI、MSIX、EXE 等多种安装格式对接

- 仓库索引自动更新，无需手动 `update`

#### 第三方包管理器

| 工具 | 特点 | 典型用户 |
| --- | --- | --- |
| [**Chocolatey**](https://chocolatey.org/) | 面向管理员和开发者，支持批量部署与自动化脚本 | 企业 IT、DevOps |
| [**Scoop**](https://scoop.sh/) | 轻量级，**无需管理员权限**，软件安装在用户目录 | 个人开发者 |

```powershell
# Chocolatey（需管理员权限）
choco install git
choco upgrade all

# Scoop（用户级安装）
scoop install git
scoop update *
```

#### 包格式演进

| 格式 | 说明 |
| --- | --- |
| **MSI** | 传统 Windows Installer 格式，由 `msiexec` 处理 |
| **MSIX** | 现代打包格式，支持沙箱隔离与增量更新，微软推荐的未来方向 |

#### 与 Linux 的简要对比

|  | Linux | Windows |
| --- | --- | --- |
| 统一性 | 各发行版各自为政 | 近年以 WinGet 趋向统一，但官网下载仍占很大比例 |
| 依赖管理 | 核心优势，自动解析 | 传统方式无此能力；WinGet 仅做有限支持 |
| 软件来源 | 发行版官方仓库为主 | 官网 EXE/MSI 与 Store / WinGet 并存 |
| 权限模型 | 通常需 `sudo` 装系统级软件 | UAC 提权；Scoop 等工具可绕过 |

## Linux软件包的组成

软件包的本质大多都是对一堆文件（包含软件元信息、安装逻辑、实际文件等）的**归档**，不同的包管理器对应不同的包格式和归档方式。

这里分别以 Arch Linux(`.pkg.tar.zst`) 和 Debian(`.deb`) 的软件包格式为例，简要介绍软件包的组成。

### Arch Linux 的软件包结构

Arch 的二进制包格式为 **`.pkg.tar.zst`**（[zstd](https://en.wikipedia.org/wiki/Zstandard) 压缩的 [tar](https://en.wikipedia.org/wiki/Tar_(computing)) 归档），由 [makepkg](https://wiki.archlinux.org/title/Makepkg) 根据 [PKGBUILD](https://wiki.archlinux.org/title/PKGBUILD) 构建，[pacman](https://wiki.archlinux.org/title/Pacman) 负责安装。

#### 文件命名

```
pkgname-pkgver-pkgrel-arch.pkg.tar.zst
```

示例：`firefox-136.0-1-x86_64.pkg.tar.zst`

- `pkgver`：上游版本（可带 epoch，如 `1:2.0-1`）
- `pkgrel`：Arch 打包修订号
- `arch`：目标架构（`x86_64`、`any` 等）

#### 内部结构

```
example-1.0.0-1-any.pkg.tar.zst
├── .PKGINFO          # 包元数据（必需）
├── .BUILDINFO        # 构建环境信息（必需）
├── .MTREE            # 文件校验信息（必需）
├── .INSTALL          # 安装/卸载脚本（可选）
├── .Changelog        # 变更日志（可选）
└── usr/              # 实际要安装的文件树
    ├── bin/
    ├── lib/
    └── share/
```

#### 核心元数据文件

| 文件 | 作用 |
| --- | --- |
| **`.PKGINFO`** | pacman 读取此文件做依赖解析、版本比较；包含包名、版本、依赖、冲突、备份文件列表等 |
| **`.BUILDINFO`** | 记录构建时的环境（编译器版本、构建依赖等），用于可复现构建审计 |
| **`.MTREE`** | 记录每个文件的权限、时间戳、SHA-256 哈希，安装后用于完整性校验 |
| **`.INSTALL`** | 定义安装/升级/卸载前后执行的 hook 脚本 |

`.PKGINFO` 片段示例：

```
pkgname = firefox
pkgver = 136.0-1
pkgdesc = Standalone web browser from Mozilla
arch = x86_64
depend = gtk3
depend = libxt
backup = etc/firefox/firefox.js
```

官方仓库的包还带有 OpenPGP 分离签名（`.pkg.tar.zst.sig`），pacman 验证通过后才允许安装——这是官方仓库与 AUR 在信任链上的关键区别。

#### 查看与安装

```bash
tar -tf some-package.pkg.tar.zst          # 列出包内文件
tar -xOf some-package.pkg.tar.zst .PKGINFO  # 查看元数据
sudo pacman -U some-package.pkg.tar.zst     # 安装本地包
```

### Debian 的软件包结构

Debian 系（Debian、Ubuntu 等）的二进制包格式为 **`.deb`**，由 [dpkg-deb](https://man7.org/linux/man-pages/man1/dpkg-deb.1.html) / [debuild](https://manpages.debian.org/latest/devscripts/debuild.1.en.html) 构建，[dpkg](https://manpages.debian.org/latest/dpkg/dpkg.1.en.html) / [apt](https://manpages.debian.org/latest/apt/apt.8.en.html) 负责安装。

#### 外层：`ar` 归档

`.deb` 不是 tar，而是经典的 **`ar` 归档**，固定包含三个成员，顺序不能乱：

```
example_1.0.0_amd64.deb
├── debian-binary      # 格式版本号（文本，内容为 "2.0"）
├── control.tar.xz     # 元数据 + 维护脚本
└── data.tar.xz        # 实际要安装的文件
```

#### `control.tar.*` — 控制信息

| 文件 | 作用 |
| --- | --- |
| **`control`** | 核心元数据（必需）：包名、版本、依赖、描述等 |
| **`md5sums`** | 各文件的 MD5 校验和 |
| **`conffiles`** | 配置文件列表，升级时不自动覆盖用户修改 |
| **`preinst` / `postinst`** | 安装前 / 安装后脚本 |
| **`prerm` / `postrm`** | 卸载前 / 卸载后脚本 |

`control` 文件片段示例：

```
Package: nginx
Version: 1.24.0-2ubuntu7
Architecture: amd64
Depends: libc6 (>= 2.34), libssl3 (>= 3.0.0)
Description: small, powerful, scalable web/proxy server
```

#### `data.tar.*` — 实际文件

解压后是按目标文件系统布局的目录树，安装时 `dpkg` 将其展开到 `/` 根目录：

```
data.tar.xz
├── usr/bin/nginx
├── usr/lib/...
└── etc/nginx/nginx.conf
```

#### 查看与安装

```bash
ar t nginx_1.24.0_amd64.deb                    # 查看 ar 成员
mkdir /tmp/deb-inspect && cd /tmp/deb-inspect
ar x ../nginx_1.24.0_amd64.deb                 # 解压 .deb
tar -xOf control.tar.xz ./control              # 查看元数据
tar -tf data.tar.xz | head                     # 浏览待安装文件
sudo dpkg -i nginx_1.24.0_amd64.deb            # 安装本地包
```

#### 两者设计哲学对比

|  | Arch `.pkg.tar.zst` | Debian `.deb` |
| --- | --- | --- |
| 归档层数 | 单层 tar，结构扁平 | 两层：ar → tar |
| 元数据与数据 | 混在同一 tar 根目录 | 严格分离（control / data） |
| 完整性校验 | `.MTREE`（SHA-256） | `md5sums`（MD5） |
| 安装脚本 | `.INSTALL`（单文件，多 hook） | 四个独立脚本 |
| 配置文件保护 | `.PKGINFO` 的 `backup` 字段 | `conffiles` 文件 |
| 签名 | 包级 OpenPGP 分离签名 | 仓库级签名（Release 文件） |

构建流程对照：

```
Arch：  PKGBUILD → makepkg → .pkg.tar.zst → pacman
Debian：debian/ 目录 + 源码 → debuild → .deb → dpkg/apt
```

#### 在Arch Linux上安装Debian包

##### 格式转换

使用 [debtap](https://github.com/AladW/debtap) 可将 `.deb` 解包并重新打包为 Arch 可识别的 `.pkg.tar.zst`：

```bash
# 安装 debtap（AUR）
yay -S debtap

# 首次使用需更新数据库
sudo debtap -u

# 转换并安装
debtap package.deb
sudo pacman -U package.pkg.tar.zst
```

转换工具会尝试猜测依赖名，但映射经常不准确，装完后可能缺库或产生冲突，**仅适合偶尔应急**。

通用转换工具 [alien](https://wiki.debian.org/Alien) 思路类似，主要在 Debian/Ubuntu 侧使用（如将 `.rpm` 转为 `.deb`）。

##### 容器隔离

若必须用 Debian 版软件且无法转换，可在 Arch 上运行 Debian 容器，与宿主系统隔离：

```bash
docker run -it debian:bookworm
# 或使用 Distrobox、systemd-nspawn 等
```

##### 手动编译

以上方法都行不通，那就只能去官方软件仓库手动clone源码然后再本地构建编译了。

## AUR软件包的安全审查

基于上面介绍的[Arch Linux的软件包结构](#Arch-Linux-的软件包结构)，我们就能够从结构的角度对软件包进行全面审查了。

在Arch Linux上，访问AUR仓库一般使用[AUR Helper](https://wiki.archlinux.org/title/AUR_helpers)，目前主流的AUR Helper有[yay](https://github.com/Jguer/yay)、[paru](https://github.com/Morganamilo/paru)、[pikaur](https://github.com/actionless/pikaur)等。

!!! warning
    Arch Linux 官方**不支持**（unsupported）[AUR helpers](https://wiki.archlinux.org/title/AUR_helpers)，官方推荐熟悉手动构建流程（获取 PKGBUILD → 审查 → `makepkg` → `pacman -U`），以便排查问题并审查软件来源。

    此外，[AUR 软件包均为用户提交内容](https://wiki.archlinux.org/title/AUR)，PKGBUILD 完全非官方且未经彻底审查，使用前必须自行检查 PKGBUILD、`.install` 等文件。部分 AUR Helper（如 yay、paru）可在安装前展示 PKGBUILD 或 diff，但这**不能替代**仔细的人工审查。

通用的安装/更新与审查流程可直接参考[Arch Wiki](https://wiki.archlinux.org/title/Arch_User_Repository#Installing_and_upgrading_packages)。

若使用 AUR Helper，应优先选择支持 **File review** 和 **Diff view** 的工具（如 yay、paru），并养成以下习惯：

#### 安装前先获取、后构建

不要直接「一键安装」，先用 Helper 只拉取构建文件，审查通过后再构建：

```bash
# yay：仅获取 PKGBUILD，不构建
yay -G package_name
cd package_name

# paru：同上
paru -G package_name
cd package_name
```

审查完成后，再在包目录内手动 `makepkg -si`，或确认无误后交给 Helper 安装。

#### 更新时查看 diff

AUR 包更新时，维护者可能修改 PKGBUILD 或安装脚本——这正是投毒事件常见的攻击面：

```bash
# 在已 clone 的包目录中
git pull
git show                    # 查看最近一次提交的变更
git difftool @~..@          # 与上一版本逐文件对比
```

yay / paru 在更新时通常也会展示 diff，**不要习惯性按 `y` 跳过**。

#### 需要重点审查的文件

| 文件 | 关注什么 |
| --- | --- |
| **`PKGBUILD`** | `source` 是否指向可信地址；`pkgver` 是否异常；`build()` / `package()` 有无可疑命令 |
| **`.install`** | `pre_install` / `post_install` 等 hook 是否执行远程脚本、修改系统关键路径 |
| **补丁 / 脚本** | `.patch`、`.sh` 等附带文件的内容 |
| **`.SRCINFO`** | 与 PKGBUILD 是否一致（应通过 `makepkg --printsrcinfo` 生成） |

尤其警惕：`curl ... \| bash`、`wget` 拉取不明二进制、向 `~/.bashrc` / `~/.ssh` 写入内容、base64 编码的隐蔽载荷等。

#### 辅助工具

Arch Wiki 提到 [traur](https://aur.archlinux.org/packages/traur) AUR、[ks-aur-scanner](https://aur.archlinux.org/packages/ks-aur-scanner) AUR 等可辅助扫描 PKGBUILD，但**只是辅助**，不能代替自己读一遍。

#### `--editmenu`

```bash
# 安装前用编辑器打开 PKGBUILD（yay）
yay --editmenu -S package_name

# paru 默认会在构建前展示文件列表，更新时展示 diff
# 可在 /etc/paru.conf 中确认未关闭审查相关选项
```

可设置 `DIFFVIEWER` / `EDITOR` 环境变量，让 diff 和编辑使用自己熟悉的工具（如 `vimdiff`、`nvim`）。

#### 审查清单

1. 维护者是否可信？包页面评论、投票数、最近更新时间

2. `source` 来源是否官方？校验和（`sha256sums`）是否匹配

3. 构建/安装脚本有无网络请求、权限提升、修改其他用户文件

4. **更新时**：本次变更改了什么？是否只该改 `pkgver` 却动了 `build()`？

5. 有疑问时，可以到[aur-general 邮件列表](https://lists.archlinux.org/mailman3/lists/aur-general.lists.archlinux.org/) 求助


[^1]: [Arch Linux安装要点记录](../../../blog/posts/Arch%20Linux安装要点记录.md)
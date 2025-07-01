---
title: Arch Linux安装要点记录
categories:
  - Misc
date: 2025-05-19 08:52:48
description: >
  记录一下在可移动设备/真机上安装和配置Arch Linux的过程安装过程中遇到的一些问题
authors:
  - virtualguard101
tags:
  - linux
---

**记录一下在可移动设备/真机上安装和配置Arch Linux的过程安装过程中遇到的一些问题**

Arch Linux是一个支持高度定制化的Linux发行版，其采用滚动更新的方式对系统进行更新，更新策略激进，适合愿意花时间在自己系统的计算机用户或喜欢折腾的计算机用户。

这里需要特别说明一点，在安装之前，需要反思自己是否真的适合使用Arch！否则Arch的高度定制化与激进的更新策略将会使你陷入极大的麻烦！毕竟高度定制化的代价就是你需要为系统付出比其他稳定发行版多得多的时间去维护它。

<!-- more -->

## 基本安装

针对这部分内容，教程[Arch Guide | Nakano Miku](https://arch.icekylin.online/guide/)有详尽的阐述，包括从安装准备到系统美化的所有内容。

这里记录几个我在真机安装过程中遇到的问题。

### 格式化EFI分区前未备份原有系统启动引导（双系统）

我在安装过程中由于急于求成，在为EFI分区扩容时未备份原有系统（这里是Win11）的启动引导程序就直接将其格式化了，结果安装完Arch的基本系统才发现Win11进不去了.....

虽说安装前有备份Win11的系统映像，但为了一个EFI分区动用这个实属大材小用，因为基本数据的分区并没有任何问题。在这个问题上，我选择使用WinPE镜像系统对Win11的启动引导进行还原。只需准备一个装有WinPE镜像的U盘，启动进入WinPE，按照下图的提示，选择修`UEFI`引导进行修复即可：

![](https://i.imgur.com/8fTXOCP.jpeg)

### 输入法异常

这在教程[Arch Guide | Nakano Miku](https://arch.icekylin.online/guide/)有提示，（如果是按照此教程进行的安装）执行命令`fcitx5-diagnose`进行问题诊断并按照输出提示修复即可。

### 杂项

关于桌面环境的选择，可以参考这篇文章：[Xorg, X11, Wayland? Linux Display Servers And Protocols Explained
](https://linuxiac.com/xorg-x11-wayland-linux-display-servers-and-protocols-explained/)

## 在可移动设备安装

该部分可参考[将Arch Linux系统安装在可移动设备上的要点 | ToBeHonest's BLOG](https://b2og.com/archives/23)。

第一次安装中，我就将Arch装在了一个256G、使用USB3.1的U盘上，同时由于使用[虚拟机](https://arch.icekylin.online/guide/rookie/pre-virt.html)运行安装镜像，所以并没有碰到什么大问题。

---
**[参考文献]：**

- [在可移动设备上安装 Arch Linux | Arch Wiki](https://wiki.archlinuxcn.org/zh-sg/%E5%9C%A8%E5%8F%AF%E7%A7%BB%E5%8A%A8%E8%AE%BE%E5%A4%87%E4%B8%8A%E5%AE%89%E8%A3%85_Arch_Linux)

- [将Arch Linux系统安装在可移动设备上的要点 | ToBeHonest's BLOG](https://b2og.com/archives/23)

- [Arch Guide | Nakano Miku](https://arch.icekylin.online/guide/)

- [ArchLinuxTutorial | Arch Linux Studio](https://archlinuxstudio.github.io/ArchLinuxTutorial/#/)

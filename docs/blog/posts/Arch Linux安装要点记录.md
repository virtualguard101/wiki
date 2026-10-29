---
title: Arch Linux安装要点记录
categories:
  - Misc
date: 2026-10-29 01:59:48
excerpt: 记录一下在可移动设备/真机上安装和配置Arch Linux的过程安装过程中遇到的一些问题
authors:
  - virtualguard101
tags:
  - Linux
  - Blog
---

**记录一下在可移动设备/真机上安装和配置Arch Linux的过程安装过程中遇到的一些问题**

Arch Linux是一个支持高度定制化的[Linux](../../note/tools/linux/Linux基础、杂项.md)发行版，其采用滚动更新的方式对系统进行更新，更新策略激进，适合愿意花时间在自己系统的计算机用户或喜欢折腾的计算机用户。

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

## 多系统共存

在已有一个 Arch（btrfs，`@` / `@home` 子卷，ESP 挂载在 `/boot`）的本机上，往另一个分区再加装一个 Arch 时，几个可能遇到的坑：

### 共享 swap 分区：重复 `mkswap` 会让旧系统的 UUID 失效

新旧系统若共用同一个 swap 分区，新装时再次 `mkswap` 会重新生成 UUID，旧系统 `/etc/fstab` 与 GRUB 的 `resume=` 随即指向一个不存在的 UUID，表现为开机后 `swapon --show` 为空、swap 为 0B。

- 不要对共享 swap 重复 `mkswap`；
- 或装完后回旧系统，同步新的 swap UUID：

```bash
lsblk -f            # 确认 swap 现在的分区与 UUID
sudo sed -i 's/<旧UUID>/<新UUID>/g' /etc/fstab
sudo sed -i 's/<旧UUID>/<新UUID>/g' /etc/default/grub
sudo grub-mkconfig -o /boot/grub/grub.cfg
sudo swapon -a && swapon --show
```

### `grub-install`：ESP 挂在 `/boot` 时，`--efi-directory` 就写 `/boot`

```bash
grub-install --target=x86_64-efi --efi-directory=/boot --bootloader-id=ARCH
```

把 `--efi-directory` 写成 `/boot/efi` 或 `/boot/EFI` 会生成 `EFI/EFI/…` 的错误嵌套（如 `/boot/EFI/EFI/GRUB/grubx64.efi`），引导路径错乱且极具迷惑性。`--bootloader-id` 用唯一名字（如 `ARCH`），别与已有项冲突。

### 多系统：复用原 ESP，不要重新格式化

新装时把现有 ESP 挂到 `/mnt/boot` 复用即可，**不要** `mkfs.fat` 格式化它——这会清掉其它系统（Windows/Kali 等）的引导文件与 NVRAM 项。这和前面提到的[把Windows的引导给扬了](#格式化EFI分区前未备份原有系统启动引导双系统)是同一个问题。

### fstab 用 `genfstab -U` 生成，且先挂完再生成

挂载顺序：根(`subvol=/@`) → `/home`(`subvol=/@home`) → `/boot`，再 `swapon`；都挂好后再：

```bash
genfstab -U /mnt > /mnt/etc/fstab
```

手写或沿用旧注释（如 `# /dev/nvme0n1p6`）在分区表变化后容易对不上号。

### 清理多余的 UEFI 启动项

固件菜单容易残留孤儿项（`Linpus lite`、`kali`、`Windows`、`rEFInd` 等）：

```bash
efibootmgr -v                        # 先看 BootCurrent 和各项，确认哪些是孤儿
sudo efibootmgr -b 0000 -B           # 按编号删除孤儿项
sudo efibootmgr -o 0005,2001,2002,2003   # 重排启动顺序，保留 U 盘/网络项
```

ESP 上无主的 `EFI/<id>/` 目录（如 `EFI/kali`、`EFI/Microsoft`）也可一并删除；删前先确认整盘没有对应系统的数据分区。

### 重新安装被删掉引导的系统

引导被删不影响日后重装：ESP 本身没有被格式化，只是删掉了几个子目录和 NVRAM 项，结构完好。重装时用对应安装映像引导、把 ESP 挂上（**别格式化**）即可，installer 会自动重建各自的引导文件并重新写 NVRAM 项。**真正的约束在数据分区，不在引导。**

- **Windows**：会自动写回 `\EFI\Microsoft\Boot\bootmgfw.efi` 并重建 `Windows Boot Manager` 项；但需要一块 **NTFS** 分区放系统，外加 **MSR(16MB)** 和 **Recovery** 分区。整盘若已分满，要先腾空间（缩容某个 btrfs 或加盘）。

- **Kali / 其它 Linux**：装到已有 ESP 即可，grub 会自动写 `\EFI\kali\...` 并注册 NVRAM 项；需要一块 **ext4** 分区。swap 可与现有系统共用，但**别再 `mkswap`**（否则又是 UUID 失效的老问题）。

重装后记得两件事：

```bash
sudo grub-mkconfig -o /boot/grub/grub.cfg   # os-prober 才会把新系统加进 GRUB 菜单
sudo efibootmgr -o 0005,2001,2002,2003      # 重排启动顺序（新安装器常把自己排到第一位）
```

### 引导问题的快速修复

若遇到引导无法进入旧系统的问题, 且时间紧迫无法进行完整排查，可尝试以下**快速修复旧系统的引导**:

- 使用安装介质进入安装系统环境
    
- 然后挂载旧系统的根分区到 `/mnt`，ESP 挂载到 `/mnt/boot`，必要时挂载 `/home` 等其他分区:

    ```bash
    mkdir -p /mnt/boot
    mount /dev/nvmen1p1 /mnt/boot   # 挂载 ESP
    mount -o subvol=@ /dev/nvmen1px /mnt   # 挂载根分区(btrfs文件系统)
    ```

- 删除新引导项（NVRAM 中的孤儿项）和 ESP 上无主的 `EFI/<id>/` 目录，确保旧系统的引导优先:

    ```bash
    rm -rf /mnt/boot/EFI/<id>   # 删除无主的 EFI 目录
    rm -rf /mnt/boot/EFI/<new>  # 删除新引导的 EFI 目录
    ```

- 切换到旧系统的根分区后重新生成 GRUB 配置并更新 NVRAM 启动顺序:

    ```bash
    arch-chroot /mnt   # 切换到旧系统的根目录
    sudo grub-mkconfig -o /boot/grub/grub.cfg
    sudo efibootmgr -o 0005,2001,2002,2003
    ```

但这种方式显然无法修复新分区的启动问题, 但是可以保证旧系统的引导优先，从而在紧急情况下快速恢复可用的启动环境.

---
**[参考文献]：**

- [在可移动设备上安装 Arch Linux | Arch Wiki](https://wiki.archlinuxcn.org/zh-sg/%E5%9C%A8%E5%8F%AF%E7%A7%BB%E5%8A%A8%E8%AE%BE%E5%A4%87%E4%B8%8A%E5%AE%89%E8%A3%85_Arch_Linux)

- [将Arch Linux系统安装在可移动设备上的要点 | ToBeHonest's BLOG](https://b2og.com/archives/23)

- [Arch Guide | Nakano Miku](https://arch.icekylin.online/guide/)

- [ArchLinuxTutorial | Arch Linux Studio](https://archlinuxstudio.github.io/ArchLinuxTutorial/#/)

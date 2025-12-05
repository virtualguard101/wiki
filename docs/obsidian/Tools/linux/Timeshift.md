---
date: 2025-09-23 23:38:00
title: Timeshift
permalink: 
publish: true
---

# Timeshift

Timeshift 可帮助定期创建文件系统的增量快照，然后在以后恢复到这些快照，以撤销对系统的所有更改[^1]。

它支持针对所有文件系统的 rsync 快照，也可使用 Btrfs 驱动器的内置快照功能，这需要驱动器根目录和 home 目录分别使用 @ 和 @home 子卷布局配置。

## 安装与基本配置

我的操作系统是 [**Arch Linux**](../../../blog/posts/Arch%20Linux安装要点记录.md), 使用[Btrfs文件系统](https://arch.icekylin.online/guide/advanced/btrfs)

基本安装与配置可以参考[设置 Timeshift 快照 | archlinux 简明指南](https://arch.icekylin.online/guide/rookie/desktop-env-and-app.html#_12-%E8%AE%BE%E7%BD%AE-timeshift-%E5%BF%AB%E7%85%A7)

## 基本使用

可通过[`timeshift-gtk`(Timeshift的GUI版本)](https://man.archlinux.org/man/timeshift-gtk.1.en)查看和管理备份快照。

我个人习惯直接通过命令行使用

- 查看当前备份快照

    ```bash
    sudo timeshift --list
    ```

- 检查配置

    ```bash
    sudo timeshift --check
    ```

- 创建一个快照

    ```bash
    sudo timeshift --create --comments "[some-infomation-here]" --tags [snapshot-tag]
    ```

    - 这里的 `--tag` 参数是为方便 Timeshift 管理快照而设置的，通常有以下类型的快照类型:

        - D - Daily（每日）：标记为每日快照

        - W - Weekly（每周）：标记为每周快照

        - M - Monthly（每月）：标记为每月快照

        - H - Hourly（每小时）：标记为每小时快照

        - B - Boot（启动）：标记为系统启动时创建的快照

        - O - Ondemand（按需）：标记为手动创建的快照（默认值）

    - 不同的快照有不同的保留策略:

        - 每日快照保留7天

        - 每周快照保留4周

        - 每月快照保留6个月

- 删除某个快照

    ```bash
    sudo timeshift --delete --snapshoot [snapshoot-name]
    ```

## 将快照备份到外部设备

[archlinux 简明指南](https://arch.icekylin.online/guide/rookie/desktop-env-and-app.html#_12-%E8%AE%BE%E7%BD%AE-timeshift-%E5%BF%AB%E7%85%A7)的备份策略是将快照备份在本地磁盘，这样的话如果是硬盘不可拆卸的笔记本电脑，想要**快速迁移**整个系统的配置就需要先将快照导出到外部存储设备；然后在新电脑安装基本系统；最后通过 `timeshift --restore` 执行“恢复”。

注意用于导出的外部设备需要和快照的文件系统相同。

### 具体操作

导出有两种方式:

- 直接导出

    - 挂载外部设备与 `timeshift` 快照所在的分区

        - 可通过 `--check` 命令查看当前快照所在的分区

            ```bash
            $ sudo timeshift --check --verbose
            Using system disk as snapshot device for creating snapshots in BTRFS mode
            Mounted '/dev/nvme0n1p6' (subvolid=0) at '/run/timeshift/1295525/backup'
            btrfs: Quotas are not enabled
            Daily snapshots are enabled
            Last daily snapshot is 1 hours old
            Weekly snapshots are enabled
            Last weekly snapshot is 6 days old
            ------------------------------------------------------------------------------
            ```
        
        - 挂载

            ```bash
            sudo mount /dev/nvme0n1p6 /mnt/origin
            sudo mount /dev/sda1 /mnt/usb
            ```

        - 使用 `ls` 命令应该可以看到快照目录

            ```bash
            $ sudo ls /mnt/origin/timeshift-btrfs/snapshots/
            2025-09-01_17-00-01  2025-09-08_17-00-00  2025-09-15_18-00-00  2025-09-17_19-00-00  2025-09-18_20-00-00  2025-09-19_20-00-00  2025-09-20_20-00-00  2025-09-21_20-00-01
            ```
            不同设备的快照路径可能有所差异

        - 使用 `rsync` 直接复制

            ```bash
            sudo rsync -aAXHv --progress /mnt/origin/timeshift-btrfs/snapshots /mnt/usb
            ```
            这会把所有快照都复制过去，如果磁盘空间有限，也可以选择某个或某些快照的目录复制，或者使用下面介绍的压缩

- 压缩导出
    
    挂载的步骤与直接导出无异，只是导出的方式有区别

    压缩导出用 `tar` 把快照文件压缩到一个压缩包中，等到要用的时候再解压

    ```bash
    sudo tar -cvpzf /mnt/usb/arch-backup-250921.tar.gz /mnt/origin/timeshift-btrfs/snapshots/2025-09-21_20-00-01
    ```

    压缩需要一些时间

### 两种方式的区别与迁移要点

两种方法最终的效果基本没有区别。在 Btrfs 文件系统下，快照的本质就是子卷 (subvolume)，==数据结构和原始目录一模一样==。

- 唯一的区别就是

    - 原始快照在 Btrfs 内部是**写时复制 (COW)**的子卷，能节省空间。

    - 解压出来后只是一个普通目录，不再有 Btrfs 子卷属性。

- 如果目标是 ==恢复数据（/home、配置文件等）== → 压缩和解压完全够用。

- 如果目标是 ==完整恢复 Timeshift 快照功能== → 解压和压缩则需要在新机器上：

    - 创建 Btrfs 分区

    - 解压 tar.gz 到 timeshift/snapshots/xxxx

    - 再用 `timeshift --restore` 去识别和恢复

    这样效果和直接复制 Timeshift 镜像一样。


[^1]: [Timeshift | Arch Linux 中文维基](https://wiki.archlinuxcn.org/wiki/Timeshift)
---
date: 2026-03-25 08:46:26
title: ufw
permalink: ufw
publish: true
tags:
  - 工具
  - Linux
---

# ufw

> [UFW Essentials: Common Firewall Rules and Commands for Linux Security | DigitalOcean](https://www.digitalocean.com/community/tutorials/ufw-essentials-common-firewall-rules-and-commands)

UFW 是 Ubuntu/Debian 系 Linux 发行版默认的防火墙配置工具，它本质上是一个简化前端（front-end），底层依赖 Linux 内核的 netfilter/iptables（或现代的 nftables）机制来实现数据包过滤。

## 安装

```bash
sudo apt update
sudo apt install ufw
```

## 配置与使用

- 设置默认策略

    ```bash
    sudo ufw default deny incoming    # 默认拒绝所有入站连接（最安全）
    sudo ufw default allow outgoing   # 默认允许所有出站连接（方便更新、下载等）
    ```

!!! warning
    若是在ssh连接shell中配置，为避免连接中断，务必在规则中先允许ssh流量通过再启用防火墙

    ```bash
    sudo ufw allow OpenSSH          # 使用应用名称
    sudo ufw allow ssh              # 使用协议名称
    sudo ufw allow 22/tcp           # 使用端口和协议
    sudo ufw allow from 192.168.1.0/24 to any port 80 proto tcp # 使用源地址和目标地址
    ```

- 启用防火墙

    ```bash
    sudo ufw enable
    ```

- 禁用防火墙

    ```bash
    sudo ufw disable
    ```

- 查看防火墙状态信息

    ```bash
    sudo ufw status verbose
    ```

!!! tip
    - 注意在只指定端口而不带协议时，UFW 默认会同时开放该端口的 TCP 和 UDP 两个传输层协议

    - 大部分情况下不需要在修改规则后reload，UFW 会立即把规则应用到 iptables（防火墙实时生效）

- 移除一个规则

    ```bash
    sudo ufw delete allow 22/tcp    # 端口
    sudo ufw delete allow OpenSSH   # 应用名称
    sudo ufw delete allow ssh       # 协议/服务名称
    ```

    还可以通过规则编号来移除一个规则，首先按编号列出所有规则:

    ```bash
    $ sudo ufw status numbered    # 按编号列出所有规则
    Status: active

        To                         Action      From
    --                         ------      ----
    [1] OpenSSH                    ALLOW IN    Anywhere                  
    [2] 80/tcp                     ALLOW IN    Anywhere                  
    [3] 443/tcp                    ALLOW IN    Anywhere                  
    [4] 22/tcp (v6)                ALLOW IN    Anywhere (v6)
    ```

    ```bash
    sudo ufw delete 1    # 移除编号为1的规则
    ```

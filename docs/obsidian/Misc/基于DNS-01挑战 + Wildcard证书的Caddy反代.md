---
date: 2026-03-31 01:53:02
title: 基于DNS-01挑战 + Wildcard证书的Caddy反代
permalink: bypass-http_01-and-TLS_ALPN_01
publish: true
tags:
  - 解决方案
---

# 基于DNS-01挑战 + Wildcard证书的Caddy反代

若为域名解析配置了Cloudflare代理，使用[Caddy](反向代理.md#Caddy)进行反代操作时，大概率会碰到 HTTP-01 或 TLS-ALPN-01 挑战失败（522 错误或 ALPN 协商失败）。

每次更新Caddy的反代配置后实际执行反代前，或者更新证书，都需要手动关闭Cloudflare代理，非常繁琐。

通过 DNS-01 挑战 + Wildcard 证书（`*.virtualguard101.com`） 可以完美解决这个问题：以后新增子域无需反复开关 Cloudflare Proxy，也无需重新申请证书。

## 准备工作

### 创建 Cloudflare API Token

登录 Cloudflare → My Profile → API Tokens → Create Token → Custom token → 选择 Zone: Read 和 Zone: Edit 权限 → Create Token

权限配置有两个:

- Zone - Zone - Read

- Zone - DNS - Edit

Zone Resource 选择 Specific zone → 选中你的域名（如 `virtualguard101.com`） → 点击 Continue to Summary → Create Token

保存 API Token 到环境变量：

```bash
export CLOUDFLARE_API_TOKEN="your_api_token"
```

或者写入 `.env` 文件：

```bash
CLOUDFLARE_API_TOKEN=your_api_token
```

### 构建带 Cloudflare DNS 插件的 Caddy

- 安装 Golang 环境

    ```bash
    sudo apt update && sudo apt install -y golang-go
    ```

- 手动构建 Caddy 的二进制文件

    ```bash
    # 添加 xcaddy 到 PATH（如果之前没加，建议永久加入 ~/.bashrc）
    export PATH=$PATH:~/go/bin

    # 构建（会在当前目录生成 caddy 可执行文件）
    xcaddy build --with github.com/caddy-dns/cloudflare

    # 移动到系统目录并设置权限
    sudo mv caddy /usr/bin/caddy
    sudo chmod +x /usr/bin/caddy

    # 验证（version 不会显示插件，需用 list-modules 检查）
    caddy version
    caddy list-modules --skip-standard | grep -i cloudflare
    ```

    最后一条命令应该会输出 `dns.providers.cloudflare`，表明当前的 Caddy 版本已经支持 Cloudflare DNS 插件。

## 配置 Caddy 反代

```Caddyfile
{
    # 全局设置（可选，推荐加上邮箱，便于 Let's Encrypt 通知）
    email your_email@example.com
}

*.virtualguard101.com {
    # 使用 DNS-01 挑战 + Cloudflare
    tls {
        dns cloudflare {env.CLOUDFLARE_API_TOKEN}
        # 可选：如果 DNS 传播慢，可以添加以下两行
        # propagation_delay 30s
        # resolvers 1.1.1.1 1.0.0.1
    }

    # 按不同子域路由到不同后端
    @backend1 host backend1.virtualguard101.com
    handle @backend1 {
        reverse_proxy backend1:port
    }

    @backend2 host backend2.virtualguard101.com
    handle @backend2 {
        reverse_proxy backend2:port
    }

    # 如果还有其他子域，继续添加类似 block
    # @other_backend host other_backend.virtualguard101.com
    # handle @other_backend {
    #     reverse_proxy other_backend:port
    # }

    # 默认处理（可选）
    handle {
        respond "Hello from wildcard Caddy" 200
    }
}
```

手动测试：

```bash
# 使用 --envfile 加载环境变量
sudo caddy run --config caddyfile --adapter caddyfile --envfile .env
```

## 配置 systemd 服务

```bash
sudo nano /etc/systemd/system/caddy.service
```

```ini
[Unit]
Description=Caddy (with Cloudflare DNS-01)
After=network.target network-online.target
Requires=network-online.target

[Service]
Type=notify
User=root
Group=root
EnvironmentFile=/path/to/.env
ExecStart=/usr/bin/caddy run --config /path/to/Caddyfile --adapter caddyfile
ExecReload=/usr/bin/caddy reload --config /path/to/Caddyfile --adapter caddyfile
TimeoutStopSec=5s
LimitNOFILE=1048576
LimitNPROC=512
PrivateTmp=true
ProtectSystem=full
AmbientCapabilities=CAP_NET_BIND_SERVICE CAP_NET_RAW

[Install]
WantedBy=multi-user.target
```

启动服务：

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now caddy
```

查看状态：

```bash
sudo systemctl status caddy
```

查看实时日志：

```bash
sudo journalctl -u caddy -f
```

## 后续维护操作

### 新增子域

只需在 Caddyfile 中添加新的 @host + handle 块，然后执行 `sudo systemctl reload caddy` 即可（无需重新申请证书）。

### 重启/更新

- 重载配置

    ```bash
    sudo systemctl reload caddy
    ```

- 重启服务

    ```bash
    sudo systemctl restart caddy
    ```

- 查看近期日志

    ```bash
    sudo journalctl -u caddy -n 100
    ```

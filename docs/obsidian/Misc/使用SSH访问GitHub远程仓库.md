---
date: 2025-10-20 23:41:43
title: 使用SSH访问GitHub远程仓库
permalink:
publish: true
---

# 使用SSH访问GitHub远程仓库

> [SSH](远程服务器使用基础.md)
>
> [Adding a new SSH key to your GitHub account](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account)

先创建SSH密钥：
```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
```

然后将公钥添加到GitHub：

```bash
cat ~/.ssh/id_ed25519.pub
```

1. 打开GitHub的[SSH and GPG keys](https://github.com/settings/ssh/new)页面，点击“New SSH key”按钮。

2. 在“Title”字段中输入一个易于识别的名称，例如“MacBook Pro”。

3. 在“Key”字段中粘贴之前复制的公钥内容。

4. 点击“Add SSH key”按钮完成添加。

最后，测试SSH连接：
```bash
ssh -T git@github.com
```

如果返回“Hi username! You've successfully authenticated, but GitHub does not provide shell access.”则说明连接成功。

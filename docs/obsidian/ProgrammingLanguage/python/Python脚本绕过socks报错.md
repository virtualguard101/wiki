---
date: 2026-03-23 09:36:26
title: Python脚本绕过Socks报错
permalink: python-socks
publish: true
tags:
  - 解决方案
  - Python
---

# Python脚本绕过Socks报错

> [Python脚本绕过Socks报错 | Grok](https://grok.com/share/bGVnYWN5_463dc13b-303e-441e-a2f4-30ae31e805ca)

在本地运行Python脚本时，若本身有设置代理（Clash、v2ray等）且未进行特殊配置，基本会导致类似如下的报错:

```bash
Traceback (most recent call last):
  File "/home/virtualguard/vg101/notebooks/lab/ai/agent/main.py", line 144, in <module>
    llm = OpenAICompatibleClient(
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/virtualguard/vg101/notebooks/lab/ai/agent/main.py", line 112, in __init__
    self.client = OpenAI(api_key=api_key, base_url=base_url)
                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/virtualguard/vg101/notebooks/lab/ai/agent/.venv/lib/python3.12/site-packages/openai/_client.py", line 168, in __init__
    super().__init__(
  File "/home/virtualguard/vg101/notebooks/lab/ai/agent/.venv/lib/python3.12/site-packages/openai/_base_client.py", line 887, in __init__
    self._client = http_client or SyncHttpxClientWrapper(
                                  ^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/virtualguard/vg101/notebooks/lab/ai/agent/.venv/lib/python3.12/site-packages/openai/_base_client.py", line 817, in __init__
    super().__init__(**kwargs)
  File "/home/virtualguard/vg101/notebooks/lab/ai/agent/.venv/lib/python3.12/site-packages/httpx/_client.py", line 686, in __init__
    proxy_map = self._get_proxy_map(proxy, allow_env_proxies)
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/virtualguard/vg101/notebooks/lab/ai/agent/.venv/lib/python3.12/site-packages/httpx/_client.py", line 245, in _get_proxy_map
    key: None if url is None else Proxy(url=url)
                                  ^^^^^^^^^^^^^^
  File "/home/virtualguard/vg101/notebooks/lab/ai/agent/.venv/lib/python3.12/site-packages/httpx/_config.py", line 214, in __init__
    raise ValueError(f"Unknown scheme for proxy URL {url!r}")
ValueError: Unknown scheme for proxy URL URL('socks://127.0.0.1:7897')
```

这个错误几乎总是因为环境变量里设置了 socks 代理（通常是 Clash、v2ray、sing-box 等工具默认导出的那种），但当前运行的 Python 脚本 / 依赖库（最常见是 httpx 或 urllib3）不支持 socks:// 这个 scheme。

网络上的解决方案通常是直接在shell的环境变量中删除 socks 代理的相关配置:

```bash
unset all_proxy
unset ALL_PROXY
```

但是在真的需要代理的时候，这个方法有概率会引入新的问题，而且每次在脚本运行前都需要手动设置环境变量，不利于代码可移植性。

基于Python的一些第三方库，可以通过对Python脚本进行一些特殊配置来绕过Socks报错或指定代理服务器:

## 脚本开头强行清空代理环境变量

```python
import os

# 放在脚本最开头，越前面越好，最好在任何 import requests / httpx 之前
os.environ.pop('http_proxy', None)
os.environ.pop('https_proxy', None)
os.environ.pop('HTTP_PROXY', None)
os.environ.pop('HTTPS_PROXY', None)
os.environ.pop('all_proxy', None)     # Clash 常用
os.environ.pop('ALL_PROXY', None)

# 原代码部分
import requests
# ... 或 import httpx
# ... 或 from huggingface_hub import ...
```

这种方式对大部分场景都有效，且不需要额外安装任何包。

## http代理

```python
import os

os.environ['http_proxy']  = 'http://127.0.0.1:port'
os.environ['https_proxy'] = 'http://127.0.0.1:port'
# 强烈建议同时删除 socks 相关的变量
os.environ.pop('all_proxy', None)
os.environ.pop('ALL_PROXY', None)

# 然后正常 import requests / httpx
```

确定需要使用 http 代理时，可以使用这种方式。Clash 通常也开了 http 端口，可以直接使用，无需前两行的配置，只需要删除 socks 相关的变量即可。

## socks5代理

必须使用 socks5 代理时，则需要额外安装socks库:

```bash
pip install httpx[socks]    # 如果用的是 httpx
# 或
pip install requests[socks]   # 如果用的是 requests
```

然后配置代理:

```bash
import os

# 推荐用 socks5h:// （域名解析走代理，防泄露）
os.environ['http_proxy']  = 'socks5h://127.0.0.1:7897'
os.environ['https_proxy'] = 'socks5h://127.0.0.1:7897'
# 或者直接在代码里设置（更保险）

# 如果是 requests
import requests
proxies = {
  'http':  'socks5h://127.0.0.1:port',
  'https': 'socks5h://127.0.0.1:port'
}
requests.get("https://...", proxies=proxies)

# 如果是 httpx
import httpx
client = httpx.Client(proxies="socks5h://127.0.0.1:port")
```

注意协议是 `socks5h://` 而不是 `socks5://`，因为后者不支持域名解析走代理[^1]:

| 代理 scheme | DNS 解析位置 | 实际行为 | 常见使用场景 / 风险点 |
|:-----------:| ------------ | -------- | --------------------- |
| `socks5://` | 客户端本地 | Python 先把域名（如 api.openai.com）解析成 IP，然后把 IP 发给代理服务器 | 容易发生 DNS 泄露（本地 ISP / 系统 DNS 看到你访问了什么域名） |
| `socks5h://` | 代理服务器端 | Python 只把原始域名发给代理，让代理去解析域名并连接目标 | 域名解析也走代理，更隐私，特别适合 Tor、VPN 出国、敏感场景 |


[^1]: [Python脚本绕过Socks报错 | Grok](https://grok.com/share/bGVnYWN5_463dc13b-303e-441e-a2f4-30ae31e805ca)
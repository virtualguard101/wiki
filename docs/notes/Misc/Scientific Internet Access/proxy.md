# 透明代理

>全球化浪潮无法阻挡，我们常常有访问一些资料的客观需求。但有的时候因为一些因素往往导致无法正常访问（包括但不限于终端中下载文件特别慢、无法访问部分网站、部分应用无法正常使用等）。虽然前路千沟万壑，但无法阻挡我们前行的脚步[^1]。

透明代理是一种网络代理设置，其特点是客户端不需要特别配置就能使用代理服务。当网络流量通过透明代理时，客户端通常不会意识到数据正在被代理转发。

## Clash 付费订阅

Clash 本身是一个网络连接的代理内核，通过预先定义的规则，对网络连接进行转发。Clash 内核规定了配置文件 config.yaml 的格式。支持 VMess、Shadowsocks、Trojan、Snell 协议。现在人们口中的 Clash 通常指 [Clash.Meta（现改名成 mihomo）](https://github.com/MetaCubeX/mihomo)，是一个基于开源项目 Clash 的二次开发版本，增加了一些独有特性。支持所有原版 Clash 开源核心的全部特性，支持原 Clash Premium 核心部分特性。基于目前原版内核已无人维护且 Meta 更新较为活跃，更推荐使用 Meta 而非原版[^2]。

对于普通需求的群体或是刚入门CS不久的小白，可以使用**Clash + 付费订阅**的配置进行基础过渡（这通常也能满足绝大多数需求）；提供节点订阅服务的供应方我们称其为**机场**，更多信息这里不作展开，可自行上网查阅资料或参考[官方文档](https://wiki.metacubex.one/)

付费订阅的步骤非常简单，一般分为三步：

1. 安装 Clash 客户端

    参考[官方文档](https://wiki.metacubex.one/startup/faq/)，在[三方工具/客户端列表](https://wiki.metacubex.one/startup/client/client/)中选择并下载对应系统的 Clash 客户端（建议选择[Clash Verge Rev](https://github.com/clash-verge-rev/clash-verge-rev)）。  

    在其GitHub仓库界面进入[releas界面](https://github.com/clash-verge-rev/clash-verge-rev/releases)，选择对应的操作系统的包进行下载并安装。

    !!! tip
        下载过程受网络环境影响可能会十分缓慢，若无法下载，尝试切换网络环境或者从安装有科学上网工具的设备上拷贝（⚠️注意钓鱼软件与木马！）

2. 导入订阅  

    打开下载的客户端，点击侧栏的`订阅`界面，将在机场获取的订阅链接直接粘贴到输入框，随后点击`导入`即可。这部分内容通常在机场上会有清晰的使用文档可供参考。

3. 启用代理  

    进入侧栏的`设置`界面，开启`系统代理`选项，即可启用代理；可视情况决定是否开启其余功能。


<!-- ## 自建配置 -->
<!-- [ ] Clash 自建配置 -->
<!-- >[打造自己的 Clash 配置并提供订阅](https://yizhimengxin.me/2022/10/27/%E6%89%93%E9%80%A0%E8%87%AA%E5%B7%B1%E7%9A%84Clash%E9%85%8D%E7%BD%AE%E5%B9%B6%E6%8F%90%E4%BE%9B%E8%AE%A2%E9%98%85/) -->


[^1]: [🕊 纵使千山多万壑，犹有青鸾踏云间 | archlinux 简明指南](https://arch.icekylin.online/guide/rookie/transparent.html#%F0%9F%95%8A-%E7%BA%B5%E4%BD%BF%E5%8D%83%E5%B1%B1%E5%A4%9A%E4%B8%87%E5%A3%91-%E7%8A%B9%E6%9C%89%E9%9D%92%E9%B8%BE%E8%B8%8F%E4%BA%91%E9%97%B4)

[^2]: [透明代理#Clash | archlinux 简明指南](https://arch.icekylin.online/guide/rookie/transparent#clash)
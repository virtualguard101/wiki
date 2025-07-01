---
title: docker-compose + nginx快速构建个人站点
date: 2025-04-26 23:28:57
description: >
  本文主要讲解如何从零开始利用docker-compose + nginx快速构建一个个人站点；并利用Github Action实现文章部署自动化；最后是如何使用certbot为站点自动化申请ssl证书。整套配置流程做下来用时基本上不会超过3天。
# sticky: 1
authors:
  - virtualguard101
categories: 
  - Projects
tags: 
  - web开发
  - docker
---

**本文主要讲解如何从零开始利用docker-compose + nginx快速构建一个个人站点；并利用Github Action实现文章部署自动化；最后是如何使用certbot为站点自动化申请ssl证书。整套配置流程做下来用时基本上不会超过3天**

起因是我决定搭建一个个人站点用于模块化整合资源，在搜罗主页主题时因为部署简单相中了[remio-home | kasuie](https://github.com/kasuie/remio-home)，有多简单呢？简单到只需要进行一些及其简单的配置（cv大法可用）后，在服务器上输入一行`docker-compose up -d`即可。结合大佬的一些建议和我自己的一些 ~~偷懒~~ 自动化的想法，便有了下文。

如题，本文主要讲解如何从零开始在一台云服务器上利用docker-compose + nginx快速构建一个个人站点。得益于强大的现代化工具链以及开源社区的支持，我们完成这个简易项目所需的计算机理论基础并不多，甚至可以说是几乎为零，只需要知道文档应该怎么读，如何正确打开开发中的“cv大法”来为自己的自动化工具链编写配置文件。当然，最好有一点web开发的基础，这样在遇到意料之外的问题时不至于束手无策。

<!-- more -->

通过该项目你会了解到以下内容：

- **1. 远程服务器的基础使用**  
- **2. docker、docker-compose部署服务的基础操作**  
- **3. web开发实现原理基础——静态资源部署**  
- **4. hexo静态网页生成工具的使用**  
- **5. Github Action配置自动化部署**  
- **6. nginx基础配置（反向代理、二级域名）**  
- **7. 在容器内使用certbot申请ssl证书，并通过定时任务自动化续签**

下面是完成该项目所需的基础条件：

- 一台服务器
- 一个有效域名

**服务器**可在云服务器运营商处租用。国内比较可靠的运营商有阿里云、腾讯云等。

**域名**同样需要在运营商购买，也可通过特殊手段申请免费域名（不过免费申请的域名如有人出钱购买就会被回收）。获得域名后根据DNS云解析平台的文档进行解析配置即可。

## 准备工作

### 部署环境
服务器的初始配置可参考这篇文章[远程服务器的基础使用](https://note.virtualguard101.xyz/notes/%E5%B7%A5%E5%85%B7/ssh/)，这里不再赘述。由于需要使用`docker`进行部署，我们需要先在服务器上安装一下docker。通过以下命令安装：

```bash
curl -fsSL https://get.docker.com | bash -s docker
sudo apt install docker-compose
```

将当前用户添加到docker用户组：

```bash
sudo groupadd docker # 若尚不存在 docker 组，则需先创建
sudo usermod -aG docker $USER
```

由于是通过容器部署服务，环境处于“隔离”状态，`nginx`无需下载安装，可通过镜像运行于容器中。

### 主页测试部署

首先挑选一个能够使用docker部署的web主页，这里我们以[remio-home | kasuie](https://github.com/kasuie/remio-home)为例。根据文档进行配置与部署，部署完成后访问对应端口，观察配置是否生效。

按照主题文档配置完`docker-compose.yml`后，将宿主机的端口改为80（http默认端口），`docker-compose down && docker-compose up -d` 或 `docker-compose restart` 重启服务，通过外网设备进行访问，正常情况下和本地访问结果无异。也可通过端口转发在本地主机进行测试访问，具体这里不展开。

在通过外网设备进行访问时，若先前配置了DNS云解析，可通过域名进行访问。

## 静态网页资源测试

### hexo基础使用
互联网中有着数不胜数的静态网页生成工具，这里我们使用[hexo](https://hexo.io/zh-cn/)。

首先进入[主题选择页](https://hexo.io/themes/)选择几个心仪的主题，随后根据主题文档和官方文档构建静态站点目录和安装依赖。然后还是各个配置文件的修改与测试，这个过程相对枯燥且繁琐。

需要注意的是，有些主题在后面的部署过程中可能会出现各种各样的兼容性问题，遇到无法暂时解决的，可以更换主题。

配置完主题后，通过`hexo s`命令测试生成静态网页，通过浏览器访问`localhost:4000`生成网页，查看是否符合预期。确认无误后，即可进入部署阶段。

## 部署

### Github Page + 用户自定义域名

有Github Page静态网页部署经验的同志对此应该不陌生，配合hexo的[一键部署](https://hexo.io/zh-cn/docs/one-command-deployment)使用起来方便到不能再方便了，详情这里不再展开。针对此部署方法，就算不想看官方文档，网络上也有数不胜数的教程。

这种部署方法固然方便，但只能部署（.github.io）或绑定到一个域名下（custom domain），若想要通过多个二级域名来分隔部署web资源，或是将来可能需要部署其他无法通过Github Page来部署的服务（如用户登陆服务、数据库服务等），这样的方法就会极大地限制web服务的可扩展性。简单来说，是否选择该部署方法取决于部署需求，确认只有存放静态资源的需求则该方法操作便捷且功能绰绰有余。

### docker-compose + nginx

废话说了这么多，接下来正片开始。

在现代 web 开发中，使用 Nginx 代理不同的子域名到相应的 web 项目是一个常见的需求。同时，为了使我们的web服务能够与使用docker容器部署的主页处于同一个服务端口上，我们就需要把处于不同容器的web服务通过docker-compose合成为一个，并映射到宿主机的80端口上以供外界访问。

看上去很复杂，但事实上，由于我们并不需要了解容器内的服务具体在做些什么，理论上，我们只需要简单了解docker的工作原理以及`docker-compose.yml`和`nginx.conf`的配置规则即可实现前文提到的**一键部署**。

当然，缺点也很明显：根域名（主页）和各二级域名（web服务）均需要通过nginx进行转发，且“处于一条绳上”，一旦nginx的配置或是其本身出现问题，所有写在配置里的服务就直接给一锅端了。

~~当然这也契合部分人开（摸）发（鱼）习惯，很喜欢容器化开发者中流传的一句话：“我就喜欢配一天环境啥也不干的感觉☝🤓”~~

两个配置文件的编写上，如果是单纯的多个二级域名的配置，网络上的教程一抓一大把，但我们的这个项目的难点就在于此，因为我们还要把先前就已成功部署的主页服务也融合进来，如何正确将它们配置到同一个端口上对于不熟悉docker和第一次接触nginx的人算的上是个挑战（比如我）。

然而经过一段时间的尝试（AI+），我们就能发现这并非什么难事：

#### docker配置

以下配置模板仅供参考

```yml
version: "3.8"

services:
  remio-home:
    image: kasuie/remio-home
    container_name: remio-home
    ports:
      - "8080:3000"
    environment:
      - GTMID=.....
      - PASSWORD=.....
      - AMAP_KEY=.....
    volumes:
      - ./remio-home/config:/remio-home/config
      - ./remio-home/icons:/remio-home/public/icons
      - ./remio-home/fonts:/remio-home/public/fonts
    networks:
      - web_network
    restart: unless-stopped

  nginx:
    image: nginx:latest
    container_name: nginx
    ports:
      - "80:80"
      # - "443:443"
    volumes:
      - ./nginx/conf.d/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./nginx/log:/var/log/nginx
      # - ./certbot/www:/usr/share/certbot/www:ro
      # - ./certbot/ssl:/etc/letsencrypt:ro
    depends_on:
      - subsite1
      - subsite2
      - subsite3
    networks:
      - web_network
    command:  nginx -g 'daemon off;'

  # certbot:
  #   container_name: certbot
  #   image: certbot/certbot
  #   volumes:
  #     - ./certbot/www:/usr/share/certbot/www:rw #http验证目录，可设置rw可写，与nginx容器对应的宿主机目录时一致的
  #     - ./certbot/ssl:/etc/letsencrypt:rw #证书位置，同上，注意不要只映射到live，而是它的上一级

  subsite1:
    image: nginx:latest
    container_name: subsite1
    volumes:
      - ./sub-sites/subsite1/public:/usr/share/nginx/html
    networks:
      - web_network

  subsite2:
    image: nginx:latest
    container_name: subsite2
    volumes:
      - ./sub-sites/subsite2/public:/usr/share/nginx/html
    networks:
      - web_network

  subsite3:
    image: nginx:latest
    container_name: subsite3
    volumes:
      - ./sub-sites/subsite3/public:/usr/share/nginx/html
    networks:
      - web_network

networks:
  web_network:
    driver: bridge

```

docker配置的关键在于`volumes`，即**挂载卷**的路径配置。

在nginx附属服务（二级域名）的配置中，挂载卷参数的`:`前填入的是需要挂载的宿主机路径，`:`后是容器内的映射路径。这里我们需要挂载的路径是各个二级域名下需要“展示”的**前端文件**，即前文中提到的由静态网页生成工具生成的**静态资源**。

在hexo中，我们通常使用命令`hexo cl && hexo g`清理旧版本的静态文件并生成新版，生成的静态文件默认处于各项目根目录的`public`路径下。

静态资源的整理可在任意主机上进行，部署时只需确保由静态网页生成的静态资源处于服务器上并挂载到容器的正确路径下即可。通常情况下，为确保隐私安全，静态文件的整理工作我们一般在本地主机上进行。在后续的章节中我们会介绍如何通过配置Github Action实现使静态文件从本地自动化部署至服务器上。

#### nginx配置

`nginx.conf`的配置是该项目的核心，若出现错误导致部署无法进行，70%的问题出在nginx上，而nginx的问题有80%出在配置上（数据是瞎编的😋，但问题是真的）。

以下是`nginx.conf`的参考配置，受限于篇幅，只列举主页及其中的一个二级域名的配置：

```conf
events {}

http {
    ; server {
    ;     listen 80;
    ;     # listen [::]:80;

    ;     server_name  virtualguard101.xyz;#域名
    ;     server_tokens off;

    ;     #配置http验证可访问
    ;     location /.well-known/acme-challenge/ {
    ;         #此目录都是nginx容器内的目录，对应宿主机volumes中的http验证目录，而宿主机的又与certbot容器中命令--webroot-path指定目录一致，从而就整个串起来了，解决了http验证问题
    ;         root /usr/share/certbot/www;
    ;     }
    ;     #http跳转到https
    ;     location / {
    ;         return 301 https://$host$request_uri;
    ;     }
    ; }

    server {
        listen 80;
        server_name virtualguard101.xyz;

        location / {
            proxy_pass http://remio-home:3000;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }       
        # 强制HTTPS重定向
        # return 301 https://$host$request_uri;
    }

    ; server {
    ;     listen 443 ssl http2;
    ;     server_name virtualguard101.xyz;

    ;     ssl_certificate /etc/letsencrypt/live/virtualguard101.xyz/fullchain.pem;
    ;     ssl_certificate_key /etc/letsencrypt/live/virtualguard101.xyz/privkey.pem;

    ;     location / {
    ;         proxy_pass http://remio-home:3000;
    ;         proxy_set_header Host $host;
    ;         proxy_set_header X-Real-IP $remote_addr;
    ;         proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    ;         proxy_set_header X-Forwarded-Proto $scheme;
    ;     }
    ; }


    ; server {
    ;     listen 80;
    ;     # listen [::]:80;

    ;     server_name  projects.virtualguard101.xyz;#域名
    ;     server_tokens off;

    ;     #配置http验证可访问
    ;     location /.well-known/acme-challenge/ {
    ;         #此目录都是nginx容器内的目录，对应宿主机volumes中的http验证目录，而宿主机的又与certbot容器中命令--webroot-path指定目录一致，从而就整个串起来了，解决了http验证问题
    ;         root /usr/share/certbot/www;
    ;     }
    ;     #http跳转到https
    ;     location / {
    ;         return 301 https://$host$request_uri;
    ;     }
    ; }

    server {
        listen 80;

        server_name projects.virtualguard101.xyz;

        location / {
            proxy_pass http://projects:80;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # return 301 https://$host$request_uri;
    }

  ;   server {
  ;       listen 443 ssl http2;
  ;       server_name projects.virtualguard101.xyz;

  ;       ssl_certificate /etc/letsencrypt/live/projects.virtualguard101.xyz/fullchain.pem;
  ;       ssl_certificate_key /etc/letsencrypt/live/projects.virtualguard101.xyz/privkey.pem;

  ;       location / {
  ;           proxy_pass http://projects:80;
  ;           proxy_set_header Host $host;
  ;           proxy_set_header X-Real-IP $remote_addr;
  ;           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
  ;           proxy_set_header X-Forwarded-Proto $scheme;
  ;       }
  ;   }
  }
```

nginx配置的关键在于反向代理转发的配置，这是nginx一个十分重要的特性，利用它能够实现nginx中许多核心功能，如负载均衡、websocket代理等。对于我们目前的项目需求，暂时无需使用到这些较为复杂的功能，我们现在只需弄明白参数`proxy_pass`具体是做什么的，以及其最为基础的配置规则，剩下的交给cv大法即可。

在nginx配置中，`proxy_pass`用于将客户端的请求代理到指定的后段服务器，简单理解就是把请求作了一次转发。其基础语法如下：

```conf
location /path/ {
    proxy_pass http://backend_server:port;
}
```

该配置会将客户端上的请求转发至运行在`port`端口上名为`backend_server`的服务。结合上面的配置模板进行理解，我们可以发现主页服务在前面的docker配置中我们“恰好”将其配置在了容器的`3000`端口上，而其他的二级域名（nginx服务）我们均将其配置在了容器的`80`端口上，那么在外网设备（客户端）通过域名访问对应服务时，nginx就会将访问请求转发到对应的端口上。

那么nginx怎么知道客户发送了访问请求？这就是**监听**要做的事。http服务默认通过`80`端口访问，通过配置`listen`参数我们可以使nginx服务监听`80`端口，就像饭点食堂阿姨站在特定窗口等着你去打饭一样。

配置模板中注释掉的模块是https的配置，由于我们还未申请ssl证书，现在只能先使用http。关于ssl证书的申请我们也会在后续的章节介绍。

docker 与 nginx的配置完成后，我们便可通过`docker-compose up -d`命令进行服务部署，此时正常情况下网页已经可以通过外网设备访问。若出现问题，一般情况下会反映在各个服务容器上，可通过`docker-compose logs`命令查看日志信息。

## Github Action自动化部署

~~作为一个懒人~~为了提高效率，写个自动化配置把部署的工作交给计算机来做自然是个不错的方法。Github Action为我们提供了一个简单的自动化构建平台，通过模块化的配置和与git远程仓库结合的管理方式极大简化了配置难度，同时集成了版本控制。

Github Action自动化的配置通常位于子站点项目根目录的`.github/workflows`下。由于自动化部署的方式多种多样，配置自然也同理，故以下配置模板仅供参考。

```yml
name: Deploy Subsite

on:
  push:
    branches: [main]

jobs:
  hexo-build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
        
      - name: Setup Node
        uses: actions/setup-node@v3
        with:
          node-version: 18
          
      - name: Install Dependencies
        run: |
          npm install -g hexo-cli
          npm install
        
      - name: Build Site
        run: hexo clean && hexo generate
        
      - name: Deploy to Server
        uses: appleboy/scp-action@v0.1.7
        with:
          host: ${{ secrets.SERVER_IP }}
          username: ${{ secrets.SERVER_USER }}
          key: ${{ secrets.SSH_KEY }}
          source: "public/*"
          target: "/home/<user>/sub-sites/<subsites_dir>/"
          
      # - name: Refresh Nginx
      #   uses: appleboy/ssh-action@v1.0.0
      #   with:
      #     host: ${{ secrets.SERVER_IP }}
      #     username: ${{ secrets.SERVER_USER }}
      #     key: ${{ secrets.SSH_KEY }}
      #     script: |
      #       docker exec nginx_main nginx -s reload
```

配置模板中，`Deploy to Server`模块是配置中较为核心的模块。该模块利用**scp**工具将生成的静态文件传送至站点服务器的指定路径下，其中的以`secrets`开头的三个变量分别是服务器的ip地址、用户与ssh私钥，通过仓库的`settings` >> `secrets and variables` >> `actions` 配置。
ssh私钥需在服务器上生成。

通过上述自动化配置，在每次我们将本地仓库的更改推送至远程仓库时，github会自动在后台使用hexo生成静态文件，并通过scp将其发送至服务器的指定路径下。

至此，我们仅需在本地的各个站点项目路径下修改配置或撰写文章，并将更改推送至github远程仓库，即可实现站点资源的自动化部署。

## ssl认证与https模块配置（可选）

经过上面五节的配置工作，我们的站点的雏形已经完成，接下来就是最后的收尾工作。关于ssl证书与https，尽管我们并不认为它是一个网页的必要组成部分，但我们还是强烈建议为自己的站点配置ssl证书与https模块以增强安全性与可扩展性。得益于[certbot](https://certbot.eff.org/)的ssl证书免费申请功能，我们已经能够较为容易地完成这项工作。

### 首次申请ssl证书

由于在该项目中，我们所有的服务均配置于docker容器中，因此我们同样需要将certbot的服务功能配置进docker-compose.yml中以实现后续的ssl证书自动化续签。事实上，certbot官方是不建议使用docker作为certbot的服务载体的，详情可参考[Get Certbot with Docker](https://eff-certbot.readthedocs.io/en/stable/install.html#alternative-1-docker)

在配置前，首先需要拉取certbot的docker镜像：

```bash
docker pull certbot/certbot
```

随后将前文中`docker-compose.yml`中`certbot`模块的注释去掉，并将nginx挂载卷中有关certbot的路径的注释去掉。启动服务，并通过以下命令进行测试申请：

```bash
# --dry-run是只测试不实际生成; --webroot-path对应着certbot内的http验证目录;-d后面是域名;--rm是运行后接着删除，certbot容器不需要一直开启，只是启动下生成证书即可
docker compose run --rm  certbot certonly --webroot --webroot-path /usr/share/certbot/www/ --dry-run -d [your_domain]
```

按照提示输入邮箱信息，若返回结果`The dry run was successful`，则说明测试成功，即可将`--dry-run`去掉以进行实际的证书获取：

```bash
docker compose run --rm  certbot certonly --webroot --webroot-path /usr/share/certbot/www/ -d [your_domain]
```

申请成功后，可通过以下命令查看所有已申请的证书：

```bash
docker compose run --rm certbot certificats
```

确认证书信息无误后即可开始nginx`https`模块的配置。与`docker-compose.yml`类似，将`nginx.conf`配置模板中https模块的注释去掉，同时将原来未注释的http模块注释掉，`docker-compose down && docker-compose up -d`重启服务。完成后通过外网设备访问网页，正常情况下，网址栏会显示该网页是安全的。

### ssl证书自动化续签

使用certbot一个很大的原因就是因为其可通过配置**定时任务**进行ssl证书的自动化续签。具体配置十分简单，一个bash的问题：

创建bash脚本，并写入定时申请命令：

```bash
vim sslrenew.sh   # 创建脚本文件

# 写入命令
docker compose run certbot renew
```

`crontab -e`添加定时任务，每个月第一天凌晨四点执行，也可根据自己情况进行配置：

```bash
0 4 1 * * ~/sslrenew.sh
```

配置完成后，可通过`crontab -l`命令查看配置的定时命令，确认配置是否写入。

**BASE END**

到此为止，所有的基础配置也就完成了。此时我们的个人站点已经可以被世界上所有接入互联网的设备访问了，同时我们也可根据个人需求为站点添加各种各样的功能与服务。

主要参考文献：
- [docker部署nginx多级子域名 | 蓝易云](https://cloud.tsyidc.com/web/822.html)
- [docker部署certbot与nginx来获取ssl证书添加https及自动更新 | vishun](https://www.cnblogs.com/vishun/p/15746849.html)
- [使用Certbot自签SSL证书 | kasuie](https://kasuie.cc/article/22)

---

## 增添服务

既然我们都选择了使用云服务器来构建我们的个人站点，那么仅使用它来存放静态页面显然是大材小用。对于站点功能的丰富，还是那句话，在成熟工具链丰富的现代开发环境下，并不是什么很难的事情。很多时候，我们只需要正确打开别人写好的文档即可。

对于功能扩展这部分的内容，更多的还是将目光放在部署工具供应者的使用文档上，这里只基于该文介绍的站点部署方法简单介绍一下我个人摸索出的**标准化部署流程**以及部署过程中可能碰到的**问题**。

### 标准化部署流程

以下流程为个人在实际部署过程中摸索出的不同服务部署过程的共通点，仅供参考。

现在，假设我们想要在服务器上部署一个AI对话服务，那么我们便可遵循以下流程进行服务的配置及部署：

#### 一、工具链选取及基础配置工作

- **0. 选取对应的服务部署工具链，查阅官方文档并结合当前环境分析部署可行性。**

我们想要在服务器上部署一个AI对话服务，那么结合当前部署环境，我们就应该在网络上查找对应的`docker`镜像（image）。这里我们使用[LLM Frontend | SillyTavern](https://github.com/SillyTavern/SillyTavern)进行部署。

该框架具有docker镜像，且支持使用docker-compose部署，符合当前的环境要求，且部署难度和成本相对较低。

- **1. 拉取docker镜像（可跳过）**

执行以下命令以获取待部署的docker镜像：

```bash
docker pull ghcr.io/sillytavern/sillytavern:latest
```

在使用docker-compose进行部署时，若`docker-compose.yml`配置无误，镜像会自动拉取。执行这一步主要是为了提前判定镜像是否处于可获取的状态。

- **2. 根据工具文档及个人需求进行配置文件的配置或修改**

项目主页：[SillyTavern - LLM Frontend for Power User](https://sillytavern.app/)
项目仓库：[SillyTavern](https://github.com/SillyTavern/SillyTavern)

#### 二、docker-compose.yml配置

由于docker的容器环境是我们站点的部署基础，这部分的配置便显得尤为重要。可参考以下步骤进行配置：

- **1. 依照文档给出的配置框架结合部署环境进行基础配置**

官方给出的`docker-compose.yml`如下：

```yml
services:
  sillytavern:
    build: ..
    container_name: sillytavern
    hostname: sillytavern
    image: ghcr.io/sillytavern/sillytavern:latest
    environment:
      - NODE_ENV=production
      - FORCE_COLOR=1
    ports:
      - "8000:8000"
    volumes:
      - "./config:/home/node/app/config"
      - "./data:/home/node/app/data"
      - "./plugins:/home/node/app/plugins"
      - "./extensions:/home/node/app/public/scripts/extensions/third-party"
    restart: unless-stopped
```

我们可结合部署环境与部署需求对`environment`、`volumes`、`port`中的值进行修改，同时还需注意`docker-compose.yml`与服务自身配置（`config.yaml`）的对应关系。比如，针对`port`参数，`config.yaml`中默认将服务映射在`8000`端口上，若两个配置不对应，在访问时就会遇到`502(Bad Gateway)`错误。

还有一点需要注意：由于nginx服务也运行于容器中，故在此项目的实际配置与部署过程中，真正有效的端口参数是`port`参数的**容器服务端口**。

- **2. 网络关系配置**

容器化技术的一大亮点在于不同服务容器环境相互独立的情况下也可通过形形色色的配置建立起各个容器间的联系。配置这些东西过程被厌恶容器技术的人所诟病，这些人认为该过程徒增工作复杂度，殊不知这是被他们所忽略的本职工作。

服务间网络关系的配置也是上述关系配置中的一环，通过前文的配置我们知道，各个服务的网络配置通过`networks`参数控制，而在该项目中我们统一使用`web_network`作为各个服务的网络配置参数。故在官方文档原有框架的基础上，我们需要为模块追加如下配置：

```yml
networks:
  - web_network
```

<!-- 否则会导致sillytavern容器未连接到web_network网络，出现容器错误 -->

- **3. 服务依赖关系**

和网络关系相比，不同服务的依赖关系在体现各个服务容器之间的联系上更加直接。

在本项目中，由于需要使用nginx对各个服务进行转发，依赖关系便体现在各个部署在二级域名上的服务与nginx服务上。完成`sillytavern`服务的配置后，我们需要在nginx模块的`depend_on`参数追加如下配置：

```yml
depend_on:
  - .....
  - sillytavern
```

<!--显式声明容器依赖关系，确保sillytavern先于nginx启动，否则会出现nginx容器错误 -->

#### 三、nginx-https模块配置

- **1. 反向代理基础配置（http模块）**

依照前文基础配置的`nginx.conf`模板进行修改即可。

- **2. ssl证书申请及https模块配置**

遵循`复制模板`-`注释`-`解除注释`-`申请`-`解除注释`的“五步原则”。注释及解除注释操作的对应模块如下：

**注释**：注释**http反向代理模块**  
**第一次解除注释**：解除**http ACME验证挑战模块**注释  
**第二次解除注释**：解除**https反向代理模块**注释

--- 
完成以上三大步，8小步的配置与部署操作，部署工作基本也就完成了。

## 常见问题

部署过程中经常会碰到一些奇奇怪怪的问题，特别是不熟悉docker、nginx配置规则的初学者。下面是我在部署过程中遇到的问题的汇总。

### nginx错误、服务访问错误

通常表现为nginx容器无法正常运行，网页访问`500`、网页访问`502`等，具体原因可能有如下几种：

- `nginx.conf`配置错误

通常是反向代理模块中`proxy_pass`参数的配置有误，比如后端服务的**端口**或**服务名称**与`docker-compose.yml`中配置的不对应。

- `docker-compose.yml`配置错误

通常是前文提到的不同容器间关系的配置有误或者缺失，特别是nginx服务与其他需要通过nginx服务进行转发的服务之间的关系。如`networks`配置、容器依赖关系配置；以及前文提到的服务配置与docker-compose配置的对应关系问题，如服务端口的对应问题。

### ssl证书申请（certbot）错误

通常表现为无法申请ssl证书、申请证书后访问显示“~~https~~网页不安全”等，具体原因可能有如下几种：

- 无法申请ssl证书（certbot无法正常运行）

**1. 同一域名在短时间内申请次数过多**

**2. `nginx.conf`中http ACME验证挑战模块配置有误**

**3. 在特殊环境（如需要进行用户验证）下未注释http反向代理模块导致无法访问服务的问题（如`401`）**

**4. 域名本身无法正常访问（`5xx`、`4xx`）**

- 访问问题（提示网站不安全）

**1. 申请ssl证书时信息有误，如二级域名名称错误**

**2. `nginx.conf`中https模块二级域名（server_name）配置有误**

**3. `nginx.conf`中https模块证书路径有误**

关键在与证书与域名的对应关系是否有误。

---
**END**


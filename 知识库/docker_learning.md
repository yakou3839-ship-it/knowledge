

# Docker 零基础完整教程（概念+作用+安装+命令速查）

# 一、什么是 Docker

## 1. 核心定义

Docker 是一款**容器化工具**，基于 Linux 内核技术（Namespace、Cgroups、UnionFS），可以把程序、依赖、运行环境打包成标准化**容器**。

简单理解：容器是轻量级、独立隔离的运行单元，自带全套运行环境；和虚拟机相比，容器共享宿主机内核，秒级启动、资源占用极低。

## 2. 四大核心概念

- **镜像（Image）**：只读模板，是容器的“安装包”，包含代码、运行库、配置、运行环境，例如 nginx、mysql 官方镜像。
- **容器（Container）**：镜像运行起来的实例，可自由创建、启停、删除，容器之间环境完全隔离、互不冲突。
- **Dockerfile**：自定义脚本文件，用于手动编写规则、构建专属镜像。
- **Docker Hub**：官方公共镜像仓库，海量开源镜像可直接拉取使用。

# 二、Docker 有什么用（核心优势）

解决开发运维中的各类经典痛点，是目前服务部署、微服务架构的标配工具：

## 1. 统一运行环境，根治环境不一致问题

开发、测试、生产环境完全统一，彻底解决“本地能跑、服务器报错”的问题，所有依赖、环境配置全部打包进镜像。

## 2. 极致轻量化，资源利用率极高

**同等硬件条件下**，容器共享宿主机内核，仅隔离业务进程，单容器最低仅占用几十MB内存，一台普通服务器可稳定运行上百个轻量容器；而虚拟机需要搭载完整独立操作系统，资源开销极大，同配置服务器仅能运行数台虚拟机。

## 3. 一键部署，分发便捷

镜像打包完成后，可在任意安装了Docker的设备上拉取运行，无需重复安装软件、配置环境，大幅提升部署效率。

## 4. 服务完全隔离，杜绝版本冲突

不同项目、不同版本的软件（如MySQL5.7/8.0、Python3.8/3.11）可独立运行在不同容器中，端口、文件系统完全隔离，互不干扰。

## 5. 适配微服务与集群架构

前后端分离、微服务、K8s集群的底层核心全部基于Docker容器化实现，是云服务、自动化运维的基础。

# 三、Docker 与虚拟机对比（清晰区别）

| 特性       | Docker容器               | 虚拟机                   |
| :--------- | :----------------------- | :----------------------- |
| 内核依赖   | 共享宿主机内核           | 拥有独立完整系统内核     |
| 启动速度   | 秒级启动                 | 分钟级启动               |
| 资源占用   | 极低，仅占用业务进程资源 | 极高，需占用系统完整资源 |
| 隔离级别   | 进程级轻量隔离           | 硬件级强隔离             |
| 单机承载量 | 可运行上百个             | 仅可运行数个至十几个     |

# 四、Docker 极简安装教程

## 1. Windows / Mac

直接下载安装 **Docker Desktop**，启动软件后即可使用完整Docker引擎。

桌面版可以直接在一个文件夹中运行`docker compose up -d`来启动一个yml文件（多容器编排）

## 2. Linux 服务端✅️

```bash
# Ubuntu 安装
apt update && apt install docker.io

# CentOS 安装
yum install docker

# 启动
systemctl start docker
# 停止
systemctl stop docker
#重启
systemctl restare docker
#设置开机启动
systemctl enable docker
#取消开机启动
systemctl disable docker
#查看docker服务状态
systemctl status docker
# 验证安装成功
docker --version
docker run hello-world
```

# 五、Docker添加加速器✅️

> docker自带的仓库几乎无法使用
>
> 如果采用docker桌面版可以直接用vpn

```bash
#在root/etc/docker/下面创建一个daemon.json的文件✅️
cd /etc/docker
touch daemon.json

#往里面写入配置文件，每个加速源都不一样，具体上网搜✅️
#这里有个小坑，不加dns配置不成功

#重载配置+重启docker✅️
systemctl daemon-reload
systemctl restart docker
```



# 六、Docker 全套命令速查表（实操必备）

## 1. 基础环境查看命令✅️

```bash
docker --version          # 查看Docker版本
docker info               # 查看Docker详细信息（镜像、容器、存储、驱动）
docker help               # 查看全部命令帮助
docker 子命令 --help      # 查看单个命令帮助（例：docker run --help）
```

## 2. 镜像（Image）操作命令

**基础命令**

```bash
# 搜索、拉取镜像✅️
docker search 镜像名                  # 搜索仓库镜像
docker pull 镜像名                    # 拉取最新版镜像
docker pull 镜像名:版本               # 指定版本拉取镜像

# 查看本地镜像✅️
docker images                        # 列出本地所有镜像
docker images | grep python          # 过滤指定镜像
docker image ls                      # 等价 docker images
docker images -q                     #查看所用镜像id

# 镜像重命名打标签，会产生一个新的镜像✅️
docker tag 镜像原名 镜像重命名:版本重命名

# 删除镜像✅️
docker rmi 镜像ID/镜像名             # 删除指定镜像
docker image prune                   # 清理悬空无标签镜像
docker rmi $(docker images -q)       # 删除全部本地镜像（慎用）

# 镜像离线迁移（导出/导入）✅️
docker save -o 压缩名.tar 要导出的镜像名:镜像标签名      # 导出镜像为tar包，这里默认导出在当前位置下
docker save -o /docker/压缩名.tar 要导出的镜像名:镜像标签名  #导出在指定位置下
docker save -o 总压缩名.tar 镜像1:标签1 镜像2:标签2 ....
docker load -i nginx.tar             # 从tar包导入镜像
```

**高级命令（构建自己的镜像）**

```bash
# 构建镜像✅️
docker build -t 镜像名:版本名 .           # 基于当前目录Dockerfile构建镜像并命名打标签，.代表当前目录
docker build -f ./docker/Dockerfile -t app .  # 指定Dockerfile文件路径构建

docker build                            # 构建镜像主命令
-f ./docker/Dockerfile                  # -f：指定Dockerfile文件路径
# 当前目录下 docker 文件夹里的 Dockerfile，不是默认当前目录的Dockerfile
-t app                                  # -t：给镜像打标签，格式 名称:版本
# 这里只写 app，等价于 app:latest（默认latest标签）
.                                       # 构建上下文 = 当前执行命令的目录
```

> 一句话结论
>
> **整个 project 文件夹 ≠ 镜像**，project 只是本地源码目录；执行 `docker build` 生成的 `app:latest` 才是镜像。
>
> 1. **分清三个概念**
>
>    **①project（本地项目文件夹）**
>
>    你电脑上的源码、Dockerfile、配置文件，只是一堆本地文件，没有运行环境，不能	直接启动。
>
>    ```
>    project/
>      docker/Dockerfile
>      app.py
>      requirements.txt
>    ```
>
>    **②构建上下文（命令最后的 `.`）**
>    `docker build ... .` 最后的 `.` 就是 project 根目录，Docker 会读取这里的所有文件，作为构建原料。
>
>    **③镜像（image）**
>    执行 build 后，Docker 引擎把基础系统 + 复制的代码 + 安装的依赖打包成**只读镜像**，存在本地 Docker 仓库，用 `docker images` 能查到。
>    本例镜像名：`app`（完整 `app:latest`）
>
> 2. **两者关系**
>
>    project 是**原材料**，镜像才是**成品**：
>
>    - build 读取 project 里的代码、Dockerfile；
>
>    - 按照 Dockerfile 步骤一层层打包；
>
>    - 输出独立的 Docker 镜像；
>
> 3. **project 文件夹删掉，镜像依然存在。**
>
> 4. **直观验证**
>
>    ①构建镜像
>
>    ```
>    docker build -f ./docker/Dockerfile -t app .
>    ```
>
>    ②查看镜像（能看到app）	  
>
> 	```
>	docker images
> 	```
> 	
> 	③删除本地 project 整个文件夹
>	
> 	④依旧能基于镜像启动容器
>	
> 	```
>	docker run -p 5000:5000 app
> 	```
>	
> 	⑤证明镜像和本地项目文件夹相互独立。
>	
> 4. 补充：容器和镜像区别
> 
> - 镜像：只读模板，相当于安装包；
>- 容器：镜像运行出来的实例，相当于运行中的软件。

## 3. 容器（Container）核心命令（最高频）

### 3.1 启动容器核心参数

通用模板：`docker run [参数] 镜像名`

> 如果最后面跟了个 /bin/bash 可以在创建容器后直接进入到容器内部

- **-d**：后台守护进程运行
- **--name**：自定义容器名称✅️
- **-p 宿主机端口:容器端口**：端口映射
- **-v 宿主机目录:容器目录**：数据挂载持久化✅️
- **--restart always**：开机自启、容器退出自动重启
- **-e KEY=VALUE**：设置容器环境变量
- **-it**：交互式终端，进入容器内部✅️
- **--rm**：容器停止后自动删除（临时测试专用）
- **-volumes-from**：复用另一个容器已经挂载好的全部数据卷（volume）、绑定挂载（bind mount）✅️   （用得少）

### 3.2 容器启停、查看、删除

```bash
# 查看容器✅️
docker ps                  # 查看正在运行的容器
docker ps -a               # 查看所有容器（含已停止）
docker ps -q               # 仅输出容器ID
docker container ls        # 等价 docker ps

# 启停重启容器✅️   容器名可以后面堆积，一次操作多个
docker stop 容器名/ID      # 优雅停止容器   
docker kill 容器名/ID      # 强制杀死运行中容器
docker start 容器名/ID     # 启动已停止容器
docker restart 容器名/ID   # 重启容器

# 删除容器✅️   容器名可以往后推挤，一次删除多个
docker rm 容器名/ID                 # 删除已停止容器
docker rm -f 容器名/ID              # 强制删除运行中容器
docker container prune              # 批量清理所有停止的容器
docker rm $(docker ps -a -q)        # 删除所有容器（慎用）
```

### 3.3 容器调试、日志、详情查看

```bash
# 进入容器终端✅️
docker exec -it 容器名 bash         # 进入运行中容器（推荐，退出不停止容器）
#用exit退出，进入容器中无法再使用docker等命令，只能基于容器的环境运行一些东西
docker attach 容器名                # 附着容器输出（不推荐，退出即停容器）

# 查看容器日志✅️（但是不知道日志怎么看）
docker logs 容器名                  # 查看容器全部日志
docker logs -f 容器名               # 实时滚动查看日志
docker logs --tail 100 容器名       # 仅查看最后100行日志

# 查看容器详细信息✅️ （但是不知道怎么看）
docker inspect 容器ID               # 查看容器完整元数据（IP、挂载、端口等）
docker inspect -f '{{.NetworkSettings.IPAddress}}' 容器ID  # 仅输出容器IP
```

### 3.4 宿主机与容器文件互传✅️

#### **方法一手动**✅️

```bash
docker cp /宿主机路径/文件 容器名:/容器路径    # 宿主机文件拷贝到容器
docker cp 容器名:/容器路径/文件 /宿主机路径    # 容器文件拷贝到宿主机
```

#### **方法二自动同步**✅️

**①Bind Mount 绑定挂载**✅️

```bash
#语法特征：冒号左侧是宿主机绝对路径，以 / 开头
-v /宿主机路径:/容器内绝对路径[:权限]
# 示例
-v /home/yakou/code:/app:ro
#如果要挂载多个卷，直接继续 -v 
```

> 底层逻辑：直接把宿主机任意目录 / 文件**原封不动挂载进容器**，Docker 不接管、不管理该目录
>
> 要注意当前操作的环境是虚拟机（宿主机）还是容器，还是什么，每个位置操作不一样

**②Named Volume（命名数据卷，Docker 托管卷）**✅️

```bash
#语法特征：冒号左侧是纯名称，不含 / 斜杠
-v 自定义卷名:/容器内绝对路径[:权限]
# 示例
-v flask-data:/app      
#如果要挂载多个卷，直接继续 -v 
```

> 底层逻辑：Docker 统一管理，数据固定存放于宿主
>
> `var/lib/docker/volumes/卷名/_data`，生命周期由 Docker 管控。
>
> 补充：匿名卷 `-v /app` 属于 Volume 分支，无自定义名称，自动生成随机 ID，极少使用。

#### 总结

> **Bind Mount**
> **优点：**
>
> - 宿主机路径可见，直接操作文件，开发调试方便；
> - 自定义存放位置，可挂载独立磁盘分区；
> - 备份、拷贝文件简单，直接 cp 目录即可。
>
> **缺点：**
>
> - 无 Docker 统一管理，docker volume 命令无法管控；
> - 权限跟随宿主机，经常出现容器内文件读写权限报错；
> - 挂载空宿主机目录会清空容器内原有文件；
> - 容易误删宿主机业务目录，风险高。
>
> **Named Volume**
> **优点：**
>
> - Docker 统一生命周期管理，查看、清理、迁移标准化；
> - 首次挂载自动复制镜像内文件，开箱即用；
> - 权限由 Docker 维护，数据库等服务极少权限异常；
> - 数据隔离，不会污染宿主机自定义业务目录，安全性更高；
> - 支持批量清理闲置存储。
>
> **缺点：**
>
> - 底层目录路径很深，不方便日常直接编辑文件；
> - Windows/Mac 环境下同样存在文件同步延迟；
> - 备份需要通过容器打包，不能直接复制文件夹。

## 4. 数据卷（Volume）✅️

> 这里指的仅是docker托管的数据卷（有固定的位置）✅️

```bash
docker volume ls                     # 列出所有数据卷
docker volume create vol-mysql       # 创建自定义命名数据卷
docker volume inspect vol-mysql      # 查看数据卷详细挂载路径
docker volume rm vol-mysql           # 删除指定数据卷
docker volume prune                  # 清理所有未使用的数据卷
```

**数据卷容器**（用的少了）✅️

> Named vloume方式永久保存数据；多个容器挂载同一个数据卷

```bash
#1.创建启动c3数据卷容器，使用-v参数设置数据卷
docker run -it --name=容器名 -v 数据卷名:容器目录绝对地址 镜像名 （/bin/bash自选）
#2.创建c1、c2容器挂载到c3容器上，使用-volumes-from参数设置数据卷
docker run -it --name=c1 --volumes-from c3 镜像名 （/bin/bash可选）
docker run -it --name=c2 --volumes-from c3 镜像名 （/bin/bash可选）
```

> 如果采用上述方式，数据全同步（c1、c2、c3与数据卷）
>
> 注意：删除c3后，c1和c2之间数据还是共享的，容器之间配置信息的传递，数据卷的生命周期一直持续到没有容器使用它为止。

## 5. 网络（Network）操作命令✅️（没用过）

```bash
docker network ls                    # 查看所有Docker网络
docker network create net-demo       # 创建自定义网桥网络
docker network connect net-demo 容器名 # 将容器加入指定网络
docker network disconnect net-demo 容器名 # 断开容器与网络连接
docker network rm net-demo           # 删除自定义网络
docker network inspect 网络名         # 查看网络详细信息
```

## 6. 系统垃圾清理命令✅️（没用过）

```bash
docker system df          # 查看镜像、容器、数据卷磁盘占用
docker system prune       # 清理停止容器、悬空镜像、无用网络
docker system prune -a    # 清理所有未使用的镜像、容器、网络（谨慎使用）
docker system prune --volumes # 连带清理无用数据卷
```

## 7.Docker上部署MySQL✅️

> 实例，辅助学习端口映射

**部署mysql步骤**

1. 搜索mysql镜像

   ```bash
   docker search mysql
   ```

2. 拉取mysql镜像

   ```bash
   docker pull mysql:版本号
   ```

3. 创建容器，设置端口映射、目录映射

   ```bash
   # 在/root目录下创建mysql目录用于存储mysql数据信息
   mkdir ~/mysql
   cd ~/mysql
   docker run -id \
   -p 3307:3306 \
   --name=c_mysql \
   -v $PWD/conf:/etc/mysql/conf.d \
   -v $PWD/logs:/logs \
   -v $PWD/data:/var/lib/mysql \
   -e MYSQL_ROOT_PASSWORD=123456 \
   mysql:5.7
   
   #参数说明：
   -p 3307:3306：将容器的 3306 端口映射到宿主机的 3307 端口。
   -v $PWD/conf:/etc/mysql/conf.d：将主机当前目录下的 conf/my.cnf 挂载到容器的
   /etc/mysql/my.cnf。配置目录
   -v $PWD/logs:/logs：将主机当前目录下的 logs 目录挂载到容器的 /logs。日志目录
   -v $PWD/data:/var/lib/mysql ：将主机当前目录下的data目录挂载到容器的
   /var/lib/mysql 。数据目录
   -e MYSQL_ROOT_PASSWORD=123456：初始化 root 用户的密码。
   ```

4. 进入容器，操作mysql

   ```bash
   docker exec –it c_mysql /bin/bash
   ```

5. 使用外部机器连接容器中的mysql

   可是使用一些专门的工具，也可以使用cmd（缺少插件）

   > 连接的主机ip为：宿主机的ip（通过ip a获得）
   >
   > 端口为：上面映射的左边的端口：3307
   >
   > username：默认是root
   >
   > password：123456

## 8. Docker Compose 多容器编排命令

适用于多服务项目（前端+后端+数据库），通过 `docker-compose.yml` 一键管理所有服务

```bash
docker-compose up                # 前台启动所有服务
docker-compose up -d             # 后台守护启动所有服务
docker-compose logs -f           # 实时查看全部服务日志
docker-compose logs -f nginx     # 仅查看指定服务日志
docker-compose ps                # 查看所有编排容器状态
docker-compose stop              # 停止服务，保留容器与数据
docker-compose start             # 启动已停止的编排服务
docker-compose restart           # 重启所有服务
docker-compose down              # 停止并删除容器、网络（保留数据卷）
docker-compose down -v           # 删除容器、网络、数据卷（谨慎）
docker-compose build             # 重新构建所有服务镜像
docker-compose pull              # 拉取所有服务最新镜像
```

## 8. 镜像仓库推拉命令

```bash
docker login                       # 登录Docker Hub官方仓库
docker login 私有仓库地址           # 登录自定义私有仓库
docker push myapp:v1               # 推送本地镜像到仓库
docker logout                      # 退出仓库登录
```

# 七、Docker 新手万能实操模板

```bash
# 1. 临时测试容器（用完即删）
docker run --rm -it nginx bash

# 2. 生产常驻服务模板
docker run -d --name 容器名 -p 宿主机端口:容器端口 -v 宿主机挂载路径:容器路径 --restart always 镜像名

# 3. 一键清理服务器Docker垃圾
docker system prune

# 4. 多服务项目启动
docker-compose up -d
```

# 八、Docker 适用场景总结

- 后端项目（Java/Python/Go/Node）打包、自动化部署
- 本地/服务器快速部署数据库、中间件（MySQL、Redis、MQ等）
- 统一团队开发环境，规避环境差异问题
- 云服务器批量运维、自动化部署
- 微服务架构、K8s容器集群底层支撑
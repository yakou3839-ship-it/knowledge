## docker过时了？podman

**podman特性**

> - 开源













##  docker部署技术

> 最成熟高效的软件部署技术

**概要**

用容器化技术给应用程序封装独立的运行环境，每个运行环境就是一个容器，运行容器的计算机被称为宿主机

**docker与虚拟的最大的区别**

docker容器之间共用同一个系统内核，而每个虚拟机都包含一个操作系统的完整内核，所以docker容器比虚拟机更轻、更小、启动速度更快

![image-20260801093338253](assets/image-20260801093338253.png)

![image-20260801093348585](assets/image-20260801093348585.png)

**docker镜像与docker hub‘**

镜像就是模版，可以把镜像类比成软件安装包，而容器是安装出来的软件

> 镜像与容器之间的关系就像是模具与糕点，可以使用一个模具做出很多糕点，也可以把模具分享给其他人使用，docker仓库就是用来存放分享镜像的地方，每个人都可以把镜像上传到仓库中，而其他人就可以下载使用。
>
> docker的官方仓库就是docker hub

**docker的安装**

> docker是基于linux的容器化技术，windows和mac电脑上都是虚拟了一个linux子系统（wsl）来运行docker（docker desktop）

**配置镜像源**

> 国内的环境没有办法访问docker官方仓库，当然国内有仓库镜像

linux下

- 修改config文件，配置docker的镜像源

win与mac下

- 在桌面版的docker engine中配置

**几个重要的docker命令**

- docker pull docker.io/library/nginx:latest
  - 其中docker.io是docker仓库的注册地址，表名这是docker官方仓库
  - library是命名空间，表示官方仓库，用其他人的需要指明命名空间
  - nginx是镜像，latest是版本名
  - docker pull --platform=xxxxxx nginx：指定宿主机架构下载，默认会自动适配宿主机架构
- docker images：列出所有下载过的镜像
- docker rmi 镜像名/id：删除指定镜像
  - rm是remove，i是images
  - docker rm 容器名/id：正在运行的容器，需要加一个-f表示强制的意思
- docker run nginx：使用镜像创建一个容器
  - run -d表示分离模式，让容器在后台运行，当前窗口仍可以进行操作
  - run -p：端口映射，容器内的网络与宿主机的网路是隔离的，需要添加一个端口，将容器内的端口映射到宿主机的端口（冒号前面是宿主机，后面是容器）
  - run -v：把宿主机与容器的文件目录进行绑定（互相影响），也被称为挂载卷（最大作用是数据的持久化保存，因为当我们删除容器的时候，容器内的数据会被同时删除）主要有两种挂载
    - 绑定挂载：直接把宿主机的命令写在命令里面（-v 宿主机目录：容器内目录）
    - 命名卷挂载：用docker创建一个存储空间并起一个名字，在挂载的时候，直接填写卷名：容器内目录就可以了
  - run -e：用来往容器中传递环境变量
    - 具体可传递的环境变量需要去镜像中找一下
  - run --name：给容器命名
  - -it：让控制台进入容器内进行交互
  - --rm：当容器停止的时候就容器删除掉（用于临时调试一个容器）
  - --restart：配置容器在停止时的重启策略
    - 后跟always：只要容器停止就立刻重启
    - unless-stopped：和always差不多，但是该命令对于手动停止的容器不会重启
- docker volum
  - docker volum create 卷名：创建一个挂载卷
  - docker volum inspect 卷名：查看命名卷所在位置
  - docker volum list：显示所有创建的卷
  - docker volum rm 卷名：删除
  - docker volum prune -a：删除所有没有任何容器使用的卷
- docker ps：查看正在运行的容器
  - ps是process status（进程状态）的缩写
  - -a ：查看所有容器，包括没有运行的

- 已有容器的启停
  - docker start 容器名/id
  - docker stop容器名/id
- docker inspect 容器名：查看容器的各种配置

- docker create 只创建不启动容器，后面跟的参数和run差不多

- docker logs ：查看容器的日志，后面加-f表示滚动查看日志
- 

**docker的技术原理**

每个docker容器都是一个独立的运行环境，每个容器内部表现的都像是一个独立的linux系统

- docker exec 容器名/id：可以在容器内执行linux命令（后面可以跟一些命令，直接运行不进入）
  - docker exec -it 容器id /bin/sh：进入一个正在运行的docker容器内部获得一个交互式的命令行环境

**dockerfile**

> dockerfile是制作模具（镜像）的图纸，是一个文件，里面详细列出了镜像是如何制作的

准备Dockerfile：

```dockerfile
FROM 基础镜像

#给镜像添加元信息
LABEL author="xiaoming" version="1.0" description="python demo service"

#设置环境变量，构建阶段和容器运行阶段均可读取
#单个变量：ENV APP_ENV=production
#多个变量：ENV VERSION="1.0" NAME="demo"

#构建阶段临时变量，仅在docker build过程中生效，容器运行后不存在
ARG BUILD_VERSION=v1.0 FROM python:${BUILD_VERSION}
#效果：#docker build --build-arg BUILD_VERSION=v1.1 -t test
#与ENV的区别，ENV容器运行依然存在

#有点像cd，切换到镜像内的一个目录作为工作目录，后面的命令都是在个目录下面执行的
WORKDIR 目录

#将代码文件拷贝到镜像内的工作目录
COPY ..   第一个点表示dockerfile同目录下的所有文件，第二个点表示工作目录下
#COPY有个缓存依赖：在RUN先用COPY requirements.txt .   ，在RUN之后再慢慢将全部代码复制到容器中

#和COPY几乎一致，额外有两个特性
#1.如果源是本地tar压缩包，自动解压到目录路径
#2.源支持URL网络地址（下载文件）
ADD archive.tar.gz /data


#构建镜像阶段执行命令，安装依赖 RUN表示这个命令要在镜像里面进行执行，多个命令尽量用&&串联
RUN pip install -r requirements.txt
#缓存依赖 COPY . .   先安装之前COPY的依赖，后续在慢慢复制代码

#声明镜像提供服务的端口是那个，这里只是一个提示，不会自动开放端口，实际使用的时候还是以-p参数为准，可以同时声明多个窗口
EXPOSE 8000

#容器运行时的默认启动命令（构建镜像阶段不运行），每当容器启动的时候，容器内部会自动执行这个命令是的容器有一个python在运行，一个dockerfile里只能写一个cmd
#与ENTRYPOINT搭配使用,简单服务只用CMD，需要固定启动程序、传参场景使用ENTRYPOINT
#下面的CMD命令可以拆为
#ENTRYPOINT ["python"]
#CMD ["app.py"]

CMD ["python3","main.py"]



#切换后续指令执行的用户（默认root），尽量不要在容器内使用root运行程序，可以配合 RUN adduser -D 用户名   先创建用户
USER 用户名


#声明持久化数据卷，容器运行时自动挂载匿名卷，不要用来持久化数据库数据
VOLUME ["/data"]
#Dockerfile 无法指定宿主机目录挂载，挂载宿主机目录只能在 docker run -v 指定

```

制作镜像：

- docker build -t 镜像名 .
  - 名字后面可以   :版本号  也可以不写
  - .   指的是在当前文件夹构建    （会找到dockerfile，然后去执行）



推送镜像到docker hub中

- 先在docker hub中创建一个账号
- 在电脑上运行docker login登录账号
- docker push 用户名/镜像



**docker网络**

> 默认是bridge桥接模式，每个容器都分配了一个内部ip地址，容器可以通过内部ip地址互相访问，但容器与宿主机的网络是隔离的。

创建子网（桥接模式）：

docker network create network1

- 同一个子网的容器可以通信，跨子网则不可以通信。同一个子网的容器可以已使用容器的名字互相访问而不必使用内部ip地址

- ![image-20260801110313769](assets/image-20260801110313769.png)

 Host模式：

> docker容器直接共享宿主机的网络，容器直接使用宿主机的ip地址，无需-p参数进行端口映射，容器内的服务直接运行在宿主机的端口上，通过宿主机的ip和端口就能访问到容器

None模式：

> 不连接网络

**docker compose**

> 有些时候一个完整的应用可能是由很多部分组成的，比如前端、后端、数据库等，那如何用docker将他们容器化？可以很自然的想到将这些模块都打包在一起，做成一个巨大的容器，但只要有一个模块发生故障，整个容器都可能崩溃
>
> 多应用的最佳实践是将每个模块都打包成一个独立的容器，但是使用多个容器增加了很多的使用成本，因为想创建多个容器就要多次执行docker run，并且尝试管理容器的时候容器出错，这时候一个容器编排技术就很有用
>
> docker compose使用yml文件管理多个容器，里面列出来容器之间是如何创建以及如何协同工作的，可以简单地把docker compose文件理解成一个或多个docker run命令，按照特定的格式列到了一个文件里面
>
> docker会为每一个compose文件都自动创建一个子网，同一个compose文件定义的所有容器都会自动加入同一个子网
>
> docker compose还可以自定义容器的启动顺序

启动命令

- docker compose up：根据yaml文件启动
  - 会识别当前目录下严格叫docker-compose.yaml的文件
  - 对于非标准的文件名可以在compose后面加-f指定自定义的文件名
- docker compose down：停止并删除容器
- docker compose stop：只停止不删除
- docker compose start：启动停止的容器

> docker compose适合个人使用，单机运行，对于企业级服务器集群大规模的服务器编排需求，需要另外一个软件Kubernetes登场
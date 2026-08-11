# MySQL 完整详解：是什么、用途、全套学习路线（超详细）
## 一、什么是 MySQL
### 1. 基础定义
MySQL 是一款**开源、免费、跨平台的关系型数据库管理系统（RDBMS）**。
- 关系型：数据以**表（行+列）** 存储，表与表之间可以建立关联关系；
- 开源：社区版完全免费商用，企业版付费；
- 语言：使用标准 SQL（结构化查询语言）操作数据；
- 适配：Windows / Linux / Mac / Docker 全部支持，Web、后端、小程序、APP 通用。

### 2. 核心组成
1. **数据库 Server（mysqld 服务）**
后台常驻进程，负责接收客户端指令、读写磁盘数据、权限校验、事务处理。
2. **客户端**
用来连接服务端操作数据库：mysql 命令行、Navicat、DBeaver、Python/Java 代码等。
3. **库（database）**
一个项目对应一个数据库，比如 `flask_demo`、`shop`；库下面有多张数据表。
4. **表（table）**
存储一类数据，例如用户表 `user`、商品表 `goods`；由字段（列）和数据（行）组成。
5. **字段（column）**
表的属性，如 id、username、phone、age，有数据类型（数字、字符串、日期）。
6. **记录（row）**
一行完整数据，代表一条用户/商品信息。

### 3. 对比通俗理解
- MySQL = 一个带锁、带规则、高效的**文件管理仓库**
- 数据库 = 仓库里的一个文件夹（项目）
- 数据表 = 文件夹里的 Excel 表格
- SQL = 操作表格的指令（增删改查）

## 二、MySQL 有什么用（核心场景）
### 1. Web/后端开发（最主流）
网站、管理系统、Flask/Django/SpringBoot 项目存储业务数据：
- 用户账号、密码、头像、手机号
- 订单、购物车、商品库存、分类
- 文章、评论、点赞、后台权限

### 2. APP/小程序数据存储
所有小程序、安卓/iOS App 几乎都搭配 MySQL 存业务数据。

### 3. 数据分析、后台报表
存储业务流水，配合 SQL 统计销售额、注册量、活跃用户。

### 4. 和你前面 Docker 结合使用
你之前学的容器部署：
- 单独启动 mysql 容器：`docker run -d -v mysql-data:/var/lib/mysql mysql:5.7`
- 后端项目（flask-demo）连接容器内 MySQL，实现代码持久化存储数据。

### 5. 优势为什么选 MySQL，不用 Excel/文本
1. 支持百万、千万条数据高速查询，txt/excel 打开卡顿；
2. 支持多用户同时读写，不会冲突；
3. 有权限控制：不同账号只能看指定数据；
4. 事务：转账、下单要么全部成功，要么全部回滚，不会出现数据错乱；
5. 约束：限制手机号长度、年龄不能为负数，保证数据规范；
6. 支持联合多表查询、分页、排序、分组统计。

## 三、MySQL 核心专业概念（必懂）
### 1. 数据类型（建表必备）
1. 数字
- `INT`：整数（id、年龄、数量）
- `FLOAT/DECIMAL`：小数（价格、金额，金额优先 decimal 避免精度丢失）
2. 字符串
- `VARCHAR(n)`：可变长度字符串（用户名、手机号、地址）
- `CHAR(n)`：固定长度
- `TEXT`：大文本（文章内容）
3. 时间
- `DATE`：日期 `2026-07-01`
- `DATETIME`：完整时间 `2026-07-01 12:30:00`

### 2. 约束（保证数据合法）
1. `PRIMARY KEY` 主键：唯一标识一行，一般用 id，不能为空、不能重复
2. `NOT NULL`：字段不能为空（用户名、手机号必填）
3. `UNIQUE`：值不能重复（账号、手机号）
4. `DEFAULT`：默认值（注册时间默认当前时间）
5. `FOREIGN KEY` 外键：多表关联（订单表关联用户id）

### 3. 四大核心操作 CRUD（所有业务基础）
- C Create 新增：`INSERT` 添加数据
- R Read 查询：`SELECT` 读取数据（使用最多）
- U Update 修改：`UPDATE` 更新已有数据
- D Delete 删除：`DELETE` 移除数据

### 4. 事务 InnoDB（重中之重）
MySQL 默认引擎 InnoDB 支持事务，四大特性 ACID：
- 原子性：一组操作不可分割，全成功或全失败
- 一致性：执行前后数据合法
- 隔离性：多个用户操作互不干扰
- 持久性：提交后数据永久落地磁盘
适用场景：下单扣库存、转账、支付。

### 5. 索引
给字段建立索引，大幅提升查询速度，类似书本目录；缺点：新增/修改数据会变慢。

### 6. 存储引擎
- InnoDB：默认，支持事务、外键，业务开发首选
- MyISAM：不支持事务，查询快，几乎淘汰

## 四、完整学习路线
### 阶段1：环境搭建（3种方式）

#### 方式1：Docker 安装（强烈推荐，无环境污染）

一键启动 MySQL5.7（命名卷持久化数据）
```bash
# 创建mysql命名卷，启动容器
docker run -d \
--name mysql57 \
-p 3306:3306 \
-v mysql-data:/var/lib/mysql \
-e MYSQL_ROOT_PASSWORD=123456 \
mysql:5.7
```
参数解释：
- `-p 3306:3306`：端口映射，宿主机3306连接容器数据库
- `-e MYSQL_ROOT_PASSWORD` 设置root管理员密码
- `-v mysql-data:/var/lib/mysql` 命名卷持久化，删除容器数据不丢失

连接数据库
```bash
#标准版格式
docker exec -it 容器名称 mysql -u数据库用户名 -p数据库密码
#容器名称：启动容器 --name 后定义的名字，如 c_mysql、mysql57
#数据库用户名：MySQL 账号，默认 root
#数据库密码：MYSQL_ROOT_PASSWORD 设置的密码
#示例
docker exec -it mysql57 mysql -uroot -p123456
```
#### 方式2：本地安装 Windows/Mac

官网下载 MySQL 安装包，配置环境变量，端口3306。

##### 启动mysql服务

**方法①：图形界面启动（新手推荐）**

> 1. 快捷键 `Win + R`，输入 `services.msc` 回车打开服务列表
> 2. 找到 MySQL 服务，名称一般是 `MySQL80`（8.0 版本）/ `MySQL57`（5.7 版本）
> 3. 右键 → **启动**；右键属性可设置「自动」开机自启

**方法②：CMD 命令启动（管理员 CMD）**

> 1. 快捷键 `Win + R`，输入 `services.msc` 回车打开服务列表
> 2. 找到 MySQL 服务，名称一般是 `MySQL80`（8.0 版本）/ `MySQL57`（5.7 版本）
> 3. 在cmd中输入`net start 版本名`

##### 登录mysql（启动服务后执行）

> `mysql -uroot -p`

如果在cmd中显示没有mysql命令，将mysql安装目录下的bin文件加入环境变量

#### 方式3：Linux yum/apt 本地安装❌️（没有找到安装包）

服务器生产环境部署使用。

> windows与linux的安装包不互通

####  本地图形工具辅助连接（Navicat/DBeaver）


地址：127.0.0.1（可以直接用localhost），端口3306，账号root，密码123456

### 阶段2：SQL 基础语法（1~3天吃透）

> mysql语句必须以分号（;）结尾不然视为没有结束

#### 1. 数据库操作✅️

```sql
-- 创建库
CREATE DATABASE shop;
-- 查看所有库
SHOW DATABASES;
-- 查看指定库的信息
SHOW CREATE DATABASE 库名;
-- 显示当前库所有表   需要实现use 库名
show tables;
-- 使用库
USE 库名;
-- 删除库
DROP DATABASE IF EXISTS 库名;
-- 更改数据库字符集     字符集名称：常用 utf8mb4（推荐）、utf8、latin1
ALTER DATABASE 数据库名 DEFAULT CHARACTER SET 字符集名称;
```

#### 2. 数据表操作✅️

```sql
-- 创建用户表
CREATE TABLE 表名(
    id INT PRIMARY KEY AUTO_INCREMENT, -- 自增主键
    username VARCHAR(50) NOT NULL UNIQUE,
    phone VARCHAR(11),
    age INT DEFAULT 18,
    create_time DATETIME DEFAULT NOW()
);

-- 查看表结构
DESC 表名;
-- 删除表
DROP TABLE IF EXISTS 表名;
-- 添加列
ALTER TABLE 表名 ADD 列名 类型;
-- 删除列
ALTER TABLE 表名 DROP COLUMN 列名;
-- 显示表中所有列   等价于desc 表名
show columns from 表名;    
```

#### 3. CRUD 增删改查（核心）

**新增 INSERT✅️**

```sql
-- 如果不带括号表示按列序增加全部列值
INSERT INTO 表名(列名,列名...) VALUES(值,值...);
```

**查询 SELECT（最复杂、最重要）✅️**

```sql
-- 显示表中所有数据
SELECT * FROM 表名;
-- 指定列、条件查询
SELECT 列名,列名... FROM 表名 WHERE 条件;
-- 分页、排序
SELECT * FROM 表名 ORDER BY 列名 DESC LIMIT 0,10;
-- 模糊查询
SELECT * FROM 表名 WHERE 列名 LIKE '%zhang%';
```

**修改 UPDATE✅️**

```sql
UPDATE 表名 SET 列名=值 WHERE 条件;
```

**删除 DELETE✅️**

```sql
DELETE FROM 表名 WHERE 条件;
```

#### 4. 条件、运算符、聚合函数✅️

WHERE 条件：`> < >= <= != AND OR`
聚合统计：`COUNT() SUM() AVG() MAX() MIN()`

```sql
-- 统计用户总数
SELECT COUNT(id) FROM user;
-- 按年龄分组统计
SELECT age,COUNT(id) FROM user GROUP BY age;
```

#### 5. 多表关联查询（JOIN）

业务必备：用户表、订单表联合查询
- INNER JOIN 内连接（只查两边匹配数据）
- LEFT JOIN 左连接（左表全部数据，匹配右表）

#### 6. 子查询、别名、去重 DISTINCT

### 阶段3：进阶核心（3~7天）

1. 事务实操：`BEGIN; COMMIT; ROLLBACK;` 模拟转账失败回滚
2. 索引创建、查看、删除，理解索引优化场景
3. 视图 VIEW、存储过程、函数（简单了解）
4. 用户权限管理：创建账号、分配访问库权限
```sql
-- 创建新用户，只能本地访问shop库
CREATE USER 'yakou'@'localhost' IDENTIFIED BY '666666';
GRANT ALL ON shop.* TO 'yakou'@'localhost';
```
5. 日期函数、字符串函数常用内置函数

### 阶段4：项目实战（重中之重，巩固所有知识点）

#### 实战：结合你学的 Flask + Docker + MySQL

完整流程：
1. Docker 启动 MySQL 容器
2. Python Flask 使用 pymysql 连接数据库
3. 写接口：用户注册、登录、商品增删改查、下单接口
4. 容器打包后端项目，实现整套容器化业务服务

### 阶段5：调优&生产运维（进阶，工作必备）

1. 慢查询日志，定位慢 SQL
2. SQL 优化：避免 select *、避免模糊前置%、合理建立索引
3. 分页大数据优化、千万级数据查询思路
4. MySQL 备份与恢复 `mysqldump`
5. 主从复制简单概念（面试高频）

## 五、学习配套工具（提高效率）
1. 图形客户端（推荐新手）
- DBeaver：免费开源，全平台
- Navicat：界面简洁，付费（破解版慎用）
2. 命令行：自带 mysql 客户端
3. 代码驱动：
- Python：pymysql / sqlalchemy
- Java：Mybatis、JDBC

## 六、学习资料推荐
### 视频
1. B站：黑马MySQL入门全套、尚硅谷MySQL基础（零基础友好）
2. 适合你：搭配Flask的Web+MySQL实战教程

### 书籍
1. 《MySQL必知必会》：薄，入门首选，语法全覆盖
2. 《高性能MySQL》：进阶调优，工作必看

### 练习平台
1. LeetCode 数据库题库：刷SQL查询题
2. 本地自建库反复写增删改查，不要只看视频不动手

## 七、学习避坑指南
1. 不要只看视频不敲代码：SQL 一定要手打，手熟才会
2. 不要跳过多表查询：实际项目全是多表联查，是面试重点
3. 不要忽略事务：转账、下单场景必考
4. 不要混淆 InnoDB 和 MyISAM，业务统一用 InnoDB
5. 不要用 float 存金额，使用 decimal 防止金额误差
6. Docker 部署 MySQL 必须用命名卷，否则删除容器数据全部丢失
7. UPDATE / DELETE 不加 WHERE 会修改/删除全表数据，操作前先 SELECT 验证条件

## 八、完整学习周期规划参考
1. 1天：Docker搭建MySQL环境，熟悉图形工具连接
2. 2~3天：基础SQL，库、表、增删改查、条件、分组排序
3. 3天：多表JOIN、事务、索引、权限管理
4. 3~5天：商城多表实战，手写全套业务SQL
5. 3天：Flask + MySQL 容器化完整项目打通
6. 空余刷题：LeetCode SQL题库巩固查询逻辑
整体两周可以达到独立开发后端数据库业务的水平。

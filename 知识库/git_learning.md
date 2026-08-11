# Git 小白零基础完整学习手册
> 文档说明：面向纯新手，包含Git作用、核心概念、安装配置、全套命令、完整实操流程、分支协作、版本回退、常见报错解决方案，排版分层清晰，可直接复制保存为 `.md` 文件使用

## 目录
1. [一、Git 是什么 & 核心作用](#一git-是什么--核心作用)
2. [二、Git 四大核心区域（必懂底层逻辑）](#二git-四大核心区域必懂底层逻辑)
3. [三、Git 安装与首次全局配置](#三git-安装与首次全局配置)
4. [四、Git 全场景命令大全（分类整理）](#四git-全场景命令大全分类整理)
    - 4.1 基础配置命令
    - 4.2 仓库初始化/克隆命令
    - 4.3 文件暂存 & 提交本地仓库
    - 4.4 查看状态、日志、历史版本
    - 4.5 分支管理核心命令
    - 4.6 远程仓库（GitHub/Gitee）操作
    - 4.7 版本回退、撤销修改（高危操作标注）
    - 4.8 临时储藏修改（stash）
5. [五、新手标准完整实操流程（一步一复制）](#五新手标准完整实操流程一步一复制)
    - 5.1 本地新建项目上传远程仓库
    - 5.2 拉取别人远程仓库到本地修改
6. [六、团队多人协作基础流程](#六团队多人协作基础流程)
7. [七、新手高频报错与解决办法](#七新手高频报错与解决办法)
8. [八、新手避坑总结](#八新手避坑总结)

---

## 一、Git 是什么 & 核心作用
### 1. Git 定义
Git 是**免费开源分布式版本控制系统**，由Linux之父林纳斯开发，是程序员必备工具；配套远程平台：GitHub（国外）、Gitee（国内码云）、GitLab（企业私有）。

### 2. 核心作用（小白通俗版）
1. **版本备份，随时回滚**
    记录每一次代码修改快照，写错代码、删错文件可一键回到任意历史版本，不用手动复制N份项目备份。
2. **多人团队协作开发**
    多人同时改同一个项目，自动区分每个人修改内容，合并代码、解决冲突，避免文件互相覆盖。
3. **离线可用（分布式核心优势）**
    不同于老式SVN（必须联网），Git本地完整存储全部代码历史，断网也能提交版本，联网后同步远程即可。
4. **代码云端永久存储**
    将本地项目推送至GitHub/Gitee，电脑丢失、重装系统都能一键拉回完整代码。
5. **分支隔离开发**
    新建分支单独写新功能，不污染主线稳定代码，功能完成后再合并。

### 3. 分布式 vs 集中式（SVN）区别
| 对比项 | Git（分布式） | SVN（集中式） |
| ---- | ---- | ---- |
| 存储方式 | 本地完整副本+云端备份 | 仅服务器存完整代码，本地只有当前文件 |
| 离线操作 | 支持，断网可提交版本 | 不支持，无网络无法提交 |
| 分支功能 | 轻量、创建切换秒级完成 | 笨重，分支操作速度慢 |
| 数据安全 | 每个人本地都是完整备份 | 服务器损坏则全部代码丢失 |

---

## 二、Git 四大核心区域（必懂底层逻辑）
### 区域流转链路
`工作区(编辑代码) → git add → 暂存区(临时存放变更) → git commit → 本地仓库(永久保存版本) → git push → 远程仓库(云端)`
反向同步：`远程仓库 → git pull/git fetch → 本地仓库 → 工作区`

1. **工作区 Working Directory**
    电脑上能直接看到的项目文件夹，所有写代码、增删改文件操作都在这里，Git不会自动记录修改。
2. **暂存区 Stage/Index**
    「临时购物车」，使用`git add`把需要提交的变更放入暂存区，可选择性提交部分文件，不放入暂存区的修改不会生成版本记录。
3. **本地仓库 Local Repository**
    项目文件夹内隐藏 `.git` 目录，存储项目全部历史快照、提交记录、分支信息；执行`git commit`才会把暂存区内容永久保存成本地版本，**断网可用**。
    ⚠️ 禁止手动删除/修改 `.git` 文件夹，会丢失全部版本记录。
4. **远程仓库 Remote Repository**
    托管在网络平台（GitHub/Gitee）的云端仓库，用于多人共享、代码备份；本地通过`push`上传、`pull`下载同步。

### 基础概念补充
- **分支 Branch**：代码开发支线，默认主分支 `main`（新版Git）/ `master`（旧版）；开发新功能新建分支隔离代码。
- **提交 commit**：每一次版本快照，拥有唯一hash标识（一串字母数字），用于定位历史版本。
- **冲突 Conflict**：多人修改同一文件同一行代码，合并时Git无法自动判断保留内容，需要手动修改解决。

---

## 三、Git 安装与首次全局配置
### 1. 下载安装
官网地址：https://git-scm.com/downloads
- Windows：下载exe安装包，全程默认下一步，勾选 `Git Bash Here`（右键文件夹快速打开命令行），安装路径**禁止中文、空格**。
- Mac：终端执行 `xcode-select --install` 快速安装。
- 验证安装：打开Git Bash/终端输入
```bash
git --version
# 输出版本号即安装成功
```

### 2. 首次配置（三种方法）

> 这里还是建议全局，这样方便，因为有的时候一个文件夹是git仓库，但是该文件夹里面还有个文件夹也是git仓库，这样用单独的配置比较麻烦

**①所有仓库共用，仅执行一次**

Git提交记录会携带你的用户名+邮箱，必须配置，建议邮箱和Gitee/GitHub账号邮箱一致：

```bash
# 设置全局用户名（替换为自己昵称/姓名）
git config --global user.name "XiaoMing"
# 设置全局邮箱（替换为平台注册邮箱）
git config --global user.email "xiaoming@shturl."
# 查看全部配置，验证是否生效
git config --list
```
> 单仓库单独配置（不加--global，仅当前项目生效）：去掉 `--global` 参数即可。

**②单个仓库单独设置（不同文件夹不同账号）**

```python
# 进入公司项目文件夹
cd D:\work\company_project
# 仅当前仓库生效
git config user.name "公司姓名"
git config user.email "公司邮箱@company.com"
```

**③系统级**

> 这台电脑上所有的用户共用一个，一般不会这样设置

### 3. SSH密钥配置（免密码推送远程仓库，推荐）

==问题==

> 这里采用自定义路径保存后无法连接，采用默认的可以连接，问题没解决

每次HTTPS推送需要输入账号密码，SSH配置后永久免密：

```
ssh-keygen -t ed25519 -C "你的注册邮箱"
```

> 这里的邮箱，需要到gitee账号里面设置
>
> 暂时不知道需不需要和git文件夹的用户配置保持一致
>
> 步骤：
>
> - ①会提示你输入路径（它默认有个路径，但是在c盘）可以选择其他路径但要记好
> - ②输入查看这个秘钥时的密码（直接enter可以不设密码）
> - ③确认密码（如果没有直接enter）

```bash
# Windows查看公钥内容
cat ~/.ssh/id_ed25519.pub
#cat后面你的路径根据你上面添加的路径
```
复制输出全部内容，打开Gitee/GitHub个人设置 → SSH公钥，粘贴保存；测试连接：

```bash
# Gitee测试
ssh git@gitee.com
# GitHub测试
ssh git@github.com
# 出现success提示即配置完成
```

---

## 四、Git 全场景命令大全（分类整理）
### 4.1 基础配置命令
```bash
# 全局设置用户名
git config --global user.name "名字"
# 全局设置邮箱
git config --global user.email "邮箱"
# 查看所有配置
git config --list
# 删除某一项全局配置
git config --global --unset user.name
# 设置Git默认编辑器（新手推荐notepad）
git config --global core.editor notepad
```

### 4.2 仓库初始化/克隆命令

> 为什么要放在第二个，因为你创建这个仓库就是为了完成某个项目，所以直接将项目的远程仓库先克隆到本地	
>
> 一般情况都是这个流程，而不是先创文件夹，然后在里面工作，最后在将内容推送

```bash
# 1.本地新建空项目，初始化Git仓库（进入项目文件夹执行）
git init
# 生成隐藏.git文件夹，开启版本管理

# 2.克隆远程已有仓库到本地（两种协议）
#使用clone必须要保证文件夹为空
# HTTPS（每次推送输密码）
git clone https://gitee.com/xxx/demo.git
# SSH（免密，推荐）
git clone git@gitee.com/xxx/demo.git

# 克隆指定分支，不下载全部分支历史
git clone -b dev git@gitee.com/xxx/demo.git
# 浅克隆，仅拉取最新1条记录（超大仓库提速）
git clone --depth 1 git@gitee.com/xxx/demo.git
```

### 4.3 文件暂存 & 提交本地仓库（最常用流程）
#### git add 放入暂存区
```bash
# 添加单个文件到暂存区
git add index.html
# 添加整个文件夹全部文件
git add src/
# 添加当前目录所有新增/修改文件（不含删除）
git add .
# 添加全部变更：新增、修改、删除（最全，日常推荐）
git add -A
# 交互式添加，选择性提交部分代码块
git add -p
```

#### git rm 删除文件
```bash
# 删除文件，同时加入暂存区（本地文件直接删除）
git rm test.js
# 仅从暂存区移除，保留本地源文件（误add后撤销）
git rm --cached test.js
```

#### git commit 提交本地版本
```bash
# 简洁提交，-m 后写本次修改说明（强制规范）
git commit -m "完成首页登录页面开发"
# 打开编辑器编写详细提交描述
git commit
# 直接提交已跟踪文件，跳过git add（不含新增文件）
git commit -a -m "修复按钮点击bug"
# 修正上一次提交（修改提交备注/补充遗漏文件）
git commit --amend
```

### 4.4 查看状态、日志、历史版本
```bash
# 查看文件完整状态（未跟踪/已暂存/已修改）
git status
# 简洁状态输出（新手首选）
git status -s
# A=新增 M=修改 D=删除 ??=未跟踪文件

# 查看完整提交日志
git log
# 简洁单行日志，看提交hash与备注
git log --oneline
# 查看所有操作记录（包括回退删除的提交，恢复丢失版本必备）
git reflog
# 查看指定文件修改历史
git log test.html
```

### 4.5 分支管理核心命令

**有关git分支的一些理解**

> 先说结论：**不是完整复制一份仓库，底层只是新建了一个轻量指针，几乎不占空间**
>
> 1. ==Git 分支底层原理==
>
> Git 保存数据的核心是 **提交快照（commit 对象）**，所有分支本质只是一个**指向某次 commit 的指针**。
>
> - 创建分支时，**不会复制任何代码文件、不会复制历史记录、不产生新文件副本**；
> - 仅新增一个 41 字节左右的文本指针，记录当前提交哈希值。
>
> 举个直观例子：
> 你在 `main` 分支，当前提交是 `commit-A`：
>
> ```
> main → commit-A
> ```
>
> 执行 `git dev` 创建 dev 分支：
>
> ```
> dev
>    ↘
> main → commit-A
> ```
>
> 两个分支同时指向**同一份提交快照**，代码、历史完全共用，没有任何复制。
>
> 2. ==什么时候才会产生“不一样的文件”？==
>
> 只有你在新分支**做新提交**，才会生成新快照：
>
> 1. 切换到 dev：`git checkout dev`
> 2. 修改代码、add、commit → 生成 `commit-B`
>    此时结构变成：
>
> ```
> dev → commit-B
>       ↓
> main → commit-A
> ```
>
> 此时 dev 独有 commit-B，main 还停留在旧提交；
> **共用部分依然不会重复存储**，Git 只会存储改动差异，重复文件共用一份存储。
>
> 3. ==和“复制整个项目文件夹”的本质区别==
>
> | 操作               | 存储开销                             | 历史记录                   | 同步关系         |
> | ------------------ | ------------------------------------ | -------------------------- | ---------------- |
> | Git 创建分支       | 几乎0开销，仅一个指针                | 共用全部提交历史           | 能自由合并、切换 |
> | 手动复制项目文件夹 | 完整复制所有代码、所有历史，体积翻倍 | 两套完全独立历史，互不识别 | 无法便捷合并代码 |
>
> 4. ==常用分支操作印证轻量化==
>
> 1. 创建分支瞬间完成，哪怕仓库几十G，一秒建好；
>    `git branch feature`
> 2. 切换分支只是移动指针，替换工作区文件，不会复制仓库；
> 3. 删除分支 `git branch -d feature`，只是删掉一行指针，代码快照还在（只要没被回收）。
>
> 5. ==补充误区纠正==
>
> 很多人以为分支是“仓库副本”，混淆了 Git 和 SVN：
>
> - SVN 的分支是复制整套目录，占用大量空间；
> - Git 分支是指针式设计，极致轻量化，所以工程里可以随意建几十上百个分支。
>
> ==简单一句话总结==
>
> 创建分支 ≠ 复制仓库，只是给当前代码快照多起了一个名字；
> 只有在新分支提交修改后，才会产生差异化的新版本，共用不变的文件数据。

```bash
# 查看本地所有分支，*代表当前所在分支
git branch
# 查看本地+远程全部分支
git branch -a
# 创建新分支（仅创建，不切换）
git branch dev
# 创建并直接切换到新分支（高频使用）
# 如果操作已经存在的分支，则不会成功
git checkout -b dev
# Git新版简化命令，等价上面一句
git switch -c dev
# 切换已有分支
git checkout main
# 新版简化切换
git switch main

# 删除本地分支（分支已合并才能删）
# 删除分支需要先退出当前分支
git branch -d dev
# 强制删除未合并分支（谨慎使用，丢失分支代码）
git branch -D dev

# 合并分支：把dev分支代码合并到当前main分支
git merge dev
# 变基合并（团队规范提交记录更整洁）
git rebase dev
```

**一些合并分支的知识**

> 核心原因：你**还没执行 commit 提交**，改动停留在「工作区 / 暂存区」，不属于任何分支
>
> 1. 先讲 Git 三层结构（看懂就全明白）
>
> 1. **工作区**：你电脑文件夹里看得见的代码文件（正在编辑的文件）
> 2. **暂存区 (stage)**：`git add` 后存放改动的中间层
> 3. **提交快照 (commit)**：`git commit` 才会把改动固定到**当前分支指针**
>
> 关键规则：
>
> - 只要没 `commit`，你的修改只存在**本地工作区**，不属于任何分支；
> - 切换分支时，Git 只会同步「已经 commit 保存好的版本」，不会动你未提交的改动；
> - 所以切回 main，你没保存的修改还留在文件夹，看起来主线代码被改了。
>
> 2. 完整复现你的场景
>
> 1. 切到 dev 分支：`git checkout dev`
> 2. 修改 test.py，**不 add、不 commit**
> 3. 切回 main：`git checkout main`
> 4. 打开 test.py，发现修改还在 → 你以为主线被改了
>
> 原理
>
> dev 分支没有保存这份修改，切换分支时 Git 不会丢弃你未提交的编辑内容，工作区文件原样保留。
>
> 此时 dev 和 main 的**已提交代码完全没变**，只是你手里有一份游离的未保存改动。

### 4.6 远程仓库（GitHub/Gitee）操作

```bash
# 查看已关联的远程仓库（默认别名origin）
git remote -v
# 给本地仓库关联远程地址（新建本地项目上传远程必用）
git remote add origin git@gitee.com/xxx/demo.git
# 修改已关联的远程地址
git remote set-url origin 新仓库SSH地址
# 删除远程关联
git remote remove origin

# 拉取远程最新代码（推荐，分两步更安全）
git fetch origin # 仅下载远程更新，不自动合并
git merge origin/main # 手动合并远程主线到本地

# 一步拉取+合并（新手简单使用）
git pull origin main

# 推送本地分支到远程仓库（首次推送加--set-upstream绑定上下游）
#推送那个需要激活那个分支
#origin是远程仓库默认别名
#这个main是自己仓库的里的分支名
git push --set-upstream origin main(本地分支):main(远程分支)
# 绑定后后续直接推送
git push origin main
# 强制推送（高危！覆盖远程代码，仅个人仓库使用，团队禁止）
git push -f origin main

# 将本地新建分支同步到远程
git push origin dev
# 删除远程分支
git push origin --delete dev
```

**关于一些远程仓库的知识**

> 1. 远程不存在目标分支：
>    - `git push origin main`：自动新建远程分支，不建立上下游；
>    - `git push -u origin main`：自动新建远程分支 + 永久绑定上下游（推荐首次推送使用）。
> 2. 远程已存在同名分支：
>    - 若远程无新增提交：可直接推送，无需拉取；
>    - 若远程有本地未同步的新提交：推送会被拦截，必须先拉取合并，再推送。

### 4.7 版本回退、撤销修改（高危操作标注）

#### 场景1：工作区修改错，未add、未提交，恢复文件原始状态
```bash
# 恢复单个文件到最近提交版本
git checkout -- test.js
# 恢复所有文件
git checkout -- .
```

#### 场景2：已经git add放入暂存区，想撤销暂存（文件保留修改）
```bash
# 撤销单个文件暂存
git reset HEAD test.js
# 撤销全部文件暂存
git reset HEAD .
```

#### 场景3：已经commit提交本地，需要回退版本（三种模式）
1. soft 软回退：保留修改在工作区（推荐）
```bash
# HEAD~1 代表回退1个版本，数字可修改
git reset --soft HEAD~1
# 指定hash值回退到任意历史版本
git reset --soft 3ac91df
```
2. mixed 默认模式：修改退回工作区，清空暂存区
```bash
git reset HEAD~1
```
3. hard 硬回退（⚠️极度高危！本地所有修改彻底删除，无法找回）
```bash
git reset --hard HEAD~1
git reset --hard 3ac91df
```

#### 场景4：远程仓库已推送提交，公共分支安全撤销（不用reset）
```bash
# 生成反向提交，新增一条记录覆盖错误版本，团队协作唯一推荐
git revert 提交hash值
```

### 4.8 临时储藏修改（切换分支不想提交半成品代码）
开发写到一半，临时切分支改bug，不想提交半成品代码使用stash：
```bash
# 储藏当前所有未提交修改
git stash
# 储藏并添加备注，方便区分多个储藏记录
git stash save "临时储藏首页未写完代码"

# 查看所有储藏记录
git stash list
# 恢复最新储藏内容，保留储藏记录
git stash apply
# 恢复并删除储藏记录（常用）
git stash pop
# 删除指定储藏记录
git stash drop stash@{0}
# 清空全部储藏
git stash clear
```

---

## 五、新手标准完整实操流程（一步一复制）

> 在最开始之前需要给git设置一个全局的名字和邮箱，要不然没有办法提交

### 5.1 流程A：本地全新项目上传Gitee/GitHub
1. 电脑新建项目文件夹，右键打开 Git Bash Here
2. 初始化仓库
```bash
git init
```
3. 新建代码文件，写入内容后放入暂存区
```bash
git add -A
```
4. 提交本地版本
```bash
git commit -m "项目初始化，基础文件搭建"
```
5. Gitee/GitHub网页新建空白仓库，复制SSH地址
6. 本地关联远程仓库
```bash
git remote add origin git@gitee.com/用户名/项目名.git

# 删除绑定
git remote remove origin
```
7. 首次推送绑定远程分支
```bash
git push --set-upstream origin main
```
完成，网页刷新即可看到上传代码。

### 5.2 流程B：拉取别人的远程仓库到本地修改
1. 新建空文件夹，右键打开Git Bash
2. 克隆远程仓库到本地
```bash
git clone git@gitee.com/他人账号/项目.git
```
3. 进入项目文件夹
```bash
cd 项目文件夹名
```
4. 修改代码，提交推送
```bash
git add -A
git commit -m "新增xx功能"
git push origin main
```

### 5.3 日常每日开发固定三步
```bash
# 1.上班先拉取远程最新代码，避免冲突
git pull origin main
# 2.写完代码提交本地
git add -A
git commit -m "本次修改描述"
# 3.下班推送云端备份
git push origin main
```

---

## 六、团队多人协作基础流程
适合2-5人小型开发团队，规范无冲突：
1. 所有人默认基于 `main` 主线，禁止直接在main写代码；
2. 开发新功能，从main创建专属功能分支：
```bash
git checkout main
git pull origin main # 先同步最新主线
git checkout -b feature/login # 创建登录功能分支
```
3. 在功能分支开发、多次提交，完成后推送远程分支：
```bash
git push origin feature/login
```
4. 网页端发起合并请求（PR/MR），负责人审核代码；
5. 审核通过后合并至main分支；
6. 其他成员同步最新主线代码：
```bash
git checkout main
git pull origin main
```
7. 不需要的功能分支完成合并后删除本地+远程分支。

### 代码冲突解决步骤
1. 执行`git merge`/`git pull`后提示冲突，打开冲突文件；
2. 文件内标记 `<<<<<<< HEAD`（本地代码）、`=======`、`>>>>>>> 远程版本`，手动删除标记，保留正确代码；
3. 冲突文件加入暂存区，完成合并提交：
```bash
git add .
git commit -m "解决合并代码冲突"
```

---

## 七、新手高频报错与解决办法
1. **报错：fatal: remote origin already exists**
    问题：本地已经关联过远程仓库，重复执行`git remote add`
    解决：先删除旧远程，再重新关联
    ```bash
    git remote remove origin
    git remote add origin 新地址
    ```

2. **报错：Please make sure you have the correct access rights**
    问题：SSH密钥未配置/公钥粘贴错误，无仓库访问权限
    解决：重新生成SSH密钥，复制完整公钥添加到Gitee/GitHub账号

3. **报错：failed to push some refs to 远程地址**
    问题：远程存在本地没有的新版本，推送冲突
    解决：先拉取合并再推送
    ```bash
    git pull origin main --allow-unrelated-histories
    git push origin main
    ```

4. **报错：nothing to commit, working tree clean**
    正常提示：当前无任何文件修改，无需操作

5. **推送提示输入用户名密码，频繁弹窗**
    问题：使用HTTPS地址克隆，切换SSH地址即可免密
    
    ```bash
    git remote set-url origin SSH仓库地址
    ```
    
6. **git reset --hard 误删本地代码，想找回**
    解决：通过`git reflog`找到删除前提交hash，再次reset恢复
    ```bash
    git reflog
    git reset --hard 目标hash值
    ```

---

## 八、新手避坑总结
1. 绝对不要手动删除项目内 `.git` 隐藏文件夹，所有版本记录全部丢失；
2. 提交备注 `-m` 必须写清晰说明，禁止写“更新、修改、随便改改”；
3. 团队协作禁止使用 `git push -f` 强制推送，会覆盖队友代码；
4. `git reset --hard` 属于高危命令，执行前确认无未备份代码；
5. 上传代码前检查敏感文件（密码配置、密钥、本地缓存文件），添加 `.gitignore` 过滤不上传；
6. 新电脑使用Git第一件事：配置全局用户名邮箱，否则提交记录无作者；
7. 大型项目优先使用SSH协议克隆，避免HTTPS频繁输入账号密码；
8. 半成品代码切换分支前用`git stash`储藏，不要随意提交半成品。

### 补充：.gitignore 过滤文件配置
项目根目录新建 `.gitignore` 文件，写入不需要提交的文件/文件夹，示例模板：
```gitignore
# 系统缓存文件
.DS_Store
Thumbs.db
# 代码编辑器缓存
.idea/
.vscode/
# 日志文件
*.log
# 依赖包文件夹
node_modules/
# 本地环境配置
config.local.js
# 编译产物
dist/
build/
```

---

# 使用说明
将全文全部复制，新建文本文档粘贴，保存后修改后缀名从 `.txt` 改为 `Git小白学习手册.md`，可用Typora、VSCode、Obsidian等工具打开，自动渲染分级标题、表格、代码块。
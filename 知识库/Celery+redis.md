# Celery 完整讲解

## 一、Celery 是什么

**Celery 是 Python 开发的分布式异步任务队列框架**。

简单理解：把耗时的任务**丢到后台单独执行**，不让主线程卡住。

核心特性：

1. 异步任务：接收请求立刻返回，任务后台慢慢跑
2. 定时任务：周期性执行任务（定时爬虫、定时报表）
3. 分布式：任务可以分发到多台机器执行
4. 支持任务重试、任务超时、任务状态追踪

> ⚠️ Celery **本身不存储消息**，必须搭配消息中间件（broker）。

## 二、经常和谁连用（两大核心组件）

### 1. Broker 消息代理（消息中转站，必须有）

作用：接收任务、存放待执行任务，celery worker 从这里取任务

常用选型：

- **Redis**（最常用，中小型项目首选）
- **RabbitMQ**（生产级、稳定性高，复杂分布式项目）

> ❌ MySQL/PostgreSQL 不推荐当 Broker（性能差，轮询锁容易出问题）

### 2. Backend 结果存储（可选，需要获取任务返回结果才用）

作用：保存任务执行后的返回值、执行状态

常用：

- Redis
- MySQL / PostgreSQL
- MongoDB

### 日常技术组合（行业主流搭配）

1. FastAPI / Django + Celery + Redis(Broker) + Redis(Backend)

   

   Python Web 项目最通用方案

2. Django + Celery + RabbitMQ + MySQL Backend

   

   大型后台系统、企业项目

3. FastAPI + Celery + RabbitMQ

额外经常配套工具：

- Flower：Celery WEB 监控面板，查看任务运行情况、worker 状态
- Supervisor /systemd：托管 celery worker 进程，保证后台常驻运行

## 三、适用场景（什么时候该用 Celery）

### ✅ 典型场景

1. **Web 接口耗时操作，防止接口超时**

   用户请求触发：发送邮件、推送短信、消息通知、生成 PDF、图片处理

   > 前端点按钮，如果同步处理图片要 5 秒，接口会超时；丢 celery 后台处理，页面立刻返回 “任务处理中”

2. **定时周期性任务**（Celery Beat）

   - 每天凌晨统计报表、数据汇总
   - 定时清理过期日志、清理临时文件
   - 定时爬虫、定时同步第三方数据
   - 定时检查订单状态、自动关闭超时订单

3. **大量任务削峰、异步解耦**

   高并发场景：大量消息推送、批量生成文件，避免瞬间压垮服务

   请求先进入队列，worker 慢慢消费，限流削峰

4. **分布式任务分发**

   多台服务器共同处理任务，横向扩容：增加机器启动更多 worker 提升处理速度

### ❌ 不适合使用场景

1. 需要**立刻拿到任务结果**的超短耗时任务（直接同步执行就行，没必要引入队列）
2. 简单脚本、单机小型工具（引入 celery 增加运维复杂度）
3. 高实时性流式消息处理（优先 Kafka + 消费程序，Celery 不适合海量实时数据流）

## 四、简单架构梳理

```
Web服务(FastAPI/Django) → 推送任务 → Broker(Redis)
                                   ↓
Celery Worker进程 ← 取任务、执行任务
任务结果 → Backend(Redis/数据库)
开发者可查询Backend获取任务成功/失败/返回数据
Celery Beat：定时生成任务，推入Broker
Flower：监控所有worker和任务
```
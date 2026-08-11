## 1. WebSocket

一种基于 TCP、支持**全双工长连接**的通信协议；握手阶段借用 HTTP（101 协议升级），连接建立后客户端与服务端可双向实时收发消息。

- 协议：`ws://`（明文）、`wss://`（加密，生产推荐）
- 对比 HTTP：HTTP 一问一答短连接，服务端无法主动推送；WebSocket 适合 IM 聊天、实时行情、弹幕、在线协同。
- 常用搭配：结合 Redis 发布订阅实现 WebSocket 服务集群消息互通。

## 2. Redis（企业核心用途）

内存型 KV 数据库，项目里承担多种角色：

1. **热点数据缓存**（最常用），减轻 MySQL 压力，解决数据库访问瓶颈；
2. 分布式 Session、接口限流、存储验证码；
3. **分布式锁**，解决微服务并发竞争问题；
4. 利用数据结构实现：计数器、排行榜 (ZSet)、签到 (BitMap)、UV 统计；
5. Pub/Sub 发布订阅、简易消息队列；
6. 搭配 WebSocket：存储在线用户、实现集群间消息转发；
7. 可作为 Celery 的 Broker 与 Result Backend。

> 注意：不建议当做核心主数据库；Redis 作简易队列存在消息丢失风险，核心业务选用专业 MQ。

## 3. Celery Broker

Celery 是 Python 分布式异步任务框架；

**Broker = 消息中间人 / 任务队列**，负责接收、暂存异步任务，供 Worker 拉取执行。

- 流程：业务代码提交任务 → Broker 保存任务 → Worker 消费执行；
- 主流选型：RabbitMQ（官方推荐，消息可靠，生产核心业务首选）、Redis（部署简单，中小型项目常用，存在丢消息风险）；
- ⚠️ 区分：
  - Broker：存放**待执行任务**
  - Result Backend：存放**任务执行后的返回结果**（可选择不配置）

## 整套技术常见联动链路示例

前端 WebSocket 发送请求 → Web 服务提交异步任务至 Celery Broker (Redis/RabbitMQ) → Celery Worker 后台执行任务 → 任务完成后，后端通过 WebSocket 向前端推送结果；

系统同时使用 Redis 承担缓存、分布式锁、消息中转等能力。
# 基于 A2A 官方示例库的测试：天气选日 + 12306 查票

这是一个一次性使用的 A2A 多语言示例，基于官方 `a2a-samples` 的
`weather_and_airbnb_planner` 与 `airbnb_planner_multiagent` 改造而来：

- Host Agent（Python ADK）：读取用户的时间范围和出行路线，先派给天气 Agent，
  再派给车票 Agent。
- Weather Agent（Java Quarkus + LangChain4j + A2A Java SDK）：调用内置的
  Open-Meteo 中国天气 MCP，返回日期范围内的每日天气，并推荐天气最好的一天。
- Ticket Agent（Python LangGraph + A2A Python SDK）：调用 12306 查票 MCP，
  只查询并展示车次、余票和票价，不下单。

两个 Agent 分别用 Java 和 Python 编写，通过 A2A 协议与 Host 通信，体现跨语言互操作。
所有 Agent 的模型统一使用 DeepSeek：Host 通过 LiteLLM 的 `deepseek/deepseek-chat`，
Java 天气 Agent 通过 LangChain4j 的 OpenAI 兼容接口，Python 车票 Agent 通过
`langchain-deepseek`。

## 目录结构

```text
.
├─ host/            # Python ADK Host（官方 weather_and_airbnb_planner 改编）
├─ weather_agent/   # Java Quarkus 天气 Agent + mcp/china_weather_mcp.py
├─ ticket_agent/    # Python LangGraph 车票 Agent
├─ scripts/         # setup.ps1 / start_all.ps1 / stop_all.ps1
├─ .env.example     # 配置模板
└─ README.md
```

## 前提条件

- Windows 10/11，PowerShell
- [uv](https://docs.astral.sh/uv/)（Python 包管理）
- JDK 17+（`scripts/setup.ps1` 会尝试用 winget 安装）
- DeepSeek API Key（在 https://platform.deepseek.com 申请）
- 网络可用（首次运行需要拉取 Python/Maven 依赖，以及 `uvx mcp-server-12306`）

## 配置

1. 复制 `.env.example` 为 `.env`（或运行 setup 脚本自动复制）。
2. 编辑 `.env`：

```dotenv
DEEPSEEK_API_KEY="你的 key"
DEEPSEEK_MODEL="deepseek-chat"
LITELLM_MODEL="deepseek/deepseek-chat"
TICKET_MCP_COMMAND=uvx
TICKET_MCP_ARGS=["mcp-server-12306"]
```

如果 `mcp-server-12306` 需要登录态，可取消注释并填写：

```dotenv
TICKET_MCP_ENV_JSON={"12306_COOKIE": "你的 cookie"}
```

## 安装与启动

```powershell
cd "C:\Users\Administrator\Desktop\基于A2A官方示例库的测试"
powershell -ExecutionPolicy Bypass -File .\scripts\setup.ps1
powershell -ExecutionPolicy Bypass -File .\scripts\start_all.ps1
```

浏览器打开 <http://localhost:8083>，示例提问：

> 8月20日到8月25日，从北京到上海，帮我选天气最好的一天并查车票。

也可以手动分三个终端启动：

```powershell
# 终端 1：天气 Agent（Java，10001）
cd weather_agent
.\mvnw.cmd quarkus:dev

# 终端 2：车票 Agent（Python，10002）
cd ticket_agent
uv run .

# 终端 3：Host UI（8083）
cd host
uv run .
```

停止全部服务：

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\stop_all.ps1
```

## 注意事项

- 天气数据来自 Open-Meteo，中国城市可用；预报仅支持今天起约 14-16 天，
  日期范围不要超过该限制。
- 12306 MCP 默认通过 `uvx mcp-server-12306` 启动；若该服务要求登录，
  请配置 `TICKET_MCP_ENV_JSON`。
- 所有 Agent 使用 DeepSeek `deepseek-chat`；如需换模型，修改 `.env` 中的
  `DEEPSEEK_MODEL` 和 `LITELLM_MODEL`（Host 的 LiteLLM 格式为 `deepseek/模型名`）。
- 本示例只查票展示，不会产生真实订单。
- 当前示例仅供演示，请把远端 Agent 返回的内容视为不可信输入。

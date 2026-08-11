## skill与function call的区别

用真实业务场景举例，层层区分：Function Call / Tool / Skill

场景：智能客服助手，需求：用户可以查天气、查订单、知识库问答

### 1. Tool（原子工具，一个个独立函数）

```
# Tool 1
def get_weather(city: str):
    """查询城市实时天气"""
    ...

# Tool 2
def query_order(order_id: str):
    """根据订单号查询订单信息"""
    ...

# Tool 3
def search_knowledge(query: str):
    """向量库召回相关文档"""
    ...

# Tool 4
def rerank_docs(query: str, docs: list):
    """对召回文档做重排序"""
    ...
```

Tool = 单一功能函数。

### 2. Function Call（模型调用工具的通信方式）

模型不能直接运行代码，依靠 FC 输出结构化 JSON，通知程序执行哪个 Tool。

用户提问：`郑州今天多少度？`

LLM 输出（Function Call 结构）：

json

```
{
  "name": "get_weather",
  "parameters": {"city": "郑州"}
}
```

程序读到这段 JSON → 执行`get_weather("郑州")`

拿到结果再塞回给大模型整理回答。

> 重点：**Function Call 只是一套 “指令格式”，它本身不是能力，是沟通手段。**

### 3. Skill（技能：一套串联的流程，包含多次工具调用 + 业务规则）

我们定义一个 **知识库问答 Skill**

目标：实现高质量 RAG 问答，完整链路：

```
召回文档(search_knowledge) → Rerank筛选文档 → 整理上下文交给LLM生成答案
```

### 这个 Skill 包含：

1. 固定系统提示词（问答规范、输出格式）
2. 连续调用 2 个 Tool：`search_knowledge` + `rerank_docs`
3. 规则：文档不足 3 条直接回复 “无法找到相关资料”
4. 结果清洗、过滤无用文本

### 用户提问：“怎么申请退款？”

Skill 内部自动执行：

1. LLM 通过 FC 调用 `search_knowledge("怎么申请退款")`
2. 获取一堆候选文档
3. 再次调用 FC 执行 `rerank_docs` 过滤低相关文档
4. 把高质量文档组装 prompt 传给 LLM 生成最终答案

✅ **一个 Skill = 多条工具调用 + 流程编排 + 业务约束**

你外部只需要调用【知识库问答 Skill】，不用关心内部先召回还是先 rerank。

### 三者层级关系可视化

plaintext

```
Skill：知识库问答（完整业务能力）
    ├─ 系统Prompt
    ├─ 业务判断规则
    └─ 内部流程：
        ├─ FunctionCall → Tool(search_knowledge)
        └─ FunctionCall → Tool(rerank_docs)
```

### 对比直观区分

1. 用户问天气

   👉 直接一次 FunctionCall 调用 get_weather

   **只有单次工具调用，没必要封装成 Skill**

2. 用户问产品政策

   👉 需要召回 + 重排 + 摘要，一连串操作

   **封装成【知识库问答 Skill】对外暴露，上层 Agent 直接调用这个 Skill**

### 结合 LangGraph（呼应你之前的知识点）

我们搭建主调度图：

- 节点 1：意图识别
- 分支 A：【天气 Skill】（简单：内部单次 FC 调用天气工具）
- 分支 B：【知识库 RAG Skill】（子图，内部包含召回、rerank 两个工具节点）

主图不需要关心 RAG 内部怎么做，只需要触发`rag_skill`节点。

👉 **整个子图 = 一个 Skill，子图内部依靠 Function Call 驱动各个 Tool 执行。**

### 面试极简例子总结

- Tool：单个函数（查天气、检索文档）
- Function Call：大模型输出 JSON 指令，用来触发 Tool 的通信机制
- Skill：把多个 Tool、流程、提示词打包成一个完整可复用任务单元，底层依靠 Function Call 完成工具调度







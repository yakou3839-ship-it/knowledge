# AI 应用开发：Pydantic vs Schema 完整讲解

先理清核心结论：

1. **Schema（模式）是抽象概念**：一套「数据约束规则」，定义数据应该长什么样、字段类型、校验条件；
2. **Pydantic 是 Python 工具库**：在 Python 代码里**实现 Schema** 最主流的框架；
3. 日常大家口中说的 `schema`，很多时候直接指代**Pydantic 模型类**。

> 补充：很多人会写错 `scheme`，正确术语是 **schema**
>
> scheme = 方案、计划；schema = 数据模式（不要混淆）

## 一、基础概念拆解

### 1. Schema（数据模式）

任何描述**数据结构、类型、限制条件**的规范都叫 Schema。

常见种类：

- JSON Schema：通用 JSON 数据规范（独立于编程语言）
- OpenAPI Schema：接口文档的数据模型（FastAPI 自动生成）
- SQL Schema：数据库表结构
- **Pydantic Model：Python 运行时的 Schema 实现**

Schema 只回答问题：

✅ 这个数据有哪些字段？

✅ 每个字段是什么类型？

✅ 取值有什么限制（不能为空、最大长度、数字范围）？

### 2. Pydantic

Python 库，依靠**类型注解**定义数据模型，自动完成：

- 类型强制转换
- 数据合法性校验（不合法直接抛异常）
- 序列化：对象 ↔ dict ↔ JSON
- 导出标准 JSON Schema

**AI 开发为什么离不开它？**

AI 项目高频场景：

1. 调用大模型结构化输出（强制 LLM 返回 JSON，用 Pydantic 校验）
2. FastAPI 搭建 AI 服务，接口入参、出参校验
3. RAG、Agent 工具调用参数定义
4. 解析向量库元数据、对话历史结构

## 二、两者关系一句话

**Pydantic Model = Python 代码层面的 Schema 载体。**

Pydantic 模型可以导出 JSON Schema；

JSON Schema 是通用标准，可以被 Pydantic 反向解析。

关系链路：

```
Pydantic Model(代码) ⇄ JSON Schema(通用标准文本)
```





总结：

指定模型的回答结构化，用pydantic定义schema

```python
# 这一个类，就是我们手写的【Python Schema】
class UserIntentSchema(BaseModel):
    # 字段+类型+校验规则，构成数据模式
    intent: str = Field(description="用户请求意图")
    confidence: float = Field(ge=0.0, le=1.0, description="置信度，0~1")
    keywords: List[str] = Field(default=[], description="提取关键词")
   
# 【重点】Pydantic模型可以导出标准JSON Schema
    json_schema = UserIntentSchema.model_json_schema()
    print("\n=====导出JSON Schema =====")
    print(json_schema)
    
    
{
    "properties": {
        "intent": {"description": "用户请求意图", "type": "string"},
        "confidence": {
            "description": "置信度，0~1",
            "maximum": 1.0,
            "minimum": 0.0,
            "type": "number"
        },
        "keywords": {
            "default": [],
            "description": "提取关键词",
            "items": {"type": "string"},
            "type": "array"
        }
    },
    "required": ["intent", "confidence"],
    "type": "object"
}
```

这个 `json_schema` 就是大家传给大模型的**结构化输出约束**！
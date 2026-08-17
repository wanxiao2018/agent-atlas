# Tool Calling

**中文建议：** 工具调用  
**常见别名：** Tool Use / Function Calling（部分生态中）  
**成熟度：** 🟢  
**词条状态：** ✅ Atlas-quality  
**重要程度：** ★★★★★  
**学习阶段：** 入门必懂  
**最后更新：** 2026-08-17

---

## 30 秒理解

**Tool Calling 是让模型不只“说”，还能请求外部系统替它“做”的机制。**

模型本身通常只能接收输入并生成输出。通过 Tool Calling，它可以表达类似：

> “请调用 `search_web`，参数是 `query=agent harness`。”

真正的搜索并不是模型自己完成的，而是 **Harness / Runtime 收到这个结构化请求以后去执行工具，再把结果返回给模型**。

所以最重要的一句话是：

> **模型负责选择和提出调用，系统负责真正执行。**

---

## 先建立一个直觉

把模型想成坐在办公室里的分析师。

如果没有工具，它只能依靠脑中的知识回答问题。

如果给它：

- 搜索引擎；
- 数据库；
- 计算器；
- 邮件；
- 文件系统；
- Shell；
- 浏览器；

它就可以说：

```text
我需要最新价格
   ↓
调用价格查询工具
   ↓
系统执行
   ↓
得到真实结果
   ↓
模型继续判断
```

工具是“手”，模型不是自己长出了一双手，而是学会了**什么时候该让外部能力介入**。

---

## 为什么需要 Tool Calling？

LLM 有三个天然限制：

1. **知识可能过时** —— 模型权重不是实时数据库；
2. **不能天然访问私有数据** —— 例如你的 CRM、邮件、代码仓库；
3. **不能天然改变外部世界** —— 例如发邮件、写文件、更新数据库。

Tool Calling 把模型和这些能力连接起来。

因此 Agent 的 Action 很多时候就是某种 Tool Call。

```text
Model
  ↓  选择动作
Tool Call
  ↓
Harness / Runtime
  ↓  真正执行
External System
  ↓
Tool Result / Observation
  ↓
Model
```

---

## 技术定义

在工程上，Tool Calling 通常指：

> **模型根据开发者提供的工具定义，生成一个结构化的工具调用请求；宿主系统解析该请求、执行对应函数或外部能力，再把结果作为新的上下文返回模型。**

一个工具定义通常至少包含：

```text
name
├── 工具叫什么

description
├── 什么时候应该使用

input schema
├── 参数有哪些
├── 参数类型是什么

output / result
└── 执行后返回什么
```

OpenAI 的 Function Calling 会让模型生成符合定义 schema 的函数参数；Anthropic 更常使用 `tool use` 这一术语；MCP 中也有自己的 `tools` primitive。名称不同，但都在处理“模型如何请求外部能力”这个问题。

---

## 你可能是在这句话里遇到它

> “The agent called a tool to search the repository, then used the result in the next turn.”

这句话可以拆成：

```text
Agent Loop
   ↓
Model 发现自己缺信息
   ↓
生成 Tool Call
   ↓
Harness 执行工具
   ↓
返回 Tool Result
   ↓
Tool Result 进入 Context
   ↓
下一轮 Model Call
```

所以这里的 `called a tool` 不是“模型内部多想了一步”，而是**模型和外部环境真的发生了一次交互**。

---

## 一个最小例子

假设有一个天气工具：

```python
get_weather(city: str) -> str
```

用户问：

> “北京现在天气怎么样？”

模型可能输出一个结构化请求：

```json
{
  "tool": "get_weather",
  "arguments": {
    "city": "北京"
  }
}
```

然后系统执行：

```python
result = get_weather("北京")
```

得到：

```text
晴，28°C
```

再把结果送回模型：

```text
Tool result: 晴，28°C
```

模型最后才生成自然语言答案。

---

## Tool Calling ≠ Tool Execution

这是最容易被忽略的一条边界。

```text
Tool Calling
= 模型提出“我要调用什么、参数是什么”

Tool Execution
= 宿主系统真正运行代码 / API / 浏览器操作
```

如果模型输出：

```text
请调用 delete_file("important.db")
```

文件并不会因为模型“说了”就自动消失。

是否真的执行、是否需要审批、是否在 Sandbox 中运行，都由外部系统决定。

这也是为什么 **Tool Calling 和权限控制必须一起理解**。

---

## Tool Calling 和 Function Calling 有什么区别？

| 概念 | 最简单理解 |
|---|---|
| Tool Calling / Tool Use | 更宽泛：模型请求使用某种外部能力 |
| Function Calling | 常指通过结构化函数 schema 表达工具调用的一种接口形式 |
| Hosted Tool | 平台直接提供并执行的工具，例如 web search / file search |
| MCP Tool | 由 MCP Server 按 MCP 协议暴露的工具 |

在很多日常讨论里，`Tool Calling` 和 `Function Calling` 会被近似使用；但理解系统架构时，建议把 Tool Calling 当成更上位的概念。

---

## Tool Calling 和 MCP 有什么关系？

`MCP` 不是 Tool Calling 的替代品。

更准确地说：

```text
Tool Calling
= 模型“想调用工具”的机制

MCP
= 外部系统如何以标准协议暴露工具 / 资源 / Prompt
```

所以一个 MCP Server 可以暴露 `search_database` 工具，而 Agent 仍然通过自己的 Tool Calling 机制决定是否调用它。

→ [继续看 MCP](mcp.md)

---

## 为什么工具设计会直接影响 Agent 能力？

工具越多不一定越好。

一个工具如果：

- 名字含糊；
- description 写得不清楚；
- 参数 schema 太复杂；
- 一次返回大量无关内容；
- 错误信息不可理解；

模型就可能选错工具、传错参数，或者把宝贵 Context 浪费在噪声上。

因此 Tool Design 本身已经成为 Agent Engineering 的重要部分。

可以把它理解成：

> **你不是在给传统程序员设计 API，而是在给模型设计“可理解的行动空间”。**

---

## Concept Graph Relations

```text
Agent ──uses────────→ Tools

Agent Loop ─contains→ Tool Calling

Tool Calling ─produces→ Tool Request

Harness ─executes───→ Tool Request

Tool Result ─feeds──→ Context

MCP ─exposes────────→ Tools
```

### 关系说明

- `Agent → Tools`：Agent 借助工具获得外部能力；
- `Agent Loop → Tool Calling`：工具调用通常发生在循环中的某一轮；
- `Harness → Tool Request`：真正解析和执行请求的是外围运行系统；
- `Tool Result → Context`：工具结果通常会成为下一轮模型输入；
- `MCP → Tools`：MCP Server 可以按统一协议暴露工具。

---

## 不同生态怎么叫？

| 生态 | 常见说法 |
|---|---|
| OpenAI | Tools / Function Calling / Function Tools |
| Anthropic | Tool Use / Tools |
| MCP | Tools primitive |
| Agent Frameworks | Tools / Functions / Actions |

名称不同，但遇到这些词时可以先问：

> **“是不是模型在请求一个模型外部的能力？”**

如果是，大概率就在 Tool Calling 这一概念附近。

---

## 常见误解

### ❌ 有 Tool Calling 就一定是 Agent

不一定。固定 workflow 也可以调用工具。

真正的 Agent 通常还包含“根据工具反馈动态决定下一步”的循环。

### ❌ 模型自己执行了函数

通常不是。模型生成调用意图，宿主系统执行。

### ❌ 工具越多 Agent 越强

不一定。工具过多、描述模糊会增加选择难度和 Context 成本。

### ❌ Tool Result 一定可信

不是。外部工具也可能返回错误、恶意或被污染的数据。

---

## Terminology Observatory

**成熟度：🟢 稳定术语。**

“模型调用外部函数 / 工具”已经成为现代 LLM API 和 Agent 系统中的基础能力。

需要注意的是，不同厂商的 API 命名仍不完全一致，因此：

```text
Tool Calling
Tool Use
Function Calling
```

在文档中经常交叉出现。

---

## 下一步应该学什么？

1. [Function Calling](function-calling.md) —— 结构化函数调用接口；
2. [MCP](mcp.md) —— 工具如何通过统一协议被暴露；
3. [Agent Loop](../02-agent-core/agent-loop.md) —— 工具结果怎样进入下一轮；
4. [Harness](../03-infrastructure/harness.md) —— 谁真正执行调用并管理权限；
5. [Sandbox](../03-infrastructure/sandbox.md) —— 高风险代码和命令在哪里安全执行。

---

## 一手资料

- OpenAI, [Function Calling in the OpenAI API](https://help.openai.com/en/articles/8555517)
- OpenAI, [A practical guide to building agents](https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/)
- OpenAI Agents SDK, [Tools / Function tools](https://openai.github.io/openai-agents-python/)
- Anthropic, [Writing effective tools for AI agents](https://www.anthropic.com/engineering/writing-tools-for-agents)
- Model Context Protocol, [Tools specification](https://modelcontextprotocol.io/specification/2025-06-18/server/tools)

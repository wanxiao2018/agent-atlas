# MCP

**英文全称：** Model Context Protocol  
**中文建议：** 模型上下文协议  
**成熟度：** 🟡  
**词条状态：** ✅ Atlas-quality  
**重要程度：** ★★★★★  
**学习阶段：** 入门 → 工程实践  
**最后更新：** 2026-08-17

---

## 30 秒理解

**MCP 是一种让 AI 应用用统一方式连接外部工具、数据和工作流的开放协议。**

如果没有 MCP，每接一个数据库、GitHub、文件系统或业务工具，Agent 应用都可能需要自己写一套不同的适配代码。

MCP 想解决的问题很像：

> **不要让每个 AI 应用和每个外部系统都单独“拉一根线”，而是约定一个共同接口。**

官方常用的类比是：**MCP 像 AI 应用世界里的 USB-C。**

---

## 先建立一个直觉

假设你有三个 AI 应用：

```text
Claude
ChatGPT
Coding Agent
```

又有四个外部系统：

```text
GitHub
PostgreSQL
Google Drive
内部 CRM
```

如果每一对都单独开发连接方式：

```text
3 个 AI 应用 × 4 个系统 = 12 套集成
```

系统越多，组合爆炸越严重。

MCP 的思路是：

```text
AI 应用
   ↓
统一 MCP Client
   ↓
MCP Protocol
   ↓
不同 MCP Server
   ├── GitHub
   ├── Database
   ├── Files
   └── CRM
```

于是外部能力可以更容易被不同 AI 应用复用。

---

## MCP 到底是什么？

MCP 不是一个 Agent，也不是一个工具，更不是一个 Agent Framework。

它是一套**通信协议与能力模型**。

当前官方架构采用：

```text
Host
├── MCP Client A ───── MCP Server A
├── MCP Client B ───── MCP Server B
└── MCP Client C ───── MCP Server C
```

其中：

### Host

AI 应用本身，例如一个聊天应用、IDE 或 Agent 产品。

Host 负责：

- 创建和管理 MCP Clients；
- 权限和用户同意；
- 安全策略；
- 上下文聚合；
- 与模型 / Agent 的集成。

### Client

Host 内部与某一个 Server 建立连接的协议客户端。

官方架构中，一个 Client 与一个 Server 保持 1:1 的会话关系。

### Server

对外暴露具体能力。

例如一个 GitHub MCP Server 可以暴露：

- 仓库资源；
- 搜索工具；
- 创建 Issue 的工具；
- 预定义 Prompt。

MCP 基础消息使用 JSON-RPC，并通过初始化与 capability negotiation 确认双方支持哪些功能。

---

## MCP Server 能暴露什么？

理解 MCP 最关键的是记住三个核心 primitive：

```text
MCP Server
├── Prompts
├── Resources
└── Tools
```

它们不是同一个东西。

### Prompts

预定义的模板或交互流程。

可以先理解为：

> “这里有一套可以直接使用的任务模板。”

### Resources

给模型 / 应用提供上下文的数据。

例如：

- 文件内容；
- 数据库 schema；
- Git 历史；
- 应用内部信息。

MCP 官方把 Resources 设计为更偏 **application-controlled**：Host / Client 决定什么时候把这些资源加入 Context。

### Tools

可以真正执行的外部能力。

例如：

- 查询数据库；
- 调 API；
- 搜索；
- 写文件；
- 运行计算。

MCP 官方将 Tools 描述为更偏 **model-controlled**：模型可以根据当前语境选择并调用工具。

一个很好用的记忆方式：

```text
Prompts    → “怎么问 / 怎么开始”
Resources  → “给模型看什么”
Tools      → “让模型能做什么”
```

---

## 你可能是在这句话里遇到它

> “The agent connects to a GitHub MCP server and discovers its available tools.”

这句话不是说：

> “MCP 自己在运行 Agent。”

而是：

```text
Agent Application / Host
        ↓
创建 MCP Client
        ↓
连接 GitHub MCP Server
        ↓
双方协商 capabilities
        ↓
Client 获取 tools/list
        ↓
Agent 看到可用工具
        ↓
模型决定是否调用
```

MCP 负责的是**连接、发现和协议交互**。

至于模型为什么选择某个工具、工具结果如何进入下一轮 Agent Loop，则属于 Harness / Agent Runtime 的问题。

---

## MCP 和 Tool Calling 的关系

这是最容易混淆的一组概念。

### Tool Calling

解决：

> **模型如何表达“我想调用这个工具”。**

### MCP

解决：

> **工具、资源和 Prompt 如何以标准方式被外部系统暴露给 AI 应用。**

所以：

```text
MCP Server
   ↓ exposes
Tool
   ↓ discovered by
Agent Host
   ↓ provided to
Model
   ↓ Tool Calling
Tool Request
   ↓
MCP Client → MCP Server
```

两者互相配合，但不是同一层。

→ [Tool Calling](tool-calling.md)

---

## MCP ≠ API

MCP 最终仍可能通过 API 与后端系统交互，但它不是普通 REST API 的简单重命名。

普通 API 关注：

```text
程序 ↔ 服务
```

MCP 额外定义了适合 AI 应用的概念和生命周期，例如：

- capability negotiation；
- tools；
- resources；
- prompts；
- session；
- sampling 等客户端能力；
- 安全边界和用户授权。

你可以理解成：

> **API 是底层能力接口；MCP 是让 AI Host/Client 能以统一方式理解和使用这些能力的一套协议。**

---

## MCP ≠ Agent Framework

| 概念 | 主要负责什么 |
|---|---|
| MCP | AI 应用与外部能力之间的标准连接协议 |
| Agent Framework / SDK | 帮开发者构建 Agent、Loop、Handoff 等逻辑 |
| Harness | 模型外部的整体运行与控制系统 |
| Tool Calling | 模型请求使用某项工具的机制 |
| API | 一个系统对外暴露功能的程序接口 |

一个 Agent Framework 可以支持 MCP；一个 Harness 也可以内置 MCP Client。

但 MCP 本身并不负责“把整个 Agent 跑起来”。

---

## 为什么 MCP 对 Agent 很重要？

### 1. 降低集成成本

同一个 MCP Server 可以被多个兼容客户端使用。

### 2. 让能力更容易被发现

客户端可以通过协议列出 Server 暴露的 tools / resources / prompts。

### 3. 建立边界

MCP 架构强调 Host 负责用户授权和安全策略，并保持不同 Server 之间的隔离。

### 4. 让 Agent 生态更加模块化

Agent 不必把所有外部能力直接写死在应用代码里。

---

## 一个最小心智模型

```text
User
  ↓
AI Host
  ├── Model
  ├── Agent Loop
  └── MCP Client
          ↓ JSON-RPC / MCP
      MCP Server
       ├── Tool: search_repo
       ├── Tool: create_issue
       ├── Resource: repo://README
       └── Prompt: review_pr
```

模型不需要知道 Server 内部怎么实现 GitHub API。

它只需要看到 Host 提供给它的工具定义，并在需要时选择调用。

---

## 安全为什么特别重要？

MCP 连接的是**真实系统能力**。

如果一个 Server 暴露：

```text
delete_database
send_email
publish_post
transfer_money
```

那么“模型能发现工具”绝不等于“模型应该无条件执行工具”。

因此 MCP 官方规范明确强调：

- Host 控制连接权限和生命周期；
- 用户授权和同意应由 Host 管理；
- 工具调用应有清晰的人类可见性；
- 敏感操作需要合理审批；
- Server 提供的 metadata / annotations 不能默认视为可信。

这也是 MCP 必须和 **Permissions / Guardrails / Human-in-the-loop** 一起学习的原因。

---

## Concept Graph Relations

```text
Agent / Host ─uses──────→ MCP Client

MCP Client ─connects────→ MCP Server

MCP Server ─exposes─────→ Tools
MCP Server ─exposes─────→ Resources
MCP Server ─exposes─────→ Prompts

Resources ─feed─────────→ Context

Model ─uses─────────────→ Tool Calling

Tool Calling ─may-route-via→ MCP
```

---

## 常见误解

### ❌ MCP = “给 Agent 加工具”

不完整。MCP 不只包含 Tools，还包含 Resources、Prompts 和协议生命周期。

### ❌ 有 MCP 就自动变成 Agent

不是。MCP 只是连接协议。

### ❌ MCP Server 能看到整个聊天记录

不应该默认如此。官方架构强调 Server 只应获得完成自身职责所需的上下文，全局上下文由 Host 控制。

### ❌ MCP 替代所有 API

不是。Server 内部往往仍然调用传统 API、数据库或本地程序。

---

## Terminology Observatory

**成熟度：🟡 正在快速标准化和扩展。**

MCP 已经形成正式规范、版本化协议和广泛客户端 / Server 生态，因此早已不是一个随意 Buzzword。

但协议仍在快速演进：新的 revision、能力和生态实践会持续出现，所以 Agent Atlas 暂时保留 🟡，并要求词条定期复查。

---

## 下一步应该学什么？

1. [Tool Calling](tool-calling.md) —— 模型如何决定调用工具；
2. [Context Engineering](../05-context-memory/context-engineering.md) —— Resources 和 Tool Results 怎么进入 Context；
3. [Harness](../03-infrastructure/harness.md) —— 谁管理 MCP Client 和 Agent Loop；
4. [Runtime](../03-infrastructure/runtime.md) —— 调用和任务在哪里运行；
5. Guardrails / Permissions —— 谁允许高风险动作真正发生。

---

## 一手资料

- Model Context Protocol, Introduction: https://modelcontextprotocol.io/docs/getting-started/intro
- MCP Architecture: https://modelcontextprotocol.io/specification/2025-06-18/architecture
- MCP Tools specification: https://modelcontextprotocol.io/specification/2025-06-18/server/tools
- MCP Resources specification: https://modelcontextprotocol.io/specification/2025-11-25/server/resources
- MCP Overview / primitives: https://modelcontextprotocol.io/specification/2024-11-05/server/index

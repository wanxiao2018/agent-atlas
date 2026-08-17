# 核心概念地图

> **Don't just define the term. Locate it.**

Agent Atlas 的核心不是一串互不相关的术语，而是一张不断生长的 **Agent Engineering Concept Graph**。

这张图的作用不是声称“所有 Agent 都必须按这种架构实现”，而是帮助学习者回答三个问题：

1. 我现在看到的这个词，大致属于 Agent 系统的哪一层？
2. 它依赖谁、影响谁、通常和谁一起出现？
3. 如果我已经懂了这个词，下一步最值得理解哪个相邻概念？

## v0.2 核心骨架

```text
                       ┌── Prompt
                       │
                  Context
                ↙      ↓       ↘
             Memory   RAG    Compaction
                │
                ↓
Model ─────→ Agent ←──── Harness
                         │
            ┌────────────┼────────────┐
            ↓            ↓            ↓
        Agent Loop      Tools       Runtime
            │            │            │
            ↓            ↓            ↓
         Planning       MCP        Sandbox
            │
            ↓
      Action/Observation
```

## 怎么读这张图？

### Model → Agent

`Model` 提供语言理解、生成与推理能力，但一个能够持续完成任务的 `Agent` 通常还需要模型之外的执行机制。

所以阅读 Agent 系统时，一个非常重要的问题是：

> 现在描述的是 **model capability**，还是 **agent system capability**？

很多初学者会把两者混在一起。

### Context → Memory / RAG / Compaction

`Context` 是模型在一次调用时实际能看到的信息集合。

它的内容可能来自：

- Prompt / system instructions
- 当前对话历史
- Memory 中取回的信息
- RAG 检索结果
- Tool results
- Files / repository context

而 `Compaction` 解决的是：当历史越来越长时，怎样压缩旧信息，同时尽量保留继续完成任务所需的内容。

因此：

```text
Memory ≠ Context
RAG ≠ Memory
Compaction ≠ Summarization 的简单同义词
```

它们都与 Context 有关，但负责的是不同问题。

### Harness → Agent Loop / Tools / Runtime

`Harness` 可以暂时理解为：**围绕模型、让 Agent 能可靠工作的外围执行与控制系统。**

其中经常会包含：

```text
Harness
├── Agent Loop
├── Context management
├── Tool dispatch
├── State management
├── Permissions
├── Retry / recovery
├── Runtime integration
└── Tracing / observability
```

注意：这是一种帮助理解的分解，不是统一标准。

### Agent Loop → Planning → Action / Observation

Agent Loop 是 Agent 持续工作的“心跳”。

一个最小抽象可以写成：

```text
观察当前状态
   ↓
决定下一步
   ↓
执行 Action
   ↓
获得 Observation
   ↓
更新 Context / State
   ↓
继续下一轮或结束
```

`Planning` 可能发生在一次循环前，也可能在循环过程中不断重规划。

### Tools → MCP

`Tools` 是 Agent 能够调用的外部能力，例如：

- 搜索
- 数据库查询
- 文件读写
- Shell / code execution
- 浏览器
- 邮件 / 日历 / Slack

`MCP` 不是“Tool”的同义词。它更接近一种标准化连接方式，让客户端 / Agent 系统能够发现并使用外部提供的 tools、resources 等能力。

### Runtime → Sandbox

`Runtime` 关注 Agent 的代码、工具调用或任务到底在哪个执行环境中运行。

`Sandbox` 则强调隔离和限制：即使 Agent 能执行代码，也不应默认拥有对真实机器、凭据、网络和文件系统的无限权限。

因此：

```text
Sandbox 通常属于 Runtime / execution environment 的一个重要设计问题
Runtime 不等于 Sandbox
```

---

## Concept Graph 的关系类型

为了让后续知识库可以真正变成“图”，Agent Atlas 不只记录“相关术语”，还计划记录关系类型。

| 关系 | 含义 | 示例 |
|---|---|---|
| `contains` | A 通常包含 B | Harness → Agent Loop |
| `feeds` | A 为 B 提供信息 | Memory → Context |
| `uses` | A 使用 B | Agent → Tools |
| `executes-in` | A 在 B 中执行 | Tool code → Runtime |
| `isolated-by` | A 受 B 隔离 | Code execution → Sandbox |
| `connects` | A 连接多个系统 | MCP → Agent / external tools |
| `produces` | A 产生 B | Action → Observation |
| `precedes` | 学习或流程上通常先于 | Planning → Action |
| `contrasts-with` | 概念边界对比 | Agent ↔ Workflow |
| `confused-with` | 高频混淆 | Harness ↔ Framework |
| `evolved-from` | 术语 / 工程范式演化 | Prompt Engineering → Context Engineering |

这些关系未来可以用于生成可点击的交互式 Concept Map。

---

## 第一批核心节点

### Foundation

- [Agent](01-foundations/agent.md)
- [LLM](01-foundations/llm.md)
- [Prompt](01-foundations/prompt.md)
- [Context Window](01-foundations/context-window.md)

### Agent Core

- [Agent Loop](02-agent-core/agent-loop.md)
- [Planning](02-agent-core/planning.md)
- [Action / Observation](02-agent-core/action-observation.md)
- [Stop Condition](02-agent-core/stop-condition.md)

### Infrastructure

- [Harness](03-infrastructure/harness.md)
- [Runtime](03-infrastructure/runtime.md)
- [Sandbox](03-infrastructure/sandbox.md)
- [State](03-infrastructure/state.md)

### Tools

- [Tool Calling](04-tools/tool-calling.md)
- [Function Calling](04-tools/function-calling.md)
- [MCP](04-tools/mcp.md)

### Context & Memory

- [Context Engineering](05-context-memory/context-engineering.md)
- [Memory](05-context-memory/memory.md)
- [RAG](05-context-memory/rag.md)

---

## 下一版地图要补什么？

v0.2 先建立主骨架，后续至少要继续补三类关系：

**可靠性层**：Evals、Tracing、Observability、Guardrails、Human-in-the-loop、Retry、Checkpoint。

**多 Agent 层**：Sub-agent、Handoff、Orchestrator、Supervisor、Router、Shared State。

**工程范式层**：Prompt Engineering、Context Engineering、Harness Engineering、Loop Engineering，以及它们之间的边界与演化。

最终目标不是画出一张看起来很复杂的图，而是让读者能够从任何一个陌生词出发，沿着关系找到自己下一步真正需要理解的概念。

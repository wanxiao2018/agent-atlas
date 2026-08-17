# Agent Atlas

> **不只解释这个词，还告诉你它在整个 Agent 世界的哪里。**  
> **Don't just define the term. Locate it.**

Agent Atlas 是一个面向 **Agent / Agentic AI 学习者与实践者** 的**语境型概念地图（Contextual Concept Atlas）**。

它不是为了做最大最全的 A–Z 术语表，也不是为了重复已有的 Agent 课程和 Awesome List。它更关注一个真实而高频的问题：

> 当你在书、论文、技术博客、GitHub、SDK 文档里突然遇到 `Harness`、`Agent Loop`、`Compaction`、`MCP`、`Scaffolding` 这样的词时，怎样快速知道它到底在说什么，并把它放回整个 Agent Engineering 的知识结构里？

因此，每个核心概念不仅回答“它是什么”，还尽量回答：

1. **30 秒怎么理解？**
2. **为什么会出现这个概念？**
3. **你通常会在哪种原文语境里遇到它？**
4. **它在整个 Agent 系统的什么位置？**
5. **它和相邻概念是什么关系？**
6. **它最容易和什么混淆？**
7. **不同公司 / 框架是否用不同名字表达相近概念？**
8. **这个术语是稳定概念，还是正在形成的新说法？**
9. **有哪些一手资料可以继续深入？**

---

## 从这张图开始

这张图是 Agent Atlas v0.2 的第一版核心概念骨架。它不是唯一正确的 Agent 架构，而是一张帮助初学者建立心智模型的“地图底图”。

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

第一次阅读时，不必试图一次记住所有词。先理解几条主线：

- **Model → Agent**：模型如何从“生成文本”变成“围绕目标持续行动的系统”。
- **Context → Memory / RAG / Compaction**：模型这一轮到底能看到什么，以及信息如何被取回、保留和压缩。
- **Harness → Loop / Tools / Runtime**：模型外部的执行与控制系统怎样让 Agent 真正工作起来。
- **Agent Loop → Planning → Action / Observation**：Agent 如何一轮一轮决定下一步，并根据反馈继续行动。
- **Tools → MCP**：Agent 如何获得模型本身没有的外部能力。
- **Runtime → Sandbox**：Agent 在什么环境里真正执行代码、命令或其他操作。

→ [进入完整核心概念地图](concept-map.md)

---

## Agent Atlas 与普通 Glossary 有什么不同？

### 1. Contextual Glossary｜语境型解释

不仅给定义，还解释这个词**为什么会出现在你正在读的那句话里**。

例如你看到：

```text
The harness re-enters the agent loop after the tool result is returned.
```

Agent Atlas 不会只分别翻译 `harness` 和 `agent loop`，而会解释整句话背后的执行过程：

```text
模型请求工具
   ↓
Harness 执行工具
   ↓
得到结果 / Observation
   ↓
结果加入 Context
   ↓
进入下一轮 Agent Loop
```

### 2. Concept Graph｜概念关系图

术语不是孤立单词，而是图中的节点。

我们会记录类似这样的关系：

- `Harness` **contains** `Agent Loop`
- `Runtime` **may use** `Sandbox`
- `MCP` **connects** Agent / Tools / external systems
- `Memory` **feeds** `Context`
- `Agent Loop` **produces** `Action / Observation` cycles
- `Harness` **is often confused with** `Framework`

### 3. Terminology Observatory｜术语观察站

Agent 领域变化很快。我们会区分：

- 🟢 **Stable**：定义与用法相对稳定
- 🟡 **Evolving**：行业广泛使用，但边界或命名仍在演化
- 🔴 **Emerging / Contested**：新兴、争议较大，尚未形成稳定共识

并尽量记录：早期来源、流行时间、当前常见含义与不同生态的差异。

### 4. Concept Boundaries｜概念边界

很多时候真正困难的不是“不知道 A”，而是“不知道 A 和 B 到底差在哪”。

因此 Agent Atlas 会系统整理：

- Agent vs Workflow
- Harness vs Framework
- Harness vs Runtime
- Context vs Memory
- Memory vs RAG
- Tool Calling vs Function Calling
- Agent Loop vs Loop Engineering
- Skill vs Tool
- Skill vs MCP
- Sub-agent vs Multi-Agent
- Tracing vs Observability

---

## 我们不追求什么？

Agent Atlas **不以术语数量作为主要 KPI**。

我们更关心：

- 有多少核心概念真正解释清楚；
- 有多少概念关系被明确建立；
- 有多少组易混淆概念被讲透；
- 有多少真实原文语境被拆解；
- 有多少重要结论能追溯到一手资料。

一个词只有“定义”，只能算 **🚧 Stub**；当它至少具备**定义、语境、关系、边界、来源**后，才有资格成为 **✅ Atlas-quality** 词条。

---

## 推荐阅读顺序

如果你刚进入 Agent Engineering，可以先按这条主线阅读：

**Agent → Agent Loop → Harness → Runtime → Sandbox → Tool Calling → MCP → Context Engineering → Memory → RAG → Handoff → Evals → Harness Engineering → Loop Engineering**

也可以直接从你正在阅读材料里遇到的陌生词开始，再顺着“相关概念”不断向外探索。

→ [查看学习路线](roadmap.md)  
→ [了解项目设计原则](reference/project-principles.md)  
→ [查看词条标准模板](reference/term-template.md)

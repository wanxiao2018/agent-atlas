# Agent Atlas

> **不只解释这个词，还告诉你它在整个 Agent 世界的哪里。**  
> **Don't just define the term. Locate it.**

Agent Atlas 是一个面向 **Agent / Agentic AI 学习者与实践者** 的**语境型概念地图（Contextual Concept Atlas）**。

它不是为了做最大最全的 A–Z 术语表，也不是为了重复已有的 Agent 课程和 Awesome List。它更关注一个真实而高频的问题：

> 当你在书、论文、技术博客、GitHub、SDK 文档里突然遇到 `Harness`、`Agent Loop`、`Compaction`、`MCP`、`Scaffolding` 这样的词时，怎样快速知道它到底在说什么，并把它放回整个 Agent Engineering 的知识结构里？

因此，每个核心概念不仅回答“它是什么”，还尽量回答：它为什么出现、通常出现在哪种语境、在系统中位于哪里、与哪些概念相连、最容易和什么混淆，以及哪些一手资料值得继续阅读。

---

## 从这张图开始

这张图是 Agent Atlas 的核心概念骨架。它不是唯一正确的 Agent 架构，而是一张帮助初学者建立心智模型的“地图底图”。

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

第一次阅读时，不必一次记住所有词。先理解几条主线：

- **Model → Agent**：模型如何从“生成输出”进入“围绕目标持续行动”的系统。
- **Context → Memory / RAG / Compaction**：模型这一轮到底能看到什么，以及信息如何被取回、保留和压缩。
- **Harness → Loop / Tools / Runtime**：模型外部的执行与控制系统怎样让 Agent 真正工作起来。
- **Agent Loop → Planning → Action / Observation**：Agent 如何一轮一轮决定下一步，并根据反馈继续行动。
- **Tools → MCP**：Agent 如何获得模型本身没有的外部能力。
- **Runtime → Sandbox**：Agent 在什么环境里真正执行代码、命令或其他操作。

→ [进入完整核心概念地图](concept-map.md)

---

## Agent Atlas 与普通 Glossary 有什么不同？

### Contextual Glossary｜语境型解释

不仅给定义，还解释这个词**为什么会出现在你正在读的那句话里**。

例如：

```text
The harness re-enters the agent loop after the tool result is returned.
```

我们会把它还原成执行过程：

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

### Concept Graph｜概念关系图

术语不是孤立单词，而是图中的节点。我们记录 `contains`、`feeds`、`uses`、`connects`、`confused-with` 等明确关系，让读者知道一个词的上下游和相邻概念。

### Terminology Observatory｜术语观察站

Agent 领域变化很快。我们区分稳定术语、仍在演化的行业说法，以及新兴或存在争议的表达，并尽量保留来源、时间和不同生态的使用差异。

### Concept Boundaries｜概念边界

真正困难的往往不是“不知道 A”，而是“不知道 A 和 B 到底差在哪”。因此会重点整理：

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

## 阅读方式

如果你刚进入 Agent Engineering，可以从：

**Agent → Agent Loop → Harness → Runtime → Sandbox → Tool Calling → MCP → Context Engineering → Memory → RAG**

开始建立第一条主线。

也可以直接搜索你正在阅读材料里遇到的陌生词，再沿着页面中的关系继续探索。

→ [查看学习路线](roadmap.md)  
→ [了解项目设计原则](reference/project-principles.md)  
→ [查看工程说明](reference/engineering.md)

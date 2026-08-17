# State

**中文建议：** 状态  
**成熟度：** 🟢  
**重要程度：** ★★★★☆

## 一句话解释

Agent 在一次任务运行过程中需要持续保存的当前信息，例如步骤、变量、文件引用、任务进度或会话数据。

## 为什么需要它？

没有状态，Agent 很难跨步骤保持一致性，也难以暂停、恢复或协调多阶段任务。

## 在 Agent 系统中的位置

State 通常由 Harness / Runtime 管理，并与 Session、Checkpoint、Memory 和 Context 相互作用。

## 最容易混淆

State 更偏“当前运行现在是什么情况”；Memory 更强调“哪些信息值得在之后再次检索和复用”。两者可以使用相同存储技术，但语义职责不同。

## 相关概念

- [Runtime](runtime.md)
- [Memory](../05-context-memory/memory.md)
- [Context Engineering](../05-context-memory/context-engineering.md)

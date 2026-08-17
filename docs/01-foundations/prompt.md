# Prompt

**中文建议：** 提示词 / 提示  
**成熟度：** 🟢  
**重要程度：** ★★★★☆

## 一句话解释

发送给模型、用于表达任务、约束行为或提供当前信息的输入内容。

## 为什么需要它？

Prompt 是控制模型行为的重要接口，但复杂 Agent 还需要上下文管理、工具、状态与运行时。

## 在 Agent 系统中的位置

Prompt 是 Context 的组成部分之一。Context 还可能包含历史消息、工具结果、检索内容、Memory 和文件。

## 最容易混淆

Prompt Engineering 不等于 Context Engineering，更不等于 Agent Engineering。前者主要优化“怎么表达”，后两者分别关注“模型此刻看到什么”和“完整 Agent 系统如何工作”。

## 相关概念

- [Context Engineering](../05-context-memory/context-engineering.md)
- [Context Window](context-window.md)
- [Agent](agent.md)

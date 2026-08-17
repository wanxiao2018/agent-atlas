# Context Window

**中文建议：** 上下文窗口  
**成熟度：** 🟢  
**重要程度：** ★★★★★

## 一句话解释

模型在一次推理调用中能够直接处理的上下文容量边界。

## 为什么需要理解它？

Agent 工作时间越长，历史消息、工具结果、文件内容和检索结果越多。Context Window 有限，因此系统必须决定哪些信息保留、检索、压缩或丢弃。

## 在 Agent 系统中的位置

它直接约束 Context Engineering，并影响 Memory、RAG、Compaction 与长任务设计。

## 最容易混淆

Context Window ≠ 长期记忆。窗口描述“这次调用能直接看到多少”；Memory 描述“哪些信息可以在窗口之外保存并在需要时重新取回”。

## 相关概念

- [Context Engineering](../05-context-memory/context-engineering.md)
- [Memory](../05-context-memory/memory.md)
- [RAG](../05-context-memory/rag.md)

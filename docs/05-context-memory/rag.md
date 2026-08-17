# RAG

**中文建议：** 检索增强生成  
**英文全称：** Retrieval-Augmented Generation  
**成熟度：** 🟢  
**重要程度：** ★★★★☆

## 一句话解释

先从外部知识源检索与当前任务相关的内容，再把结果放进 Context 供模型生成或决策。

## 为什么需要它？

模型参数不可能包含所有最新、私有或任务专属知识。RAG 让系统在推理时动态取回相关信息，而不是要求所有知识都固化在模型内部。

## 在 Agent 系统中的位置

RAG 是 Context 构建的一种信息来源。检索结果进入 Context 后，模型才能在当前调用中直接使用。

## 最容易混淆

RAG ≠ Memory。RAG 更强调从外部知识源检索相关知识；Memory 更强调保存并重新取回用户、任务或 Agent 过去的重要信息。底层检索技术可以重叠，但职责不同。

## 相关概念

- [Context Engineering](context-engineering.md)
- [Memory](memory.md)
- [Context Window](../01-foundations/context-window.md)

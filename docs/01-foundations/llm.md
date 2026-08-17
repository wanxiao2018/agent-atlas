# LLM

**中文建议：** 大语言模型  
**成熟度：** 🟢  
**重要程度：** ★★★★★

## 一句话解释

根据上下文预测并生成文本或结构化输出的语言模型。

## 为什么需要它？

在 Agent 中，LLM 常充当理解、推理、生成与决策核心，但它本身不等于完整 Agent。

## 在 Agent 系统中的位置

通常位于 Agent 的 Model 层，并接收当前 Context，输出文本、结构化结果或下一步动作请求。

## 最容易混淆

LLM ≠ Agent。模型负责生成与判断；Agent 系统还包含循环、工具、状态、运行环境和控制机制。

## 相关概念

- [Agent](agent.md)
- [Context Engineering](../05-context-memory/context-engineering.md)
- [Agent Loop](../02-agent-core/agent-loop.md)

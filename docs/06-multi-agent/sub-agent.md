# Sub-agent

**中文建议：** 子 Agent  
**成熟度：** 🟡  
**重要程度：** ★★★★☆

## 一句话解释

由主 Agent 或编排层委派某个子任务、通常具有独立上下文或工具配置的 Agent。

## 为什么需要它？

复杂任务可以按责任拆成更小的工作单元，降低主上下文污染，并支持并行或专业化处理。

## 在 Agent 系统中的位置

Sub-agent 通常由主 Agent、Router 或 Orchestrator 调度，并把结果返回上层任务。

## 最容易混淆

Sub-agent ≠ 普通函数。它通常拥有自己的模型调用、上下文和任务边界；是否拥有完整独立 Agent Loop 则取决于具体系统设计。

## 相关概念

- [Handoff](handoff.md)
- [Orchestrator](orchestrator.md)
- [Agent](../01-foundations/agent.md)

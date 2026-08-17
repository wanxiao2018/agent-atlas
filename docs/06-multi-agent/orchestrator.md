# Orchestrator

**中文建议：** 编排器 / 调度层  
**成熟度：** 🟡  
**重要程度：** ★★★★☆

## 一句话解释

负责决定任务如何拆分、由哪个 Agent 或组件执行，以及结果如何汇总和继续推进的协调层。

## 为什么需要它？

多个 Agent 如果没有协调，容易重复劳动、争抢状态或产生上下文冲突。Orchestrator 提供任务分配和协作边界。

## 在 Agent 系统中的位置

位于 Multi-agent 系统的协调层，可以由确定性代码、模型驱动逻辑或两者组合实现。

## 最容易混淆

Orchestrator 不一定是一个 Agent。它可以只是传统程序中的调度组件；只有当模型参与其决策时，它才更具有 agentic 特征。

## 相关概念

- [Sub-agent](sub-agent.md)
- [Handoff](handoff.md)
- [Agent Loop](../02-agent-core/agent-loop.md)

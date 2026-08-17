# Handoff

**中文建议：** 移交 / 任务交接  
**成熟度：** 🟡  
**重要程度：** ★★★★☆

## 一句话解释

一个 Agent 将当前任务的处理权、上下文或责任转交给另一个 Agent 的机制。

## 为什么需要它？

当不同 Agent 专门处理不同领域时，Handoff 让系统能够从一个角色切换到另一个角色，而不要求单个 Agent 包办全部任务。

## 在 Agent 系统中的位置

它属于 Multi-agent 协作和路由机制，常由 Agent Loop 或 Orchestrator 处理。

## 最容易混淆

Handoff 强调**控制权或责任转移**；Tool Calling 通常仍由当前 Agent 保持任务控制权，只是临时调用一个外部能力。

## 相关概念

- [Sub-agent](sub-agent.md)
- [Orchestrator](orchestrator.md)
- [Tool Calling](../04-tools/tool-calling.md)

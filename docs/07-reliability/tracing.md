# Tracing

**中文建议：** 轨迹追踪 / 链路追踪  
**成熟度：** 🟢  
**重要程度：** ★★★★★

## 一句话解释

记录一次 Agent 运行中模型调用、工具调用、Handoff、状态变化和其他关键步骤的完整链路。

## 为什么需要它？

Agent 失败往往发生在中间某一步。只有最终答案很难解释“它为什么失败”，Trace 可以帮助定位具体决策和执行节点。

## 在 Agent 系统中的位置

Tracing 是 Observability 与 Evals 的重要数据来源，也常用于调试 Harness 和 Agent Loop。

## 最容易混淆

日志可以是零散事件；Trace 更强调一次任务运行中多个事件之间的因果和层级关系。

## 相关概念

- [Evals](evals.md)
- [Agent Loop](../02-agent-core/agent-loop.md)
- [Harness](../03-infrastructure/harness.md)

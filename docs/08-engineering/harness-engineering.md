# Harness Engineering

**中文建议：** Harness 工程  
**成熟度：** 🔴  
**重要程度：** ★★★★★

## 一句话解释

围绕 Agent 的循环、工具、上下文、状态、权限、恢复和可观测性，系统设计与优化模型外围运行机制的工程实践。

## 为什么需要它？

Agent 的真实能力不只取决于模型。工具接口、Context 管理、Runtime、Sandbox、验证与恢复机制都会显著影响任务成功率和可靠性。

## 在 Agent 系统中的位置

Harness Engineering 位于系统工程层，关注“模型怎样被组织成一个可可靠运行的 Agent”，而不只是优化单次 Prompt。

## 最容易混淆

这是快速形成中的行业表达，并没有像经典软件工程术语那样完全固定的边界。阅读资料时要结合作者对 `Harness` 的具体范围判断。

## 相关概念

- [Harness](../03-infrastructure/harness.md)
- [Agent Loop](../02-agent-core/agent-loop.md)
- [Runtime](../03-infrastructure/runtime.md)
- [Loop Engineering](loop-engineering.md)

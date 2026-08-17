# Guardrails

**中文建议：** 护栏 / 约束机制  
**成熟度：** 🟡  
**重要程度：** ★★★★☆

## 一句话解释

用于限制、检查、阻止或纠正 Agent 输入、输出与行动的安全和质量控制机制。

## 为什么需要它？

Agent 能调用工具并采取真实行动，因此需要权限、验证、策略和人工确认等边界来降低错误或高风险操作的影响。

## 在 Agent 系统中的位置

Guardrails 可以部署在输入、模型输出、工具调用、执行前后和 Handoff 等多个位置。

## 最容易混淆

Guardrails 不是“绝对安全保证”。它是一组风险控制机制，仍需要权限隔离、Sandbox、审计、Evals 和 Human-in-the-loop 等共同组成安全体系。

## 相关概念

- [Sandbox](../03-infrastructure/sandbox.md)
- [Evals](evals.md)
- [Stop Condition](../02-agent-core/stop-condition.md)

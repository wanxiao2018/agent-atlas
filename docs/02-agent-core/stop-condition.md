# Stop Condition

**中文建议：** 停止条件  
**成熟度：** 🟢  
**重要程度：** ★★★★☆

## 一句话解释

决定 Agent 何时结束、暂停或不再进入下一轮循环的规则。

## 为什么需要它？

没有可靠停止条件，Agent 可能陷入无意义重试、无限搜索、超时或持续消耗资源。

## 在 Agent 系统中的位置

Stop Condition 属于 Agent Loop / Harness 的控制逻辑。最终答案、最大轮数、时间预算、成本预算、Guardrail、人工终止都可以成为停止条件。

## 最容易混淆

“任务成功”只是停止条件的一种。安全边界、资源约束和人工审批同样可以要求系统停止或暂停。

## 相关概念

- [Agent Loop](agent-loop.md)
- [Harness](../03-infrastructure/harness.md)
- [Guardrails](../07-reliability/guardrails.md)

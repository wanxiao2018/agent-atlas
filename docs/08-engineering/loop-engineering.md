# Loop Engineering

**中文建议：** 循环工程  
**成熟度：** 🔴  
**重要程度：** ★★★★★

## 一句话解释

设计 Agent 自动执行、检查、修正并再次执行的反馈闭环，使任务在较少人工逐步干预下持续逼近目标。

## 为什么需要它？

重点从“人工给模型安排每一步”转向“设计目标、反馈、验证、停止条件和环境，让 Agent 自己在循环中推进任务”。

## 在 Agent 系统中的位置

它与 Agent Loop、Harness Engineering、Evals、Verification 和 Stop Conditions 强相关。

## 最容易混淆

`Agent Loop` 是循环机制本身；`Loop Engineering` 是如何把反馈、验证和停止逻辑设计得有效。后者是正在形成中的行业表达，而不是经典标准术语。

## 相关概念

- [Agent Loop](../02-agent-core/agent-loop.md)
- [Harness Engineering](harness-engineering.md)
- [Evals](../07-reliability/evals.md)
- [Stop Condition](../02-agent-core/stop-condition.md)

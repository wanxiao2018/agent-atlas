# Planning

**中文建议：** 规划  
**成熟度：** 🟢  
**重要程度：** ★★★★☆

## 一句话解释

把目标拆成步骤、维护任务计划，或根据当前反馈决定下一步行动的过程。

## 为什么需要它？

复杂任务通常无法一次完成。Agent 需要确定先做什么、后做什么，并在环境反馈改变时调整原计划。

## 在 Agent 系统中的位置

Planning 通常发生在 Agent Loop 内：它可以在任务开始时形成显式计划，也可以在每一轮根据 Observation 动态重规划。

## 最容易混淆

Planning 不等于“必须先写出完整计划”。很多有效 Agent 采用边执行、边观察、边重新规划的方式。

## 相关概念

- [Agent Loop](agent-loop.md)
- [Action / Observation](action-observation.md)
- [Stop Condition](stop-condition.md)

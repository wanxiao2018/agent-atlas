# Action / Observation

**中文建议：** 行动 / 观察  
**成熟度：** 🟢  
**重要程度：** ★★★★★

## 一句话解释

**Action** 是 Agent 对环境采取的操作；**Observation** 是执行后返回给 Agent 的新结果或反馈。

## 为什么需要它？

Agent 不是只在内部生成文本。它通过 Action 影响外部环境，再通过 Observation 获取真实反馈，从而形成可以持续修正的闭环。

## 在 Agent 系统中的位置

Action / Observation 是 Agent Loop 的核心反馈通道：

```text
Model → Action → Environment / Tool → Observation → Context → Model
```

## 最容易混淆

工具调用请求可以视为一种 Action；工具真正执行后的返回值通常形成 Observation。**请求动作**和**动作执行结果**不是同一件事。

## 相关概念

- [Agent Loop](agent-loop.md)
- [Tool Calling](../04-tools/tool-calling.md)
- [Planning](planning.md)

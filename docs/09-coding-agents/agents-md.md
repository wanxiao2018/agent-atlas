# AGENTS.md

**中文建议：** Agent 项目指令文件  
**成熟度：** 🟡  
**重要程度：** ★★★★☆

## 一句话解释

放在代码仓库中的面向 Coding Agent 的项目级说明文件，用于告诉 Agent 如何构建、测试、修改和遵循仓库约定。

## 为什么需要它？

Coding Agent 每次进入仓库都需要快速理解本地规则。机器可读的项目说明可以减少反复沟通，并让自动化修改更符合仓库约定。

## 在 Agent 系统中的位置

属于 Repository Context / Agent Instructions：Harness 在构建 Context 时可以读取这些仓库规则并提供给模型。

## 最容易混淆

`AGENTS.md` 是一种约定形式，不同 Coding Agent 对文件名、作用域、继承和优先级的支持可能不同，不能把某个产品的行为当作统一标准。

## 相关概念

- [Skills](skills.md)
- [Context Engineering](../05-context-memory/context-engineering.md)
- [Harness](../03-infrastructure/harness.md)

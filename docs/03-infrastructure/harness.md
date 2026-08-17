# Agent Harness

**中文建议：** Agent 运行框架 / 外围执行系统  
**成熟度：** 🟡  
**重要程度：** ★★★★★  
**学习阶段：** 入门必懂  
**最后更新：** 2026-08-17

---

## 30 秒理解

**Harness 是包裹在模型外面的那套“让它真正能够工作”的系统。**

模型本身擅长理解、推理和生成，但它通常不会天然拥有文件系统、Shell、工具调用、权限控制、状态保存、重试、停止条件、Tracing 等工程能力。

Harness 的作用，就是把这些能力组织起来，让模型从“会回答”变成“能执行任务”。

可以先记住一个非常粗略但好用的心智模型：

> **Model 是大脑，Harness 是工作环境 + 工具 + 规则 + 调度机制。**

## 先建立一个直觉

假设你雇了一个非常聪明的软件工程师。

如果他只有大脑，却没有：

- 电脑；
- 代码仓库；
- 终端；
- 文件权限；
- 测试环境；
- 工作流程；
- 日志；
- 失败后的恢复机制；

那么他再聪明也很难真正完成工程任务。

LLM 也是类似的。

```text
Model
= 会理解、推理、生成的大脑

Harness
= 让这个大脑能够持续工作的外围系统
```

所以当你看到 Claude Code、Codex、各种 Coding Agent 时，不要只盯着“它用了哪个模型”。

很多时候，**真正决定体验差异的，是模型外面的 Harness。**

## 为什么会出现 Harness 这个概念？

早期很多人会把 Agent 简单理解成：

```text
LLM + Prompt + Tool Calling
```

但真正把 Agent 放进生产环境以后，会迅速遇到一堆问题：

- 工具到底怎么注册？
- 工具调用失败怎么办？
- 模型什么时候继续，什么时候停止？
- 上下文太长怎么办？
- 怎么保存任务状态？
- 怎么恢复一个中断任务？
- 执行代码时怎么隔离风险？
- 哪些动作必须人工批准？
- 怎么记录 Agent 到底做过什么？
- 多 Agent 之间怎么交接？

这些问题单靠模型本身解决不了。

于是就需要一层外围系统，把这些机制统一组织起来。

这就是 Harness。

## 技术定义

在 Agent 工程语境里，`Harness` 通常指：

> **围绕模型构建的执行与控制系统，它负责把模型调用、上下文、工具、状态、运行循环、权限、安全边界和可观测性等能力组合成一个可运行的 Agent。**

这个词目前还不像 `HTTP`、`database` 那样拥有完全固定的边界。

不同团队可能把 Harness 的范围画得略有不同，但核心思想非常一致：

> **Harness 不是模型，而是“模型如何被运行、如何行动、如何被约束”的那一层系统。**

Anthropic 在 2025～2026 年多篇关于长时间运行 Agent 的工程文章里持续使用 `harness` 这个词，并把 Claude Agent SDK 称为一种 general-purpose agent harness。

## Harness 里通常有什么？

一个典型 Harness 可能包含下面这些部分：

```text
Agent Harness
│
├── Model Interface
│   └── 调用 LLM
│
├── Context Builder
│   └── 决定每一轮模型能看到什么
│
├── Agent Loop
│   └── 反复调用模型、执行动作、读取反馈
│
├── Tool System
│   ├── function tools
│   ├── web / file search
│   ├── MCP
│   └── external APIs
│
├── State / Memory
│   └── 保存任务状态与跨轮信息
│
├── Runtime
│   └── 负责 Agent 的实际运行
│
├── Sandbox
│   └── 提供隔离的文件、Shell、代码执行环境
│
├── Permissions / Approvals
│   └── 限制高风险操作
│
├── Error Handling
│   └── retry / recovery / timeout
│
├── Tracing / Logging
│   └── 记录 Agent 每一步做了什么
│
└── Stop Conditions
    └── 决定什么时候结束
```

不是每一个 Harness 都必须包含所有组件。

但只要一个系统开始负责“模型之外的 Agent 执行逻辑”，你就已经进入 Harness 的范畴了。

## Agent Harness 是怎么工作的？

一个非常简化的流程是：

```text
用户任务
   ↓
Harness 构建 Context
   ↓
调用 Model
   ↓
Model 输出下一步动作
   ↓
Harness 检查权限
   ↓
执行 Tool / Sandbox 操作
   ↓
收集 Observation
   ↓
更新 State / Context
   ↓
再次调用 Model
   ↓
直到 Final Output / Stop Condition
```

可以看到：

**模型决定“想做什么”，Harness 负责“怎么把这件事安全、可靠地真的执行出来”。**

## 一个具体例子：Coding Agent

你对 Coding Agent 说：

> “把登录接口的 bug 修掉，并确保测试通过。”

模型可能只负责这些判断：

```text
先查看代码
→ 运行测试
→ 分析报错
→ 修改 auth.py
→ 再运行测试
```

而背后的 Harness 可能负责：

```text
读取仓库文件
创建 / 管理工作目录
执行 pytest
限制 Shell 权限
把命令输出返回模型
记录修改
追踪 token 和步骤
失败后重试
控制最大运行时长
最终收集 diff
```

所以用户看到的是：

> “Agent 在修 bug。”

工程上真正发生的是：

> **Model + Harness 在协同完成任务。**

## 为什么同一个模型，做出来的 Agent 体验会差很多？

这是理解 Harness 最重要的一点。

假设两个产品都使用同一个模型：

```text
Product A → Model X
Product B → Model X
```

它们仍然可能表现差异非常大。

因为 Harness 可能不同：

```text
A:
Model X
+ 好的工具描述
+ 清晰上下文
+ 稳定 Agent Loop
+ Sandbox
+ 自动测试
+ 错误恢复

B:
Model X
+ 混乱 Prompt
+ 工具返回噪声
+ 无状态管理
+ 无限重试
+ 没有验证机制
```

即使底层模型完全相同，最后的 Agent 能力也可能明显不同。

这也是为什么现在越来越多人开始讨论 [Harness Engineering](../08-engineering/harness-engineering.md)。

## Harness 和 Agent Loop 是什么关系？

可以这样理解：

```text
Harness = 整个运行系统
Agent Loop = Harness 里的核心控制循环
```

就像：

```text
汽车 ≠ 发动机
汽车包含发动机

Harness ≠ Agent Loop
Harness 通常包含 Agent Loop
```

[Agent Loop](../02-agent-core/agent-loop.md) 负责“继续还是结束、执行工具后怎么再进入下一轮”。

Harness 的范围更大。

## Harness 和 Sandbox 有什么区别？

这是非常容易混淆的一组词。

### Sandbox

更像一个**隔离的工作间**。

它主要解决：

- 在哪里执行代码；
- 能访问哪些文件；
- 能不能联网；
- 哪些系统资源可用；
- 如何隔离风险。

### Harness

更像负责整个 Agent 工作流程的**管理系统**。

```text
Harness
└── 可以调用 Sandbox
```

因此：

> **Sandbox 通常是 Harness 可以使用的一部分，而不是 Harness 本身。**

## Harness、Runtime、Framework 有什么区别？

| 概念 | 最简单的理解 |
|---|---|
| Model | 做推理和生成的核心模型 |
| Framework / SDK | 开发者用来搭建 Agent 的工具箱 |
| Harness | 实际包裹并运行模型的 Agent 执行系统 |
| Runtime | Agent 在运行时的执行与生命周期环境 |
| Sandbox | 用于隔离执行命令、代码和文件操作的环境 |
| Orchestrator | 负责协调多个 Agent / 任务之间关系的组件 |

现实项目中这些边界可能重叠。

例如某个 Agent SDK 本身就提供了大量 Harness 能力，所以人们也可能直接把它叫 Agent Harness。

## Harness ≠ Framework

这两个词经常被混用，但可以先这样区分：

```text
Framework / SDK
= “用什么搭”

Harness
= “最终围绕模型运行起来的那套东西”
```

例如你可以用一个 SDK 自己搭 Harness。

当然，有些 SDK 本身已经把 Harness 大部分能力做好了，所以二者在实际语言中会出现重叠。

## Harness 不是越复杂越好

这是现在 Agent 工程里很重要的一条原则。

Anthropic 在关于 Harness 的工程实践中多次指出：

> Harness 的很多组件，本质上都编码了“模型自己做不到什么”的假设。

但模型能力会持续提升。

例如过去可能需要 Harness 强制：

```text
任务必须拆成 10 个 sprint
```

后来更强的模型可能已经能够自己保持长期任务的连贯性。

这时候过于复杂的 Harness 反而可能：

- 限制模型；
- 增加成本；
- 引入更多故障点；
- 让系统更难调试。

所以好的 Harness Engineering 不是“不断增加组件”，而是：

> **只保留真正有用、可验证的结构。**

## 一个非常重要的变化：Brain 和 Hands 可以分开

现代 Agent 系统越来越强调：

```text
Brain
= Model + orchestration / harness logic

Hands
= Sandbox / compute environment
```

也就是说，负责决策和权限的 Harness 不一定和执行模型生成代码的机器放在一起。

这样做可以带来：

- 更好的安全隔离；
- 更持久的任务状态；
- 更灵活的计算资源；
- 凭证不必暴露给执行环境。

这也是理解现代 Coding Agent 架构的一条重要线索。

## 常见误解

### ❌ 误解 1：Harness 就是 Prompt

不是。

Prompt / instructions 只是 Harness 可能管理的一部分。

### ❌ 误解 2：Harness 就是 Agent SDK

不完全是。

SDK 是构建和运行 Harness 的一种方式；具体产品里的 Harness 还可能包含自己的权限、状态、工具、部署和恢复逻辑。

### ❌ 误解 3：Harness 就是 Sandbox

不是。

Sandbox 主要负责隔离执行；Harness 负责整个 Agent 的运行控制。

### ❌ 误解 4：模型升级以后 Harness 不重要了

也不是。

更强模型可能减少某些 scaffolding，但工具、权限、状态、安全、Tracing 等工程问题仍然需要外围系统处理。

### ❌ 误解 5：Harness 越复杂，Agent 越强

不一定。

真正重要的是每个组件是否解决了可验证的问题。

## 在 Agent 系统中的位置

```text
Agentic System
│
├── Model
│
└── Harness  ← 你在这里
    ├── Instructions / Context
    ├── Agent Loop
    ├── Tools
    ├── State / Memory
    ├── Runtime
    ├── Sandbox
    ├── Permissions
    ├── Guardrails
    └── Tracing / Evals
```

一个非常好记的简化式：

> **Agent ≈ Model + Harness**

再次强调：这是心智模型，不是严格的形式化定义。

## 你什么时候会遇到这个词？

现在它特别常见于：

- Coding Agent；
- Claude Agent SDK；
- 长时间运行 Agent；
- Managed Agents；
- Sandbox Agent；
- Agent Evals；
- Harness Engineering；
- 多 Agent 系统。

尤其是在讨论“为什么同一个模型换个 Agent 产品就表现不同”时，Harness 是非常关键的词。

## 和其他术语的关系

建议接着阅读：

1. [Agent](../01-foundations/agent.md) —— Harness 最终服务的完整 Agent 系统；
2. [Agent Loop](../02-agent-core/agent-loop.md) —— Harness 内部最核心的循环结构；
3. [Runtime](runtime.md) —— Agent 具体在哪里、如何运行；
4. [Sandbox](sandbox.md) —— 代码和命令在哪里安全执行；
5. [Context Engineering](../05-context-memory/context-engineering.md) —— Harness 每轮应该给模型什么信息；
6. [Harness Engineering](../08-engineering/harness-engineering.md) —— 如何系统地优化 Harness。

## 成熟度说明

`Harness` 在 Agent 工程中已经被 Anthropic、OpenAI 等团队越来越频繁地使用，但它的**边界和中文翻译仍未完全统一**。

因此 Agent Atlas 暂时标记为 🟡：

- 概念已经非常重要；
- 用法正在快速普及；
- 但行业仍在形成更稳定的共同语言。

## 参考来源

- Anthropic, [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents), 2025-11-26.
- Anthropic, [Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps), 2026-03-24.
- Anthropic, [Scaling Managed Agents: Decoupling the brain from the hands](https://www.anthropic.com/engineering/managed-agents), 2026-04-08.
- OpenAI Agents SDK, [SDK overview](https://openai.github.io/openai-agents-python/).

# Agent Harness

**中文建议：** Agent 运行框架 / 外围执行系统  
**常见别名：** Harness / Agent Harness / Scaffolding（部分语境）  
**成熟度：** 🟡  
**词条状态：** ✅ Atlas-quality  
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

---

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

---

## 为什么会出现 Harness 这个概念？

早期很多人会把 Agent 简单理解成：

```text
LLM + Prompt + Tool Calling
```

但真正把 Agent 放进生产环境以后，会迅速遇到一堆问题：

- 工具到底怎么注册？
- 工具调用失败怎么办？
- 模型什么时候继续，什么时候停止？
- Context 太长怎么办？
- 怎么保存任务状态？
- 怎么恢复一个中断任务？
- 执行代码时怎么隔离风险？
- 哪些动作必须人工批准？
- 怎么记录 Agent 到底做过什么？
- 多 Agent 之间怎么交接？

这些问题单靠模型本身解决不了。

于是就需要一层外围系统，把这些机制统一组织起来。

这就是 Harness。

---

## 技术定义

在 Agent 工程语境里，`Harness` 通常指：

> **围绕模型构建的执行与控制系统，它负责把模型调用、Context、工具、State、Agent Loop、权限、安全边界和可观测性等能力组合成一个可运行的 Agent。**

这个词目前还不像 `HTTP`、`database` 那样拥有完全固定的边界。

不同团队可能把 Harness 的范围画得略有不同，但核心思想非常一致：

> **Harness 不是模型，而是“模型如何被运行、如何行动、如何被约束”的那一层系统。**

Anthropic 在 2025–2026 年关于 long-running agents 的工程文章里持续使用 `harness`；OpenAI 2026 年也直接把新版 Agents SDK 描述为“a more capable harness for the agent loop”；Microsoft Agent Framework 也把 harness 描述为把模型变成能真正工作的 Agent 的 scaffolding / runtime。

---

## 你可能是在这句话里遇到它

> “The harness executes the tool call, updates the context, and runs the next agent turn.”

这句话可以拆成：

```text
Model
  ↓ 生成 Tool Call
Harness
  ↓ 检查权限
Runtime / Tool Executor
  ↓ 真正执行
Observation
  ↓
Harness 更新 Context / State
  ↓
Agent Loop 下一轮
  ↓
Model 再次判断
```

这就是为什么你读 Agent 文章时，不能把 `harness` 只理解成“一个 SDK”。

它描述的是**模型外面负责推进工作的一整套机制**。

---

## Harness 里通常有什么？

一个典型 Harness 可能包含：

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

---

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

> **模型决定“想做什么”，Harness 负责“怎么把这件事安全、可靠地真的执行出来”。**

---

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

---

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
+ 清晰 Context
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

---

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

---

## Harness 和 Sandbox 有什么区别？

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
└── 可以调用 / 管理 Sandbox
```

因此：

> **Sandbox 通常是 Harness 可以使用的一部分，而不是 Harness 本身。**

→ [Sandbox](sandbox.md)

---

## Harness、Runtime、Framework 有什么区别？

| 概念 | 最简单的理解 |
|---|---|
| Model | 做推理和生成的核心模型 |
| Framework / SDK | 开发者用来搭建 Agent 的工具箱 |
| Harness | 实际包裹并运行模型的 Agent 执行与控制系统 |
| Runtime | Agent 在运行时的执行与生命周期层 |
| Sandbox | 用于隔离执行命令、代码和文件操作的环境 |
| Orchestrator | 负责协调多个 Agent / 任务之间关系的组件 |

现实项目中这些边界可能重叠。

例如某个 Agent SDK 本身就提供了大量 Harness 能力，所以人们也可能直接把它叫 Agent Harness。

---

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

---

## Harness ≠ Runtime

这条边界比 Harness vs Framework 更模糊。

可以先用职责区分：

```text
Harness
= 整体的控制、工具、Context、权限、循环设计

Runtime
= 一次 run / session 实际怎么被执行和维持
```

但有些官方文档会直接把 Harness 称为“wrapped around the model 的 runtime”。

所以遇到这两个词时，**不要死背术语边界，要看作者把哪些职责放在哪一层。**

→ [Runtime](runtime.md)

---

## Harness 不是越复杂越好

这是现在 Agent 工程里很重要的一条原则。

Anthropic 在关于 Harness 的工程实践中指出：很多 Harness 组件本质上都编码了“模型自己暂时做不到什么”的假设。

但模型能力会持续提升。

例如过去可能需要 Harness 强制：

```text
任务必须拆成 10 个 sprint
```

后来更强的模型可能已经能够自己保持更长时间的任务连贯性。

这时候过于复杂的 Harness 反而可能：

- 限制模型；
- 增加成本；
- 引入更多故障点；
- 让系统更难调试。

所以好的 Harness Engineering 不是“不断增加组件”，而是：

> **只保留真正有用、可验证的结构。**

---

## 一个非常重要的变化：Brain 和 Hands 可以分开

现代 Agent 系统越来越强调：

```text
Brain
= Model + orchestration / Harness logic

Hands
= Sandbox / Compute environment
```

也就是说，负责决策和权限的 Harness 不一定和执行模型生成代码的机器放在一起。

OpenAI 与 Anthropic 2026 年都公开讨论过这种分离思路。

这样做可以带来：

- 更好的安全隔离；
- 更持久的任务状态；
- 更灵活的计算资源；
- 凭证不必暴露给执行环境；
- Sandbox 出错后可重新创建并恢复任务。

这也是理解现代 Coding Agent 架构的一条重要线索。

---

## 不同生态怎么使用 Harness 这个词？

### Anthropic

`harness` 已经成为长时间 Agent、Claude Agent SDK 和 Agent 运行设计中的常用工程词。

### OpenAI

2026 年新版 Agents SDK 明确使用 “a more capable harness for the agent loop”，并把工具、Memory、Sandbox 等作为 Harness 可适配的部分。

### Microsoft Agent Framework

直接提供 Harness Agent，并把 Harness 定义为让模型能够工具调用、多步执行、Context 管理和长期工作的 scaffolding。

### 社区 / Coding Agent 语境

`Harness Engineering` 也越来越常用来描述：

> “不是换模型，而是优化模型周围的系统。”

这说明该词正在快速形成共同语言，但边界仍未完全标准化。

---

## Concept Graph Relations

```text
Harness ─enables───────→ Agent

Harness ─contains──────→ Agent Loop
Harness ─dispatches────→ Tools
Harness ─manages───────→ Context
Harness ─integrates────→ Runtime
Harness ─uses──────────→ State / Memory
Harness ─applies───────→ Permissions / Guardrails
Harness ─records───────→ Tracing / Evals

Runtime ─connects──────→ Sandbox
```

这也是 Agent Atlas 主图中：

```text
Model ─────→ Agent ←──── Harness
                         │
            ┌────────────┼────────────┐
            ↓            ↓            ↓
        Agent Loop      Tools       Runtime
```

这部分关系的核心依据。

---

## 常见误解

### ❌ Harness 就是 Prompt

不是。Prompt / instructions 只是 Harness 可能管理的一部分。

### ❌ Harness 就是 Agent SDK

不完全是。SDK 是构建和运行 Harness 的一种方式；具体产品里的 Harness 还可能包含自己的权限、状态、工具、部署和恢复逻辑。

### ❌ Harness 就是 Sandbox

不是。Sandbox 主要负责隔离执行；Harness 负责整个 Agent 的运行控制。

### ❌ 模型升级以后 Harness 不重要了

也不是。更强模型可能减少某些 scaffolding，但工具、权限、状态、安全、Tracing 等工程问题仍然需要外围系统处理。

### ❌ Harness 越复杂，Agent 越强

不一定。真正重要的是每个组件是否解决了可验证的问题。

---

## Terminology Observatory

`Harness` 是 Agent 工程中一个非常典型的**正在快速稳定中的术语**。

它不是 LLM 时代才存在的英语单词，但“Agent Harness / Harness Engineering”作为行业核心工程概念是在 2025–2026 年明显加速普及的。

目前已经可以看到 Anthropic、OpenAI、Microsoft 等多个一线团队使用这一概念，但：

- 边界仍有差异；
- 与 Runtime / Framework / Scaffolding 存在重叠；
- 中文还没有统一译法。

因此 Agent Atlas 标记为 🟡。

---

## 下一步应该学什么？

1. [Agent](../01-foundations/agent.md) —— Harness 最终服务的完整 Agent 系统；
2. [Agent Loop](../02-agent-core/agent-loop.md) —— Harness 内部最核心的循环结构；
3. [Tool Calling](../04-tools/tool-calling.md) —— Harness 如何接收和执行动作请求；
4. [Runtime](runtime.md) —— Agent 具体如何运行；
5. [Sandbox](sandbox.md) —— 代码和命令在哪里安全执行；
6. [Context Engineering](../05-context-memory/context-engineering.md) —— Harness 每轮应该给模型什么信息；
7. [Harness Engineering](../08-engineering/harness-engineering.md) —— 如何系统优化 Harness。

---

## 一手资料

- Anthropic, [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
- Anthropic, [Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps)
- Anthropic, Scaling Managed Agents: Decoupling the brain from the hands: https://www.anthropic.com/engineering/managed-agents
- OpenAI, [The next evolution of the Agents SDK](https://openai.com/index/the-next-evolution-of-the-agents-sdk/)
- OpenAI Agents SDK, [SDK overview](https://openai.github.io/openai-agents-python/)
- Microsoft Agent Framework, [Agent Harnesses](https://learn.microsoft.com/en-us/agent-framework/agents/harness)

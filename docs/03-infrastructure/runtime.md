# Runtime

**中文建议：** 运行时 / 运行环境  
**成熟度：** 🟢  
**词条状态：** ✅ Atlas-quality  
**重要程度：** ★★★★★  
**学习阶段：** 入门 → 工程实践  
**最后更新：** 2026-08-17

---

## 30 秒理解

**Runtime 是 Agent 真正“跑起来”的执行层。**

如果 `Model` 负责判断下一步，`Harness` 负责组织整个工作过程，那么 Runtime 关注的是：

> **这一轮任务到底在哪里运行、如何管理生命周期、怎样连接工具和状态。**

它可能是：

- 当前 Python 进程；
- 一个长期运行的服务；
- Docker 容器；
- 云端 Worker；
- 一个 Sandbox session。

---

## 先建立一个直觉

可以把 Agent 想成一个公司：

```text
Model   = 会思考的员工
Harness = SOP + 调度 + 权限 + 工作机制
Runtime = 公司真正开门营业的办公环境
Sandbox = Runtime 里受到隔离的一间实验室
```

员工脑子里想得再好，如果没有地方运行程序、保存状态、调用工具，任务还是无法真正发生。

---

## Runtime 解决什么问题？

一个 Agent 被“运行”时，系统必须处理很多非常具体的事情：

- 创建一次 run / session；
- 调用模型；
- 执行工具；
- 维护当前状态；
- 处理中断、timeout 和异常；
- 连接文件系统或外部服务；
- 暂停并等待审批；
- 保存状态后恢复；
- 启动 / 停止 Sandbox；
- 记录 tracing。

这些都属于“系统实际运行时会发生什么”的问题。

---

## 技术定义

Agent 领域并没有一个跨所有框架完全统一的 `Runtime` 边界。

在 Agent Atlas 中，我们把它定义为：

> **负责把 Agent 的定义变成一次实际运行，并管理执行环境、生命周期、状态、工具连接与恢复过程的运行层。**

这个定义刻意和 `Harness` 区分：

```text
Harness
= 整套模型外围的执行与控制设计

Runtime
= 这套设计在运行时具体如何被执行和维持
```

两者在真实框架里经常重叠，因此不要期待所有项目都严格按这条线命名。

---

## 你可能是在这句话里遇到它

> “The runtime resumes the agent from saved state and reconnects it to a sandbox session.”

拆开来看：

```text
Saved State
   ↓
Runtime 读取状态
   ↓
恢复 Run / Session
   ↓
连接 Sandbox
   ↓
恢复工具和工作区
   ↓
Agent Loop 继续
```

这里强调的是**运行中的生命周期和恢复机制**，而不是模型本身的推理能力。

---

## 一个 Runtime 通常会管什么？

```text
Agent Runtime
│
├── Run / Session lifecycle
├── Model invocation
├── Tool execution / dispatch
├── Context + State plumbing
├── Sandbox connection
├── Pause / Resume
├── Timeout / Cancellation
├── Retry / Error handling
├── Persistence / Snapshot
└── Tracing / Logs
```

不同 SDK 会把其中一些功能放到 Runner、Session、Executor、Engine 或 Harness 中。

所以看到 `Runtime` 时，最稳妥的问题不是：

> “它的标准组件到底是哪几个？”

而是：

> **“这个项目里，谁负责让 Agent 从定义变成一次真正的执行？”**

---

## Runtime 和 Harness 有什么区别？

这是非常容易混淆的一组词。

| 概念 | 更关注 |
|---|---|
| Harness | 整体执行与控制系统应该如何组织 |
| Runtime | Agent 在运行时如何真正执行和维持生命周期 |

一个简单类比：

```text
Harness ≈ 公司的组织制度 + 工作系统
Runtime ≈ 公司今天真正开始营业以后发生的运行过程
```

Microsoft Agent Framework 的文档甚至直接把 Harness 描述成“包在模型外的 runtime”。这恰好说明两者在业界并没有绝对清晰的词汇边界。

因此 Agent Atlas 更重视**概念职责**，而不是假装存在唯一术语标准。

---

## Runtime 和 Sandbox 有什么区别？

### Runtime

回答：

> Agent 的 run / session 怎么执行？

### Sandbox

回答：

> 某些高风险代码、文件和命令应该在哪个受控边界内执行？

所以：

```text
Runtime
└── may manage / connect to
    Sandbox
```

OpenAI Agents SDK 的 Sandbox Agents 就明确区分：Agent 定义本身与每次 run 使用的 sandbox client / live session 是分开的；真正的 transport 和 session 信息在运行时提供。

---

## Runtime 和 Session / State 有什么区别？

```text
Runtime = 执行者
Session = 一段连续任务 / 对话的容器
State   = 当前需要保存的数据
```

例如：

```text
Runtime
  ↓ manages
Session #42
  ↓ contains / references
State
  ├── conversation history
  ├── approvals
  ├── current plan
  └── sandbox snapshot id
```

Runtime 可以消失后重新启动，而 State 如果被持久化，任务仍然可以恢复。

这也是长时间运行 Agent 的关键设计之一。

---

## 为什么“Brain 和 Hands 分离”越来越重要？

现代 Agent 架构经常把：

```text
Brain
= Model + Harness / orchestration

Hands
= Compute / Sandbox
```

分开运行。

OpenAI 2026 年的 Agents SDK 演进明确强调了把 harness 与 compute 分离的好处：

- 凭据可以留在执行环境之外；
- Sandbox 失效时，可以从外部保存的 state 恢复；
- 可以按需创建多个计算环境；
- 更容易扩展和隔离任务。

这时 Runtime 就承担了非常重要的“把 Brain 和 Hands 接起来”的职责。

---

## Concept Graph Relations

```text
Harness ─integrates────→ Runtime

Runtime ─runs──────────→ Agent Loop
Runtime ─executes──────→ Tool Calls
Runtime ─manages───────→ Session
Runtime ─reads/writes──→ State
Runtime ─connects──────→ Sandbox

Sandbox ─isolates──────→ Code / Commands
```

---

## 常见误解

### ❌ Runtime = Sandbox

不是。Sandbox 是强调隔离的执行环境；Runtime 的职责通常更广。

### ❌ Runtime = Harness

不是严格同义词，但业界边界可能重叠。需要看具体框架语境。

### ❌ Runtime 只是“服务器”

过于狭窄。Runtime 还涉及 session、状态、工具、恢复、取消等运行逻辑。

### ❌ 模型越强，Runtime 越不重要

不是。模型能力再强，也需要实际的执行环境、状态持久化和安全边界。

---

## Terminology Observatory

**成熟度：🟢，但边界依赖具体框架。**

`runtime` 是软件工程中的成熟术语；但“Agent Runtime”到底包含哪些组件，各家框架并没有统一标准。

因此阅读资料时，建议先看作者具体把 Runner、Session、Sandbox、State 中哪些职责划进 Runtime。

---

## 下一步应该学什么？

1. [Harness](harness.md) —— 整体外围系统；
2. [Sandbox](sandbox.md) —— 执行环境如何隔离；
3. [State](state.md) —— Runtime 需要保存什么；
4. [Agent Loop](../02-agent-core/agent-loop.md) —— Runtime 在反复运行什么；
5. [Tool Calling](../04-tools/tool-calling.md) —— Runtime 经常需要执行什么动作。

---

## 一手资料

- OpenAI, [The next evolution of the Agents SDK](https://openai.com/index/the-next-evolution-of-the-agents-sdk/)
- OpenAI Agents SDK, [Sandbox concepts](https://openai.github.io/openai-agents-python/sandbox/guide/)
- OpenAI Agents SDK, [Sandbox API reference](https://openai.github.io/openai-agents-python/ref/sandbox/)
- Microsoft Agent Framework, [Agent Harnesses](https://learn.microsoft.com/en-us/agent-framework/agents/harness)

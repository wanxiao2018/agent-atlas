# Agent Loop

**中文建议：** Agent 循环 / 智能体循环  
**常见别名：** Agentic Loop / Tool Loop（更窄）  
**成熟度：** 🟢  
**词条状态：** ✅ Atlas-quality  
**重要程度：** ★★★★★  
**学习阶段：** 入门必懂  
**最后更新：** 2026-08-17

---

## 30 秒理解

**Agent Loop 是让 Agent 能够连续工作的核心循环。**

它通常会反复做几件事：

```text
观察当前情况
   ↓
调用模型判断下一步
   ↓
执行 Action
   ↓
得到 Observation
   ↓
更新 Context / State
   ↓
继续下一轮或结束
```

如果说 Model 是“大脑”，那么 Agent Loop 就像：

> **让大脑不断看结果、做决定、再继续行动的工作节奏。**

---

## 先建立一个直觉

想象你在修一个坏掉的水龙头。

你不会：

> 看一眼 → 一口气把所有动作都提前决定好 → 闭着眼执行到底。

真实过程更像：

```text
看到漏水
 ↓
判断可能是垫圈问题
 ↓
拆开
 ↓
发现并不是垫圈
 ↓
重新判断
 ↓
检查阀芯
 ↓
更换
 ↓
打开水测试
 ↓
仍然漏？继续
不漏了？结束
```

Agent 处理复杂任务也是这样。

它最重要的能力之一不是“一开始就把整个计划猜对”，而是：

> **执行一步以后，看到真实反馈，再重新决定下一步。**

---

## 为什么需要 Agent Loop？

很多现实任务都有不确定性。

例如：

> “帮我把这个项目跑起来并修掉启动错误。”

Agent 一开始并不知道真正错误是什么。

它必须：

```text
读取项目
 ↓
运行程序
 ↓
看到报错
 ↓
分析报错
 ↓
修改代码
 ↓
再次运行
 ↓
看到新的结果
 ↓
继续修复或结束
```

如果没有 Loop，模型最多只能根据第一次输入预测接下来可能发生什么。

而 Agent Loop 让模型能够利用**真实环境反馈**继续工作。

---

## 技术定义

在工程上，Agent Loop 通常指：

> **一个运行控制过程，它反复调用当前 Agent 的模型，检查模型输出，并根据输出执行工具调用、handoff 或其他动作，再把行动结果加入 Context / State，直到得到最终输出或触发停止条件。**

不同框架的实现细节会不同，但核心结构非常接近。

OpenAI Agents SDK 当前就把 built-in agent loop 作为核心能力：处理 tool invocation，把结果送回模型，并继续运行直到任务完成。Anthropic 对 agent 的描述也强调 self-directed loop：plan、act、observe、adjust、repeat。

---

## 你可能是在这句话里遇到它

> “After the tool result is returned, the harness enters another iteration of the agent loop.”

这句话真正说的是：

```text
Model
  ↓ 请求 Tool
Harness / Runtime
  ↓ 执行
Tool Result
  ↓ 形成 Observation
Context / State 更新
  ↓
再次调用 Model
```

这里的 “another iteration” 就是**又进入一轮模型—环境交互**。

不是模型单纯“继续想”，而是系统中已经出现了新的外部结果。

---

## 一个最小 Loop 长什么样？

可以先记住这个简化版本：

```python
context = [user_request]

while True:
    response = model(context, tools=tools)

    if response.is_final:
        return response.output

    if response.tool_calls:
        tool_results = run_tools(response.tool_calls)
        context.extend(tool_results)
```

真正的生产系统通常还会多很多东西：

```text
Agent Loop
├── Model Call
├── Tool Execution
├── Context Update
├── State Update
├── Handoff
├── Guardrails
├── Retry / Error Handling
├── Approval
├── Tracing
└── Stop Conditions
```

---

## Loop 中到底“循环”的是什么？

初学者经常以为：

> “Agent Loop = 模型一直在自己思考。”

更准确地说，循环的是整个**模型—环境交互过程**。

典型一轮可以写成：

```text
Context_t
   ↓
Model
   ↓
Action_t
   ↓
Environment / Tool
   ↓
Observation_t
   ↓
Context_(t+1)
```

然后进入下一轮。

这里：

- `Context_t`：模型当前能看到的信息；
- `Action_t`：模型决定采取的动作；
- `Observation_t`：执行动作以后得到的新反馈。

这也是为什么 `Action / Observation` 是理解 Agent 的一组核心概念。

---

## 一个具体例子

任务：

> “帮我找出这个 Python 项目为什么测试失败，并修复。”

可能的 Agent Loop：

```text
Round 1
Model: 先运行 pytest
Action: pytest
Observation: 3 tests failed

Round 2
Model: 错误集中在 parser.py，先读文件
Action: read parser.py
Observation: 得到源码

Round 3
Model: 发现边界条件错误，修改代码
Action: edit parser.py
Observation: 修改成功

Round 4
Model: 再跑测试
Action: pytest
Observation: 1 test failed

Round 5
Model: 继续检查剩余失败
...

Round N
Observation: all tests passed
Model: 输出最终结果
Loop: stop
```

这里真正体现 Agent 能力的不是“它会写代码”，而是：

> **执行 → 看结果 → 改变策略 → 再执行。**

---

## 一轮 Agent Loop ≠ 一个 Shell 命令

这在 Coding Agent 里很容易误解。

OpenAI Sandbox Agent 文档明确指出：

> 一个 turn 仍然是一次模型步骤，而不是一个 shell command 或 sandbox action。

也就是说一轮模型调用之后，执行层内部可能完成多个操作；只有需要模型再次根据新结果做决定时，才真正进入下一轮模型 turn。

所以：

```text
Model Turn
  ↓
Runtime / Sandbox 内部可能执行若干操作
  ↓
需要新判断
  ↓
Next Model Turn
```

这帮助我们区分：

**Agent Loop 的轮次** 和 **执行环境里的动作次数**。

---

## Loop 为什么不能无限跑？

如果没有停止机制，Agent 可能：

- 重复调用同一个工具；
- 陷入错误重试；
- 不断搜索但不收敛；
- 消耗大量 token 和 API 成本；
- 对外部系统执行过多操作。

因此成熟的 Harness 一定要考虑 [Stop Condition](stop-condition.md)。

常见停止条件包括：

### 1. 模型给出最终输出

```text
final_output → stop
```

### 2. 达到最大轮数

```text
max_turns = 20
```

### 3. 达到时间或成本预算

```text
运行超过 10 分钟 → stop
成本超过预算 → stop
```

### 4. Guardrail 被触发

例如高风险操作被拦截。

### 5. 需要 Human-in-the-loop

Agent 暂停，等待人类批准后继续。

---

## Agent Loop ≠ 无限循环

名字里虽然有 `Loop`，但目标不是“一直循环”。

好的 Agent Loop 应该是：

> **任务未完成时继续，已经完成或不应该继续时可靠停止。**

所以 Loop 设计实际上同时包含两个问题：

```text
什么时候继续？
什么时候停止？
```

---

## Agent Loop 和 Chain-of-Thought 有什么区别？

| 概念 | 核心是什么 |
|---|---|
| Chain-of-Thought | 模型推理过程相关概念 |
| Agent Loop | 模型与工具、环境之间的多轮执行控制 |
| Conversation Loop | 用户和模型多轮聊天 |
| Retry Loop | 某一步失败后重复尝试 |

最简单的判断方式：

> **有没有新的 Action / Observation 改变系统状态，再让模型重新决策？**

如果有，它更接近 Agent Loop。

---

## Agent Loop 和 Workflow 是什么关系？

Workflow 也可以有循环。

区别不在“有没有 while”，而在于：

> **谁决定下一步？**

固定 Workflow：

```text
程序员：A → B → C → D
```

Agent Loop：

```text
程序员定义规则和边界
        ↓
模型根据当前结果决定下一步
```

很多真实系统其实是混合形式：

> **外层 Workflow 固定，内部某些节点运行 Agent Loop。**

---

## Loop Engineering 和 Agent Loop 是一回事吗？

不是。

`Agent Loop` 是系统里的**循环机制**。

`Loop Engineering` 更接近一种工程实践：

> 如何设计目标、反馈、验证、停止条件和环境，让 Agent 在循环中越来越接近正确结果。

可以理解为：

```text
Agent Loop       = 循环本身是什么
Loop Engineering = 这个循环怎么设计才有效
```

→ [Loop Engineering](../08-engineering/loop-engineering.md)

---

## Agent Loop 和 Harness 是什么关系？

```text
Harness
├── Agent Loop
├── Tools
├── Context Management
├── Runtime
├── Permissions
└── Tracing
```

Agent Loop 通常是 Harness 的核心控制结构之一。

可以简单记：

```text
Harness = 整套运行系统
Agent Loop = 其中不断推进任务的“心跳”
```

---

## 不同生态怎么表达这个概念？

### OpenAI Agents SDK

直接使用 `agent loop`，Runner 负责工具调用、handoff 和继续运行。

### Anthropic

经常用 loop / agentic loop / self-directed loop 描述 plan → act → observe → adjust 的过程。

### Coding Agent 文档

也常看到：

- tool loop；
- execution loop；
- feedback loop；
- run loop。

这些词可能强调不同层次，因此要看具体语境，不要看到 `loop` 就自动认为完全同义。

---

## Concept Graph Relations

```text
Harness ─contains──────→ Agent Loop

Runtime ─runs──────────→ Agent Loop

Context ─feeds─────────→ Agent Loop / Model

Agent Loop ─uses───────→ Planning
Agent Loop ─produces───→ Action
Action ─produces───────→ Observation
Observation ─feeds─────→ Context

Agent Loop ─governed-by→ Stop Condition
```

这条链是 Agent Atlas 核心地图最重要的一条：

```text
Agent Loop
   ↓
Planning
   ↓
Action / Observation
```

---

## 常见误解

### ❌ Agent Loop 就是模型一直自言自语

不是。核心是模型与环境之间不断发生新的交互。

### ❌ 循环次数越多，Agent 越强

不是。无效循环只会增加成本和错误概率。

### ❌ 只要写一个 `while True` 就有 Agent 了

不是。还需要工具协议、Context 更新、停止条件、异常处理等完整机制。

### ❌ 模型必须先生成完整计划才能进入 Loop

不一定。很多 Agent 会边执行、边观察、边重新规划。

### ❌ 一个 Tool Call 就等于一轮 Loop

也不一定。具体 SDK / Runtime 对“turn”的定义可能不同。

---

## Terminology Observatory

**成熟度：🟢 稳定基础概念。**

“观察—行动—反馈—再决策”的闭环思想远早于 LLM Agent。

LLM 时代的新变化是：

- Model Call 成为决策核心；
- Tool Calling 成为主要 Action 接口；
- Context 管理成为 Loop 的关键资源问题；
- Harness / Runtime 负责把这个循环工程化。

因此 `Agent Loop` 的核心含义已经很稳定，但具体框架对 turn、tool execution、handoff 的实现仍会不同。

---

## 下一步应该学什么？

1. [Agent](../01-foundations/agent.md) —— 谁在这个 Loop 里工作；
2. [Action / Observation](action-observation.md) —— 每轮最关键的反馈关系；
3. [Stop Condition](stop-condition.md) —— Loop 什么时候结束；
4. [Harness](../03-infrastructure/harness.md) —— 谁负责真正运行这个 Loop；
5. [Runtime](../03-infrastructure/runtime.md) —— Loop 的实际生命周期；
6. [Loop Engineering](../08-engineering/loop-engineering.md) —— 如何设计更好的反馈循环。

---

## 一手资料

- OpenAI Agents SDK, [SDK overview](https://openai.github.io/openai-agents-python/)
- OpenAI Agents SDK, [Sandbox concepts](https://openai.github.io/openai-agents-python/sandbox/guide/)
- OpenAI, [The next evolution of the Agents SDK](https://openai.com/index/the-next-evolution-of-the-agents-sdk/)
- Anthropic, [Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents)
- Anthropic, [Trustworthy agents in practice](https://www.anthropic.com/research/trustworthy-agents)

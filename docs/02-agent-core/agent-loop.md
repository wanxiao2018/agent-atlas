# Agent Loop

**中文建议：** Agent 循环 / 智能体循环  
**成熟度：** 🟢  
**重要程度：** ★★★★★  
**学习阶段：** 入门必懂  
**最后更新：** 2026-08-17

---

## 30 秒理解

**Agent Loop 是让 Agent 能够连续工作的核心循环。**

它通常会反复做几件事：

```text
观察当前情况 → 调用模型判断下一步 → 执行动作 → 得到新结果 → 再判断
```

直到模型认为任务已经完成，或者系统触发某个停止条件。

如果说 Model 是“大脑”，那么 Agent Loop 就像“**让大脑不断看结果、做决定、再继续做事的工作节奏**”。

## 先建立一个直觉

想象你在修一个坏掉的水龙头。

你不会这样做：

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

它最重要的能力之一，不是“一开始就把整个计划想完”，而是：

> **执行一步以后，能够看到新的环境反馈，然后重新决定下一步。**

这就是 Loop。

## 为什么需要 Agent Loop？

很多现实任务都有“不确定性”。

例如你让 Agent：

> “帮我把这个项目跑起来并修掉启动错误。”

它一开始并不知道会出现什么错误。

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

如果没有循环机制，模型最多只能根据第一次输入猜测接下来会发生什么。

而 Agent Loop 让模型能够利用**真实反馈**继续工作。

## 技术定义

在工程上，Agent Loop 通常指：

> **一个运行控制过程，它反复调用当前 Agent 的模型，检查模型输出，并根据输出执行工具调用、handoff 或其他动作，再把行动结果加入上下文，直到得到最终输出或触发停止条件。**

不同框架实现细节会不同，但核心结构非常接近。

OpenAI Agents SDK 的 `Runner` 就明确实现了一个 agent loop：

1. 调用当前 Agent 的模型；
2. 检查模型输出；
3. 如果是最终输出，结束；
4. 如果发生 handoff，切换 Agent 后继续；
5. 如果产生 tool calls，执行工具并把结果追加到上下文，然后继续；
6. 超过最大轮数时停止并抛出错误。

## 一个最小 Loop 长什么样？

可以先记住这个非常简化的版本：

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
├── model call
├── tool execution
├── context update
├── state update
├── handoff
├── guardrails
├── retry / error handling
├── approval
├── tracing
└── stop conditions
```

## Loop 中到底“循环”的是什么？

初学者经常以为是“模型一直在自己思考”。

其实更准确地说，循环的是整个**模型—环境交互过程**。

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

- `Context_t`：当前模型能看到的信息；
- `Action_t`：模型决定采取的动作；
- `Observation_t`：执行动作以后得到的新反馈。

这也是为什么 `Action / Observation` 是理解 Agent 的一组核心概念。

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

这里真正体现 Agent 能力的不是“它会写代码”，而是它可以：

**执行 → 看结果 → 改变策略 → 再执行。**

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

例如：

```text
max_turns = 20
```

### 3. 达到时间或成本预算

```text
运行超过 10 分钟 → stop
成本超过 $5 → stop
```

### 4. Guardrail 被触发

例如高风险操作被拦截。

### 5. 需要 Human-in-the-loop

Agent 暂停，等待人类批准后继续。

## Agent Loop ≠ 无限循环

名字里虽然有 `Loop`，但目标并不是“一直循环”。

好的 Agent Loop 应该是：

> **在任务未完成时继续，在已经完成或不应该继续时可靠地停下来。**

所以 Loop 设计实际上同时包含两个问题：

```text
什么时候继续？
什么时候停止？
```

## Agent Loop 和 Chain-of-Thought 有什么区别？

| 概念 | 核心是什么 |
|---|---|
| Chain-of-Thought | 模型内部/输出层面的推理过程 |
| Agent Loop | 模型与工具、环境之间的多轮执行控制 |
| Conversation Loop | 用户和模型多轮聊天 |
| Retry Loop | 某一步失败后重复尝试 |

最简单的判断方式：

> **有没有真实 Action 和新的 Observation 回到系统里？**

如果有，它更接近 Agent Loop。

## Agent Loop 和 Workflow 又是什么关系？

Workflow 也可以有循环。

区别不在“有没有 while”，而在于：

**谁决定下一步？**

固定 workflow：

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

> 外层 workflow 固定，内部某些节点运行 agent loop。

## Loop Engineering 和 Agent Loop 是一回事吗？

不是。

`Agent Loop` 是系统里的**循环机制**。

`Loop Engineering` 更接近一种工程实践：

> 如何设计目标、反馈、验证、停止条件和环境，让 Agent 在循环中越来越接近正确结果。

可以理解为：

```text
Agent Loop      = “循环本身是什么”
Loop Engineering = “这个循环应该怎么设计才有效”
```

## 常见误解

### ❌ 误解 1：Agent Loop 就是模型一直自言自语

不是。核心是模型与环境之间不断发生新的交互。

### ❌ 误解 2：循环次数越多，Agent 越强

不是。无效循环只会增加成本和错误概率。

### ❌ 误解 3：只要写一个 `while True` 就有 Agent 了

不是。还需要工具协议、上下文更新、停止条件、异常处理等完整机制。

### ❌ 误解 4：模型必须先生成完整计划才能进入 Loop

不一定。很多 Agent 会边执行、边观察、边重新规划。

## 在 Agent 系统中的位置

```text
Agentic System
└── Harness
    ├── Agent Loop  ← 你在这里
    │   ├── Model Call
    │   ├── Action
    │   ├── Observation
    │   └── Stop Condition
    ├── Tools
    ├── State
    ├── Runtime
    └── Tracing
```

因此，Agent Loop 通常可以看作 Harness 最核心的控制结构之一。

## 你什么时候会遇到这个词？

它经常出现在：

- OpenAI Agents SDK 的 Runner；
- Claude Agent SDK；
- Coding Agent；
- Browser Agent；
- Tool-use Agent；
- Harness Engineering；
- 长时间运行 Agent；
- Agent Evals。

## 和其他术语的关系

建议继续阅读：

1. [Agent](../01-foundations/agent.md) —— 谁在这个 Loop 里工作；
2. [Action / Observation](action-observation.md) —— 每轮最关键的输入输出关系；
3. [Stop Condition](stop-condition.md) —— Loop 什么时候应该结束；
4. [Harness](../03-infrastructure/harness.md) —— 谁负责真正运行这个 Loop；
5. [Loop Engineering](../08-engineering/loop-engineering.md) —— 如何把 Loop 设计得更可靠。

## 成熟度说明

`Agent Loop` 已经是 Agent SDK 与 Agent 工程中非常稳定的基础概念，因此标记为 🟢。

具体 Loop 的结构会因框架不同而变化，但“模型 → 动作 → 反馈 → 再调用”的核心模式已经非常稳定。

## 参考来源

- OpenAI Agents SDK, [Running agents](https://openai.github.io/openai-agents-python/running_agents/).
- OpenAI Agents SDK, [SDK overview](https://openai.github.io/openai-agents-python/).
- Anthropic, [Building Effective AI Agents](https://www.anthropic.com/engineering/building-effective-agents).

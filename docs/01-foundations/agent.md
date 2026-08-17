# Agent

**中文建议：** 智能体 / AI 智能体  
**常见别名：** AI Agent / Agentic Agent（后者较少必要）  
**成熟度：** 🟡  
**词条状态：** ✅ Atlas-quality  
**重要程度：** ★★★★★  
**学习阶段：** 入门必懂  
**最后更新：** 2026-08-17

---

## 30 秒理解

**Agent 是一种能够围绕目标连续工作，并根据中间结果决定下一步行动的软件系统。**

普通的一次 LLM 调用更像“你问一句，它答一句”；Agent 更像“你给它一个任务，它自己判断接下来该查资料、调用工具、修改文件、继续尝试，还是结束任务”。

所以，Agent 最重要的变化不是“模型突然更聪明了”，而是：

> **模型被放进一个可以持续观察、决策和行动的系统里。**

---

## 先建立一个直觉

假设你对一个人说：

> “帮我比较北京、上海、深圳三地的 AI 工程师岗位情况，最后给我一个结论。”

如果这个人只能坐在椅子上回答，他只能依靠脑子里已经知道的信息。

但如果你给他：

- 浏览器；
- Excel；
- 文件夹；
- 计算器；
- 一套工作规则；
- 允许他反复检查和修改结果；

那么他就从“回答问题的人”变成了“执行任务的人”。

在这个类比里：

```text
LLM / Model ≈ 大脑
Tools       ≈ 可以使用的工具
Context     ≈ 当前桌面上能看到的信息
Memory      ≈ 能保存下来的信息
Harness     ≈ 工作环境 + 工作流程 + 权限 + 调度机制
Agent       ≈ 在这套系统中真正开始做事的执行者
```

这个类比不是严格定义，但非常适合建立第一层直觉。

---

## 为什么会出现 Agent？

LLM 很擅长生成文本、理解信息和进行推理，但很多真实任务并不是“一问一答”就能完成。

例如：

> “找到最近三个月关于 Agent Harness 的一手资料，总结观点差异，并做成一份报告。”

完成这个任务至少需要：

1. 搜索资料；
2. 阅读结果；
3. 判断哪些来源可信；
4. 继续补充搜索；
5. 整理信息；
6. 发现缺口后再次查询；
7. 输出最终结果。

问题在于：**下一步做什么，往往要等上一步结果出来以后才能决定。**

这正是 Agent 的价值所在。

```text
目标
 ↓
模型判断下一步
 ↓
调用工具 / 执行动作
 ↓
得到新信息
 ↓
重新判断
 ↓
继续行动或结束
```

---

## 技术上，Agent 到底是什么？

目前业界对 `Agent` 没有唯一、完全统一的定义。

Anthropic 在《Building Effective Agents》中明确指出，不同团队对 Agent 的边界理解并不完全相同。Anthropic 2026 年关于 trustworthy agents 的定义更强调：Agent 会自己决定如何完成任务，而不是完全遵循固定脚本，并在 self-directed loop 中计划、行动、观察和调整。

OpenAI 则把 agents 描述为能够代表用户独立完成任务的系统，并强调复杂、多步任务、工具和 orchestration。

因此，Agent Atlas 采用一个适合工程实践的定义：

> **Agent 是由模型驱动、能够根据当前 Context 和环境反馈，在多步过程中自主选择下一步行动，以完成某个目标的软件系统。**

这里有四个关键词。

### 1. Goal：它有目标

Agent 通常不是单纯预测下一句话，而是围绕某个任务持续工作。

例如：

- 修复一个 bug；
- 安排一次旅行；
- 分析一组数据；
- 调研一家公司；
- 完成一个代码仓库里的功能。

### 2. Decision：模型参与决定下一步

如果每一步都是程序员提前写死的：

```text
先 A → 再 B → 再 C → 最后 D
```

这更接近传统 Workflow。

Agent 的典型特征是：

> **模型会根据当前结果决定下一步做什么。**

### 3. Action：它可以行动

行动可能包括：

- 调用搜索；
- 读取文件；
- 写代码；
- 执行命令；
- 调 API；
- 调用另一个 Agent；
- 更新数据库；
- 请求人类批准。

### 4. Feedback：它会看到行动结果

Agent 调用工具后，会把结果重新放回 Context，再继续判断。

这就形成了 [Agent Loop](../02-agent-core/agent-loop.md)。

---

## 你可能是在这句话里遇到它

> “The agent inspected the repository, ran the tests, fixed the failing code, and verified the result.”

这句话里 `agent` 指的通常不是“一个模型连续输出了四段文字”。

实际系统更可能是：

```text
User Goal
   ↓
Agent / Harness
   ↓
Model 决定读仓库
   ↓
Tool / Filesystem
   ↓
Observation
   ↓
Model 决定跑测试
   ↓
Runtime / Sandbox
   ↓
Observation
   ↓
Model 修改代码
   ↓
再次测试
   ↓
验证完成
```

所以在技术文章里看到 “the agent did X” 时，要习惯继续追问：

> **到底是 Model 做的，还是 Harness / Tool / Runtime 替 Agent 系统执行的？**

这会极大减少概念混淆。

---

## Agent 是怎么工作的？

一个高度简化的 Agent 可以这样理解：

```text
用户目标
   ↓
构建 Context
   ↓
调用 Model
   ↓
Model 决定：
   ├── 给出最终答案 → 结束
   ├── 调用 Tool ──────┐
   ├── Handoff ────────┤
   └── 继续推理         │
                       ↓
                  得到新结果
                       ↓
                  更新 Context
                       ↓
                  再调用 Model
```

真正的 Agent 系统还可能加入：

- Memory；
- State；
- Sandbox；
- Guardrails；
- Human-in-the-loop；
- Tracing；
- Evals；
- Retry / recovery；
- 多 Agent 协作。

---

## 在 Agent 系统中的位置

可以先用下面这个心智模型：

```text
Agentic System
│
├── Model
│   └── 负责理解、推理、生成和选择动作
│
├── Context
│   └── 模型当前能够看到的信息
│
└── Harness
    ├── Agent Loop
    ├── Tools
    ├── State / Memory
    ├── Runtime
    ├── Sandbox
    ├── Permissions
    └── Tracing / Evals
```

因此常有人用一句很粗略但很好记的话：

> **Agent ≈ Model + Harness**

注意，这不是学术公式，只是帮助理解：**模型本身通常只是 Agent 系统中的核心组件，而不是整个 Agent。**

---

## 一个具体例子

任务：

> “帮我找三家今晚还能预订的餐厅，比较距离和价格后推荐一家。”

一个 Agent 可能这样工作：

```text
1. 读取用户位置和要求
2. 搜索附近餐厅
3. 查看营业状态
4. 查询预订情况
5. 发现第一批结果价格太高
6. 修改搜索条件
7. 再次查询
8. 比较候选项
9. 输出推荐理由
```

重点不在“步骤很多”，而在于：

> **第 5 步出现新情况后，第 6 步是模型根据反馈临时决定的。**

这就是 agentic behavior 的核心之一。

---

## 一个最小技术例子

下面只是伪代码：

```python
context = [user_goal]

while True:
    response = model(context, tools=tools)

    if response.final_answer:
        return response.final_answer

    if response.tool_calls:
        results = run_tools(response.tool_calls)
        context.extend(results)
```

真正的 SDK 会负责更多事情，例如异常处理、handoff、guardrails、状态保存和最大轮数限制。

OpenAI Agents SDK 的 `Runner` 就内置类似的 agent loop：模型输出最终结果时结束；如果输出 tool call，则执行工具后继续；如果发生 handoff，则切换 Agent 后继续运行。

---

## Agent 和 Workflow 有什么区别？

| 概念 | 核心特点 |
|---|---|
| 普通 LLM 调用 | 输入一次，模型输出一次 |
| Workflow | 路径主要由开发者提前定义 |
| Agent | 模型会根据环境反馈动态决定下一步 |
| Agentic Workflow | 介于两者之间，既有固定结构，也让模型在局部做决策 |

现实系统并不是非黑即白。

“自主程度”更像一条连续谱：

```text
固定脚本
   ↓
Workflow
   ↓
带模型决策的 Workflow
   ↓
Agent
   ↓
长时间自主 Agent
```

---

## 不同生态里，“Agent”边界一样吗？

不完全一样。

### Anthropic

更强调：模型自主决定自己的过程和工具使用，在循环中 plan → act → observe → adjust。

### OpenAI Agents SDK

工程接口里的 `Agent` 可以是“配置了 instructions、tools，以及可选 handoffs / guardrails / structured output 的 LLM”。具体自主程度由 Runner 和应用逻辑决定。

### Microsoft Agent Framework

也会把 Agent 视为模型 + runtime / harness 能力的组合，并进一步提供 harness agent 等更完整形态。

因此看到一个库里的 `Agent` 类，不要自动认为它一定是“完全自主 Agent”。

**API 类型名和理论上的 Agent 概念不是完全一回事。**

---

## Concept Graph Relations

```text
Model ─powers──────────→ Agent

Harness ─enables───────→ Agent

Context ─feeds─────────→ Model / Agent decisions

Agent ─uses────────────→ Tools
Agent ─runs-through────→ Agent Loop
Agent ─may-use─────────→ Memory
Agent ─may-execute-in──→ Sandbox

Agent ─contrasts-with──→ Workflow
```

这也是 Agent Atlas 为什么把 `Agent` 放在整张图的中心：它本身不是一个孤立组件，而是多个概念相交的位置。

---

## 常见误解

### ❌ 误解 1：用了 LLM 就是 Agent

不是。

一个网页把用户问题发给模型，再把答案显示回来，通常只是 LLM application。

### ❌ 误解 2：用了 Tool Calling 就一定是 Agent

也不一定。

如果工具调用完全被固定流程控制，模型没有决定下一步的空间，它仍可能更接近 Workflow。

### ❌ 误解 3：Agent 一定完全无人监管

不是。

很多生产 Agent 会在高风险动作前要求人类批准。

自主并不等于没有边界。

### ❌ 误解 4：Agent 就是一个模型

更准确地说，模型通常是 Agent 的“大脑”，而 Agent 是包含模型、工具、上下文和执行机制的完整系统。

### ❌ 误解 5：越自主越先进

不一定。固定 Workflow 在可预测任务上可能更可靠、更便宜，也更容易评测。

---

## 你什么时候会遇到这个词？

几乎所有 Agent 相关资料都会出现：

- OpenAI Agents SDK；
- Claude Agent SDK；
- Coding Agent；
- Browser Agent；
- Deep Research；
- Multi-Agent；
- Agent Evals；
- Agent Harness；
- Agent Runtime。

因此这是整个 Agent Atlas 最核心的入口词之一。

---

## Terminology Observatory

`Agent` 这个词本身远早于 LLM 时代，在 AI、强化学习、机器人等领域已经使用多年。

真正快速变化的是：

> **LLM 时代大家到底把哪些系统称为 Agent。**

因此 Agent Atlas 标记为 🟡：

- 词本身非常成熟；
- LLM Agent 的工程边界仍存在不同定义；
- `agentic` 也经常被营销语境过度使用。

阅读资料时最值得问的问题是：

> **这个作者所谓 Agent，模型到底有多大程度在自行决定下一步？**

---

## 下一步应该学什么？

1. [Agent Loop](../02-agent-core/agent-loop.md) —— Agent 为什么能够连续工作；
2. [Harness](../03-infrastructure/harness.md) —— 谁把模型、工具、循环和环境组织起来；
3. [Tool Calling](../04-tools/tool-calling.md) —— Agent 如何真正请求动作；
4. [Context Engineering](../05-context-memory/context-engineering.md) —— Agent 每一步到底应该看到什么信息；
5. [Runtime](../03-infrastructure/runtime.md) —— Agent 的一次 run 实际如何执行。

---

## 一手资料

- Anthropic, [Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents)
- Anthropic, [Trustworthy agents in practice](https://www.anthropic.com/research/trustworthy-agents)
- OpenAI, [New tools for building agents](https://openai.com/index/new-tools-for-building-agents/)
- OpenAI Agents SDK, [Agents](https://openai.github.io/openai-agents-python/agents/)
- OpenAI Agents SDK, [SDK overview](https://openai.github.io/openai-agents-python/)

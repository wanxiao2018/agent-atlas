# Context Engineering

**中文建议：** 上下文工程  
**成熟度：** 🟡  
**词条状态：** ✅ Atlas-quality  
**重要程度：** ★★★★★  
**学习阶段：** 入门 → 工程实践  
**最后更新：** 2026-08-17

---

## 30 秒理解

**Context Engineering 不是只研究“Prompt 怎么写”，而是研究模型每一次调用时到底应该看到哪些信息。**

Agent 会不断产生新信息：

- 对话历史；
- Tool Results；
- RAG 检索结果；
- Memory；
- 文件；
- 系统规则；
- 当前计划；
- 运行状态。

但 Context Window 是有限的。

所以真正的问题是：

> **在这一轮里，什么信息最值得占用模型有限的注意力？**

---

## 先建立一个直觉

把模型想成一个准备做决定的人。

他桌面上可以放很多东西：

```text
任务说明
历史记录
搜索结果
文件
规则
工具说明
以前的经验
```

桌面太空：信息不足。

桌面太满：找不到重点。

Context Engineering 就是在做：

> **“下一步工作前，到底该把哪些材料摆到桌面上？”**

---

## Context 到底是什么？

Anthropic 在其 Context Engineering 工程文章中给出一个非常清晰的定义：

> Context 是模型进行一次 sampling 时包含的 token 集合。

因此，Context 不只是用户刚刚输入的 Prompt。

它可能包括：

```text
Context
├── System Instructions
├── User Messages
├── Conversation History
├── Tool Definitions
├── Tool Results
├── Retrieved Documents
├── Memory
├── MCP-provided information
├── Files / Repo Context
└── Runtime-generated state
```

这也是为什么：

> **Prompt Engineering 是 Context Engineering 的一部分，但两者不是同义词。**

---

## 为什么 Agent 特别需要 Context Engineering？

一次性问答中，Context 相对简单：

```text
Prompt
  ↓
Model
  ↓
Answer
```

Agent 则不断产生新状态：

```text
Round 1 → Tool Result
Round 2 → 新文件
Round 3 → Error Log
Round 4 → 搜索结果
Round 5 → Plan Update
...
```

如果每一轮把所有历史原封不动塞回模型：

- token 成本会持续增长；
- 注意力会被旧信息稀释；
- 过期状态可能误导模型；
- Tool Results 可能极长；
- 长任务最终会超过 Context Window。

所以长时间 Agent 的核心问题之一就是：

> **信息不断增长，但模型一次能有效使用的信息仍然有限。**

---

## 你可能是在这句话里遇到它

> “Good context engineering means retrieving the right information just in time instead of preloading everything.”

这句话可以拆成：

```text
外部信息很多
   ↓
不全部塞进 Context
   ↓
先判断当前步骤需要什么
   ↓
按需 Retrieval
   ↓
只把高价值信息放入当前 Context
   ↓
Model 做下一步判断
```

这里的关键不是 Prompt 措辞，而是**信息选择策略**。

---

## Context Engineering 通常在工程什么？

### 1. System Instructions

模型最基础的行为规则。

重点是：

- 清晰；
- 不冲突；
- 不把所有流程逻辑硬编码进去。

### 2. Tool Definitions

工具描述本身也会进入模型 Context。

如果有 200 个巨大 Tool Schema，Context 可能在任务开始前就被大量占用。

### 3. Conversation History

哪些历史消息必须保留？

哪些可以删？

哪些应该压缩？

### 4. Tool Results

例如一次 `grep` 返回 20,000 行：

```text
全部塞进去？
还是过滤？
还是让模型按需读取文件？
```

### 5. Retrieval / RAG

不是“有知识库就完事”，而是：

> **这一轮到底应该 retrieve 哪些内容？**

### 6. Memory

Memory 存在 Context 之外。

真正有价值的是：

> **什么时候把哪条 Memory 重新带回当前 Context？**

### 7. Compaction

当历史过长时，把旧 Context 转换成更小的表示，例如摘要、状态文件或结构化进度记录。

---

## Prompt Engineering vs Context Engineering

| Prompt Engineering | Context Engineering |
|---|---|
| 重点是“怎么说” | 重点是“给模型看什么” |
| 常关注 instructions 的文字表达 | 关注整个 inference context 的组成 |
| 可以是一次性的 | Agent 中通常每一轮都在动态发生 |
| 主要对象是 Prompt | 对象包括 Prompt、Tools、History、Memory、Retrieval、Tool Results 等 |

可以用一句话记：

```text
Prompt Engineering
= 写好这张纸

Context Engineering
= 决定桌子上应该摆哪些纸
```

---

## Context ≠ Memory

这是 Agent Atlas 最重要的边界之一。

### Context

模型**这一轮当前能看到的东西**。

### Memory

保存在 Context Window 之外、未来可以重新取回的信息机制。

所以：

```text
Memory Store
   ↓ retrieve
Memory Item
   ↓
Current Context
   ↓
Model
```

Memory 只有在被取回并放进 Context 后，模型这一轮才能真正“看到”。

→ [Memory](memory.md)

---

## Context ≠ Context Window

```text
Context Window
= 模型理论上一次最多能容纳多少 token

Context
= 这一次调用实际上放进去了什么 token
```

一个模型有 1M Context Window，并不意味着每次都应该塞 1M token。

更大的 Window 只是更大的容量，不自动等于更好的信息选择。

---

## Compaction 是什么角色？

随着 Agent Loop 运行：

```text
Context
 ↓ grows
Context
 ↓ grows
Context
 ↓ grows
快到上限
 ↓
Compaction
 ↓
更小的摘要 / 状态表示
 ↓
继续运行
```

但 Compaction 有代价：

**压缩通常是有损的。**

未来需要的信息可能恰好被删掉。

因此现代 Agent 会把部分原始信息保存在 Context 之外，例如：

- Session Log；
- Files；
- Memory Store；
- Database；
- Artifact Store。

需要时再重新 retrieve。

---

## “Just-in-time context” 为什么重要？

一个常见错误是：

> “既然这些信息可能有用，那一开始全放进去吧。”

问题是模型的 attention 不是无限资源。

更好的策略经常是：

```text
需要什么
 ↓
再去找
 ↓
只取相关内容
 ↓
完成当前步骤
```

例如 Coding Agent 不应该一开始把整个 5GB repository 塞给模型。

它更适合：

```text
先看 tree
→ 搜索符号
→ 找到相关文件
→ 按需读取局部
```

这本质上就是 Context Engineering。

---

## Concept Graph Relations

```text
Prompt ─feeds──────────→ Context

Memory ─feeds──────────→ Context
RAG ─feeds─────────────→ Context
Tool Results ─feed─────→ Context

Compaction ─transforms─→ Context

Context ─feeds─────────→ Model

Agent Loop ─evolves────→ Context

Harness ─manages───────→ Context Engineering
```

---

## 一个最小工程流程

```python
context = build_base_context(instructions, user_request)

while not done:
    relevant_memory = retrieve_memory(state)
    relevant_docs = retrieve_docs(state)

    current_context = compose(
        context,
        relevant_memory,
        relevant_docs,
        tool_definitions
    )

    response = model(current_context)
    result = execute_if_needed(response)

    state.update(result)

    if context_too_large(state):
        compact(state)
```

真正复杂的地方往往不是 `model()`，而是：

```text
retrieve_memory
retrieve_docs
compose
compact
```

这些正是 Context Engineering 的核心工作。

---

## 常见误解

### ❌ Context Engineering = 写更长 Prompt

完全不是。

有时最好的 Context Engineering 恰恰是**删掉信息**。

### ❌ Context Window 越大，Context Engineering 越不重要

不是。更大窗口只是放得更多，噪声和错误信息也可以放得更多。

### ❌ Memory 和 RAG 都是 Context

它们通常是 Context 的**来源**，不是当前 Context 本身。

### ❌ 所有历史都应该保留

不一定。旧 Tool Result、过期 Plan 和重复信息可能降低信号密度。

---

## Terminology Observatory

**成熟度：🟡，概念快速形成共识。**

“管理 LLM 输入上下文”这件事并不新，但 `Context Engineering` 作为独立工程术语是在 2025 年前后快速流行起来的。

Anthropic 明确把它描述为 Prompt Engineering 的自然演进：从“优化 Prompt 文本”扩展为“管理一次 inference 中所有 token 的组成”。

因此它现在已经是 Agent Engineering 的重要术语，但仍处于快速演化阶段。

---

## 下一步应该学什么？

1. [Memory](memory.md) —— 信息如何跨 Context 保存；
2. [RAG](rag.md) —— 外部知识如何按需取回；
3. Compaction —— 长历史怎么压缩；
4. [Context Window](../01-foundations/context-window.md) —— Context 的容量边界；
5. [Harness](../03-infrastructure/harness.md) —— 谁负责执行 Context 策略。

---

## 一手资料

- Anthropic, [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- Anthropic, [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
- Anthropic, Scaling Managed Agents: Decoupling the brain from the hands: https://www.anthropic.com/engineering/managed-agents
- Anthropic, [Writing effective tools for AI agents](https://www.anthropic.com/engineering/writing-tools-for-agents)

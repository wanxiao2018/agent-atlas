# Memory

**中文建议：** 记忆  
**成熟度：** 🟡  
**词条状态：** ✅ Atlas-quality  
**重要程度：** ★★★★★  
**学习阶段：** 入门 → 工程实践  
**最后更新：** 2026-08-17

---

## 30 秒理解

**Memory 是让 Agent 把重要信息保存到当前 Context Window 之外，并在以后需要时重新取回的机制。**

如果没有 Memory，一个长时间 Agent 很容易变成：

> “这一轮很聪明，下一轮重新失忆。”

所以 Memory 解决的不是“让模型权重永久改变”，而是：

```text
先保存
   ↓
以后检索
   ↓
重新放回 Context
   ↓
模型再次使用
```

---

## 先建立一个直觉

把 Context 想成你正在使用的办公桌。

桌子上只能放有限材料。

Memory 更像：

- 笔记本；
- 文件柜；
- 项目日志；
- 数据库；
- Git commit；
- 写给“下一班同事”的交接记录。

你不需要让所有东西一直铺在桌面上。

只要保证：

> **重要信息能被保存，而且未来真的能找回来。**

---

## 为什么 Agent 特别需要 Memory？

Agent 的工作越来越长：

```text
几分钟
→ 几小时
→ 多次 session
→ 几天
```

但模型 Context Window 仍然有限。

Anthropic 在长时间 Agent 实践中描述了一个非常典型的问题：

> 每个新 session 都像换了一个新工程师，新的人如果看不到上一班留下的记录，就不知道之前发生了什么。

因此长时间任务需要把关键状态留在 Context 之外，例如：

```text
progress.md
feature_list.json
project files
session log
memory store
checkpoint
```

新一轮 Agent 再通过这些外部信息恢复工作。

---

## 技术定义

Agent 领域中的 `Memory` 边界并没有完全统一。

在 Agent Atlas 中，我们采用一个实用定义：

> **Memory 是用于写入、持久化、组织、检索并重新注入有用信息的机制，使 Agent 能够跨轮次、跨 Context Window 或跨 Session 延续知识与经验。**

Memory 通常至少涉及两个动作：

```text
WRITE
什么值得记？
怎么保存？

READ / RETRIEVE
什么时候需要？
取哪一条？
怎么重新放回 Context？
```

只有“存下来”而从不取回，不是有效 Memory。

---

## 你可能是在这句话里遇到它

> “The agent writes lessons to memory so future runs can reuse them.”

拆开来看：

```text
Run #1
   ↓
发现一个重要经验
   ↓
Memory Write
   ↓
持久化到 Context Window 外

──────── session boundary ────────

Run #2
   ↓
遇到相似问题
   ↓
Memory Retrieval
   ↓
相关经验进入 Current Context
   ↓
Model 使用
```

这才是 `memory` 在 Agent 系统里的典型含义。

---

## Memory ≠ Context

这是最重要的一条边界。

### Context

模型**现在这一轮正在看到什么**。

### Memory

信息**存在哪里，以及以后怎么重新找回来**。

所以：

```text
Memory Store
   ↓ retrieve
Memory Item
   ↓ inject
Context
   ↓
Model
```

如果某条 Memory 没有进入当前 Context，模型这一轮通常就无法直接利用它。

→ [Context Engineering](context-engineering.md)

---

## Memory ≠ Conversation History

对话历史可以充当一种短期 Memory，但二者不能完全等同。

Conversation History 通常是：

```text
User message
Assistant message
Tool result
...
```

而更完整的 Agent Memory 可能是：

```text
Memory
├── 用户偏好
├── 项目决策
├── 失败教训
├── 当前任务进度
├── 可复用策略
└── 跨 Session 状态
```

有时它甚至根本不是聊天文本，而是结构化文件或数据库记录。

---

## Memory ≠ RAG

二者都涉及“存储 + 检索”，所以经常混淆。

可以先这样区分：

### RAG

更常解决：

> **外部知识库里有什么相关知识？**

例如：

```text
公司文档
产品手册
论文库
```

### Memory

更常解决：

> **这个 Agent / 用户 / 任务过去发生过什么，未来需要记住什么？**

例如：

```text
用户偏好深色主题
上次部署失败因为端口冲突
这个任务已经完成步骤 1-4
```

但真实系统中两者技术实现可以重叠，例如都用向量检索。

所以区别主要是**语义职责**，而不是底层数据库类型。

---

## Memory 可以分成哪些类型？

分类方法很多，没有唯一标准。

对初学者可以先使用这一套：

### Working / Short-term Memory

当前任务的临时工作信息。

例如：

- 当前 TODO；
- 中间变量；
- 当前 plan。

### Episodic Memory

“以前发生过什么”。

例如：

> 上次执行这个部署流程时，在 migration 步骤失败过。

### Semantic Memory

稳定事实。

例如：

> 用户更喜欢 Python，而不是 JavaScript。

### Procedural Memory

“这类事情应该怎么做”。

例如：

> 修改 API 后要先运行 schema tests，再跑 integration tests。

这套分类主要用于建立直觉，不代表所有框架都会用同样名称。

---

## Memory 写什么，比“有没有 Memory”更重要

一个危险做法是：

> 所有东西都记住。

这会造成：

- 垃圾 Memory；
- 冲突信息；
- 过期偏好；
- 错误经验被不断强化；
- Retrieval 时噪声越来越大。

所以 Memory Engineering 至少有四个问题：

```text
1. What to write?
2. How to represent it?
3. When to retrieve?
4. When to forget / update?
```

Memory 不是无限仓库，而是一套信息管理策略。

---

## 文件系统为什么常被当作 Agent Memory？

对于 Coding Agent 和长时间 Agent，文件系统非常实用。

例如：

```text
progress.md
├── 已完成什么
├── 当前问题
└── 下一步是什么

feature_list.json
├── task status
└── validation state
```

优点是：

- 简单；
- 可读；
- 可 diff；
- 新 session 可以直接读取；
- 不必把所有历史一直留在 Context。

Anthropic 的 long-running agent 实践就大量依赖环境中的持久 artifact 来跨 Context Window 传递进度。

---

## Session Log 也可以是一种 Memory 吗？

可以。

Anthropic 在 Managed Agents 架构中提出了一个很有价值的区分：

```text
Session Log
= 可恢复的完整外部记录

Context Window
= 当前模型真正看到的有限切片
```

模型不必永久携带整个历史。

Runtime / Harness 可以从 Session 中：

```text
向前读
回退几步
选择一段
重新组织
```

再把需要的内容送回 Context。

这是一种非常典型的：

> **Memory 在外，Context 在内。**

---

## Memory 和 Compaction 有什么关系？

Compaction 解决：

> Context 快满了，怎么把当前内容变小？

Memory 解决：

> 哪些东西值得离开当前 Context 后仍然保存？

所以一个长时间 Agent 可能这样做：

```text
Current Context
   ↓
提取重要事实 → Memory
   ↓
Compaction
   ↓
较小 Context
   ↓
继续工作
```

未来需要细节时，再从 Memory / Session / Files 重新检索。

---

## 一个最小 Memory Loop

```python
state = load_state()

while not done:
    memories = memory.retrieve(state.current_task)

    context = compose_context(
        instructions,
        state,
        memories
    )

    response = model(context)
    result = execute(response)

    if should_remember(result):
        memory.write(extract_memory(result))

    state.update(result)
```

真正难的地方通常是：

```text
should_remember()
extract_memory()
retrieve()
```

这三步决定 Memory 是否真的有价值。

---

## Concept Graph Relations

```text
Agent ─uses────────────→ Memory

Memory ─stores─────────→ Facts / Experience / State

Memory ─feeds──────────→ Context

Context Engineering ─selects→ Memory Items

Compaction ─may-write──→ Memory

Session ─persists──────→ History

Runtime ─loads─────────→ Memory / State
```

---

## 常见误解

### ❌ Memory = 模型训练

不是。绝大多数 Agent Memory 不修改模型权重。

### ❌ 所有聊天历史都叫 Memory

可以算最简单的短期记忆，但 Agent Memory 通常范围更广。

### ❌ Memory 越多越好

不是。垃圾记忆会污染后续 Context。

### ❌ 存进数据库以后模型就“知道了”

不是。信息还需要被检索并重新带入当前 Context。

### ❌ Memory 和 RAG 完全相同

技术可能重叠，但通常解决的语义问题不同。

---

## Terminology Observatory

**成熟度：🟡，概念成熟但分类仍高度不统一。**

“Memory”本身当然不是新词，但 LLM Agent 领域对：

```text
short-term
long-term
episodic
semantic
procedural
file memory
session memory
```

等分类尚没有统一标准。

所以读不同框架文档时，不应只看名字，而要问：

> **它保存什么？保存在哪里？什么时候取回？怎么进入 Context？**

---

## 下一步应该学什么？

1. [Context Engineering](context-engineering.md) —— Memory 怎么重新进入模型；
2. [RAG](rag.md) —— 外部知识检索和 Memory 有什么边界；
3. Compaction —— 长 Context 怎么压缩；
4. [State](../03-infrastructure/state.md) —— Memory 和运行状态有什么区别；
5. [Runtime](../03-infrastructure/runtime.md) —— 谁负责加载和持久化这些信息。

---

## 一手资料

- Anthropic, Effective context engineering for AI agents: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- Anthropic, Effective harnesses for long-running agents: https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
- Anthropic, Scaling Managed Agents: Decoupling the brain from the hands: https://www.anthropic.com/engineering/managed-agents
- OpenAI Agents SDK, Sandbox / memory support: https://openai.github.io/openai-agents-python/sandbox/guide/
- OpenAI Agents SDK release notes (sandbox memory support): https://openai.github.io/openai-agents-python/release/

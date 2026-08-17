# Agent Atlas 项目原则

Agent Atlas 的目标不是成为“术语数量最多的 Agent 词典”，而是成为一个能够帮助读者建立 **Agent Engineering 心智模型** 的语境型概念地图。

## 核心定位

> **Don't just define the term. Locate it.**  
> 不只解释这个词，还告诉你它在整个 Agent 世界的哪里。

我们的核心用户不是完全没有接触过 AI 的人，也不是已经长期从事 Agent Infra 的专家，而是这类学习者：

> 已经开始阅读 Agent 相关书籍、论文、GitHub、技术博客和 SDK 文档，但经常被突然出现的专业术语和概念关系卡住的人。

## 四个核心模块

### 1. Contextual Glossary｜语境型解释

一个术语脱离语境很容易变成“记住了中文翻译，但还是不会读技术资料”。

因此词条应该尽量回答：

- 这个词通常会在哪类材料中出现？
- 作者为什么在这里使用这个词？
- 放进完整句子后，它承担什么语义？
- 如果把它换成另一个相近词，含义会发生什么变化？

### 2. Concept Graph｜概念关系图

每个术语都应该尽量挂到 Concept Graph 中，而不是作为孤立词条存在。

优先记录：

- 包含 / 组成
- 依赖 / 使用
- 输入 / 输出
- 前后流程
- 概念对比
- 高频混淆
- 术语演化

### 3. Terminology Observatory｜术语观察站

Agent Engineering 的术语体系仍在快速变化。

因此需要区分：

- 老概念在 LLM 时代的新用法；
- 已经比较稳定的行业术语；
- 不同公司使用不同名字表达的相近概念；
- 2025–2026 新兴的新说法；
- 仍有明显争议的定义。

不要把刚刚流行的新词包装成几十年来一直存在的标准术语。

### 4. Concept Boundaries｜概念边界

优先解决“看起来很像”的概念。

例如：

- Agent vs Workflow
- Harness vs Framework
- Harness vs Runtime
- Context vs Memory
- Memory vs RAG
- Tool Calling vs Function Calling
- Agent Loop vs Loop Engineering
- Skill vs Tool
- Skill vs MCP
- Sub-agent vs Multi-Agent
- Tracing vs Observability

如果一个词条没有解释它最容易和谁混淆，往往说明它还没有真正讲透。

---

## Progressive Disclosure｜渐进式披露

一篇词条应该同时服务不同深度的读者。

推荐按以下层级组织：

```text
30 秒理解
   ↓
建立直觉
   ↓
真实语境
   ↓
技术定义
   ↓
工作机制
   ↓
Concept Graph 中的位置
   ↓
概念边界
   ↓
不同生态差异
   ↓
术语演化与争议
   ↓
一手资料
```

读者可以在任何一层停止，而不必为了查一个词被迫读完整篇长文。

---

## Atlas-quality 标准

### 🚧 Stub

只有基础定义，或者内容仍明显不完整。

### 🟨 Developing

已经有较完整解释，但缺少一个或多个关键维度，例如真实语境、概念关系、边界或来源。

### ✅ Atlas-quality

至少满足：

- [ ] 30 秒理解
- [ ] 技术定义
- [ ] 至少一个真实使用语境
- [ ] 在 Concept Graph 中的位置
- [ ] 至少一组概念边界 / 易混淆概念
- [ ] 相关概念及关系类型
- [ ] 术语成熟度说明
- [ ] 一手或高质量来源

重要核心词还应尽量加入：

- [ ] 不同生态 / 厂商叫法
- [ ] 术语演化史
- [ ] 真实工程案例
- [ ] 最小伪代码 / 流程图
- [ ] 常见误解

---

## 不以词条数量作为 KPI

Agent Atlas 不追求“500+ Terms”这种表面数字。

更值得追踪的指标是：

- Atlas-quality 核心概念数量
- 已建立的 Concept Graph 关系数量
- 已整理的 Concept Boundaries 数量
- 已拆解的真实英文语境数量
- 有一手来源支撑的词条比例
- 已标注术语成熟度的比例
- 定期复核的快速变化词条数量

50 个真正讲透的词，比 500 个自动生成、彼此孤立的定义更有价值。

---

## Source-backed，而不是 AI-filled

AI 可以帮助：

- 搜索候选术语；
- 对比多家文档；
- 起草解释；
- 检查结构；
- 发现可能混淆的概念。

但 AI 生成的内容不能因为“看起来像解释”就自动成为正式词条。

尤其是快速变化、新兴或存在争议的概念，应优先核对：

1. 官方文档 / 官方工程博客
2. 原始论文
3. 协议规范 / 标准
4. 高质量工程实践文章

必要时明确写：

> 当前没有统一定义，以下是截至某日期更常见的工程用法。

---

## 与其他优秀项目的关系

Agent Atlas 不试图替代：

- 系统性的 Agent 入门课程；
- Awesome List / 资源导航；
- Agent Pattern Encyclopedia；
- 各厂商官方文档。

如果其他项目已经把某个方向做得更好，我们应该链接和引用，而不是重新复制一份。

Agent Atlas 的价值在于：

> **把读者正在遇到的陌生词，放回完整的 Agent Engineering 概念网络中。**

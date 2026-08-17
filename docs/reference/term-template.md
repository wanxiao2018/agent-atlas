# Agent Atlas 词条模板

> Agent Atlas 的目标不是“翻译术语”，而是让第一次遇到这个词的人建立正确直觉，并能够继续读懂更专业的材料。

## Term

`English Term`

**中文建议：**  
**常见别名 / Related names：**  
**术语成熟度：** 🟢 Stable / 🟡 Evolving / 🔴 Emerging or Contested  
**词条状态：** 🚧 Stub / 🟨 Developing / ✅ Atlas-quality  
**重要程度：** ★★★★★  
**学习阶段：** 入门 / 进阶 / 工程实践  
**最后更新：** YYYY-MM-DD

---

## 30 秒理解

用 2～4 句话回答：

1. 它是什么？
2. 它最核心的作用是什么？
3. 为什么 Agent 领域的人会频繁提到它？

这一部分必须做到：**没有计算机专业背景的人也基本能看懂。**

---

## 先建立一个直觉

不要急着下定义。先用一个生活场景、工作场景或简单故事，让读者脑中形成画面。

例如：

- Model 像“大脑”；
- Tool 像“手里的工具”；
- Sandbox 像“允许动手操作、但与外界隔离的工作间”。

类比只帮助理解，不应代替技术定义；如果类比存在明显边界，要指出类比在哪些地方会失效。

---

## 你可能是在这句话里遇到它

这是 Agent Atlas 与普通词典最重要的区别之一。

至少提供一个接近真实技术材料的使用语境，例如：

```text
The harness re-enters the agent loop after the tool result is returned.
```

然后拆解：

```text
tool result returned
        ↓
Harness 得到 Observation
        ↓
写回 Context / State
        ↓
进入下一轮 Agent Loop
```

回答：

- 作者为什么在这里使用这个词？
- 这句话描述的是结构、过程、角色还是工程范式？
- 如果读者只知道中文翻译，最容易误解在哪里？

如果例句来自真实来源，应注明来源；如果是为了教学而改写，要明确写“教学化示例”。

---

## 为什么会出现这个概念？

回答它解决了什么真实问题。

推荐结构：

```text
原来的问题
    ↓
为什么普通 LLM / 旧方案不够
    ↓
这个概念提供了什么能力
```

不要只写“为了提升效率 / 提高准确率”这种空泛表述。

---

## 技术定义

在已经建立直觉之后，再给出更严格的工程解释。

尽量说明：

- 输入是什么；
- 输出是什么；
- 谁负责控制它；
- 它与模型、工具、环境、Context、State 之间是什么关系；
- 是否存在多种实现方式；
- 如果行业尚无统一定义，要明确写出“边界仍在变化”。

---

## 它是怎么工作的？

如果这个概念涉及过程，用步骤解释。

```text
Step 1 → Step 2 → Step 3 → ... → 结束
```

如果适合，加入伪代码、状态图或流程图。

重点是帮助读者形成运行机制，而不是展示复杂代码。

---

## 它在 Agent 系统中的位置

先把这个概念挂回 Agent Atlas Concept Graph。

核心骨架：

```text
                       ┌── Prompt
                       │
                  Context
                ↙      ↓       ↘
             Memory   RAG    Compaction
                │
                ↓
Model ─────→ Agent ←──── Harness
                         │
            ┌────────────┼────────────┐
            ↓            ↓            ↓
        Agent Loop      Tools       Runtime
            │            │            │
            ↓            ↓            ↓
         Planning       MCP        Sandbox
            │
            ↓
      Action/Observation
```

解释：

- 当前词位于哪里？
- 它上游依赖什么？
- 下游影响什么？
- 它是组件、过程、协议、环境、数据，还是工程方法？

这张图只是心智模型，不要把一种实现方式写成唯一标准。

---

## Concept Graph 关系

不要只列“相关词”，尽量明确关系类型。

| From | Relation | To | 为什么 |
|---|---|---|---|
| A | `contains` | B | ... |
| A | `uses` | C | ... |
| A | `confused-with` | D | ... |

建议优先使用：

`contains` · `feeds` · `uses` · `executes-in` · `isolated-by` · `connects` · `produces` · `precedes` · `contrasts-with` · `confused-with` · `evolved-from`

---

## 一个具体例子

不要只写抽象伪代码。尽量给一个读者能想象的真实任务，例如：

> “帮我查三家酒店，比较价格和距离，然后整理成表格。”

逐步指出这个术语具体发生在哪一步。

---

## 一个最小技术例子

使用伪代码或非常短的代码解释机制，而不是为了展示复杂代码。

```python
# pseudo code
while not done:
    result = model(context)
    observation = run_tools(result.tool_calls)
    context.append(observation)
```

如果该概念并不适合代码示例，可以改用消息序列、数据流或状态变化。

---

## Concept Boundaries｜最容易混淆的概念

不要只说“它和 X 不一样”，而要回答：

1. 为什么初学者会觉得它们像？
2. 它们真正的边界在哪里？
3. 有没有一句最简单的判断方法？

推荐表格：

| 概念 | 负责什么 | 不负责什么 | 最简单判断 |
|---|---|---|---|
| A | ... | ... | ... |
| B | ... | ... | ... |

例如：

- Harness vs Framework
- Context vs Memory
- Agent Loop vs Loop Engineering

---

## 不同生态怎么叫？

当术语存在厂商 / 框架差异时，单独整理。

| 生态 | 常见叫法 | 是否完全等价 | 备注 |
|---|---|---|---|
| OpenAI | ... | ... | ... |
| Anthropic | ... | ... | ... |
| Google / ADK | ... | ... | ... |
| LangChain / LangGraph | ... | ... | ... |

注意：不要因为两个 API 看起来类似，就直接声称概念完全等价。

---

## 常见误解

至少列出 2～3 个初学者高频误区。

例如：

- ❌ 有 Tool Calling 就一定是 Agent
- ❌ Agent 一定是完全自主的
- ✅ 自主程度更像连续谱，关键要看系统是否允许模型根据反馈决定下一步行动

---

## 你什么时候会遇到这个词？

告诉读者它通常出现在哪里，例如：

- Agent SDK 文档
- Coding Agent
- 多 Agent 系统
- Evals / tracing
- Agent research paper
- 系统设计文章

这样读者下一次看到它时能快速识别语境。

---

## Terminology Observatory｜术语演化

对于重要或新兴词，尽量回答：

**早期来源 / 前身概念：**  
**大约何时开始在 LLM / Agent 圈流行：**  
**哪些公司 / 社区频繁使用：**  
**当前常见含义：**  
**是否存在定义争议：**  

尤其要区分：

- 经典计算机科学术语；
- 旧概念在 LLM 时代的新用法；
- 新的行业包装词；
- 真正出现了新工程边界的新术语。

---

## 成熟度说明

解释为什么标记为 🟢 / 🟡 / 🔴。

- 🟢 **Stable**：定义和用法相对稳定，跨来源差异较小
- 🟡 **Evolving**：行业普遍使用，但边界、命名或实现仍在演化
- 🔴 **Emerging / Contested**：新兴说法或定义争议较大，尚未形成稳定共识

不要仅根据“这个词最近很火”判断成熟度。

---

## 相关概念与下一步阅读

给读者一个明确的下一跳，而不是堆链接。

例如：

- 如果你刚理解 **Harness** → 下一步看 **Agent Loop** 和 **Runtime**
- 如果你刚理解 **Memory** → 下一步看 **Context**、**RAG**、**Compaction**

---

## 参考来源

优先顺序：

1. 官方文档 / 官方工程博客
2. 原始论文
3. 标准或协议规范
4. 高质量技术文章

避免只引用二手解释。对快速变化的 Agent 术语，应注明资料日期并定期复查。

---

## 发布前 Atlas-quality 检查

- [ ] 30 秒解释真正能让新人看懂
- [ ] 技术定义没有被类比替代
- [ ] 至少一个真实 / 教学化语境
- [ ] 已挂回 Concept Graph
- [ ] 关系不是只有“相关术语”三个字
- [ ] 至少讲清一个 Concept Boundary
- [ ] 新兴术语有成熟度与演化说明
- [ ] 重要事实有可靠来源
- [ ] 没有为了凑长度重复表达同一句话
- [ ] 没有把某一家厂商实现误写成行业唯一标准

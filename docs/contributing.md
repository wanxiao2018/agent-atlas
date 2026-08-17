# 贡献指南

Agent Atlas 不是单纯的术语收集项目。新增一个词之前，先判断：**这个词是否能帮助读者补全 Agent Engineering 的概念地图？**

## 新增术语

1. 先确认术语是否已有页面或属于某个现有概念的别名。
2. 复制 `reference/term-template.md` 的结构。
3. 文件名统一使用英文小写 kebab-case，例如 `context-engineering.md`。
4. 中文翻译不确定时明确写“暂无统一译法”，不要强行创造标准中文名。
5. 新兴词必须注明成熟度，并尽量给出一手来源。
6. 明确它在 Concept Graph 中的位置，以及至少一个关系类型。
7. 至少解释一个最容易混淆的相邻概念。
8. 尽量加入一个真实或教学化英文使用语境。
9. 一次提交尽量只解决一个概念或一组强相关概念。

## 词条状态

### 🚧 Stub

只有基础定义，允许作为待完善占位页存在。

### 🟨 Developing

已有完整解释，但仍缺少语境、Concept Graph、概念边界或可靠来源中的一项或多项。

### ✅ Atlas-quality

至少具备：

- 30 秒理解
- 技术定义
- 一个真实 / 教学化语境
- Concept Graph 中的位置
- 明确的概念关系
- 至少一个 Concept Boundary
- 术语成熟度说明
- 可靠来源

## 写作原则

- **白话解释优先，但不能牺牲准确性。**
- **Progressive Disclosure。** 最上面让新人 30 秒理解，越往下越深入。
- **解释概念关系，而不只翻译单词。**
- **区分行业通用定义和某家公司自己的实现。**
- **诚实处理争议。** 没有统一定义时直接说没有统一定义。
- **不要把刚流行的新词包装成历史悠久的标准术语。**
- **不要为了词条数量自动生成大量模板化内容。**
- **能引用一手资料时，不用二手总结代替。**
- **如果已有优秀项目把某个主题讲得更好，优先链接过去而不是复制。**

## 引用与链接格式

参考来源不要直接裸露 URL，统一使用标准 Markdown 链接：

```md
- Anthropic, [Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents)
- OpenAI, [New tools for building agents](https://openai.com/index/new-tools-for-building-agents/)
- OpenAI Agents SDK, [Agents](https://openai.github.io/openai-agents-python/agents/)
```

正文中引用资料时，也优先把资料标题本身做成链接，例如：

```md
Anthropic 在 [Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents) 中讨论了 workflow 与 agent 的区别。
```

详细规范见 [引用与链接规范](reference/citation-style.md)。仓库中的 Markdown source-link Action 会自动修正常见的 `标题: https://...` 写法，但自动化只作为兜底。

## Concept Graph 关系

推荐使用明确关系，而不是只写“相关”：

- `contains`
- `feeds`
- `uses`
- `executes-in`
- `isolated-by`
- `connects`
- `produces`
- `precedes`
- `contrasts-with`
- `confused-with`
- `evolved-from`

详细说明见 [核心概念地图](concept-map.md)。

## 发布前自检

提交前请问自己：

> 如果读者是在一本 Agent 书或一篇技术文章里第一次看到这个词，这一页能不能让他回到原文后真正继续读下去？

如果答案仍然只是“他知道了这个词的中文翻译”，那这个词条还没有完成。

# 引用与链接规范

Agent Atlas 的参考来源既要便于读者阅读，也要保持 Markdown 源文件干净、可迁移。

## 基本规则

参考来源中的网页链接统一使用标准 Markdown 链接格式：

```md
- 机构 / 作者, [资料标题](URL)
```

不要写成裸 URL：

```md
Anthropic, Building Effective Agents: https://www.anthropic.com/engineering/building-effective-agents
```

应该写成：

```md
- Anthropic, [Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents)
```

## 推荐格式

### 官方文档 / 官方工程博客

```md
- Anthropic, [Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents)
- OpenAI, [New tools for building agents](https://openai.com/index/new-tools-for-building-agents/)
- OpenAI Agents SDK, [Agents](https://openai.github.io/openai-agents-python/agents/)
```

### 需要标注日期时

```md
- Anthropic, [Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents), 2024-12-19.
```

日期只在它对理解术语演化、版本差异或资料时效性有帮助时加入，不需要为了形式统一给所有来源强行补日期。

### 学术论文

推荐保留作者 / 机构与论文标题：

```md
- Author et al., [Paper Title](https://arxiv.org/abs/xxxx.xxxxx), arXiv, 2026.
```

### 标准 / 协议规范

```md
- Model Context Protocol, [Architecture](https://modelcontextprotocol.io/specification/2025-06-18/architecture), specification.
```

如果引用的是带版本日期的规范，应尽量保留版本或日期，避免读者打开后看到已经变化的定义却不知道来源版本。

## 正文中的引用

正文里提到某篇资料时，也优先把资料标题本身做成链接：

```md
Anthropic 在 [Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents) 中区分了 workflow 与 agent。
```

避免：

```md
Anthropic 在 Building Effective Agents 中提到这个概念：https://...
```

## 为什么采用这种格式？

1. **阅读更顺畅**：读者看到的是有意义的标题，不是一长串 URL。
2. **Markdown 可移植**：GitHub、MkDocs 和大多数 Markdown 渲染器都能一致显示。
3. **方便维护**：标题和来源机构保留后，即使链接失效，也更容易重新定位原始资料。
4. **更适合 Agent Atlas**：我们强调 source-backed，而不是简单堆链接。

## 自动规范化

仓库包含 `scripts/normalize_markdown_links.py` 和对应 GitHub Action。

它会把下面这种常见格式：

```md
Anthropic, Building Effective Agents: https://...
```

自动规范为：

```md
- Anthropic, [Building Effective Agents](https://...)
```

自动化只是兜底。新增或修改词条时，仍应直接按本页规范书写。

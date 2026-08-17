# Agent Atlas

> **Don't just define the term. Locate it.**  
> **不只解释这个词，还告诉你它在整个 Agent 世界的哪里。**

Agent Atlas 是一个面向 Agent / Agentic AI 学习者与实践者的 **Agent Engineering 语境型概念地图（Contextual Concept Atlas）**。

它不追求成为最大的 A–Z 术语表，也不重复已有的 Agent 课程、Awesome List 或 Pattern Encyclopedia。它解决一个更具体的问题：当你在书、论文、GitHub、技术博客或 SDK 文档里突然遇到陌生术语时，怎样快速理解它，并把它放回完整的 Agent Engineering 心智模型中。

[在线阅读 Agent Atlas](https://wanxiao2018.github.io/agent-atlas/)

## 核心概念骨架

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

## 核心能力

- **Contextual Glossary**：不只解释定义，还解释真实使用语境。
- **Concept Graph**：记录概念之间的包含、依赖、使用、对比与演化关系。
- **Terminology Observatory**：区分稳定术语、演化中的术语和新兴 / 争议说法。
- **Concept Boundaries**：系统讲清 Harness vs Framework、Context vs Memory 等高频混淆。

## 工程结构

```text
docs/                         # 面向读者的知识内容
  data/concept-graph.json     # Concept Graph 单一数据源
  reference/                  # 写作、引用与工程规范
scripts/                      # 内容规范化与项目校验
.github/workflows/            # CI 与 GitHub Pages 部署
mkdocs.yml                    # 站点导航与渲染配置
```

Agent Atlas 把**公开内容**和**开发状态**分开：页面只呈现当前可用的知识，不展示“以后再补”“当前只是某个草稿版本”之类的开发过程文案。内容成熟度、图谱状态和质量检查由仓库数据与 CI 管理。

## 本地开发

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
make check
make serve
```

常用命令：

```bash
make serve    # 本地预览
make build    # 严格构建站点
make check    # 运行全部质量检查
make format   # 规范化参考来源 Markdown 链接
```

## CI / CD

Pull Request 和 `main` 分支提交都会运行质量门禁，包括：

- Markdown 引用格式检查；
- Concept Graph 节点 / 边 / 路径一致性检查；
- 禁止临时版本号和占位文案进入公开内容；
- `mkdocs build --strict`。

只有构建通过的 `main` 内容才应发布到 GitHub Pages。

## 贡献

- [贡献指南](docs/contributing.md)
- [项目原则](docs/reference/project-principles.md)
- [词条模板](docs/reference/term-template.md)
- [引用与链接规范](docs/reference/citation-style.md)
- [工程说明](docs/reference/engineering.md)

# Agent Atlas

> **Don't just define the term. Locate it.**  
> **不只解释这个词，还告诉你它在整个 Agent 世界的哪里。**

Agent Atlas 是一个面向 Agent / Agentic AI 学习者与实践者的 **Agent Engineering 语境型概念地图（Contextual Concept Atlas）**。

它不追求成为最大的 A–Z 术语表，也不重复已有的 Agent 课程、Awesome List 或 Pattern Encyclopedia。它更关注：当你在书、论文、GitHub、技术博客或 SDK 文档里突然遇到一个陌生术语时，怎样快速理解它，并把它放回完整的 Agent Engineering 心智模型中。

**当前阶段：v0.2 · 从 Glossary 升级为 Contextual Concept Atlas**

## 在线阅读

https://wanxiao2018.github.io/agent-atlas/

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

## 四个核心模块

- **Contextual Glossary**：不只解释定义，还解释真实使用语境。
- **Concept Graph**：记录概念之间的包含、依赖、使用、对比与演化关系。
- **Terminology Observatory**：区分稳定术语、演化中的术语和新兴 / 争议说法。
- **Concept Boundaries**：系统讲清 Harness vs Framework、Context vs Memory 等高频混淆。

## Atlas-quality

Agent Atlas 不以术语数量作为主要 KPI。

一个词只有基础定义时标记为 **🚧 Stub**；具备定义、语境、关系、边界和可靠来源后，才进入 **✅ Atlas-quality**。

更值得积累的是：

- 真正讲透的核心概念
- Concept Graph 关系
- 易混淆概念对
- 真实技术原文语境
- 一手资料来源

## 本地预览

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
mkdocs serve
```

然后打开 `http://127.0.0.1:8000`。

## 自动发布

仓库包含 `.github/workflows/pages.yml`。推送到 `main` 后，GitHub Actions 会构建 MkDocs 站点并通过 GitHub Pages 发布。

仓库 Pages 已配置为 **GitHub Actions** 发布模式。

## 项目原则

详细设计原则见：`docs/reference/project-principles.md`。

词条统一模板见：`docs/reference/term-template.md`。

## License

内容许可方案待确定。在正式开放外部贡献前补充 LICENSE。

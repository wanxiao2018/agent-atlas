# Agent Atlas

Agent / Agentic AI 中文概念地图与入门词典。

目标不是做中英翻译表，而是帮助读者建立 **概念关系、工程直觉与学习路线**。

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

首次使用时，在仓库 **Settings → Pages → Build and deployment → Source** 中选择 **GitHub Actions**。

预期地址：`https://wanxiao2018.github.io/agent-atlas/`

## 内容结构

- 基础层
- Agent 核心机制
- Agent 基础设施
- 工具系统
- 上下文与记忆
- Multi-agent
- 可靠性与评测
- Harness / Loop Engineering
- Coding Agent

## License

内容许可方案待确定。在正式开放外部贡献前补充 LICENSE。

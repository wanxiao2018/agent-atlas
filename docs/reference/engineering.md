# 工程说明

Agent Atlas 按长期维护的知识工程项目设计，而不是把开发过程直接暴露给读者。

## 产品面与开发面分离

**产品面**是 GitHub Pages 上的内容。它只描述当前成立、当前可用的知识，不使用：

- “这个页面以后会补充……”之类占位文案；
- “当前是某个临时 v0.x 阶段”之类开发阶段标签；
- 为了凑数量而公开大量模板化空页面。

**开发面**位于仓库内部，包括 Concept Graph 状态、Issue / PR、CI 结果和内容质量元数据。未完成工作应在这里管理，而不是写给最终读者看。

## 单一数据源

Agent Atlas 有三类核心源文件：

```text
docs/**/*.md                    # 知识内容

docs/data/concept-graph.json   # 概念节点与关系

mkdocs.yml                     # 站点信息架构
```

页面负责解释；Concept Graph 负责结构化关系；MkDocs 负责导航和渲染。三者通过 CI 做一致性校验。

## 内容生命周期

内容成熟度可以在仓库数据中使用：

```text
planned → stub → developing → atlas-quality
```

这些状态是**工程元数据**，用于排期、检查和统计；它们不应该变成“以后再写”的公开占位句。

一个简短词条可以是合法内容，只要它准确、自洽且没有伪装成已经完成的深度词条。核心词则应逐步达到 Atlas-quality 标准。

## 质量门禁

CI 在 Pull Request 和 `main` 上检查：

1. **引用格式**：参考来源不使用裸 URL；
2. **公开文案**：拒绝临时 `v0.x`、旧占位句和明显开发过程文本；
3. **Concept Graph**：节点 ID 唯一、边的端点存在、页面路径有效；
4. **站点构建**：`mkdocs build --strict` 必须通过。

本地运行：

```bash
make check
```

## 自动格式化与 CI 的职责

`scripts/normalize_markdown_links.py` 提供本地自动格式化能力：

```bash
make format
```

CI 只负责**检查**，不会自动向 `main` 写回内容。这样任何生产内容变化都来自明确的提交，而不是机器人在后台静默改仓库。

## 发布策略

`main` 表示线上站点的最新稳定内容。GitHub Pages 从 `main` 自动构建发布。

项目不会在页面中使用临时 `v0.x` 表达“现在做到哪一步”。当未来确实需要对外发布稳定里程碑时，再使用 Git tag / GitHub Release 和明确的发布说明；内容页面本身保持面向概念，而不是面向开发阶段。

## 变更流程

推荐流程：

```text
Issue / Research
      ↓
修改 Markdown / Graph data
      ↓
本地 make check
      ↓
Pull Request
      ↓
CI Quality Gate
      ↓
Review
      ↓
merge main
      ↓
GitHub Pages deploy
```

个人维护阶段允许直接提交 `main`，但同样必须经过 CI；随着外部贡献增加，应逐步使用分支保护和 Required Checks。

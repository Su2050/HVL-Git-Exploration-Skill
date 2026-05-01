# 12 — 参考资料

这份项目包主要是一个工程方法论模板，不依赖某一个特定工具。但以下官方或较权威资料可以帮助理解为什么它采用 `AGENTS.md`、`SKILL.md`、Cursor Rules、Git 状态管理和实验追踪工具。

## AI 编程工具规则与技能

- OpenAI Developers — Custom instructions with `AGENTS.md`  
  说明 Codex 如何发现和读取 `AGENTS.md`，以及如何用全局/项目级指令给 Codex 提供稳定工作上下文。  
  https://developers.openai.com/codex/guides/agents-md

- OpenAI Developers — Agent Skills  
  说明 Codex Skill 的结构：`SKILL.md`、可选脚本、引用资料、资源等。  
  https://developers.openai.com/codex/skills

- Cursor — Best practices for coding with agents  
  说明 Cursor 中 rules、skills、项目上下文、验证命令和 Git 共享规则的重要性。  
  https://cursor.com/blog/agent-best-practices

## Git 状态管理

- Git Documentation — git-worktree  
  说明一个 Git 仓库可以支持多个 working tree，适合并行探索多个分支或方案。  
  https://git-scm.com/docs/git-worktree

- Git Documentation — git-restore  
  说明如何从指定来源恢复 working tree 或 index 内容，适合进行局部回退。  
  https://git-scm.com/docs/git-restore

## 机器学习/Agent 实验追踪

- MLflow Documentation  
  提供机器学习、LLM 和 Agent 工作流的实验追踪、评估、优化、部署等能力说明。  
  https://mlflow.org/docs/latest/

## 使用说明

这些资料不是要求团队必须使用 Codex、Cursor、MLflow 或某个特定 Git 命令。它们的作用是提供“外部状态、持久化规则、实验追踪、可回退工程实践”的背景依据。

HVL-Git 的核心思想可以迁移到其他工具：只要工具能读写文件、运行验证命令、使用 Git、保存实验记录，就可以使用这套协议。

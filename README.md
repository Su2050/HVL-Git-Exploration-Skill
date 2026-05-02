# HVL Git Exploration Skill

中文 | [English](#english)

## 中文

HVL Git Exploration 是一个 Codex Skill，用于处理没有现成标准答案、需要先借鉴全球前人研究，再通过假设、实验、验证证据和回退逐步逼近答案的复杂探索任务。

它适合科研型工程、复杂 Debug、性能优化、ML/RL 实验、机器人、仿真、AutoML、元学习，以及长时间 AI 编程任务。

## 它提供什么

- Hypothesis Verification Loop 假设验证闭环。
- Prior-art scouting：检索论文、官方文档、开源实现、benchmark、技术博客、issue 和相邻领域经验。
- `.agent/source-ledger.md`、`.agent/prior-art-map.md`、`.agent/hypothesis-backlog.md` 研究记忆。
- Git checkpoint 和实验分支。
- `.agent/*` 持久化推理记忆。
- 基于验证证据的实验记录。
- 失败后先分类，再决定重试、换方案、拆分或回退。
- sibling experiment 之间的 dirty worktree 防混入保护。
- Persistence contract：持续推进，直到成功标准满足或遇到真实停止条件。

## 仓库结构

```text
SKILL.md                 # Codex skill 入口
agents/openai.yaml       # 可选 Codex UI 元数据
scripts/hvl.py           # init/start/record/checkpoint/backtrack/status 辅助命令
references/              # 详细协议文档和模板
```

## 安装

复制或软链接到 Codex skills 目录：

```bash
mkdir -p ~/.codex/skills
cp -R hvl-git-exploration ~/.codex/skills/
```

在 Codex 中调用：

```text
Use $hvl-git-exploration for this task.
```

## 辅助命令

初始化项目：

```bash
python3 ~/.codex/skills/hvl-git-exploration/scripts/hvl.py init
```

记录一个前人研究来源：

```bash
python3 ~/.codex/skills/hvl-git-exploration/scripts/hvl.py source \
  --title "Paper or repo title" \
  --type paper \
  --priority P0 \
  --url "https://example.com" \
  --takeaway "Core reusable idea" \
  --confidence high \
  --relevance "Why it matters for this task"
```

把前人方法转成候选假设：

```bash
python3 ~/.codex/skills/hvl-git-exploration/scripts/hvl.py prior-art \
  --method "Baseline method" \
  --problem "Closest solved problem" \
  --idea "Core idea" \
  --evidence "Reported benchmark or reproduction" \
  --confidence medium \
  --adaptation "How to adapt locally" \
  --risk "What may not transfer" \
  --hypothesis "Adapting this baseline improves the target metric"
```

开始一个实验分支：

```bash
python3 ~/.codex/skills/hvl-git-exploration/scripts/hvl.py start \
  --node N1 \
  --title "Probe root cause" \
  --hypothesis "The failure is caused by stale cache state" \
  --validation "pytest tests/cache"
```

记录并提交一个实验：

```bash
python3 ~/.codex/skills/hvl-git-exploration/scripts/hvl.py record \
  --node N1 \
  --hypothesis "The failure is caused by stale cache state" \
  --changes "Added cache invalidation at refresh boundary" \
  --validation "pytest tests/cache" \
  --result pass \
  --failure-classification N/A \
  --reflection "Evidence supports the hypothesis" \
  --next "Integrate or test sibling edge cases" \
  --update-handoff \
  --commit --all \
  -m "experiment: N1 cache hypothesis passed"
```

## 安全说明

`hvl.py` 不会 push、merge、reset 或 rebase。只有显式运行命令时，它才会创建本地 Git 状态。

在开始 sibling experiment 前，如果工作区有未提交改动，`hvl.py start` 默认会拒绝继续，除非显式使用 `--checkpoint-before` 或 `--allow-dirty`。

## 许可证

MIT

---

## English

HVL Git Exploration is a Codex Skill for complex exploratory work where there is no fixed answer and progress must come from global prior art, hypotheses, experiments, validation evidence, and deliberate backtracking.

It is designed for research-like engineering tasks, complex debugging, performance work, ML/RL experiments, robotics, simulation, AutoML, meta-learning, and long-running AI coding sessions.

## What It Adds

- Hypothesis Verification Loop workflow.
- Prior-art scouting across papers, official docs, open-source implementations, benchmarks, technical blogs, issues, and adjacent domains.
- Research memory files: `.agent/source-ledger.md`, `.agent/prior-art-map.md`, and `.agent/hypothesis-backlog.md`.
- Git checkpoints and experiment branches.
- Persistent `.agent/*` reasoning files.
- Validation-driven experiment records.
- Failure classification before retrying.
- Dirty-worktree guards between sibling experiments.
- Persistence contract: continue until success criteria are met or a real stop condition is reached.

## Repository Layout

```text
SKILL.md                 # Codex skill entrypoint
agents/openai.yaml       # Optional Codex UI metadata
scripts/hvl.py           # Helper CLI for init/start/record/checkpoint/backtrack/status
references/              # Detailed protocol docs and templates
```

## Install

Copy or symlink this directory into your Codex skills folder:

```bash
mkdir -p ~/.codex/skills
cp -R hvl-git-exploration ~/.codex/skills/
```

Then invoke it in Codex:

```text
Use $hvl-git-exploration for this task.
```

## Helper CLI

Initialize a project for HVL-Git:

```bash
python3 ~/.codex/skills/hvl-git-exploration/scripts/hvl.py init
```

Record a prior-art source:

```bash
python3 ~/.codex/skills/hvl-git-exploration/scripts/hvl.py source \
  --title "Paper or repo title" \
  --type paper \
  --priority P0 \
  --url "https://example.com" \
  --takeaway "Core reusable idea" \
  --confidence high \
  --relevance "Why it matters for this task"
```

Convert a prior-art method into a candidate hypothesis:

```bash
python3 ~/.codex/skills/hvl-git-exploration/scripts/hvl.py prior-art \
  --method "Baseline method" \
  --problem "Closest solved problem" \
  --idea "Core idea" \
  --evidence "Reported benchmark or reproduction" \
  --confidence medium \
  --adaptation "How to adapt locally" \
  --risk "What may not transfer" \
  --hypothesis "Adapting this baseline improves the target metric"
```

Start an experiment branch:

```bash
python3 ~/.codex/skills/hvl-git-exploration/scripts/hvl.py start \
  --node N1 \
  --title "Probe root cause" \
  --hypothesis "The failure is caused by stale cache state" \
  --validation "pytest tests/cache"
```

Record and commit an experiment:

```bash
python3 ~/.codex/skills/hvl-git-exploration/scripts/hvl.py record \
  --node N1 \
  --hypothesis "The failure is caused by stale cache state" \
  --changes "Added cache invalidation at refresh boundary" \
  --validation "pytest tests/cache" \
  --result pass \
  --failure-classification N/A \
  --reflection "Evidence supports the hypothesis" \
  --next "Integrate or test sibling edge cases" \
  --update-handoff \
  --commit --all \
  -m "experiment: N1 cache hypothesis passed"
```

## Safety Notes

The helper does not push, merge, reset, or rebase. It creates local Git state only when explicitly invoked.

Before starting a sibling experiment, `hvl.py start` refuses to continue from a dirty worktree unless `--checkpoint-before` or `--allow-dirty` is explicit.

## License

MIT

# 从这里开始

这是一套给 AI 编程工具、科研型项目、强化学习/机器人训练、元学习和复杂系统研发使用的「专家式探索协议」项目包。

它要解决的问题不是“让 AI 更努力写代码”，而是：

> 当 AI 面对复杂目标、多个方案、连续失败、上下文压缩和多人协作时，如何像优秀专家一样：先提出假设，再做最小实验，用证据判断，失败后回到正确决策节点，而不是盲目乱试。

核心思想一句话：

> **Git 负责可回退，`.agent/*` 文档负责可理解，测试/日志/运行结果负责可验证。**

## 先判断：这个任务适不适合用它

这套系统最适合：科学研究、强化学习训练、机器人/具身智能、元学习、复杂系统、复杂 Debug、性能优化、多方案技术探索。

判断标准很简单：**没有现成标准答案，但可以通过实验和证据逐步逼近答案。**

详细说明先看：

```text
docs/00-formal-introduction.md
docs/11-rl-meta-research-guide.md
.agent/project-fit.md
```

## 最快使用方式

把整个目录放到你的项目根目录，然后执行：

```bash
python3 scripts/hvl.py init
```

如果你更喜欢 shell：

```bash
bash scripts/setup-git.sh
```

然后对 Codex / Cursor / Claude Code / 其他 AI 编程工具说：

```text
Read AGENTS.md and follow the HVL Git State Machine protocol.
For this task, use .agent/* files to record assumptions, decisions, experiments, validation results, and handoff notes.
Use Git branches and commits as external checkpoints. Do not blindly continue after failure.
```

## 这个项目包包含什么

```text
AGENTS.md                                      # 给 Codex / 通用 Agent 的总规则
.cursor/rules/hvl-git-state-machine.mdc       # 给 Cursor 的规则
.agents/skills/hvl-git-state-machine/SKILL.md # 给支持 Skills 的 Agent 使用
.agent/*                                      # 计划、假设、实验、交接、适配性判断等状态文件模板
docs/*                                        # 正式介绍、适用范围、方法论、Git 工作流、科研/RL/元学习指南
templates/*                                   # 可复制的提示词、commit 模板、实验记录模板
scripts/hvl.py                                # 可执行辅助脚本：init/start/record/checkpoint/backtrack/status
.githooks/*                                   # Git hooks：提醒 AI 记录实验和使用结构化 commit
examples/*                                    # 复杂任务示例：RL 自动插取/叉取、元学习等
```

## 最小闭环

1. 明确目标和成功标准。
2. 判断任务是否需要轻量版、标准版或科研版 HVL-Git。
3. 把方案写成假设。
4. 为当前假设开独立分支或建立 checkpoint。
5. 如果是多因素任务，先列因素并优先做单因素验证。
6. 做一个小实验。
7. 运行验证命令或收集实验证据。
8. 记录证据和反思。
9. 决定继续、重试、换方案，还是退回上一个节点。

不要追求一开始就写得完美。真正有价值的是：**每一次失败都能留下可追溯证据。**

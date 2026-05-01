# AI 专家式探索 × Git 外部状态机协议

## 1. 它是什么

这是一套给 AI 编程工具、科研型项目和复杂系统研发使用的工作协议，适合 Codex、Cursor、Claude Code、Devin 类工具，也适合团队把复杂研发、强化学习训练、元学习实验、AIoT 系统排障等任务交给 AI 协作时使用。

它可以叫：

- 中文：**假设验证回退协议**
- 中文加强版：**AI 专家式探索协议**
- 英文：**Hypothesis Verification Loop**，简称 **HVL**
- 加入 Git 后：**HVL Git State Machine**

它不是单纯的 prompt，也不是单纯的规则，而是三件东西的组合：

1. **规则 Rule**：告诉 AI 遇到复杂问题时必须怎么行动。
2. **技能/流程 Skill / Workflow**：定义“假设—实验—验证—反思—回退”的执行步骤。
3. **状态系统 State System**：用 `.agent/*` 和 Git 持久化保存推理轨迹、实验结果和回退点。

## 2. 它解决什么问题

现在 AI 编程工具解决简单问题很强，但解决复杂目标时常见三类失控：

1. **失败后乱试**：一个 patch 不行，就继续堆另一个 patch，最后问题被越改越乱。
2. **上下文丢失**：上下文压缩、模型切换、任务中断后，AI 忘记为什么走到这里。
3. **不可复盘**：代码改了很多，但没人知道哪些方案试过、为什么失败、哪个假设被证伪。

这个协议把复杂问题变成一棵可追踪的决策树：

```text
目标
 ├─ 决策节点 1
 │   ├─ 假设 A → 实验 → 验证失败 → 判断：执行问题 / 假设问题 / 前置条件问题
 │   └─ 假设 B → 实验 → 验证通过 → 进入下一节点
 └─ 决策节点 2
     ├─ 子假设 C1
     └─ 子假设 C2
```

## 3. Git 在这里不是辅助工具，而是外部状态机

推荐理解方式：

```text
.agent/* 文件：记录为什么这样做
Git：记录做了什么、改了哪里、能不能回去
测试/日志/运行结果：判断当前假设是否成立
```

也就是：

> **Git 负责“可回退”；文档负责“可理解”；验证负责“可判断”。**

## 4. 适用场景

特别适合：

- 科学研究与工程研究
- 强化学习训练、机器人控制、自动插取/叉取、仿真实验
- 元学习、AutoML、没有标准答案的算法探索
- 大型重构、复杂 bug 定位、架构迁移
- 性能优化、稳定性治理、复杂系统根因分析
- AIoT、视频分析、云边协同、多模块系统研发
- 长时间 AI 编程任务
- 多人/多 Agent 接力开发
- 需要可复盘的研发探索任务

最核心的判断标准：

> 没有现成标准答案，但可以通过实验、日志、训练曲线、仿真、测试或人工验收一步步逼近答案。

不适合：

- 一两行小改动
- 已有成熟做法且风险很低的实现任务
- 没有任何验证手段的纯猜测任务
- 目标和成功标准完全不清楚的任务
- 流程成本明显高于收益的低价值任务

更完整的适用范围见：`docs/00-formal-introduction.md` 和 `docs/11-rl-meta-research-guide.md`。

## 5. 推荐目录结构

```text
.agent/
  project-fit.md        # 判断是否适合启用 HVL-Git，以及启用轻量版/标准版/科研版
  current-plan.md       # 当前目标、阶段、成功标准、下一步
  decision-tree.md      # 决策节点、父子关系、方案分支
  assumptions.md        # 显式假设和子假设
  experiment-log.md     # 每次尝试、验证结果、反思
  validation.md         # 验证命令、测试、日志、人工检查标准
  handoff.md            # 任务中断/上下文压缩后的交接摘要
  risk-register.md      # 风险、代价、可能失败点

Git:
  main
  hvl/N1-baseline
  hvl/N2-hypothesis-a
  hvl/N2-hypothesis-b
  hvl/N3-final-integration
```

## 6. 给 AI 的一句话

```text
Treat every solution as a hypothesis. Use Git as the external state machine. Use .agent/* as the reasoning memory. Use tests/logs/runtime evidence as validation. Never blindly continue after failure.
```

科研/训练任务可以加一句：

```text
For ML/RL/research tasks, use Git branches for conceptual hypotheses and experiment trackers for concrete training runs, seeds, metrics, curves, logs, and artifacts.
```

## 7. 能力边界

这套协议不能保证 AI 一定解决所有复杂问题。它真正能提高的是：

- 不容易跑偏；
- 失败后知道退到哪里；
- 后续的人或 AI 能看懂之前为什么这么做；
- 能区分“方案本身错了”和“执行方式错了”；
- 能把复杂问题切成一组可验证的假设；
- 能把失败实验变成后续决策的证据。

效果依赖三个条件：

1. 有相对清楚的目标和成功标准。
2. 有可运行的验证手段，比如测试、日志、类型检查、benchmark、训练指标、仿真结果、人工验收标准。
3. AI 有权限读取和写入 `.agent/*`，并能正常使用 Git。

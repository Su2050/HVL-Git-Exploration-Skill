# 11 — 强化学习、元学习与科研型项目使用指南

## 1. 为什么这类项目特别需要 HVL-Git

强化学习、机器人训练、元学习和科研型算法项目，往往没有一个可以直接照抄的标准答案。

这类项目失败时，最危险的不是“失败”，而是：

> 失败以后不知道失败在哪一层，于是不断换参数、换模型、换代码，最后连自己试过什么都说不清。

HVL-Git 的作用是把探索变成一棵可回退、可复盘、可接力的决策树。

## 2. Git 分支和训练实验不要混用

在算法训练项目里，最重要的一条原则是：

> Git 分支对应“概念假设”，训练 run 对应“具体实验”。

错误做法：

```text
每个 seed 建一个 Git 分支
每个学习率建一个 Git 分支
每次训练失败就直接改代码重新训
```

推荐做法：

```text
Git branch: hvl/N2-reward-shaping-sparse-to-dense
  Run 001: seed=1, lr=3e-4, steps=1M
  Run 002: seed=2, lr=3e-4, steps=1M
  Run 003: seed=3, lr=1e-4, steps=1M

Git branch: hvl/N3-observation-add-pose-error
  Run 004: seed=1, lr=3e-4, steps=1M
  Run 005: seed=2, lr=3e-4, steps=1M
```

这样 Git 负责代码与概念变化，实验平台负责参数、曲线、指标和 artifact。

## 3. 强化学习自动插取/叉取任务模板

### 3.1 根目标

```text
让策略在给定环境约束下，稳定完成自动插取/叉取任务，并满足成功率、安全性、效率和可迁移性要求。
```

### 3.2 推荐决策节点

```text
N0：目标与成功标准
N1：任务环境与物理约束
N2：奖励函数
N3：观测空间
N4：动作空间
N5：训练算法与超参数
N6：仿真随机化与场景覆盖
N7：评估协议
N8：失败模式分析
N9：sim-to-real 迁移
N10：部署安全边界
```

### 3.3 奖励函数节点示例

```text
Node: N2 — 奖励函数是否能引导正确插取？

H2-A：奖励过于稀疏，导致策略无法学会接近与对准过程。
H2-B：距离奖励权重过高，导致策略只接近但不完成插入。
H2-C：缺少碰撞惩罚，导致策略产生不可部署动作。
H2-D：成功奖励定义过宽，导致策略利用指标漏洞。
H2-E：阶段奖励缺少连续性，导致策略在关键过渡处不稳定。
```

### 3.4 每次训练必须记录

```text
- Hypothesis ID:
- Git branch:
- Git commit:
- Environment version:
- Simulator version:
- Dataset / scenario version:
- Reward config:
- Observation space:
- Action space:
- Algorithm:
- Hyperparameters:
- Seeds:
- Training steps:
- Evaluation episodes:
- Success rate:
- Collision rate:
- Timeout rate:
- Average completion time:
- Failure mode distribution:
- Representative videos/logs:
- Result: pass / fail / inconclusive
- Reflection:
- Next decision:
```

### 3.5 失败分类示例

```text
训练曲线上升但评估失败：可能是评估分布不同，或训练奖励被投机利用。
成功率高但碰撞多：可能是奖励没有惩罚危险动作，或成功标准过宽。
不同 seed 差异很大：可能是训练不稳定，不能证明假设成立。
仿真成功但真实失败：可能是 sim-to-real gap 或传感器误差未覆盖。
策略卡在局部动作：可能是动作空间、探索策略或奖励阶段设计问题。
```

## 4. 元学习项目模板

### 4.1 根目标

```text
验证某个元学习方法是否能在目标任务分布上，以更少样本、更少更新步数或更低成本实现更好的适应能力。
```

### 4.2 推荐决策节点

```text
N0：元学习目标定义
N1：任务分布设计
N2：训练/测试任务划分
N3：baseline 选择
N4：inner loop 设计
N5：outer loop 目标
N6：模型表征
N7：优化稳定性
N8：评估协议
N9：消融实验
N10：泛化边界
```

### 4.3 常见假设

```text
H1：当前效果差是因为训练任务分布与测试任务分布不一致。
H2：提升来自更大的模型容量，而不是元学习机制本身。
H3：inner loop 步数不足，导致快速适应能力没有体现。
H4：outer loop 目标和最终评估指标不一致。
H5：baseline 太弱，导致方法优势被高估。
H6：评估存在任务泄漏或数据泄漏。
H7：模型学到的是任务 ID 或表面特征，而不是可迁移表征。
```

### 4.4 元学习项目的核心验证

```text
- 是否有强 baseline；
- 是否有相同参数量或相同计算预算的对照；
- 是否有不同任务分布下的评估；
- 是否有消融实验解释增益来源；
- 是否区分快速适应、泛化、记忆和过拟合；
- 是否记录每次实验的 seed、任务采样、评估协议和统计置信度。
```

## 5. 科研型项目的最低要求

科研型项目至少要做到：

1. 每个结论都有对应实验；
2. 每个实验都有明确假设；
3. 每个失败都有分类；
4. 每个重要版本都能回到 Git checkpoint；
5. 每个结论都能追到数据、代码、参数、环境和日志；
6. 每个“提升”都要问：是机制提升，还是实现细节、数据、评估或随机性造成的。

## 6. 给 AI 的科研型任务提示词

```text
Use HVL-Git for this research task.

This is not a one-shot implementation task. Treat the goal as a research problem.
Before changing code, define:
1. the research question;
2. the current decision node;
3. the active hypothesis and sub-hypotheses;
4. the validation signal;
5. the Git branch/checkpoint strategy;
6. the experiment tracking fields.

For every experiment, record:
- hypothesis;
- code/config changes;
- environment and data version;
- training/evaluation command;
- metrics and artifacts;
- result;
- failure classification;
- reflection;
- next decision.

If the result fails or is ambiguous, do not blindly tune parameters. Decide whether to retry implementation, redesign validation, switch hypothesis, split the node, or backtrack.
```

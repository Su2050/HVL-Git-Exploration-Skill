# 08 — 提示词库

## 1. 启动复杂任务

```text
Read AGENTS.md and use the HVL Git State Machine protocol.

Before coding:
1. inspect git status;
2. update .agent/current-plan.md;
3. create or update .agent/decision-tree.md;
4. define validation in .agent/validation.md;
5. create a checkpoint if the current state is stable.

Treat every proposed solution as a hypothesis. Use dedicated branches or commits for each major hypothesis. Record experiments in .agent/experiment-log.md and update .agent/handoff.md before stopping.
```

## 2. 让 AI 先拆假设，不要直接写代码

```text
Do not code yet.
First convert this task into a decision tree:
- root goal;
- main decision nodes;
- candidate hypotheses at each node;
- validation signal for each hypothesis;
- what evidence must return to the node before we retry, switch hypothesis, split, advance, or backtrack.
Write the result to .agent/decision-tree.md and .agent/assumptions.md.
```

## 3. 失败后强制分类

```text
The last attempt failed.
Before changing code again, classify the failure:
- measurement error;
- execution error;
- wrong hypothesis;
- missing prerequisite;
- invalid validation method;
- unrelated regression;
- factor confounding;
- ambiguous evidence;
- randomness or insufficient statistical confidence;
- simulation-real gap.

Use git diff, logs, tests, and .agent/experiment-log.md as evidence. Then return the evidence to the decision node and decide whether to retry this node, switch to a sibling hypothesis, split the problem, advance, or backtrack to the parent checkpoint.
```

## 3.1 多因素实验先隔离再组合

```text
This is a multi-factor task.
Before running combination experiments:
- list the plausible factors;
- choose the single factor under test;
- state which factors are held stable;
- define the single-factor baseline;
- only combine factors after the relevant single-factor effects are validated.
If attribution is unclear because multiple factors changed together, classify the result as factor_confounding and split the node.
```

## 4. 让 AI 使用 Git 分支探索多个方案

```text
Use Git as the external state machine.
Create one branch per major hypothesis using hvl/<node-id>-<slug>.
Do not mix unrelated hypotheses in the same branch.
After each experiment, record the result in .agent/experiment-log.md and commit with a structured message including Hypothesis, Change, Validation, Result, Reflection, and Next.
```

## 5. 交接给另一个 AI

```text
Update .agent/handoff.md so another AI can continue without reading this chat.
Include:
- current branch;
- current decision node;
- last good checkpoint;
- validated facts;
- failed hypotheses;
- active hypothesis;
- commands already run;
- next concrete step;
- known risks.
```

## 6. 让 AI 复盘历史实验

```text
Read .agent/experiment-log.md, .agent/decision-tree.md, and git log.
Summarize:
1. what has been tried;
2. what evidence each attempt produced;
3. which hypotheses are still alive;
4. which hypotheses should not be retried;
5. the next highest-leverage experiment.
```

## 7. Cursor 使用提示

```text
Use the project rules in .cursor/rules/hvl-git-state-machine.mdc.
Before editing, show me the current decision node and hypothesis.
After editing, run the validation command and update .agent/experiment-log.md.
If validation fails, do not continue coding until you classify the failure.
```

## 8. Codex 使用提示

```text
Read AGENTS.md and follow it strictly.
Use .agent/* files as persistent task memory.
Use Git checkpoints and hvl/* branches for exploration.
A solution is not complete until the validation evidence and handoff summary are recorded.
```

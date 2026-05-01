# 06 — 团队落地指南

## 适合团队怎么用

这套协议不应该一上来就变成重流程。最小落地方式是：

1. 复杂任务必须有 `.agent/current-plan.md`。
2. 失败实验必须写入 `.agent/experiment-log.md`。
3. 高风险改动必须先有 Git checkpoint。
4. 每个独立假设必须有独立分支或独立 commit。
5. 交接前必须更新 `.agent/handoff.md`。

## 对研发负责人的价值

它让你能看清：

- AI 到底试过什么；
- 哪些方案不是没想到，而是已被证伪；
- 当前卡点是工程执行问题，还是问题定义问题；
- 哪些验证手段缺失；
- 是否应该继续让 AI 探索，还是应该人介入。

## 对工程师的价值

它减少三件痛苦：

1. 接手 AI 改过的烂摊子；
2. 不知道为什么改成这样；
3. 重复尝试已经失败过的方案。

## 对 AI 的价值

AI 不再只靠上下文记忆，而是有一个外部状态系统。

即使上下文压缩，它也能从以下信息恢复：

- Git 分支和 commit；
- `.agent/current-plan.md`；
- `.agent/decision-tree.md`；
- `.agent/experiment-log.md`；
- `.agent/handoff.md`。

## 团队规则建议

### 轻量版

只要求：

```text
.agent/current-plan.md
.agent/experiment-log.md
.agent/handoff.md
```

### 标准版

要求：

```text
.agent/current-plan.md
.agent/decision-tree.md
.agent/assumptions.md
.agent/experiment-log.md
.agent/validation.md
.agent/handoff.md
```

### 严格版

额外要求：

- 每个假设独立分支；
- 每个 commit 使用结构化模板；
- PR 里说明被证伪的方案；
- 合并前必须有验证证据；
- 失败分支至少保留到复盘结束。

## 不要过度流程化

这个协议的目标不是制造文档负担，而是防止复杂探索失控。

如果是小任务，不需要完整流程。

判断标准很简单：

> 如果失败后你需要知道“刚才到底为什么那么做”，就应该用 HVL。

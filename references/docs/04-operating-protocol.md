# 04 — 操作协议

## 0. 触发条件

遇到以下情况，应进入 HVL 模式：

- 任务超过 3 个步骤；
- 可能有多个方案；
- 需要 debug；
- 涉及大改动；
- 失败成本高；
- 上下文可能压缩；
- 多人或多 Agent 接力；
- 需要把探索过程交给团队复盘。

## 1. 开始前

```bash
git status
python3 scripts/hvl.py init
```

更新：

```text
.agent/current-plan.md
.agent/validation.md
```

必须明确：

- 目标是什么；
- 成功标准是什么；
- 当前验证命令是什么；
- 失败后允许怎么回退。

## 2. 建立基线

```bash
git add -A
git commit -m "checkpoint: stable baseline before <task>"
```

如果当前状态不稳定，也要在 `.agent/handoff.md` 里写明。

## 3. 建立决策节点

在 `.agent/decision-tree.md` 中写：

```text
Node ID: N1
Parent: N0
Question: Why does login timeout occur?
Candidate hypotheses:
  A. stale token refresh state
  B. request queue deadlock
  C. backend timeout configuration
Validation signal: reproduce timeout and inspect logs
Exit condition: root cause identified with evidence
```

## 4. 选择一个假设并开分支

```bash
git checkout -b hvl/N1-token-refresh
```

或者使用脚本：

```bash
python3 scripts/hvl.py start --node N1 --title "Token refresh hypothesis" --hypothesis "Login timeout is caused by stale token refresh state"
```

## 5. 做最小实验

只做能验证当前假设的最小改动。

不要顺手做重构、优化、清理、换依赖。

## 6. 验证

```bash
# examples
npm test
pytest
make test
```

记录：

- 命令；
- 输出摘要；
- 是否复现；
- 是否通过；
- 有没有新问题。

多因素系统还要记录：

- 可能影响结果的因素清单；
- 本次实验正在验证的单一因素；
- 保持不变的控制因素；
- 本次改变的因素；
- 如果是组合实验，它对应哪些已验证的单因素基线。

优先先做单因素主效应验证，再做组合实验。只有当组合结果能追溯到对应单因素基线时，组合实验才有清晰归因价值。

## 7. 记录实验

```bash
python3 scripts/hvl.py record \
  --node N1 \
  --hypothesis "Login timeout is caused by stale token refresh state" \
  --changes "Reset refresh state after retry" \
  --validation "npm test auth.spec.ts" \
  --result fail \
  --reflection "Timeout still occurs; token refresh is probably not root cause" \
  --next "Backtrack to N1 and test request queue hypothesis"
```

## 8. 回到节点复议

实验结果不是让探索线性往前走，而是作为证据回到当前决策节点重新判断。

```bash
python3 scripts/hvl.py reconsider \
  --node N1 \
  --from-experiment E1 \
  --returned-evidence "Token refresh fix did not remove the timeout" \
  --interpretation "The refresh-state hypothesis is contradicted; request queue remains plausible" \
  --decision switch_sibling \
  --continue-to "N1 sibling: request queue hypothesis" \
  --next "Start a sibling branch for the request queue hypothesis"
```

复议时至少回答：

- 返回节点的证据是什么；
- 这个证据如何改变当前节点判断；
- 是重试当前假设、换兄弟假设、拆节点、修验证、前进，还是回退；
- 下一步进入哪个节点、分支、checkpoint 或阻塞状态。

## 9. 失败后分类

失败必须分类，不允许直接继续乱改。

```text
measurement_error
execution_error
wrong_hypothesis
missing_prerequisite
invalid_validation
unrelated_regression
factor_confounding
ambiguous_evidence
randomness_or_low_confidence
simulation_real_gap
```

## 10. 决策

| 失败类型 | 下一步 |
|---|---|
| measurement_error | 修复或隔离测量层，重新运行最小验证 |
| execution_error | 当前假设可能对，修正实现后重试 |
| wrong_hypothesis | 放弃该假设，切换兄弟分支 |
| missing_prerequisite | 先解决前置条件或标记阻塞 |
| invalid_validation | 重写验证方式 |
| unrelated_regression | 隔离回归，不把它混进当前假设 |
| factor_confounding | 回到最近的单因素基线，拆分因素后重新验证 |
| ambiguous_evidence | 拆成更小的子假设 |
| randomness_or_low_confidence | 增强统计设计或重复关键实验 |
| simulation_real_gap | 回到环境建模或迁移验证节点 |

## 11. 交接

每次自然暂停时更新：

```text
.agent/handoff.md
```

交接文件的目标：

> 另一个 AI 或人不看聊天记录，只看 Git 和 `.agent/*`，也能继续。

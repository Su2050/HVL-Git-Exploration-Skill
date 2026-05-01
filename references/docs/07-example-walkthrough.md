# 07 — 示例：复杂 bug 的探索过程

假设任务：登录接口偶发超时。

## Step 0 — 建立目标

`.agent/current-plan.md`：

```text
Target outcome: Identify and fix intermittent login timeout.
Success criteria:
1. timeout reproduction case no longer fails;
2. auth tests pass;
3. logs show request lifecycle completes;
4. no regression in token refresh flow.
```

## Step 1 — 建立基线

```bash
git status
git add -A
git commit -m "checkpoint: stable baseline before login timeout investigation"
```

## Step 2 — 建立决策节点

`.agent/decision-tree.md`：

```text
Node ID: N1
Question: What causes intermittent login timeout?
Candidate hypotheses:
  A. stale token refresh state
  B. request queue deadlock
  C. backend timeout configuration
Validation signal: reproduce timeout with logs enabled
Exit condition: root cause identified with evidence
```

## Step 3 — 尝试假设 A

```bash
git checkout -b hvl/N1-token-refresh
```

假设：token refresh 状态未正确重置。

改动：在 401 retry 后重置 refresh state。

验证：

```bash
npm test auth.spec.ts
```

结果：失败，超时仍然发生。

实验记录：

```text
Result: fail
Failure classification: wrong_hypothesis or ambiguous_evidence
Reflection: refresh reset path executed, but timeout still occurs. Need inspect request queue.
Next: Backtrack to N1 and try request queue hypothesis.
```

## Step 4 — 切换兄弟假设 B

```bash
git checkout main
git checkout -b hvl/N1-request-queue
```

假设：请求队列存在 deadlock。

改动：加入队列生命周期日志，不改业务逻辑。

验证：复现超时时检查日志。

发现：某些请求进入队列后没有被释放。

结果：假设 B 得到支持。

## Step 5 — 拆子假设

```text
Node ID: N2
Parent: N1
Question: Why is request queue not released?
Candidate hypotheses:
  A. exception path misses finally
  B. cancellation path skips release
  C. duplicate request key overwrites handler
```

继续按同样流程探索。

## 这个例子的关键点

1. 假设 A 失败后，没有继续乱改 token refresh。
2. 失败被记录下来，后续不会重复踩坑。
3. Git 分支保留了每条路径。
4. 通过日志把大问题拆成更小的子问题。
5. 最终不是“AI 蒙对了”，而是通过证据逐步缩小范围。

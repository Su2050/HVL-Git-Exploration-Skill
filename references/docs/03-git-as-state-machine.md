# 03 — 把 Git 当成 AI 的外部状态机

## 本质判断

Git 不只是版本管理工具。在复杂 AI 编程任务里，Git 应该承担“外部状态机”的角色。

```text
.agent/*：记录为什么这样做
Git：记录做了什么、改了哪里、能不能回去
测试/日志：判断这个状态是否有效
```

## 推荐分支模型

```text
main
 ├─ hvl/N1-baseline
 ├─ hvl/N2-hypothesis-a
 ├─ hvl/N2-hypothesis-b
 └─ hvl/N3-final-integration
```

### 分支命名

```text
hvl/<node-id>-<short-hypothesis-name>
```

示例：

```text
hvl/N1-reproduce-timeout
hvl/N2-token-refresh-fix
hvl/N2-query-rewrite
hvl/N3-integration
```

## Commit 的作用

普通 commit message 经常只写：

```text
fix bug
```

这对 AI 复杂探索几乎没用。

HVL 里的 commit 应该写：

```text
Hypothesis: Login timeout is caused by stale token refresh state.
Change: Reset refresh state after 401 retry.
Validation: npm test auth.spec.ts; manual login retry.
Result: fail — timeout still occurs after retry.
Reflection: Implementation worked, but timeout source is likely request queue deadlock.
Next: Backtrack to N2 and test queue hypothesis.
```

## Checkpoint 类型

### 1. Stable checkpoint

当前状态已知稳定，适合作为回退点。

```bash
git add -A
git commit -m "checkpoint: stable state before auth timeout investigation"
```

### 2. Experiment commit

当前提交代表一次实验。

```bash
git commit -m "experiment: N2 token refresh hypothesis"
```

### 3. Failed-but-informative commit

验证失败，但有价值，保留证据。

```bash
git commit -m "failed-experiment: N2 token refresh not root cause"
```

### 4. Integration commit

把通过验证的方案合并到主线。

```bash
git commit -m "integrate: validated auth timeout fix"
```

## 回退动作

### 回到当前分支上一个状态

```bash
git reset --hard <commit>
```

慎用。只在确认要丢弃未保留修改时使用。

### 切换到兄弟假设分支

```bash
git checkout hvl/N2-query-rewrite
```

### 从父节点重新开分支

```bash
git checkout <parent-checkpoint>
git checkout -b hvl/N2-new-hypothesis
```

### 保留失败分支

失败分支不要急着删除。它是证据。

```bash
git branch --list "hvl/*"
```

## 最重要的实践

复杂任务中禁止在一个分支里连续混杂尝试多个互相独立的方案。

错误做法：

```text
在同一个分支里：
- 改认证逻辑
- 改请求队列
- 改缓存策略
- 改测试
- 最后不知道哪个有效
```

正确做法：

```text
hvl/N2-auth-token
hvl/N2-request-queue
hvl/N2-cache-policy
```

每个分支独立实验、独立验证、独立结论。

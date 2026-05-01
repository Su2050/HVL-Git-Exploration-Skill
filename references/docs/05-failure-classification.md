# 05 — 失败分类

复杂问题里，失败不是一种东西。

如果 AI 把所有失败都当成“再改一下”，就会失控。

## 1. Execution error — 执行错误

### 含义

假设可能是对的，但实现错了。

### 例子

假设：bug 来自缓存未清理。

实验：加入缓存清理逻辑。

结果：仍然失败。

进一步看日志发现：清理函数根本没被调用。

### 下一步

不要放弃假设，先修正实现路径。

## 2. Wrong hypothesis — 假设错误

### 含义

实现基本符合假设，但证据表明假设不成立。

### 例子

假设：bug 来自缓存。

实验：完全绕过缓存。

结果：bug 仍然稳定复现。

### 下一步

记录证据，退回当前节点，换兄弟假设。

## 3. Missing prerequisite — 前置条件缺失

### 含义

不是方案对错问题，而是缺了环境、权限、依赖、数据或外部条件。

### 例子

测试失败不是因为代码逻辑，而是数据库迁移没跑、API key 缺失、依赖版本不对。

### 下一步

先补前置条件，或者标记 blocked。

## 4. Invalid validation method — 验证方法错误

### 含义

测试/日志/人工检查并没有真正验证目标。

### 例子

你想验证性能优化，但只跑了功能测试。

### 下一步

重新设计验证方法，不要用错误证据做决策。

## 5. Unrelated regression — 无关回归

### 含义

当前改动暴露或引入了另一个问题，但它不是当前假设的核心。

### 例子

修登录问题时，发现 UI 快照测试失败，原因是 unrelated CSS change。

### 下一步

隔离记录，不要把新问题混进当前假设。

## 6. Ambiguous evidence — 证据不清

### 含义

结果不足以判断假设成立或不成立。

### 例子

测试偶现通过，日志不完整，现象不可复现。

### 下一步

拆小实验，提高证据质量。

## 失败分类提示词

```text
The validation failed. Before changing code again, classify the failure:
1. Was the implementation faithful to the hypothesis?
2. Did the validation actually test the target behavior?
3. Is the failure caused by missing environment/data/dependency?
4. Is this an unrelated regression?
5. What evidence would distinguish execution error from wrong hypothesis?
Then decide whether to retry, switch hypothesis, split the problem, or backtrack.
```

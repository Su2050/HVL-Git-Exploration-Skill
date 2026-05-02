# Prompt for Codex

```text
Read AGENTS.md first.

Use the HVL Git State Machine protocol for this task.

Task:
<describe task here>

Rules:
1. Treat each solution as a hypothesis.
2. Before forming the main hypothesis tree, scout prior art across papers, official docs, repos, benchmarks, blogs, issues, and adjacent domains when the task is research-like or complex.
3. Record sources in .agent/source-ledger.md, synthesize methods in .agent/prior-art-map.md, and convert useful findings into .agent/hypothesis-backlog.md.
4. Use .agent/* files as persistent memory.
5. Use Git checkpoints and codex/hvl-* branches as the external state machine.
6. Before coding, update .agent/current-plan.md, .agent/decision-tree.md, and .agent/validation.md.
7. Make one conceptual change per commit.
8. After each experiment, run validation and update .agent/experiment-log.md.
9. If validation fails, classify the failure before changing code again.
10. Update .agent/handoff.md before stopping.

Do not claim success without validation evidence.
```

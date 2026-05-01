# Prompt for Codex

```text
Read AGENTS.md first.

Use the HVL Git State Machine protocol for this task.

Task:
<describe task here>

Rules:
1. Treat each solution as a hypothesis.
2. Use .agent/* files as persistent memory.
3. Use Git checkpoints and hvl/* branches as the external state machine.
4. Before coding, update .agent/current-plan.md, .agent/decision-tree.md, and .agent/validation.md.
5. Make one conceptual change per commit.
6. After each experiment, run validation and update .agent/experiment-log.md.
7. If validation fails, classify the failure before changing code again.
8. Update .agent/handoff.md before stopping.

Do not claim success without validation evidence.
```

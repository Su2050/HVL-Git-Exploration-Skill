# Prompt for Codex

```text
Read AGENTS.md first.

Use the HVL Git State Machine protocol for this task.

Task:
<describe task here>

Rules:
1. Treat each solution as a hypothesis.
2. Before forming the main hypothesis tree, classify research need as R0/R1/R2/R3. Do not scout external prior art for clear, low-risk, user-specified tasks.
3. For R2/R3 only, scout prior art across papers, official docs, repos, benchmarks, blogs, issues, and adjacent domains.
4. Record sources in .agent/source-ledger.md, synthesize methods in .agent/prior-art-map.md, and convert useful findings into .agent/hypothesis-backlog.md when prior-art scouting is used.
5. Use .agent/* files as persistent memory.
6. Use Git checkpoints and codex/hvl-* branches as the external state machine.
7. Before coding, update .agent/current-plan.md, .agent/decision-tree.md, and .agent/validation.md.
8. Make one conceptual change per commit.
9. After each experiment, run validation and update .agent/experiment-log.md.
10. If validation fails, classify the failure before changing code again.
11. Update .agent/handoff.md before stopping.

Do not claim success without validation evidence.
```

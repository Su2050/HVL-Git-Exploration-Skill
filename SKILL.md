---
name: hvl-git-exploration
description: Use this skill for exploratory, research-like, risky, multi-step, debugging-heavy, simulation/training-heavy, performance, ML/RL, robotics, AutoML, meta-learning, or complex system tasks where there is no fixed answer and progress must be made through hypotheses, experiments, logs, tests, metrics, benchmarks, simulation results, or manual acceptance. It turns Codex into an HVL-Git expert exploration agent using .agent memory files, Git checkpoints, validation evidence, failure classification, deliberate backtracking, and persistence until success criteria are met or a real stop condition is reached.
---

# HVL Git Exploration

## Core Idea

Treat every non-trivial solution as a hypothesis. Use Git as the external state machine, `.agent/*` files as durable reasoning memory, and tests/logs/metrics/artifacts/manual checks as evidence.

Use this skill when the task is closer to exploration than direct implementation: no standard answer, multiple plausible paths, ambiguous failures, noisy feedback, long-running experiments, or handoff risk.

Do not use the full protocol for tiny deterministic edits. Use lightweight mode when the overhead of a full decision tree would be larger than the task.

## Persistence Contract

Do not stop merely because the first attempt failed, evidence is ambiguous, or the next step is inconvenient. Continue the HVL loop until one of these is true:

- success criteria are met and validated;
- the user explicitly asks to pause or stop;
- a missing external decision, credential, data source, hardware resource, or permission blocks safe progress;
- the validation method is unavailable and no useful substitute can be designed;
- continuing would risk data loss, secrets exposure, destructive Git operations, excessive cost, or unsafe behavior;
- the remaining work is a long-running external process and `.agent/handoff.md` contains the exact resume path.

Before any final response, run a completion gate:

```text
Goal met?
Validation evidence collected?
Experiment state committed or intentionally left uncommitted?
If not done, what is the next experiment and why am I not running it now?
```

If the answer is "not done" and no stop condition applies, choose the next experiment and continue.

## Mode Selection

Choose the smallest useful mode:

- **Lightweight**: one `.agent/current-plan.md`, one `.agent/experiment-log.md`, one validation signal, and a Git checkpoint plan.
- **Standard**: add `.agent/project-fit.md`, `.agent/decision-tree.md`, `.agent/assumptions.md`, `.agent/validation.md`, `.agent/handoff.md`, and `.agent/risk-register.md`.
- **Research**: standard mode plus experiment tracking discipline for seeds, configs, metrics, curves, artifacts, videos, datasets, scenario versions, and statistical confidence.

Prefer research mode for ML/RL, robotics, simulation, meta-learning, AutoML, benchmark design, and scientific/engineering research.

## Start Protocol

1. State the goal, success criteria, known constraints, and strongest available validation signal.
2. Define the completion gate: what evidence proves the task is done, and what stop conditions would justify pausing.
3. Decide lightweight / standard / research mode and record the reason in `.agent/project-fit.md` when using standard or research mode.
4. Initialize or update `.agent/*` files. If useful, run:

```bash
python3 ~/.codex/skills/hvl-git-exploration/scripts/hvl.py init
```

5. Inspect Git status before edits. Respect existing user changes; do not overwrite unrelated work.
6. Create a decision node and write the active hypothesis before making risky changes.
7. For Codex-created branches, prefer `codex/hvl-<node>-<hypothesis-slug>`. If the project explicitly standardizes on `hvl/<node>-...`, follow the project.
8. Make the smallest conceptual change that tests the active hypothesis.
9. Validate using the strongest practical evidence.
10. Record result, evidence, failure classification, reflection, next decision, branch, and commit in `.agent/experiment-log.md`.
11. Save the experiment state before starting a sibling experiment. Use `record --commit --all`, `checkpoint --all`, or an intentional manual `git add` / `git commit`.
12. If success criteria are not met and no stop condition applies, immediately select the next experiment and continue.
13. Update `.agent/handoff.md` before pausing, context compression, branch switch, or final handoff.

The helper refuses to create a new experiment branch from a dirty worktree unless `--checkpoint-before` or `--allow-dirty` is explicit. This prevents one experiment's uncommitted code from leaking into the next experiment.

## Experiment Discipline

One experiment should test one conceptual claim. Avoid mixing unrelated changes such as:

- refactor plus behavior change;
- dependency change plus feature change;
- test rewrite plus implementation change;
- reward change plus observation change plus algorithm change;
- UI redesign plus data model change.

For each experiment, record:

```text
Hypothesis:
Implementation:
Validation:
Observed evidence:
Result: pass / fail / inconclusive
Failure classification:
Reflection:
Next decision:
Git branch:
Commit:
```

To finish and preserve an experiment branch after validation:

```bash
python3 ~/.codex/skills/hvl-git-exploration/scripts/hvl.py record \
  --node N1 \
  --hypothesis "..." \
  --changes "..." \
  --validation "..." \
  --result pass \
  --failure-classification N/A \
  --reflection "..." \
  --next "..." \
  --update-handoff \
  --commit --all \
  -m "experiment: N1 H1 passed with validation evidence"
```

To start the next experiment only after saving the current one:

```bash
python3 ~/.codex/skills/hvl-git-exploration/scripts/hvl.py start \
  --node N2 \
  --title "Try sibling hypothesis" \
  --hypothesis "..."
```

If the current branch has uncommitted work, `start` stops and asks for an explicit commit/checkpoint decision.

For research / ML / RL work, also record:

```text
Environment version:
Dataset or scenario version:
Config:
Seeds:
Metrics:
Artifacts:
Failure modes:
Statistical confidence:
```

Git branches represent conceptual hypotheses. Concrete training runs, seeds, curves, videos, checkpoints, and metrics belong in experiment trackers or structured logs.

## Failure Classification

When validation fails or is ambiguous, classify before editing again:

- `execution_error`: the hypothesis may be valid, but implementation was wrong.
- `wrong_hypothesis`: the implementation tested the claim and evidence contradicted it.
- `missing_prerequisite`: dependency, data, environment, permission, or API condition is absent.
- `invalid_validation`: the validation does not actually measure the target.
- `unrelated_regression`: a separate issue appeared and must be isolated.
- `ambiguous_evidence`: evidence is too weak to decide.
- `randomness_or_low_confidence`: noisy training, one seed, unstable benchmark, or insufficient statistics.
- `simulation_real_gap`: simulation evidence does not transfer to the target reality.

Then choose exactly one next action: retry implementation, switch sibling hypothesis, split the node, backtrack to a parent checkpoint, redesign validation, isolate regression, or ask for missing external information.

Do not end the work after classification alone. Classification must produce an action unless a stop condition from the Persistence Contract applies.

## Backtracking Rules

A failed experiment is useful evidence. Before abandoning a branch or approach:

1. Update `.agent/experiment-log.md`.
2. Mark the decision node result in `.agent/decision-tree.md`.
3. Record why the branch is abandoned and where to continue.
4. Preserve the branch or commit unless it contains secrets or dangerous artifacts.
5. Return to the correct parent checkpoint or sibling hypothesis.

## Stop Rules

When stopping before success, state the exact stop condition, the latest evidence, the last saved commit or dirty state, and the next executable command. Do not present a blocked or inconclusive state as completion.

## References

Load only the reference needed for the current task:

- `references/docs/00-formal-introduction.md`: full system positioning and fit criteria.
- `references/docs/04-operating-protocol.md`: detailed operating loop.
- `references/docs/05-failure-classification.md`: failure taxonomy and next actions.
- `references/docs/11-rl-meta-research-guide.md`: ML/RL, robotics, simulation, and meta-learning guidance.
- `references/templates/research-task-brief.md`: research task framing template.
- `references/templates/ml-rl-experiment-entry.md`: ML/RL experiment log template.
- `references/AGENTS.md`: project-level instruction template to copy or adapt into a repository.

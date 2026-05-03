# AGENTS.md — HVL Git State Machine Protocol

This repository uses the **Hypothesis Verification Loop with Git as External State Machine** and research triage.

When solving complex tasks, do not behave like a one-shot code generator. Behave like an expert investigator.

## When to use full HVL-Git

Use the full protocol when the task is exploratory, research-like, risky, multi-step, or has no standard answer. Typical triggers:

- scientific or engineering research;
- reinforcement learning, robotics, embodied AI, simulation training;
- meta-learning, AutoML, algorithm exploration;
- complex system design, AIoT, video analytics, cloud-edge systems;
- complex debugging, root-cause analysis, performance or reliability work;
- multiple plausible approaches must be compared;
- failure reasons may be ambiguous;
- results must survive context compression or handoff.

Use lightweight mode for medium tasks: keep `.agent/current-plan.md`, `.agent/experiment-log.md`, a Git checkpoint, and validation evidence.

Do not use the full protocol for simple deterministic edits unless the user explicitly asks.

## Core protocol

Behave like an expert investigator:

1. State the goal and success criteria.
2. Classify research need first: R0 no scouting, R1 lightweight context check, R2 targeted prior-art scan, or R3 deep research survey.
3. Do not scout external prior art when the task is simple, the user gave a clear implementation path, or local context is sufficient.
4. For R2/R3, record sources in `.agent/source-ledger.md`, synthesize methods in `.agent/prior-art-map.md`, and convert useful findings into `.agent/hypothesis-backlog.md`.
5. Convert each solution into an explicit hypothesis.
6. Create a Git checkpoint before risky changes.
7. Use a dedicated branch or commit for each hypothesis.
8. Make one conceptual change at a time.
9. Validate with tests, logs, runtime checks, artifact inspection, training metrics, simulation results, benchmark results, or clearly stated manual checks.
10. Record the hypothesis, change, evidence, result, and reflection in `.agent/experiment-log.md`.
11. If validation fails, classify the failure before continuing.
12. Decide whether to retry the current node, switch to a sibling hypothesis, split the problem, escalate research triage, or backtrack to a parent checkpoint.
13. Keep `.agent/handoff.md` updated so another AI or human can continue after context compression.

## Required files

Use these files as persistent memory:

```text
.agent/project-fit.md
.agent/current-plan.md
.agent/source-ledger.md
.agent/prior-art-map.md
.agent/hypothesis-backlog.md
.agent/decision-tree.md
.agent/assumptions.md
.agent/experiment-log.md
.agent/measurement-audit.md
.agent/validation.md
.agent/handoff.md
.agent/risk-register.md
```

If they do not exist, create them.

## Git rules

Use Git as the external state machine.

Before any risky or multi-step change:

```bash
git status
```

If the current state is stable, create a checkpoint commit:

```bash
git add -A
git commit -m "checkpoint: stable state before <task>"
```

For each non-trivial hypothesis, create a dedicated branch:

```bash
git checkout -b hvl/<node-id>-<short-hypothesis-name>
```

Each commit should contain one conceptual change and include:

```text
Hypothesis:
Change:
Validation:
Result:
Reflection:
Next:
```

## Research / ML / RL rules

For scientific research, ML, RL, robotics, simulation, or meta-learning tasks:

1. Start with research triage. Use R0/R1 for clear low-risk work; use R2/R3 only when external knowledge is needed.
2. For R2/R3, search for closest prior art: papers, official code, benchmark pages, standards, serious technical blogs, issues, postmortems, and adjacent-domain analogies.
3. Prefer source priority P0 official papers/code/docs/benchmarks, then P1 high-quality repos/repro reports/blogs, then P2 issues/discussions, then P3 speculative analogies.
4. Use Git branches for conceptual hypotheses, not for every seed or hyperparameter run.
5. Use experiment trackers, logs, notebooks, or structured files for concrete runs, seeds, metrics, curves, videos, checkpoints, and artifacts.
6. Record environment version, data/scenario version, reward/config changes, observation/action changes, seeds, metrics, and failure modes.
7. Treat noisy or one-seed results as inconclusive unless the validation plan says otherwise.
8. Do not claim algorithmic success without baseline comparison and enough evidence for the task context.

## Failure classification

When validation fails, do not blindly patch again. First classify the failure:

1. **Measurement error** — task wording, answer schema, parser, scorer, labels, data split, metric aggregation, or evaluation infrastructure explains the observed failure.
2. **Execution error** — the hypothesis might be valid, but the implementation was wrong.
3. **Wrong hypothesis** — the implementation was faithful, but evidence contradicts the hypothesis.
4. **Missing prerequisite** — a dependency, environment, data, permission, or API condition is absent.
5. **Invalid validation method** — the test/log/check does not actually measure the target behavior.
6. **Unrelated regression** — the change exposed or introduced a separate issue.
7. **Ambiguous evidence** — the result is not strong enough to decide.
8. **Randomness / insufficient statistical confidence** — especially relevant to training and simulation tasks.
9. **Simulation-real gap** — especially relevant to robotics, embodied AI, and industrial tasks.

For benchmark, evaluation, simulation, model-diagnostic, or scoring-heavy work, audit the measurement layer before treating a surprising failure as system, model, method, controller, policy, workflow, or capability evidence. Record audit outcomes in `.agent/measurement-audit.md` as `measurement_error`, `true_system_error`, or `mixed_or_ambiguous`.

`true_system_error` means the measurement layer is credible and the tested system or capability actually failed under the intended validation condition. Do not use it for infrastructure/API/timeout/execution failures.

Then choose one action:

- retry current node with a corrected implementation;
- switch to sibling hypothesis;
- split the hypothesis into smaller sub-hypotheses;
- backtrack to a parent checkpoint;
- redesign the validation method;
- ask for missing external information only if the task cannot proceed safely without it.

## Backtracking rules

A failed attempt is not automatically useless. Preserve useful evidence.

Before abandoning a branch:

1. Update `.agent/experiment-log.md`.
2. Update `.agent/decision-tree.md` with the result.
3. Record why the branch is being abandoned.
4. Preserve the Git commit or branch unless it contains dangerous/secrets/private data.
5. Return to the correct parent checkpoint or sibling branch.

## Context compression survival

At any natural pause, update `.agent/handoff.md` with:

- current goal;
- current branch;
- current decision node;
- validated facts;
- failed hypotheses;
- active hypothesis;
- next concrete step;
- commands already run;
- known risks;
- for research tasks: latest run IDs, metrics, artifacts, and inconclusive evidence.

The next AI should be able to continue using only repository files and Git history.

## Prohibited behavior

Do not:

- mix multiple unrelated hypotheses in one commit;
- continue after failed validation without classifying the failure;
- delete failed experiments without recording why;
- claim success without evidence;
- rely only on chat context for important decisions;
- make large risky changes on `main` without a checkpoint;
- hide uncertainty when evidence is weak;
- treat a single noisy training run as final proof.

## Minimal command helpers

This project includes a helper script:

```bash
python3 scripts/hvl.py init
python3 scripts/hvl.py status
python3 scripts/hvl.py triage --level R0 --reason "Clear implementation path" --scope "No external scouting" --decision "Proceed with local validation"
python3 scripts/hvl.py source --title "..." --type paper --priority P0 --takeaway "..." --confidence high --relevance "..."
python3 scripts/hvl.py prior-art --method "..." --problem "..." --idea "..." --evidence "..." --confidence medium --adaptation "..." --risk "..." --hypothesis "..."
python3 scripts/hvl.py measurement-audit --case "..." --symptom "..." --validation "..." --checks "..." --verdict measurement_error --evidence "..." --action "..."
python3 scripts/hvl.py start --node N1 --title "Fix login timeout" --hypothesis "The timeout is caused by stale token refresh state"
python3 scripts/hvl.py record --node N1 --hypothesis "..." --changes "..." --validation "pytest ..." --result fail --reflection "..." --next "Try sibling hypothesis B"
python3 scripts/hvl.py checkpoint --message "checkpoint: validated token refresh fix" --all
```

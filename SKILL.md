---
name: hvl-git-exploration
description: Use this skill for exploratory, research-like, risky, multi-step, debugging-heavy, simulation/training-heavy, performance, ML/RL, robotics, AutoML, meta-learning, or complex system tasks where there is no fixed answer and progress must be made through appropriately scoped prior-art research, hypotheses, experiments, logs, tests, metrics, benchmarks, simulation results, or manual acceptance. It turns Codex into an HVL-Git research-grade exploration agent using research triage, optional global prior art, .agent memory files, Git checkpoints, validation evidence, failure classification, deliberate backtracking, and persistence until success criteria are met or a real stop condition is reached.
---

# HVL Git Exploration

## Core Idea

Treat every non-trivial solution as a hypothesis grounded in the best available evidence. Use Git as the external state machine, `.agent/*` files as durable reasoning memory, and tests/logs/metrics/artifacts/manual checks as evidence.

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

## Research Triage

Do not perform external prior-art scouting for every task. First classify the research need:

- **R0 - No scouting**: simple deterministic edit, user gave an exact implementation path, local code context is enough, mature standard solution is obvious, low risk, or the user says not to search.
- **R1 - Lightweight context check**: medium task where local docs, repo history, existing tests, or user-provided sources are enough. No broad web/paper search by default.
- **R2 - Targeted prior-art scan**: ambiguous failure, multiple plausible approaches, architecture/performance/reliability decision, niche API behavior, or likely recent external knowledge. Check a small number of high-signal sources.
- **R3 - Deep research survey**: scientific/engineering research, ML/RL, robotics, simulation, AutoML, meta-learning, benchmark design, SOTA comparison, or costly/high-risk exploration. Build a research packet before coding.

Use the smallest level that can safely answer the task. If the user is explicit about what to build and the path is clear, stay at R0/R1 and execute. If repeated experiments fail, evidence stays ambiguous, or validation seems weak, escalate one level.

For R2/R3, search beyond exact keyword matches:

- same goal or metric;
- same failure mode;
- same constraints, hardware, data shape, latency, safety, cost, or deployment environment;
- adjacent domains with transferable methods;
- negative results, postmortems, ablations, and known failure cases.

Use the strongest available sources first:

- **P0**: papers, official code, standards, official docs, benchmark leaderboards, datasets.
- **P1**: high-quality open-source implementations, reproducibility reports, serious engineering blogs.
- **P2**: issues, discussions, forum posts, failure reports, informal experience.
- **P3**: analogies inferred by the agent. Mark these as speculative and validate locally.

For R2/R3, record what was found in `.agent/source-ledger.md` and synthesize it in `.agent/prior-art-map.md`. Convert useful findings into `.agent/hypothesis-backlog.md`. Prior art is a source of candidate hypotheses, baselines, validation methods, and failure modes; it is not final proof.

For R3, prepare a compact research packet before coding:

```text
Research question:
Closest existing solutions:
Reusable baselines or code:
Known failure modes:
Benchmark or validation signals:
Adjacent analogies:
Evidence strength:
Open gaps:
Experiment candidates:
```

For R0/R1, do not delay implementation with broad research. Record the triage reason briefly when using standard or research mode.

## Mode Selection

Choose the smallest useful mode:

- **Lightweight**: one `.agent/current-plan.md`, one `.agent/experiment-log.md`, one validation signal, and a Git checkpoint plan.
- **Standard**: add `.agent/project-fit.md`, `.agent/source-ledger.md`, `.agent/prior-art-map.md`, `.agent/hypothesis-backlog.md`, `.agent/decision-tree.md`, `.agent/assumptions.md`, `.agent/experiment-log.md`, `.agent/measurement-audit.md`, `.agent/validation.md`, `.agent/handoff.md`, and `.agent/risk-register.md`.
- **Research**: standard mode plus R2/R3 research triage, prior-art scouting when needed, and experiment tracking discipline for baselines, seeds, configs, metrics, curves, artifacts, videos, datasets, scenario versions, and statistical confidence.

Prefer research mode for ML/RL, robotics, simulation, meta-learning, AutoML, benchmark design, and scientific/engineering research.

## Start Protocol

1. State the goal, success criteria, known constraints, and strongest available validation signal.
2. Define the completion gate: what evidence proves the task is done, and what stop conditions would justify pausing.
3. Decide lightweight / standard / research mode and record the reason in `.agent/project-fit.md` when using standard or research mode.
4. Apply research triage. Use R0/R1 when the user goal and implementation path are clear; use R2/R3 only when the task needs external prior art. Record the level and reason in `.agent/project-fit.md`.
5. Initialize or update `.agent/*` files. If useful, run:

```bash
python3 ~/.codex/skills/hvl-git-exploration/scripts/hvl.py init
```

6. Inspect Git status before edits. Respect existing user changes; do not overwrite unrelated work.
7. Create a decision node and write the active hypothesis before making risky changes.
8. For Codex-created branches, prefer `codex/hvl-<node>-<hypothesis-slug>`. If the project explicitly standardizes on `hvl/<node>-...`, follow the project.
9. Make the smallest conceptual change that tests the active hypothesis.
10. Validate using the strongest practical evidence.
11. Record result, evidence, failure classification, reflection, next decision, branch, and commit in `.agent/experiment-log.md`.
12. Return the evidence to the active decision node and record the node reconsideration before moving forward, retrying, switching siblings, splitting, or backtracking.
13. Save the experiment state before starting a sibling experiment. Use `record --commit --all`, `checkpoint --all`, or an intentional manual `git add` / `git commit`.
14. If success criteria are not met and no stop condition applies, immediately select the next experiment or escalate research triage when local evidence suggests missing knowledge.
15. Update `.agent/handoff.md` before pausing, context compression, branch switch, or final handoff.

The helper refuses to create a new experiment branch from a dirty worktree unless `--checkpoint-before` or `--allow-dirty` is explicit. This prevents one experiment's uncommitted code from leaking into the next experiment.

## Experiment Discipline

One experiment should test one conceptual claim. Avoid mixing unrelated changes such as:

- refactor plus behavior change;
- dependency change plus feature change;
- test rewrite plus implementation change;
- reward change plus observation change plus algorithm change;
- UI redesign plus data model change.

For multi-factor systems (ML/RL, robotics, simulation, AutoML, hyperparameter tuning, performance work, etc.), isolate factors before combining them:

- identify the factor list that could plausibly influence the outcome;
- prefer validating single-factor main effects before running combination experiments;
- keep non-tested factors stable or explicitly record why they cannot be held stable;
- run combination experiments only when the result can be traced back to relevant single-factor baselines;
- if attribution is unclear because multiple factors changed at once, split the node or backtrack to the last stable single-factor checkpoint.

For each experiment, record:

```text
Hypothesis:
Implementation:
Validation:
Observed evidence:
Result: pass / fail / inconclusive
Failure classification:
Reflection:
Returned evidence:
Node reconsideration:
Decision after revisit:
Continue to:
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

## Node Reconsideration Loop

Experiments are not a linear chain of attempts. Treat each experiment result as evidence returned to its decision node. Before editing again, starting a sibling branch, advancing to the next node, or backtracking:

1. Re-read the node question, chosen hypothesis, validation signal, and exit condition.
2. Compare returned evidence against the expected and invalidating evidence.
3. Decide whether the node is resolved, still worth retrying, needs a sibling hypothesis, should be split into smaller subnodes, needs a validation or measurement repair, or should backtrack to a parent / single-factor checkpoint.
4. Record the reconsideration in `.agent/decision-tree.md` and `.agent/experiment-log.md`.
5. Only advance to a child or next node when the node's exit condition has been met by evidence.

Use these fields:

```text
Returned evidence:
Node reconsideration:
Decision after revisit: retry_current / switch_sibling / split_node / backtrack_parent / backtrack_single_factor / advance_next_node / repair_measurement / redesign_validation / isolate_regression / ask_external_info
Continue to:
Next concrete action:
```

To record the loop explicitly:

```bash
python3 ~/.codex/skills/hvl-git-exploration/scripts/hvl.py reconsider \
  --node N1 \
  --from-experiment E1 \
  --returned-evidence "Validation still fails after the token refresh fix" \
  --interpretation "H1 is contradicted; request queue deadlock remains plausible" \
  --decision switch_sibling \
  --continue-to "N1 sibling: request queue hypothesis" \
  --next "Start a sibling branch for the request queue hypothesis" \
  --update-handoff
```

For research / ML / RL work, also record:

```text
Environment version:
Dataset or scenario version:
Config:
Factor under test:
Controlled factors:
Changed factors:
Combination prerequisite baselines:
Seeds:
Metrics:
Artifacts:
Failure modes:
Statistical confidence:
```

Git branches represent conceptual hypotheses. Concrete training runs, seeds, curves, videos, checkpoints, and metrics belong in experiment trackers or structured logs.

## Measurement Integrity Gate

For benchmark, evaluation, simulation, model-diagnostic, or scoring-heavy work, treat the measurement layer as a first-class hypothesis. Before attributing a failure to the model, method, policy, controller, or learned capability, check whether the result could be explained by measurement error.

At minimum, inspect:

- prompt or task wording ambiguity;
- answer schema or output-format mismatch;
- parser, extractor, scorer, or equivalence-rule failure;
- retryable API, transport, timeout, or infrastructure errors;
- data leakage, template leakage, duplicate rows, or split contamination;
- label noise, adjudication ambiguity, or weak inter-annotator agreement;
- metric aggregation that hides subgroup, surface, or difficulty effects.

When evidence is surprising, clustered by surface/template, or statistically important, run a targeted measurement audit before revising the main hypothesis. Record the audit in `.agent/measurement-audit.md` or with `hvl.py measurement-audit`. Mark each suspicious failure as:

```text
measurement_error
true_system_error
mixed_or_ambiguous
```

`true_system_error` means the measurement layer is credible, and the observed failure is valid evidence that the tested system, model, method, controller, policy, workflow, or capability failed under the intended validation condition. It does not mean an infrastructure/API/timeout/execution failure; classify those separately as `execution_error`, `missing_prerequisite`, or `invalid_validation`.

If a measurement error is found, repair or quarantine the measurement layer, rerun the smallest decisive validation, and update the interpretation. If the experiment result is affected, record the experiment with failure classification `measurement_error`. Do not count a parse failure, schema mismatch, scorer false negative, or ambiguous prompt response as evidence of a weak model capability until measurement explanations have been ruled out.

## Research Roles

Use these roles as thinking lenses. For R2/R3, use the research roles below. For R0/R1, do not invoke broad Research Scout / Method Analyst work; use only lightweight Risk Critic and Experiment Designer checks unless the triage escalates. If subagents are explicitly allowed, assign eligible roles as parallel sidecar tasks; otherwise perform the roles sequentially:

- **Research Scout**: find papers, official docs, repos, benchmarks, and serious technical writeups.
- **Method Analyst**: extract methods, assumptions, evidence strength, and limits.
- **Implementation Scout**: find reusable code, dependencies, licenses, and reproduction cost.
- **Benchmark Analyst**: identify baselines, metrics, datasets, test protocols, and acceptance signals.
- **Risk Critic**: collect negative results, failure cases, non-transferable assumptions, and safety risks.
- **Experiment Designer**: convert prior art into the next minimal local experiment.

## Failure Classification

When validation fails or is ambiguous, classify before editing again:

- `measurement_error`: the observed failure comes from the task wording, answer schema, parser, scorer, metric, labels, data split, or evaluation pipeline rather than the tested capability.
- `execution_error`: the hypothesis may be valid, but implementation was wrong.
- `wrong_hypothesis`: the implementation tested the claim and evidence contradicted it.
- `missing_prerequisite`: dependency, data, environment, permission, or API condition is absent.
- `invalid_validation`: the validation does not actually measure the target.
- `unrelated_regression`: a separate issue appeared and must be isolated.
- `factor_confounding`: multiple plausible factors changed together, so the observed effect cannot be attributed to one factor.
- `ambiguous_evidence`: evidence is too weak to decide.
- `randomness_or_low_confidence`: noisy training, one seed, unstable benchmark, or insufficient statistics.
- `simulation_real_gap`: simulation evidence does not transfer to the target reality.

Then return the evidence to the active decision node and choose exactly one next action: repair or quarantine the measurement layer, retry implementation, switch sibling hypothesis, split the node, backtrack to a parent or single-factor checkpoint, redesign validation, isolate regression, or ask for missing external information.

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
- `references/templates/measurement-audit.md`: measurement-layer audit template.
- `references/templates/source-ledger.md`: source review template.
- `references/templates/prior-art-map.md`: prior-art synthesis template.
- `references/templates/hypothesis-backlog.md`: research-derived hypothesis template.
- `references/templates/ml-rl-experiment-entry.md`: ML/RL experiment log template.
- `references/AGENTS.md`: project-level instruction template to copy or adapt into a repository.

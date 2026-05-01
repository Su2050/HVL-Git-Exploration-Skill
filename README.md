# HVL Git Exploration Skill

HVL Git Exploration is a Codex skill for complex exploratory work where there is no fixed answer and progress must come from hypotheses, experiments, validation evidence, and deliberate backtracking.

It is designed for research-like engineering tasks, complex debugging, performance work, ML/RL experiments, robotics, simulation, AutoML, meta-learning, and long-running AI coding sessions.

## What It Adds

- Hypothesis Verification Loop workflow.
- Git checkpoints and experiment branches.
- Persistent `.agent/*` reasoning files.
- Validation-driven experiment records.
- Failure classification before retrying.
- Dirty-worktree guards between sibling experiments.
- Persistence contract: continue until success criteria are met or a real stop condition is reached.

## Repository Layout

```text
SKILL.md                 # Codex skill entrypoint
agents/openai.yaml       # Optional Codex UI metadata
scripts/hvl.py           # Helper CLI for init/start/record/checkpoint/backtrack/status
references/              # Detailed protocol docs and templates
```

## Install

Copy or symlink this directory into your Codex skills folder:

```bash
mkdir -p ~/.codex/skills
cp -R hvl-git-exploration ~/.codex/skills/
```

Then invoke it in Codex:

```text
Use $hvl-git-exploration for this task.
```

## Helper CLI

Initialize a project for HVL-Git:

```bash
python3 ~/.codex/skills/hvl-git-exploration/scripts/hvl.py init
```

Start an experiment branch:

```bash
python3 ~/.codex/skills/hvl-git-exploration/scripts/hvl.py start \
  --node N1 \
  --title "Probe root cause" \
  --hypothesis "The failure is caused by stale cache state" \
  --validation "pytest tests/cache"
```

Record and commit an experiment:

```bash
python3 ~/.codex/skills/hvl-git-exploration/scripts/hvl.py record \
  --node N1 \
  --hypothesis "The failure is caused by stale cache state" \
  --changes "Added cache invalidation at refresh boundary" \
  --validation "pytest tests/cache" \
  --result pass \
  --failure-classification N/A \
  --reflection "Evidence supports the hypothesis" \
  --next "Integrate or test sibling edge cases" \
  --update-handoff \
  --commit --all \
  -m "experiment: N1 cache hypothesis passed"
```

## Safety Notes

The helper does not push, merge, reset, or rebase. It creates local Git state only when explicitly invoked.

Before starting a sibling experiment, `hvl.py start` refuses to continue from a dirty worktree unless `--checkpoint-before` or `--allow-dirty` is explicit.

## License

MIT

#!/usr/bin/env python3
"""
HVL helper: Hypothesis Verification Loop with Git as external state machine.

This script is intentionally lightweight. It does not replace judgment.
It helps AI and humans create consistent branches, checkpoints, and experiment logs.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Iterable, Optional

ROOT = Path.cwd()
AGENT_DIR = ROOT / ".agent"

FILES = {
    "current-plan.md": """# Current Plan\n\n## Target outcome\n\n## Success criteria\n\n## Completion gate\n\n- What evidence proves the task is done:\n- What validation must pass:\n\n## Stop conditions\n\n- User pause/stop:\n- Missing external input/permission/resource:\n- Unsafe or destructive risk:\n- Long-running external wait:\n\n## Current decision node\n\n## Next concrete action\n\n""",
    "decision-tree.md": """# Decision Tree\n\n## N0 — Root goal\n\n- Parent: none\n- Question:\n- Candidate hypotheses:\n- Returned evidence:\n- Node reconsideration:\n- Decision after revisit:\n- Continue to:\n- Result: pending\n\n""",
    "assumptions.md": """# Assumptions\n\n## Active assumptions\n\n""",
    "experiment-log.md": """# Experiment Log\n\n## Experiments\n\n""",
    "measurement-audit.md": """# Measurement Audit\n\n## Audits\n\nUse this for benchmark, evaluation, simulation, model-diagnostic, or scoring-heavy work when a failure may come from task wording, schema, parser, scorer, labels, data split, metric aggregation, or evaluation infrastructure.\n\n""",
    "source-ledger.md": """# Source Ledger\n\n## Sources Reviewed\n\nUse this when research triage is R2/R3, or when R1 uses user-provided sources. Record papers, official docs, repos, benchmark pages, blogs, issue threads, standards, and adjacent-domain sources.\n\n""",
    "prior-art-map.md": """# Prior-Art Map\n\n## Method Families\n\nUse this when research triage is R2/R3. Record existing solutions, baselines, assumptions, evidence strength, adaptation ideas, and risks.\n\n""",
    "hypothesis-backlog.md": """# Hypothesis Backlog\n\n## Research-Derived Candidate Hypotheses\n\nUse this when research triage is R2/R3. Record hypotheses derived from prior art before promoting them into decision-tree nodes.\n\n""",
    "validation.md": """# Validation Plan\n\n## Commands\n\n```bash\n# customize this\n```\n\n""",
    "handoff.md": """# Handoff Summary\n\n## Current state\n\n## Validated facts\n\n## Failed hypotheses\n\n## Stop condition, if not complete\n\n## Next concrete step\n\n""",
    "risk-register.md": """# Risk Register\n\n""",
    "project-fit.md": """# Project Fit Assessment\n\n## Task name\n\nTBD\n\n## Use mode\n\n- [ ] Lightweight mode\n- [ ] Standard mode\n- [ ] Research mode\n\n## Research triage\n\n- Level: R0 no scouting / R1 lightweight context check / R2 targeted prior-art scan / R3 deep research survey\n- Reason:\n- Escalation trigger:\n\n## Why HVL-Git is needed\n\nTBD\n\n## Validation signals\n\nTBD\n\n## Persistence boundary\n\nContinue until success criteria pass, or record a real stop condition.\n\n""",
}


def run(cmd: list[str], check: bool = True, capture: bool = False) -> subprocess.CompletedProcess:
    try:
        return subprocess.run(cmd, check=check, text=True, capture_output=capture)
    except subprocess.CalledProcessError as exc:
        if capture and exc.stdout:
            print(exc.stdout)
        if capture and exc.stderr:
            print(exc.stderr, file=sys.stderr)
        raise


def git_available() -> bool:
    try:
        run(["git", "--version"], check=True, capture=True)
        return True
    except Exception:
        return False


def is_git_repo() -> bool:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            check=False, text=True, capture_output=True,
        )
        return result.returncode == 0 and result.stdout.strip() == "true"
    except Exception:
        return False


def ensure_git_repo() -> None:
    if not git_available():
        print("git is not available in PATH.", file=sys.stderr)
        sys.exit(1)
    if not is_git_repo():
        run(["git", "init"])
        print("Initialized new Git repository.")


def ensure_agent_files() -> None:
    AGENT_DIR.mkdir(parents=True, exist_ok=True)
    for name, content in FILES.items():
        path = AGENT_DIR / name
        if not path.exists():
            path.write_text(content, encoding="utf-8")
            print(f"Created {path}")


def append(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(text)


def now() -> str:
    return _dt.datetime.now().astimezone().isoformat(timespec="seconds")


def slugify(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "-", text)
    text = text.strip("-")
    return text[:60] or "hypothesis"


def current_branch() -> str:
    if not is_git_repo():
        return "not-a-git-repo"
    try:
        result = run(["git", "branch", "--show-current"], capture=True)
        return result.stdout.strip() or "detached-head"
    except Exception:
        return "unknown"


def current_commit() -> str:
    if not is_git_repo():
        return "not-a-git-repo"
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            check=False, text=True, capture_output=True,
        )
        if result.returncode != 0:
            return "no-commit-yet"
        return result.stdout.strip()
    except Exception:
        return "no-commit-yet"


def git_status_porcelain() -> str:
    if not is_git_repo():
        return ""
    result = run(["git", "status", "--porcelain"], capture=True)
    return result.stdout.strip()


def worktree_dirty() -> bool:
    return bool(git_status_porcelain())


def commit_changes(message: str, *, all_changes: bool = False, paths: Optional[list[str]] = None) -> bool:
    if all_changes:
        run(["git", "add", "-A"])
    elif paths:
        run(["git", "add", *paths])

    diff = run(["git", "diff", "--cached", "--name-only"], capture=True)
    if not diff.stdout.strip():
        print("No staged changes to commit.")
        return False

    run(["git", "commit", "-m", message])
    print("Checkpoint committed.")
    return True


def cmd_init(args: argparse.Namespace) -> None:
    ensure_git_repo()
    ensure_agent_files()

    hooks = ROOT / ".githooks"
    if hooks.exists():
        run(["git", "config", "core.hooksPath", ".githooks"])
        print("Configured git core.hooksPath=.githooks")

    msg = ROOT / ".gitmessage"
    if msg.exists():
        run(["git", "config", "commit.template", ".gitmessage"])
        print("Configured git commit.template=.gitmessage")

    print("HVL initialized.")
    print("Next: update .agent/current-plan.md and create a stable checkpoint if appropriate.")


def cmd_status(args: argparse.Namespace) -> None:
    ensure_agent_files()
    print(f"Branch: {current_branch()}")
    print(f"Commit: {current_commit()}")
    if is_git_repo():
        run(["git", "status", "--short"])
    log_path = AGENT_DIR / "experiment-log.md"
    if log_path.exists():
        lines = log_path.read_text(encoding="utf-8").splitlines()
        tail = lines[-30:]
        print("\n--- experiment-log tail ---")
        print("\n".join(tail))


def cmd_start(args: argparse.Namespace) -> None:
    ensure_git_repo()
    ensure_agent_files()
    node = args.node.strip()
    title = args.title.strip()
    hypothesis = args.hypothesis.strip()
    branch = args.branch or f"codex/hvl-{node}-{slugify(title or hypothesis)}"

    if args.checkout:
        if worktree_dirty():
            if args.checkpoint_before:
                message = args.checkpoint_message or f"checkpoint: before starting {node} {title}"
                commit_changes(message, all_changes=True)
            elif not args.allow_dirty:
                print("Refusing to create a new experiment branch with uncommitted changes.", file=sys.stderr)
                print("Save the current experiment first, for example:", file=sys.stderr)
                print("  hvl.py record ... --commit --all", file=sys.stderr)
                print("or:", file=sys.stderr)
                print("  hvl.py checkpoint --all -m \"experiment: <node> <result> <summary>\"", file=sys.stderr)
                print("Use --checkpoint-before to auto-commit all current changes, or --allow-dirty to bypass.", file=sys.stderr)
                sys.exit(2)
        run(["git", "checkout", "-b", branch])
        print(f"Created and switched to branch {branch}")

    entry = f"""

---

## {node} — {title}

- Parent: {args.parent or "TBD"}
- Created: {now()}
- Question: {args.question or title}
- Chosen hypothesis: {hypothesis}
- Validation signal: {args.validation or "TBD"}
- Exit condition: {args.exit_condition or "TBD"}
- Result: pending
- Git branch: {branch}
- Checkpoint commit: {current_commit()}
"""
    append(AGENT_DIR / "decision-tree.md", entry)

    assumption = f"""

---

## {node} — {hypothesis}

- Related node: {node}
- Claim: {hypothesis}
- Why it might be true: {args.why or "TBD"}
- Sub-assumptions: {args.sub or "TBD"}
- Expected evidence: {args.expected or "TBD"}
- Invalidating evidence: {args.invalidating or "TBD"}
- Current status: untested
- Git branch: {branch}
"""
    append(AGENT_DIR / "assumptions.md", assumption)
    print(f"Recorded decision node {node} and hypothesis.")


def cmd_record(args: argparse.Namespace) -> None:
    ensure_agent_files()
    branch = current_branch()
    commit = current_commit()
    result = args.result
    classification = args.failure_classification or ("N/A" if result == "pass" else "TBD")

    entry = f"""

---

### {args.experiment or 'E-' + _dt.datetime.now().strftime('%Y%m%d-%H%M%S')} — {args.node}

- Time: {now()}
- Git branch: {branch}
- Commit: {commit}
- Decision node: {args.node}
- Hypothesis: {args.hypothesis}
- Implementation: {args.changes}
- Validation method: {args.validation}
- Validation command/result: {args.validation_result or args.validation}
- Observed evidence: {args.evidence or 'TBD'}
- Result: {result}
- Failure classification: {classification}
- Reflection: {args.reflection}
- Next decision: {args.next}
"""
    append(AGENT_DIR / "experiment-log.md", entry)
    print("Recorded experiment in .agent/experiment-log.md")

    if args.update_handoff:
        handoff = f"""

---

## Latest update — {now()}

- Current branch: {branch}
- Current commit: {commit}
- Current node: {args.node}
- Active hypothesis: {args.hypothesis}
- Latest result: {result}
- Failure classification: {classification}
- Evidence: {args.evidence or 'TBD'}
- Next concrete step: {args.next}
"""
        append(AGENT_DIR / "handoff.md", handoff)
        print("Updated .agent/handoff.md")

    if args.commit:
        message = args.message or f"experiment: {args.node} {result} {slugify(args.hypothesis)}"
        commit_changes(message, all_changes=args.all, paths=args.paths)


def cmd_checkpoint(args: argparse.Namespace) -> None:
    ensure_git_repo()
    ensure_agent_files()

    if not args.all and not args.paths:
        print("No files staged by hvl.py. Use --all or --paths, or stage files manually before checkpoint.")

    message = args.message or f"checkpoint: {now()}"
    commit_changes(message, all_changes=args.all, paths=args.paths)


def cmd_backtrack(args: argparse.Namespace) -> None:
    ensure_git_repo()
    ensure_agent_files()
    entry = f"""

---

## Backtrack — {now()}

- From branch: {current_branch()}
- From commit: {current_commit()}
- Target: {args.target or 'TBD'}
- Reason: {args.reason}
- Decision: {args.decision or 'TBD'}
"""
    append(AGENT_DIR / "experiment-log.md", entry)
    append(AGENT_DIR / "handoff.md", entry)
    print("Recorded backtrack reason in experiment log and handoff.")

    if args.checkout and args.target:
        run(["git", "checkout", args.target])
        print(f"Checked out {args.target}")


def cmd_reconsider(args: argparse.Namespace) -> None:
    ensure_git_repo()
    ensure_agent_files()
    branch = current_branch()
    commit = current_commit()
    entry = f"""

---

## Reconsideration — {args.node} — {now()}

- From branch: {branch}
- From commit: {commit}
- From experiment: {args.from_experiment or 'TBD'}
- Returned evidence: {args.returned_evidence}
- Node reconsideration: {args.interpretation}
- Decision after revisit: {args.decision}
- Continue to: {args.continue_to}
- Next concrete action: {args.next}
"""
    append(AGENT_DIR / "decision-tree.md", entry)
    append(AGENT_DIR / "experiment-log.md", entry)
    print("Recorded node reconsideration in decision tree and experiment log.")

    if args.update_handoff:
        append(AGENT_DIR / "handoff.md", entry)
        print("Updated .agent/handoff.md")

    if args.checkout_target:
        run(["git", "checkout", args.checkout_target])
        print(f"Checked out {args.checkout_target}")


def cmd_triage(args: argparse.Namespace) -> None:
    ensure_agent_files()
    entry = f"""

---

## Research triage - {now()}

- Level: {args.level}
- User intent: {args.user_intent or 'TBD'}
- Reason: {args.reason}
- Scope: {args.scope}
- Sources to check: {args.sources or 'N/A'}
- Escalation trigger: {args.escalation or 'TBD'}
- Decision: {args.decision}
"""
    append(AGENT_DIR / "project-fit.md", entry)
    print("Recorded research triage in .agent/project-fit.md")


def cmd_source(args: argparse.Namespace) -> None:
    ensure_agent_files()
    entry = f"""

---

## {args.title}

- Time: {now()}
- Type: {args.type}
- Priority: {args.priority}
- URL: {args.url or 'N/A'}
- Authors / org: {args.authors or 'TBD'}
- Year / date: {args.date or 'TBD'}
- Domain: {args.domain or 'TBD'}
- Key takeaway: {args.takeaway}
- Evidence strength: {args.confidence}
- Reusable baseline / code: {args.reusable or 'TBD'}
- Known limits / failure modes: {args.limits or 'TBD'}
- Relevance to current task: {args.relevance}
- Tags: {args.tags or 'TBD'}
"""
    append(AGENT_DIR / "source-ledger.md", entry)
    print("Recorded source in .agent/source-ledger.md")


def cmd_prior_art(args: argparse.Namespace) -> None:
    ensure_agent_files()
    entry = f"""

---

## {args.method}

- Time: {now()}
- Source: {args.source or 'TBD'}
- Method family: {args.family or 'TBD'}
- Problem solved / closest analogy: {args.problem}
- Core idea: {args.idea}
- Evidence: {args.evidence}
- Evidence strength: {args.confidence}
- Assumptions / prerequisites: {args.assumptions or 'TBD'}
- Adaptation to current task: {args.adaptation}
- Risks / non-transferable parts: {args.risk}
- Candidate experiment: {args.experiment or 'TBD'}
- Next decision: {args.next or 'TBD'}
"""
    append(AGENT_DIR / "prior-art-map.md", entry)
    print("Recorded prior-art method in .agent/prior-art-map.md")

    if args.hypothesis:
        hypothesis = f"""

---

## {args.hypothesis_id or 'H-' + _dt.datetime.now().strftime('%Y%m%d-%H%M%S')} - {args.hypothesis}

- Derived from: {args.method}
- Source: {args.source or 'TBD'}
- Claim: {args.hypothesis}
- Why it might be true: {args.idea}
- Expected evidence: {args.expected or 'TBD'}
- Invalidating evidence: {args.invalidating or 'TBD'}
- Validation idea: {args.experiment or 'TBD'}
- Current status: candidate
"""
        append(AGENT_DIR / "hypothesis-backlog.md", hypothesis)
        print("Recorded candidate hypothesis in .agent/hypothesis-backlog.md")


def cmd_measurement_audit(args: argparse.Namespace) -> None:
    ensure_agent_files()
    entry = f"""

---

## {args.case}

- Time: {now()}
- Decision node: {args.node or 'TBD'}
- Git branch: {current_branch()}
- Commit: {current_commit()}
- Symptom: {args.symptom}
- Validation method: {args.validation}
- Audit checks: {args.checks}
- Verdict: {args.verdict}
- Root cause: {args.root_cause or 'TBD'}
- Evidence: {args.evidence}
- Corrective action: {args.action}
- Rerun / follow-up validation: {args.rerun or 'TBD'}
- Next decision: {args.next or 'TBD'}
"""
    append(AGENT_DIR / "measurement-audit.md", entry)
    print("Recorded measurement audit in .agent/measurement-audit.md")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="HVL Git State Machine helper")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("init", help="Initialize Git repo config and .agent files")
    p.set_defaults(func=cmd_init)

    p = sub.add_parser("status", help="Show Git status and recent experiment log")
    p.set_defaults(func=cmd_status)

    p = sub.add_parser("start", help="Start a decision node/hypothesis branch")
    p.add_argument("--node", required=True)
    p.add_argument("--title", required=True)
    p.add_argument("--hypothesis", required=True)
    p.add_argument("--parent")
    p.add_argument("--question")
    p.add_argument("--validation")
    p.add_argument("--exit-condition")
    p.add_argument("--why")
    p.add_argument("--sub")
    p.add_argument("--expected")
    p.add_argument("--invalidating")
    p.add_argument("--branch")
    p.add_argument("--checkpoint-before", action="store_true", help="Commit all current changes before creating the new branch")
    p.add_argument("--checkpoint-message", help="Commit message used with --checkpoint-before")
    p.add_argument("--allow-dirty", action="store_true", help="Allow branch creation with uncommitted changes")
    p.add_argument("--no-checkout", action="store_false", dest="checkout", help="Record only; do not create branch")
    p.set_defaults(checkout=True, func=cmd_start)

    p = sub.add_parser("record", help="Record an experiment result")
    p.add_argument("--experiment")
    p.add_argument("--node", required=True)
    p.add_argument("--hypothesis", required=True)
    p.add_argument("--changes", required=True)
    p.add_argument("--validation", required=True)
    p.add_argument("--validation-result")
    p.add_argument("--evidence")
    p.add_argument("--result", choices=["pass", "fail", "inconclusive"], required=True)
    p.add_argument("--failure-classification", choices=[
        "measurement_error",
        "execution_error",
        "wrong_hypothesis",
        "missing_prerequisite",
        "invalid_validation",
        "unrelated_regression",
        "factor_confounding",
        "ambiguous_evidence",
        "randomness_or_low_confidence",
        "simulation_real_gap",
        "N/A",
    ])
    p.add_argument("--reflection", required=True)
    p.add_argument("--next", required=True)
    p.add_argument("--update-handoff", action="store_true")
    p.add_argument("--commit", action="store_true", help="Commit the recorded experiment after writing .agent logs")
    p.add_argument("--all", action="store_true", help="With --commit, stage all changes before committing")
    p.add_argument("--paths", nargs="*", help="With --commit, stage only these paths before committing")
    p.add_argument("--message", "-m", help="Commit message used with --commit")
    p.set_defaults(func=cmd_record)

    p = sub.add_parser("checkpoint", help="Create a checkpoint commit")
    p.add_argument("--message", "-m")
    p.add_argument("--all", action="store_true", help="Stage all changes before commit")
    p.add_argument("--paths", nargs="*")
    p.set_defaults(func=cmd_checkpoint)

    p = sub.add_parser("backtrack", help="Record and optionally perform a backtrack")
    p.add_argument("--reason", required=True)
    p.add_argument("--target")
    p.add_argument("--decision")
    p.add_argument("--checkout", action="store_true")
    p.set_defaults(func=cmd_backtrack)

    p = sub.add_parser("reconsider", help="Return experiment evidence to a decision node and record the next action")
    p.add_argument("--node", required=True)
    p.add_argument("--from-experiment")
    p.add_argument("--returned-evidence", required=True)
    p.add_argument("--interpretation", required=True)
    p.add_argument("--decision", required=True, choices=[
        "retry_current",
        "switch_sibling",
        "split_node",
        "backtrack_parent",
        "backtrack_single_factor",
        "advance_next_node",
        "repair_measurement",
        "redesign_validation",
        "isolate_regression",
        "ask_external_info",
    ])
    p.add_argument("--continue-to", required=True, help="Target node, sibling hypothesis, checkpoint, branch, or stop condition")
    p.add_argument("--next", required=True, help="Concrete next action after revisiting the node")
    p.add_argument("--update-handoff", action="store_true")
    p.add_argument("--checkout-target", help="Optional branch or commit to checkout after recording")
    p.set_defaults(func=cmd_reconsider)

    p = sub.add_parser("triage", help="Record research triage level before prior-art scouting")
    p.add_argument("--level", choices=["R0", "R1", "R2", "R3"], required=True)
    p.add_argument("--reason", required=True)
    p.add_argument("--scope", required=True, help="Research scope or why research is skipped")
    p.add_argument("--decision", required=True, help="Proceed directly, lightweight check, targeted scan, or deep survey")
    p.add_argument("--user-intent")
    p.add_argument("--sources")
    p.add_argument("--escalation")
    p.set_defaults(func=cmd_triage)

    p = sub.add_parser("source", help="Record a prior-art source")
    p.add_argument("--title", required=True)
    p.add_argument("--type", choices=["paper", "official_doc", "standard", "benchmark", "repo", "blog", "issue", "discussion", "postmortem", "dataset", "other"], required=True)
    p.add_argument("--priority", choices=["P0", "P1", "P2", "P3"], required=True)
    p.add_argument("--url")
    p.add_argument("--authors")
    p.add_argument("--date")
    p.add_argument("--domain")
    p.add_argument("--takeaway", required=True)
    p.add_argument("--confidence", choices=["high", "medium", "low", "speculative"], required=True)
    p.add_argument("--reusable")
    p.add_argument("--limits")
    p.add_argument("--relevance", required=True)
    p.add_argument("--tags")
    p.set_defaults(func=cmd_source)

    p = sub.add_parser("prior-art", help="Record a prior-art method and optional candidate hypothesis")
    p.add_argument("--method", required=True)
    p.add_argument("--source")
    p.add_argument("--family")
    p.add_argument("--problem", required=True)
    p.add_argument("--idea", required=True)
    p.add_argument("--evidence", required=True)
    p.add_argument("--confidence", choices=["high", "medium", "low", "speculative"], required=True)
    p.add_argument("--assumptions")
    p.add_argument("--adaptation", required=True)
    p.add_argument("--risk", required=True)
    p.add_argument("--experiment")
    p.add_argument("--next")
    p.add_argument("--hypothesis")
    p.add_argument("--hypothesis-id")
    p.add_argument("--expected")
    p.add_argument("--invalidating")
    p.set_defaults(func=cmd_prior_art)

    p = sub.add_parser("measurement-audit", help="Record a measurement audit verdict")
    p.add_argument("--case", required=True, help="Short name for the suspicious failure or metric issue")
    p.add_argument("--node")
    p.add_argument("--symptom", required=True)
    p.add_argument("--validation", required=True)
    p.add_argument("--checks", required=True, help="Prompt/schema/parser/scorer/data/metric checks performed")
    p.add_argument("--verdict", choices=["measurement_error", "true_system_error", "mixed_or_ambiguous"], required=True)
    p.add_argument("--root-cause")
    p.add_argument("--evidence", required=True)
    p.add_argument("--action", required=True)
    p.add_argument("--rerun")
    p.add_argument("--next")
    p.set_defaults(func=cmd_measurement_audit)

    return parser


def main(argv: Optional[Iterable[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

# Measurement Audit Template

Use this when a benchmark, evaluation, simulation, model diagnostic, parser, scorer, label, split, or metric issue may explain a surprising result.

## Audit

- Case:
- Decision node:
- Git branch:
- Commit:
- Symptom:
- Validation method:
- Audit checks:
  - Prompt / task wording:
  - Answer schema / output format:
  - Parser / extractor / scorer:
  - API / timeout / infrastructure:
  - Data leakage / duplicates / split contamination:
  - Label noise / adjudication ambiguity:
  - Metric aggregation / subgroup effects:
- Verdict: measurement_error / true_model_error / mixed_or_ambiguous
- Root cause:
- Evidence:
- Corrective action:
- Rerun / follow-up validation:
- Next decision:

## Rule

Do not treat a suspicious failure as model or method evidence until plausible measurement explanations have been ruled out.

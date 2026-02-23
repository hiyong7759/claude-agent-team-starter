---
module: quality-gates-rules
tier: 1
inject: conditional
target_agents: [qa, cr, re]
version: 1.0
last_updated: 2026-02-19
---

# Quality Gates Rules

Operational gates enforced before PR, review, and execution. Derived from quality-gates.md and development-standards.md.

## Common Gates -- Always Applied (QG)

- **QG-1**: **Reuse-first**: Verify at least one existing asset or pattern candidate was considered for reuse before creating new code.
- **QG-2**: **Domain Fit**: Confirm no conflicts with domain invariants, terminology (glossary.md), or established conventions.
- **QG-3**: **Traceability**: No missing connections among WI, ADR, and Asset registry where required.
- **QG-4**: **HITL Check**: If the change involves destructive operations, network calls, installs, git writes, or production impact, confirm purpose/risks/rollback were explained and user approval was obtained before execution.

## LOW Criticality Gates (QG)

- **QG-5**: WI-ID issued and included in commit message (`WI-YYYYMMDD-<PRJ>-###`).
- **QG-6**: Goal, Reuse, and Impact recorded in 3 lines in commit or PR description.
- **QG-7**: N/A exception allowed only for trivial changes (typos, formatting).

## MEDIUM Criticality Gates (QG)

- **QG-8**: Impact analysis organized (impact, rollback plan, validation approach).
- **QG-9**: Minimum regression verification exists (test or scenario covering the change).
- **QG-10**: Registry Consumers updated when modifying shared assets. Responsibility chain: worker creates, MA confirms, EO approves.
- **QG-11**: Post-evaluation performed (10-20 minute review per agent-evaluation.md) after work completion. Simple report or comment is acceptable.

## HIGH Criticality Gates (QG)

- **QG-12**: ADR required with alternatives, risks, and rollback plan.
- **QG-13**: PG (security) and RE (reliability) perspective reviews recorded.
- **QG-14**: If contract change, backward compatibility and versioning policy specified.
- **QG-15**: Post-evaluation required with 1-3 recorded improvement actions.

## Skill Integration Order (QG)

- **QG-16**: Standard quality check sequence (canonical order):
  1. `/typecheck` -- Type validation (tsc --noEmit, mypy)
  2. `/lint` -- Code style and quality (ESLint, pylint)
  3. `/prettier` -- Code formatting verification
  4. `/test` -- Test execution
  5. `/test-coverage` -- Coverage analysis and threshold verification
- **QG-17**: `qa` runs all five skills as a unified quality check (pre-commit gate). `re` investigates any failures. `cr` verifies test quality during review.
- **QG-18**: Merge requirements: all type checks pass, no lint violations, all tests pass, coverage meets thresholds (Lines 80%, Branches 70%, Functions 80%, Statements 80%).

## Gate Enforcement (QG)

- **QG-19**: Gate failures block the corresponding action (commit, merge, or deployment). Do not proceed with unresolved gate failures.
- **QG-20**: Reference policies for gate decisions: versioning/deprecation (versioning-policy.md), sensitive info (security-policy.md), regression baseline (eval-golden-set.md).

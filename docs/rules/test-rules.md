---
module: test-rules
tier: 1
inject: conditional
target_agents: [re, qa]
version: 1.0
last_updated: 2026-02-19
---

# Test Rules

Standards for test methodology, coverage, naming, skill integration, and evaluation.

## TDD Methodology (T)

- **T-1**: Follow the Red-Green-Refactor cycle:
  - **Red**: Write a failing test first. Define expected behavior before implementation. Verify the test actually fails.
  - **Green**: Write minimal code to pass the test. Avoid premature optimization. Focus on correctness.
  - **Refactor**: Improve structure and remove duplication while keeping tests green.
- **T-2**: Tests are written before implementation whenever possible. `se` follows TDD; `re` verifies test quality and coverage.
- **T-3**: Run tests continuously during refactoring to ensure no regression.

## Coverage Thresholds (T)

- **T-4**: Minimum coverage thresholds:
  - Lines: 80%
  - Branches: 70%
  - Functions: 80%
  - Statements: 80%
- **T-5**: Exceptions to T-4: configuration files (no coverage required), generated code (excluded), experimental/prototype code (60% acceptable when explicitly marked).
- **T-6**: 100% coverage required for:
  - Security-sensitive code (authentication, authorization, data sanitization)
  - Core orchestration logic (REQ approval gates, WI generation)
  - Context injection mechanisms (Tier 0 document loading)
  - Governance enforcement (policy violation detection)
- **T-7**: Use `/test-coverage` to measure coverage and review reports before completing any WI.

## File Naming and Location (T)

- **T-8**: Python test files: `test_*.py` (pytest convention). TypeScript test files: `*.test.ts` or `*.spec.ts`.
- **T-9**: Co-located tests preferred for domain projects (`src/utils/helpers.test.ts` next to `helpers.ts`). Centralized tests preferred for system scripts (`.claude/tests/test_*.py`).

## Skill Integration Order (T)

- **T-10**: Standard quality check sequence: `/typecheck` then `/lint` then `/test` then `/test-coverage`. `qa` runs all four as a unified quality check.
- **T-11**: `re` investigates test failures and performs regression testing. `cr` verifies test quality during code review.

## Agent Responsibilities (T)

- **T-12**: `re` responsibilities:
  - Execute test suites independently (verification agent, not implementer)
  - Investigate test failures and identify root causes
  - Perform regression testing after fixes
  - Validate test quality (coverage completeness, edge case adequacy)
- **T-13**: `qa` responsibilities:
  - Unified quality verification (typecheck + lint + test + coverage)
  - Pre-commit quality gate enforcement
  - Coverage threshold validation against T-4
  - Quality metrics reporting
- **T-14**: `qa` gate criteria: all type checks pass, no lint violations, all tests pass, coverage meets T-4 thresholds.

## Evidence Pack Test Section (T)

- **T-15**: Every Evidence Pack must include a Test Evidence section containing:
  - Command executed (e.g., `/test` or `npm test`)
  - Pass/fail status with counts (X tests, Y assertions)
  - Duration
  - Coverage metrics (overall + per-metric with pass/fail against thresholds)
  - Test files created or modified (with line ranges)
  - Reproduction steps (numbered, executable)
- **T-16**: Evidence must be reproducible. Include exact commands so any agent can re-run verification independently.

## Golden Set Regression (T)

- **T-17**: Golden set categories: G-SEC (security/permissions), G-TOOL (tool calling), G-TRACE (WI/ADR/registry discipline), G-QUALITY (output format/instruction compliance).
- **T-18**: Each golden set case must define: ID (G-XXX-###), Input (user request), Expected (conditions checklist), Disallowed (prohibited actions).
- **T-19**: Run golden set regression immediately after model, routing, or policy changes. `re` owns golden set design and maintenance.

## Evaluation Criteria (T)

- **T-20**: `re` is evaluated on: regression protection sufficiency, golden set failure recurrence count, failure investigation thoroughness, evidence completeness.
- **T-21**: `qa` is evaluated on: policy compliance rate, coverage threshold enforcement accuracy, unified check consistency, pre-commit gate reliability.
- **T-22**: Evaluation triggers -- MEDIUM/HIGH tasks: post-evaluation immediately after PR merge (mandatory). LOW tasks: sampling (weekly or 1-in-10). System changes: golden set regression immediately (mandatory).

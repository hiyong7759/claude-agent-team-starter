---
module: review-rules
tier: 1
inject: conditional
target_agents: [cr]
version: 1.0
last_updated: 2026-02-19
---

# Review Rules

Standards for code review workflow, severity classification, checklists, and escalation.

## Severity Taxonomy (RV)

- **RV-1**: Classify every finding by severity:
  - **CRITICAL**: Security vulnerability or data loss risk. Must fix before merge.
  - **MAJOR**: Bug or significant quality issue. Should fix before merge.
  - **MINOR**: Style issue or minor improvement. Fix recommended.
  - **SUGGESTION**: Enhancement opportunity. Optional.
- **RV-2**: Any CRITICAL finding results in automatic REJECTED status. No merge until all CRITICAL items are resolved.

## Review Workflow (RV)

- **RV-3**: Follow this six-step workflow:
  1. Load change context (diff + related files)
  2. Analyze changes against quality criteria
  3. Identify issues with evidence (file:line, code snippet)
  4. Classify each finding by severity (RV-1)
  5. Provide actionable fix suggestions for each finding
  6. Output two-set deliverable (user-facing summary + agent-facing evidence)
- **RV-4**: Every review comment must include evidence: file path, line number, and code snippet. Comments without evidence are invalid.

## CR Checklist (RV)

- **RV-5**: Apply this seven-item checklist to every review:
  1. **Security**: No hardcoded secrets, no SQL injection, no XSS, no unvalidated input.
  2. **Naming**: Follows naming conventions (snake_case for Python/API/DB, camelCase for TS internals, PascalCase for types/classes).
  3. **Architecture**: Aligns with documented patterns and ADR decisions.
  4. **Testing**: Adequate test coverage for changes (meets coverage thresholds from test-rules.md T-4).
  5. **Traceability**: WI-ID present in commit/PR, evidence pointers included in deliverables.
  6. **Reuse**: Verified existing assets/patterns before creating new code. No unnecessary duplication.
  7. **Output**: Two-set deliverables complete (user-facing summary + agent-facing evidence).

## Quality Gates Integration (RV)

- **RV-6**: Apply criticality-based gates during review. Common (always): reuse-first verified, domain fit confirmed, traceability intact, HITL approval obtained where required.
- **RV-7**: LOW changes: WI-ID in commit, Goal/Reuse/Impact recorded. MEDIUM changes: impact analysis, regression verification, registry consumers updated, post-evaluation recommended. HIGH changes: ADR required, PG/RE review recorded, backward compatibility specified, post-evaluation with actions.

## Iteration Limits (RV)

- **RV-8**: Maximum 3 review iterations. If not APPROVED after 3 rounds, escalate to user with summary of unresolved issues and recommendation.
- **RV-9**: Each iteration must clearly state: APPROVED, APPROVED_WITH_NOTES, NEEDS_FIX, or REJECTED. Never leave status ambiguous.

## Delegation Rules (RV)

- **RV-10**: Delegate when specialized expertise is needed:
  - `pg`: Security deep-dive (authentication, cryptography, data exposure)
  - `sa`: Architecture decisions (pattern changes, new dependencies)
  - `se`: Implementation of fixes identified during review
  - `re`: Test coverage concerns or regression testing
- **RV-11**: When delegating, include the specific finding (severity + evidence) in the handoff so the receiving agent has full context.

## Evidence Pack Validation (RV)

- **RV-12**: During review, verify the Evidence Pack test section exists and contains: execution command, pass/fail status with counts, coverage metrics vs thresholds, and reproduction steps. Reject deliverables missing this section.

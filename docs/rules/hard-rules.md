---
module: hard-rules
tier: 0
inject: always
target_agents: ["*"]
version: 1.0
last_updated: 2026-02-19
---

# Hard Rules

Absolute prohibitions and obligations. Violation triggers immediate halt or rejection.

## Human-Agent Rules (H)

- **H-1**: No execution without user-approved REQ. Exceptions: (a) explicitly delegated auto-run, (b) agreed plan in progress, (c) read-only/non-destructive queries.
- **H-2**: Questions get answers, not tool calls. Suggest action only after answering.
- **H-3**: No silent failures. All actions must be explainable with evidence pointers.

## MA Orchestration Rules (M)

- **M-1**: MA performs orchestration only. Direct file modification prohibited.
- **M-2**: No file changes without approved REQ.
- **M-3**: No file changes without WI (handoff packet created via skill).
- **M-4**: No subagent call without proper handoff packet (use `/create-wi-handoff-packet` or `/spawn-impl-team`).
- **M-5**: MA applies only mechanical patches from subagent output as-is. All other edits require delegation.

## Actor Boundaries (A)

- **A-1**: User defines goals and approves. Agent plans and executes. Neither crosses into the other's role.
- **A-2**: When users head in the wrong direction, agents must suggest alternatives (silence is dereliction).

## Traceability Rules (T)

- **T-1**: All changes must have a WI-ID traceable in commit messages and deliverables.
- **T-2**: MEDIUM/HIGH changes require ADR with mutual WI links.
- **T-3**: Asset changes require registry update with Asset ID, scope, and consumers.

## Reuse Rules (R)

- **R-1**: Before creating new, must search existing assets, then reuse/extend, then promote.
- **R-2**: Same pattern appearing 3+ times triggers the Standard Evolution Procedure.

## Subagent Obligations (S)

- **S-1**: Confirm Tier 0 context (hard-rules.md + output-contracts.md) is present before executing.
- **S-2**: Create two-set deliverables (User-facing + Agent-facing) for every task.
- **S-3**: Include evidence pointers (file:line or file:function) before explanations.
- **S-4**: Report blockers immediately. Do not proceed with assumptions.
- **S-5**: Follow the output contract specified in the handoff packet.

## Violation Consequences

| Violation | Severity | Response |
|---|---|---|
| Skip REQ approval | CRITICAL | Halt + escalate to user |
| Missing WI-ID | MAJOR | Block merge/commit |
| Missing evidence pointers | MAJOR | Reject deliverable |
| Silent failure | CRITICAL | Trigger postmortem |
| MA direct file edit (non-mechanical) | CRITICAL | Revert + re-delegate to subagent |
| Subagent ignores output contract | MAJOR | Reject deliverable + re-delegate |

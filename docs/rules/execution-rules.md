---
module: execution-rules
tier: 1
inject: conditional
target_agents: [eo, "*"]
condition: execution
---
# Execution Rules

Rules for execution safety, approval gates, versioning, and template governance. Source: execution-policy.md, core-principles.md, versioning-policy.md, template-governance.md.

## Core Principles

- **EX-1**: Explain Then Execute -- explain why/what/how/risks/rollback before executing tools or commands.
- **EX-2**: Default = Ask. When in doubt, ask first. Non-destructive (read-only) first, write approval later.
- **EX-3**: Ask Before Execute (H-1). Before any state-changing action, explain the plan and get user approval. Exception: explicit auto-run delegation or pre-agreed plan.
- **EX-4**: Answer First (H-2). If user input is a question, answer it. Do not combine answering with executing changes.

## Pre-flight Check

- **EX-5**: Before script/tool execution: identify dependencies (config, env vars, libraries), verify existence on disk, halt and report if missing. Never assume.
- **EX-6**: For destructive operations, use `--dry-run` first when available.

## HITL Approval Matrix

- **EX-7**: Approval levels: A0 (no approval, read-only), A1 (notify after), A2 (user approval before), A3 (user + 2-person review).
- **EX-8**: Matrix (Criticality LOW / MEDIUM / HIGH):
  - Read-only: A0 / A0 / A0
  - Doc/draft creation: A1 / A1 / A1
  - Bulk file changes: A1 / A2 / A2
  - Git write (commit/push): A2 / A2 / A3
  - Dependency install: A2 / A2 / A3
  - Network (API/download): A2 / A2 / A3
  - Destructive (delete/init): A2 / A3 / A3
  - Production impact: A3 / A3 / A3

## REQ-Based Single Gate

- **EX-9**: Only REQ approval is required. After REQ approval: WI generation, WI execution, implementation details all auto-proceed.
- **EX-10**: Exception cases (always ask even after REQ approval): destructive ops, requirement changes, critical architecture/library decisions, unexpected blockers, security/sensitive data.
- **EX-11**: Auto-proceed after REQ approval: git ops, build/test, quality checks, file creation per WI, subagent delegation per REQ strategy.

## Versioning

- **EX-12**: Status lifecycle: Draft (experimental) -> Stable (backward-compatible) -> Deprecated (replacement provided) -> Debt (refactoring target).
- **EX-13**: Breaking change = field deletion/semantic change, gate criteria strengthening, automation output format change.
- **EX-14**: Deprecated procedure requires: replacement target, migration method, deprecation schedule, consumer impact.

## Template Governance

- **EX-15**: Templates = interface of discipline. Default = extend existing template. New creation is exception (only when fields are fundamentally different or pattern solidified after repeated WIs).
- **EX-16**: Template changes prioritize backward compatibility (additions OK, deletions need ADR). Registry registration required.

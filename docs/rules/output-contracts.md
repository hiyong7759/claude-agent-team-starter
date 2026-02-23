---
module: output-contracts
tier: 0
inject: always
target_agents: ["*"]
version: 1.0
last_updated: 2026-02-19
---

# Output Contracts

Defines what every agent output MUST contain. Non-compliance triggers deliverable rejection.

## 1. Universal Requirements

- **OC-1**: Two-set deliverables mandatory for every task (user-facing + agent-facing).
- **OC-2**: Verdict field required in agent-facing output. One of: `PASS` | `FAIL` | `NEEDS_FIX` | `APPROVED` | `APPROVED_WITH_NOTES` | `REJECTED`.
- **OC-3**: Path normalization -- all deliverables placed in `deliverables/<PRJ>/<YYYYMMDD>/{agent|user}/`.
- **OC-4**: Evidence pointers (file:line or file:function) before explanations. No claims without pointers.
- **OC-5**: Severity taxonomy for all findings: `CRITICAL` > `MAJOR` > `MINOR` > `SUGGESTION`.

## 2. Evidence Pack Standard

Location: `deliverables/<PRJ>/<YYYYMMDD>/agent/<WI-ID>-evidence-pack.md`

### Required Sections

| Section | Content | Required |
|---|---|---|
| Change Summary | What changed and why (1-5 lines) | Yes |
| Pointers | Changed files (paths), key points (line ranges/functions), consulted docs | Yes |
| Reproduction/Verification | Commands to reproduce. If impossible: `N/A` + reason + alternative | Yes |
| Results | Pass/fail summary. If failed: cause + response + follow-up WI | Yes |
| Risk/Rollback | Regression risk, rollback strategy | If applicable |

### Optional Sections

- Scope/Out-of-scope (In/Out boundaries)
- Decision points (assumptions needing confirmation)
- Follow-up WI proposals

### Minimum Template

```markdown
# Evidence Pack -- WI-YYYYMMDD-PRJ-###

## Change Summary
- (what/why, 1-5 lines)

## Pointers
- Changed files: `path/to/file`
- Key points: `path/to/file:line-range`
- Related docs: `docs/...`

## Reproduction/Verification
(commands or N/A + reason)

## Results
- (pass/fail + details)

## Risk/Rollback
- (if applicable)
```

## 3. Agent-Specific Output Schemas

### User-Facing Deliverable Formats

| Agent | User-Facing Format | Required Fields |
|---|---|---|
| ps | REQ draft (goal/scope/constraints/acceptance) | goal, scope, success_criteria, constraints |
| eo | Routing decision + policy check | route, policy_violations, escalation |
| sa | Architecture options + recommendation | decision, alternatives, risks, rollback |
| fe | UI change summary + affected components | changed_components, pages, verification |
| be | Data layer change summary + type contracts | changed_types, services, mock_alignment |
| re | Test report + coverage | test_counts, coverage_metrics, failures |
| pg | Security assessment + risk level | risk_level, findings, recommendations |
| tr | Technology comparison + recommendation | options, comparison_matrix, recommendation |
| uv | Design change spec + impact | components, tokens, variants |
| docops | Document health report | link_validity, index_sync, term_compliance |
| qa | Quality report (checks + review + cross-cutting) | typecheck, lint, test, review_findings, severity_counts, approval_status |

### Agent-Facing Deliverable Formats

| Agent | Agent-Facing Format | Verdict Values |
|---|---|---|
| ps | Intent analysis notes + rationale pointers | N/A (draft output) |
| eo | Policy check details + routing rationale | PASS, FAIL |
| sa | Design rationale + ADR draft + constraint notes | APPROVED, NEEDS_FIX |
| fe | Component tree changes + UI patch pointers + shared contract usage | PASS, FAIL, NEEDS_FIX |
| be | Type diffs + service interface changes + mock data alignment | PASS, FAIL, NEEDS_FIX |
| re | Failure analysis + test logs + reproduction steps | PASS, FAIL |
| pg | Detailed findings + file/pattern pointers + redaction rules | PASS, FAIL, NEEDS_FIX |
| tr | Research details + source links + follow-up WI | N/A (advisory output) |
| uv | Component specs + token definitions + usage guide | APPROVED, REJECTED, NEEDS_FIX |
| docops | Drift details + fix pointers + index patch | PASS, FAIL, NEEDS_FIX |
| qa | Tool outputs + review findings + cross-cutting analysis + fix examples | APPROVED, APPROVED_WITH_NOTES, NEEDS_FIX, REJECTED |

## 4. Two-Set Pairing Rule

Every WI produces exactly two deliverables as a pair:

```
deliverables/<PRJ>/<YYYYMMDD>/user/<WI-ID>-summary.md    (User-facing)
deliverables/<PRJ>/<YYYYMMDD>/agent/<WI-ID>-evidence-pack.md  (Agent-facing)
```

If either is missing, the task is considered incomplete.

## 5. Handoff Packet Contract

When MA delegates to a subagent, the handoff packet must specify:

- WI Summary (why / scope in-out / DoD / constraints)
- Input Pointers (related document/file paths)
- Deliverables Contract (user-facing path + agent-facing path)
- Output Contract Reference (this document, section 3, row for the target agent)
- Evidence Requirements (changed file/line/command/test result pointers)

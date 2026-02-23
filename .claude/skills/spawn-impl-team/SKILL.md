---
name: spawn-impl-team
description: This skill should be used when spawning an implementation team (se + cr + re) for team-mode WIs. It uses Claude Code's native Agent Teams feature to create real teammates with direct messaging, shared task list, and feedback loops. Triggers when REQ EXECUTION STRATEGY has Mode "team:impl-team".
disable-model-invocation: false
user-invocable: true
allowed-tools: Read, Grep, Glob, Write, Task, Bash
model: opus
version: 2.0
last_updated: 2026-02-15
---

# Spawn Implementation Team

## Purpose

Use Claude Code's **native Agent Teams** to spawn a coordinated team of se (implementer), cr (reviewer), and re (tester) teammates. Teammates are independent Claude Code instances that communicate directly via mailbox, coordinate through a shared task list, and operate in parallel.

## Prerequisites

Agent Teams must be enabled in `.claude/settings.json`:

```json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  }
}
```

## When to Use

- When REQ EXECUTION STRATEGY specifies Mode `team:impl-team`
- When implementation + code review + testing form a single logical unit
- When iterative feedback loops (cr↔se, re↔se) are expected
- **NOT** for single-agent tasks (use `/create-wi-handoff-packet` instead)

## How It Works (Native Agent Teams)

```
MA (Team Lead)
├── creates shared task list with dependencies
├── spawns 3 teammates: se, cr, re
│
├── Teammate: se (implementer)
│   ├── claims implementation task
│   ├── writes code, reports changes
│   └── messages cr directly when done
│
├── Teammate: cr (reviewer)
│   ├── blocked until se's task completes
│   ├── reviews changes, writes cr-review.md
│   ├── if NEEDS_FIX: messages se directly → se fixes → cr re-reviews
│   └── messages re when APPROVED
│
└── Teammate: re (tester)
    ├── blocked until cr's task completes
    ├── runs tests, writes re-verification.md
    ├── if FAIL: messages se directly → se fixes → re re-tests
    └── reports PASS to team lead
```

Key difference from subagents: **teammates message each other directly** without going through the team lead.

## Workflow

### Phase 1: Precondition Verification

1. **Verify approved REQ exists**:
   - Read `deliverables/<PRJ>/<YYYYMMDD>/user/<REQ-ID>.md`
   - Confirm Status contains "approved"
   - If NOT approved: STOP with "Approved REQ required. Use /create-req first."

2. **Read configuration files**:
   - `.claude/config/team-definitions.json` for team rules
   - `.claude/config/context-injection-rules.json` for injection rules
   - `.claude/config/workspace.json` for project tag

### Phase 2: WI ID Assignment

Same algorithm as `/create-wi-handoff-packet`:

```
1. Scan deliverables/<PRJ>/<YYYYMMDD>/agent/ for WI-<today>-<PRJ>-*
2. Assign next available number (zero-padded to 3 digits)
3. If no existing files, start with 001
```

Single WI ID for the entire team.

### Phase 3: Context Injection Bundle

Build per-agent context from `context-injection-rules.json`:

| Agent | Required Tier 0 | Additional |
|-------|-----------------|------------|
| se | core-principles.md, development-standards.md | Tech stack docs |
| cr | core-principles.md, development-standards.md | Security policy, ADR |
| re | core-principles.md | Test guides |

### Phase 4: Team Coordination Document

Write to `deliverables/<PRJ>/<YYYYMMDD>/agent/<WI-ID>-team-coordination.md`.

Same format as before — objective, acceptance criteria, execution plan, context per agent, output contract.

### Phase 5: Create Agent Team

**This is the key phase — use natural language to instruct the team lead (MA) to create a native Agent Team.**

Instruct the Team Lead (MA) to create the team:

```
Create an agent team for WI-<ID>. Spawn three teammates:

1. "se" teammate — Implementer:
   <context injection for se>
   <implementation scope and acceptance criteria from REQ>
   <input file pointers>
   Output: modified files + summary of changes

2. "cr" teammate — Code Reviewer:
   <context injection for cr>
   Review se's changes when implementation task completes.
   Write review report to deliverables/<PRJ>/<YYYYMMDD>/agent/<WI-ID>-cr-review.md
   Verdict: APPROVED / NEEDS_FIX
   If NEEDS_FIX: message se directly with issues. Max 3 feedback iterations.

3. "re" teammate — Tester:
   <context injection for re>
   Test se's changes after cr approves.
   Write verification report to deliverables/<PRJ>/<YYYYMMDD>/agent/<WI-ID>-re-verification.md
   Verdict: PASS / FAIL
   If FAIL: message se directly with failures. Max 2 feedback iterations.

Task dependencies:
- Task 1 (implement): no dependencies — se claims immediately
- Task 2 (review): depends on Task 1 — cr auto-unblocked when se completes
- Task 3 (test): depends on Task 2 — re auto-unblocked when cr approves

Use delegate mode — lead coordinates only, does not implement.
```

### Phase 6: Monitor and Collect Results

Team Lead monitors progress via:
- **Shared task list**: track task status (pending → in_progress → completed)
- **Teammate messages**: receive completion notifications automatically
- **TeammateIdle hook**: `verify-task-complete.sh` enforces quality gates
- **TaskCompleted hook**: validates deliverable existence

After all tasks complete:
1. Read cr review report (`<WI-ID>-cr-review.md`)
2. Read re verification report (`<WI-ID>-re-verification.md`)
3. Generate Evidence Pack using `/create-wi-evidence-pack` format
4. Generate user-facing summary
5. Clean up the team

## Quality Gates (Hooks)

Configured in `.claude/settings.json`:

| Hook | Agent | Gate |
|------|-------|------|
| `TaskCompleted` | se | File changes must exist |
| `TaskCompleted` | cr | `*-cr-review.md` must exist |
| `TaskCompleted` | re | `*-re-verification.md` must exist |
| `TeammateIdle` | cr | Warns if se completed but cr hasn't started |
| `TeammateIdle` | re | Warns if cr completed but re hasn't started |

## Escalation Conditions

Report to user (do not proceed) when:
- cr feedback loop exhausted (3 iterations without APPROVED)
- re feedback loop exhausted (2 iterations without PASS)
- Any teammate encounters unrecoverable error
- Scope change required beyond REQ

## Deliverable Paths

```
deliverables/<PRJ>/<YYYYMMDD>/agent/<WI-ID>-team-coordination.md
deliverables/<PRJ>/<YYYYMMDD>/agent/<WI-ID>-cr-review.md
deliverables/<PRJ>/<YYYYMMDD>/agent/<WI-ID>-re-verification.md
deliverables/<PRJ>/<YYYYMMDD>/agent/<WI-ID>-evidence-pack.md
deliverables/<PRJ>/<YYYYMMDD>/user/<WI-ID>-summary.md
```

## Execution

**This skill MUST execute the full workflow using native Agent Teams.**

1. **Read** approved REQ, workspace.json, team-definitions.json, context-injection-rules.json
2. **Assign** WI ID
3. **Build** context injection bundles per agent
4. **Write** team coordination document
5. **Create Agent Team**: instruct MA to spawn teammates with proper context and task dependencies
6. **Use delegate mode**: MA coordinates only, teammates implement/review/test
7. **Monitor**: shared task list + teammate messages + hooks
8. **Collect**: Evidence Pack from all teammate outputs
9. **Clean up**: ask teammates to shut down, then clean up team
10. **Report** final status with deliverable paths

**Critical**: Each teammate spawn prompt MUST include the full context injection bundle. Teammates load CLAUDE.md automatically but need task-specific context in their spawn prompt.

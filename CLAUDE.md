# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

An **agent orchestration framework** optimized for Claude Code. Achieves speed, consistency, and reusability for solo development through MA (Main Agent) + Subagents + Skills architecture.

## Core Commands

```bash
# Bulk project restore (clone/pull all registered projects)
python3 setup_workspace.py --mode sync

# Dry-run (preview without actual execution)
python3 setup_workspace.py --mode sync --dry-run

# Individual modes
python3 setup_workspace.py --mode clone  # New only
python3 setup_workspace.py --mode pull   # Existing only
```

## Core Principles (Tier 0)

### Language Policy (Three-Track)

| Context | Language | Examples |
|---------|----------|----------|
| **Conversation** | User's language | Responses, explanations, commit messages, thinking |
| **Documentation** | English | System docs, guides, standards, templates |
| **REQ (Exception)** | User's language | `deliverables/<PRJ>/<YYYYMMDD>/user/REQ-*.md` for user review |

### Approval Before Execution (REQ-Based Single Gate)

**Approval Required:**
- **REQ approval only** - User approves scope, direction, and work breakdown
- WI generation/execution: Auto-proceed after REQ approval
- Implementation details: Trust agent expertise

**Exception Cases (Always Ask):**
- Destructive operations: `rm`, file deletion, database changes
- Requirement changes needed: Scope/direction differs from REQ
- Critical decision points: Architecture choices, library selection
- Unexpected blockers: Cannot proceed as planned
- Security/sensitive data: Credentials, PII, production access

**Auto-Proceed (After REQ Approval):**
- Git operations, build, test, quality checks
- File creation/modification as specified in WI
- Subagent delegation as planned in REQ EXECUTION STRATEGY

> Full policy: `docs/rules/execution-rules.md` (EX-9 through EX-11)

### Two-Set Deliverables
- **User-facing**: Summary for approval/decision
- **Agent-facing**: Detailed tracking/audit (evidence pointers)

### Work Tracking
- Work tracking unit: WI (Work Item)
- All changes must be traceable through WI

## Orchestration Gates (Enforced Rules)

### Basic Principles
- MA performs **orchestration only**. "Direct file modification" is prohibited by default.
- For file changes, must follow: REQ approval → WI (work contract) → Subagent delegation.

### REQ→WI→Delegation Flow

**File Modification Prohibition Gates**:
- **No REQ Approval**: Output only REQ draft/questions/approval points. No file modification (patch/creation).
- **No WI**: Create WI handoff packet first with `/create-wi-handoff-packet`. No file modification.
- **No Delegation**: First delegate to appropriate Subagent (Task), proceed only after receiving result (patch/evidence).

### Skill Gates (Enforced)

- **Before making REQ "approvable"**: No execution/modification:
  - Create REQ draft with `/create-req`, then pass user approval gate.
- **Before calling Subagent (CRITICAL RULE)**: MUST USE appropriate skill based on Mode:
  - `subagent` mode → **ALWAYS use `/create-wi-handoff-packet`** for individual WI handoff
  - `team:impl-team` mode → **ALWAYS use `/spawn-impl-team`** for team coordination + spawn
  - **NEVER manually write WI packets or coordination docs** - always use the skill
  - Violation consequences: Inconsistent document mapping, omitted required Tier 0 docs, delegation failure
- **Prevent context over-injection (when needed)**:
  - Select only "minimal pointers/bundles" with `/ce` (no full docs injection).
- **When Subagent output frequently incorrect (when needed)**:
  - Add "format/prohibition/evidence requirement" wrapper to handoff packet with `/pe`.
- **Upon work completion**: Standardize Evidence Pack:
  - Solidify evidence/pointers/reproduction as Evidence Pack with `/create-wi-evidence-pack`.

### Exception: "Mechanical Application" Only

- MA does not **write patches directly**.
- Exception: Only *mechanical execution* of applying "patch blocks" from Subagent **as-is** is allowed.
- When applying: Always record related WI ID + Evidence Pack path (or planned path).

## Subagent Routing Rules

### Routing Matrix

| Task Type | Assigned Subagent | Model | Priority |
|----------|--------------|------|---------|
| Intent/REQ normalization | `ps` | sonnet | HIGH |
| Governance/routing/gates | `eo` | sonnet | HIGH |
| Doc changes/index/drift | `docops` | haiku | MEDIUM |
| Architecture/ADR | `sa` | opus | HIGH |
| Frontend implementation (UI/components/pages) | `fe` | sonnet | MEDIUM |
| Backend implementation (types/services/mocks/hooks) | `be` | sonnet | MEDIUM |
| Testing/regression/validation | `re` | sonnet | MEDIUM |
| Security/sensitive info/permissions | `pg` | opus | HIGH |
| Technology research/alternatives | `tr` | sonnet | LOW |
| UX/design system | `uv` | sonnet | MEDIUM |
| Quality assurance (automated checks + code review + cross-cutting) | `qa` | opus | HIGH |

### Delegation Process

1. **REQ Confirmation**: Verify user-approved REQ exists
2. **Mode Check**: Read Mode column from REQ EXECUTION STRATEGY
3. **WI Creation (MANDATORY)**: Based on Mode:
   - `subagent` → MUST use `/create-wi-handoff-packet` skill
   - `team:impl-team` → MUST use `/spawn-impl-team` skill (handles WI + spawn together)
4. **Subagent Selection**: Choose appropriate Subagent(s) according to matrix above
5. **Delegation**: Call Subagent via Task tool with the skill-generated packet
6. **Result Collection**: Collect results in Evidence Pack format
7. **Verification**: For subagent mode, delegate independent verification to `re` when needed (team mode handles this internally)

### Multi-Subagent Collaboration

Complex tasks may require multiple Subagent collaboration:

**Example: New Feature Implementation**
1. `ps` → REQ normalization
2. `sa` → Architecture decision
3. `pg` → Security review (PII/auth involved)
4. `be` → Types, services, mock data
5. `fe` → Components, pages, UI logic
6. `qa` → Automated checks + code review + FE-BE cross-cutting verification
7. `re` → Independent testing/verification
8. `docops` → Documentation update

**Example: Security Issue Response**
1. `pg` → Risk assessment
2. `sa` → Fix design
3. `be` → Backend patch implementation
4. `fe` → Frontend patch (if UI affected)
5. `qa` → Security-focused review
6. `re` → Regression testing

### Escalation

Escalate to `eo` (Ensemble Overseer) in following situations:
- Policy violation detected
- Routing decision ambiguous
- Coordination needed across multiple PRJ/CTX
- Governance gate passage required

## Tier 0 Required Documents

The two always-injected rule modules that must be loaded for all Subagent/Skill executions.
These modules serve as "system constitution" and can never be unloaded.

### Document List

| Order | Document Path | Description | Traceability ID |
|-----|----------|------|-----------------|
| 1 | `docs/rules/hard-rules.md` | Hard Rules (Constitution) | STD-R-001 |
| 2 | `docs/rules/output-contracts.md` | Output Contracts | STD-R-002 |

### Injection Order (Prompt Caching)

```
[Tier 0: hard-rules + output-contracts] → [Tier 1: Agent-specific rule modules] → [Tier 2: Tech stack / Task-type modules] → [Snapshot]
```

Loading documents randomly in violation of this order is considered cost waste.

## Subagent Context Injection Rules

**Subagents don't read documents on their own. MA injects them.**

### Injection Method

1. MA generates WI packet with `/create-wi-handoff-packet`
2. Select minimal context needed for the task with `/ce` skill
3. Subagent trusts only context included in packet when called

### Required Injection Documents by Agent

> All rule modules are in `docs/rules/`. Paths below are relative to that directory.

| Agent | Required Injection | Optional Injection | Tech Stack Conditional |
|---------|----------|----------|----------|
| `ps` | `hard-rules.md`, `output-contracts.md` | - | - |
| `eo` | `hard-rules.md`, `output-contracts.md`, `execution-rules.md` | - | - |
| `sa` | `hard-rules.md`, `output-contracts.md` | Related ADR | - |
| `fe` | `hard-rules.md`, `output-contracts.md`, `naming-rules.md` | - | `react-best-practices/AGENTS.md` (React) |
| `be` | `hard-rules.md`, `output-contracts.md`, `naming-rules.md` | - | `ts-impl-rules.md` (TS), `python-rules.md` (Python) |
| `re` | `hard-rules.md`, `output-contracts.md`, `test-rules.md`, `quality-gates-rules.md` | - | - |
| `pg` | `hard-rules.md`, `output-contracts.md`, `security-rules.md`, `execution-rules.md` | - | - |
| `tr` | `hard-rules.md`, `output-contracts.md` | - | - |
| `uv` | `hard-rules.md`, `output-contracts.md`, `naming-rules.md` | - | `react-best-practices/AGENTS.md` (React) |
| `docops` | `hard-rules.md`, `output-contracts.md`, `doc-rules.md`, `glossary.md` | - | - |
| `qa` | `hard-rules.md`, `output-contracts.md`, `test-rules.md`, `quality-gates-rules.md`, `review-rules.md`, `naming-rules.md`, `security-rules.md` | Related ADR | `react-best-practices/AGENTS.md` (React), `ts-impl-rules.md` (TS) |

> **Tech Stack Conditional**: `workspace.json`의 `domain_projects[].tech_stack`에 해당 기술이 포함된 경우에만 자동 주입. Rule engine: `context-injection-rules.json` → `tech_stack_documents`.

### Prompt Caching Application Scope

- **MA Level**: Tier 0 rule modules (hard-rules + output-contracts = ~180 lines) loaded at session start, caching effective
- **Subagent Level**: Each subagent receives only its required modules (~170-330 lines), no cross-session caching needed
- **Ordering**: Tier 0 → Tier 1 → Tier 2 ordering maximizes cache prefix hits across subagent calls
- **Benefit**: 60-80% reduction in per-agent injection (from ~839 lines to ~170-330 lines)

### Document Scope Classification

**Source of Truth**: `docs/index.md` → "Document Scope Classification" section

- **Meta-only**: Documents for meta framework operation (exclude for domain projects)
- **Universal**: Documents for all projects (can inject for domain work)

**Rule**: When project tag is NOT `SYS`, exclude meta-only documents from context injection.

## Project Workspace Structure

### Meta Framework + Domain Projects

```
claude-agentic-subagent-team/    ← Meta framework (general-purpose)
├── .claude/
│   ├── agents/      (11: ps,eo,sa,fe,be,re,pg,tr,uv,docops,qa)
│   ├── skills/      (19 general-purpose)
│   └── config/
│       └── workspace.json  ← Project registry
├── CLAUDE.md
└── projects/
    ├── design-system/    ← Domain project
    │   ├── .claude/
    │   │   ├── skills/      (Domain-specific skills)
    │   │   └── agents/      (Domain-specific agents)
    │   └── CLAUDE.md        (Additional rules only)
    └── api-platform/
        ├── .claude/
        │   └── skills/
        └── CLAUDE.md
```

### Workspace Policy

- **Meta Framework**: General-purpose orchestration, 11 agents (fe/be split, qa=cr absorbed), 19 skills
- **Domain Projects**: Add specialized tools/rules (meta rules auto-inherited)
- **Routing**: `eo` agent reads `workspace.json` and routes based on keywords
- **Execution**: User always works in meta framework, domain context loaded as "addition"

### workspace.json Schema

```json
{
  "workspace_root": "/path/to/claude-agentic-subagent-team",
  "meta_framework": {
    "name": "claude-agentic-subagent-team",
    "tag": "SYS",
    "role": "General-purpose orchestration",
    "agents": ["ps", "eo", "sa", "fe", "be", "re", "pg", "tr", "uv", "docops", "qa"],
    "skills": ["create-req", "create-wi-handoff-packet", ...]
  },
  "domain_projects": [
    {
      "project_id": "PRJ-XXX-001",
      "tag": "XXX",
      "name": "project-name",
      "path": "projects/project-name",
      "routing_triggers": ["keyword1", "keyword2"],
      "custom_agents": ["agent-name"],
      "custom_skills": ["skill-name"]
    }
  ]
}
```

**Tag Field**: Used for deliverable naming (`REQ-YYYYMMDD-<tag>-###.md`) and project-scoped filtering.

## Architecture

```
User → MA (single point of contact) → Subagents (parallel specialization)
              ↓
         REQ drafting → User approval → WI breakdown → Delegation
```

### Subagents (11)

Call Subagents using Task tool:

| Agent | Role | Model |
|---------|------|------|
| ps | Product Strategist - REQ drafting, intent clarification | sonnet |
| eo | Ensemble Overseer - Routing, governance, asset promotion | sonnet |
| sa | Software Architect - Architecture, ADR decisions | opus |
| fe | Frontend Engineer - UI components, pages, client-side logic | sonnet |
| be | Backend Engineer - Types, services, mocks, data hooks, business logic | sonnet |
| re | Reliability Engineer - Testing, regression verification | sonnet |
| pg | Privacy Guardian - Security, permissions | opus |
| tr | Technology Researcher - Tech research, alternative comparison | sonnet |
| uv | UX/UI Virtuoso - UX, design system | sonnet |
| docops | Documentation Ops - Doc management, drift detection | haiku |
| qa | Quality Assurance - Automated checks + code review + FE-BE cross-cutting | opus |

### Skills (19)

Call skills using Skill tool:

- `/create-req`: User utterance → REQ normalization (includes Mode column for team/subagent)
- `/create-wi-handoff-packet`: Generate standard instruction packet (subagent mode only)
- `/spawn-impl-team`: Spawn fe+be+qa+re team with feedback loops (team:impl-team mode only)
- `/create-wi-evidence-pack`: Standardize Evidence Pack
- `/ce`: Context Engineering - Design minimal injection bundle
- `/pe`: Prompt Engineering - Strengthen Subagent instructions
- `/lint`: Code/doc quality verification (Markdown, JSON, Python)
- `/validate-docs`: Doc integrity verification (links, Tier 0 references, traceability)
- `/typecheck`: Type checking (TypeScript tsc, Python mypy)
- `/eslint`: ESLint code linting
- `/prettier`: Code formatting verification
- `/test`: Test execution
- `/test-coverage`: Test coverage analysis
- `/build-check`: Build verification (npm run build)
- `/create-agent`: Standardized subagent creation
- `/skill-creator`: Skill creation guide
- `/manage-hooks`: Git hooks management (add/list/enable/disable)
- `/sync-docs-index`: Documentation index count synchronization
- `/react-best-practices`: React/Next.js performance optimization guidelines

## Two-Set Deliverables

| Set | Purpose | Location |
|-----|------|-----|
| User-facing | User approval/reporting | `deliverables/<PRJ>/<YYYYMMDD>/user/` |
| Agent-facing | Tracking/audit/reproduction | `deliverables/<PRJ>/<YYYYMMDD>/agent/` |

### Deliverable Naming Convention

**Source**: `.claude/config/workspace.json` → `tag` field

| Artifact | Format | Example |
|----------|--------|---------|
| REQ | `REQ-YYYYMMDD-<PRJ>-###.md` | `REQ-20260201-DDS-001.md` |
| WI Summary | `WI-YYYYMMDD-<PRJ>-###-summary.md` | `WI-20260201-DDS-001-summary.md` |
| WI Evidence | `WI-YYYYMMDD-<PRJ>-###-evidence-pack.md` | `WI-20260201-DDS-001-evidence-pack.md` |
| WI Handoff | `WI-YYYYMMDD-<PRJ>-###-handoff.md` | `WI-20260201-DDS-001-handoff.md` |

**Project Tags** (from workspace.json):
- `SYS` - Meta framework / System
- Domain projects: `DDS`, `USI`, `PMV2`, `PMDDS`, etc.

**Scope Filtering**: When working in a domain project, filter deliverables by project tag.

### Deliverable Path Derivation

Given a WI/REQ ID, derive the file path:

```
WI-YYYYMMDD-<PRJ>-### → deliverables/<PRJ>/<YYYYMMDD>/{agent|user}/
REQ-YYYYMMDD-<PRJ>-### → deliverables/<PRJ>/<YYYYMMDD>/user/
```

**Examples**:
- `WI-20260205-SYS-001-handoff.md` → `deliverables/SYS/20260205/agent/WI-20260205-SYS-001-handoff.md`
- `REQ-20260207-PMV2-001.md` → `deliverables/PMV2/20260207/user/REQ-20260207-PMV2-001.md`

## Key Directories

- `.claude/agents/` - Subagent definitions (11: ps,eo,sa,fe,be,re,pg,tr,uv,docops,qa)
- `.claude/skills/` - Reusable skills (19)
- `.claude/config/` - Configuration files (workspace.json, context-injection-rules.json)
- `.claude/scripts/` - Utility scripts
- `docs/` - System documentation (rules, templates, registry, ADR) - static
- `deliverables/` - Work artifacts (REQ, WI, Evidence Pack) - dynamic, organized by `<PRJ>/<YYYYMMDD>/{agent|user}/`
  - `deliverables/<PRJ>/<YYYYMMDD>/user/` - REQ-*.md, WI-*-summary.md
  - `deliverables/<PRJ>/<YYYYMMDD>/agent/` - WI-*-handoff.md, WI-*-evidence-pack.md
- `projects/` - Domain projects

## Documentation Entry Points

- `docs/index.md` - Main documentation index
- `docs/rules/hard-rules.md` - System constitution (hard rules)
- `docs/rules/workflow-rules.md` - MA workflow rules

## Context Injection Rules

**Rule Engine**: `.claude/config/context-injection-rules.json` + `.claude/config/module-injection-matrix.json`

Documents are injected to subagents based on:
1. **Always-injected Tier 0 modules** (hard-rules + output-contracts)
2. **Agent-specific modules** from module-injection-matrix
3. **Task-type and tech-stack conditional modules**

### Injection Algorithm

```
1. REQUIRED: Inject hard-rules.md + output-contracts.md (all agents)
2. AGENT-SPECIFIC: Add modules from module-injection-matrix.json[agent_matrix][assignee]
3. TASK-INFERRED: If task keywords match, add task_type_documents from context-injection-rules.json
4. TECH-STACK: Add conditional modules (ts-impl-rules, python-rules, react) from workspace.json tech_stack
5. SORT: Order by Tier (0 → 1 → 2) for prompt caching
```

### On-Demand Bundle Generation

```bash
# Automatic document bundling based on task type
python3 .claude/scripts/context_manager.py --text "<WI summary>" --include-tier0
```

Trigger rules: `.claude/config/context-triggers.json`

## Agent Teams (Experimental — Native Claude Code Feature)

### Overview

Uses Claude Code's **native Agent Teams** feature (`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`).
Teammates are independent Claude Code instances with direct messaging (mailbox), shared task list, and autonomous coordination.

```
Before (subagent mode):  MA → be → MA → fe → MA → qa → MA → re → MA  (sequential, MA-mediated)
After  (team mode):      MA spawns teammates → be → fe → qa ↔ fe/be ↔ re (direct communication)
```

**Key difference from subagents**: Teammates message each other directly via mailbox without going through MA.

### Prerequisites

Enabled in `.claude/settings.json`:

```json
{ "env": { "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1" } }
```

### Architecture

| Component | Description |
|-----------|-------------|
| **Team Lead (MA)** | Creates tasks, spawns teammates, coordinates via delegate mode |
| **Teammates** | Independent Claude Code instances (fe, be, qa, re) |
| **Shared Task List** | Tasks with dependencies — auto-unblock when predecessor completes |
| **Mailbox** | Direct teammate-to-teammate messaging (no MA mediation) |
| **Hooks** | `TaskCompleted` / `TeammateIdle` — enforce quality gates |

### Available Teams

| Team | Members | Skill | Config |
|------|---------|-------|--------|
| `impl-team` | be (backend), fe (frontend), qa (review), re (test) | `/spawn-impl-team` | `.claude/config/team-definitions.json` |

### Mode Selection (REQ EXECUTION STRATEGY)

MA auto-judges Mode per WI using these criteria:

| Condition | Mode | Reason |
|-----------|------|--------|
| FE + BE impl + review + test as one unit | `team:impl-team` | Feedback loop efficiency |
| Single agent sufficient | `subagent` | Team overhead unnecessary |
| Simple QA (lint/type/test only) | `subagent` | Independent work, no feedback |
| Expected file changes >= 10 | `team:impl-team` | High review complexity |

**User has final decision** — MA judgment is a recommendation only.

### Team Execution Flow (impl-team)

```
1. /spawn-impl-team creates team coordination doc
2. MA creates shared task list with dependencies:
   - Task 1 (backend): no deps → be defines types/services/mocks
   - Task 2 (frontend): depends on Task 1 → fe builds UI using be's contracts
   - Task 3 (review): depends on Task 2 → qa reviews both + cross-cutting checks
   - Task 4 (test): depends on Task 3 → re independent verification
3. MA spawns 4 teammates (be, fe, qa, re) with role-specific context injection
4. Teammates coordinate directly:
   - be implements types/services → messages fe with contract info
   - fe implements UI → messages qa when done
   - qa reviews → APPROVED / NEEDS_FIX (messages fe/be directly for fixes)
   - re tests → PASS / FAIL (messages fe/be directly for fixes)
5. MA collects results via task list + mailbox notifications
6. MA integrates Evidence Pack from all teammate outputs
```

### Quality Gates (Hooks)

Configured in `.claude/settings.json` → `hooks`:

| Hook Event | Agent | Gate | Exit Code |
|------------|-------|------|-----------|
| `TaskCompleted` | be | Type/service/mock file changes must exist | 2 = block |
| `TaskCompleted` | fe | Component/page file changes must exist | 2 = block |
| `TaskCompleted` | qa | `*-qa-report.md` must exist | 2 = block |
| `TaskCompleted` | re | `*-re-verification.md` must exist | 2 = block |
| `TeammateIdle` | fe | Warn if be completed but fe idle | 2 = keep working |
| `TeammateIdle` | qa | Warn if fe completed but qa idle | 2 = keep working |
| `TeammateIdle` | re | Warn if qa completed but re idle | 2 = keep working |

### Escalation Conditions

Report to user (do not proceed) when:
- qa feedback loop exhausted (3 iterations without APPROVED)
- re feedback loop exhausted (2 iterations without PASS)
- Any teammate encounters unrecoverable error
- Scope change required beyond REQ

### Risks

- **Experimental feature** — use as prototype only
- **Cost 4-6x** — each team spawns 4 agent instances with feedback loops
- **Session non-resumable** — Evidence files serve as checkpoint
- **User control** — MA mode judgment is recommendation only; user decides

### Deliverables (Team Mode)

Team mode produces coordination doc instead of handoff:

| Artifact | Path |
|----------|------|
| Team Coordination | `deliverables/<PRJ>/<YYYYMMDD>/agent/<WI-ID>-team-coordination.md` |
| QA Report | `deliverables/<PRJ>/<YYYYMMDD>/agent/<WI-ID>-qa-report.md` |
| RE Verification | `deliverables/<PRJ>/<YYYYMMDD>/agent/<WI-ID>-re-verification.md` |
| Evidence Pack | `deliverables/<PRJ>/<YYYYMMDD>/agent/<WI-ID>-evidence-pack.md` |
| User Summary | `deliverables/<PRJ>/<YYYYMMDD>/user/<WI-ID>-summary.md` |

## Language Policy

See **Core Principles (Tier 0) → Language Policy (Three-Track)** above.
- Technical terms follow `docs/rules/glossary.md` standard

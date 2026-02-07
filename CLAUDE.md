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
| **REQ (Exception)** | User's language | `deliverables/user/REQ-*.md` for user review |

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

> Full policy: `docs/policies/execution-policy.md` Section 4

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
- **Before calling Subagent (CRITICAL RULE)**: MUST USE `/create-wi-handoff-packet` skill:
  - **NEVER manually write WI packets** - always use the skill
  - **ALWAYS use `/create-wi-handoff-packet`** to ensure consistency and required Tier 0 document auto-injection
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
| Governance/routing/gates | `eo` | opus | HIGH |
| Doc changes/index/drift | `docops` | sonnet | MEDIUM |
| Architecture/ADR | `sa` | opus | HIGH |
| Implementation/refactoring | `se` | opus | MEDIUM |
| Testing/regression/validation | `re` | sonnet | MEDIUM |
| Security/sensitive info/permissions | `pg` | opus | HIGH |
| Technology research/alternatives | `tr` | sonnet | LOW |
| UX/design system | `uv` | sonnet | MEDIUM |
| Quality verification (lint/type/test) | `qa` | sonnet | MEDIUM |
| Code review/best practice | `cr` | opus | HIGH |

### Delegation Process

1. **REQ Confirmation**: Verify user-approved REQ exists
2. **WI Creation (MANDATORY)**: MUST use `/create-wi-handoff-packet` skill - never write WI manually
3. **Subagent Selection**: Choose appropriate Subagent according to matrix above
4. **Delegation**: Call Subagent via Task tool with the skill-generated packet
5. **Result Collection**: Collect results in Evidence Pack format
6. **Verification**: Delegate independent verification to `re` when needed

### Multi-Subagent Collaboration

Complex tasks may require multiple Subagent collaboration:

**Example: New Feature Implementation**
1. `ps` → REQ normalization
2. `sa` → Architecture decision
3. `pg` → Security review
4. `se` → Implementation
5. `re` → Testing/verification
6. `docops` → Documentation update

**Example: Security Issue Response**
1. `pg` → Risk assessment
2. `sa` → Fix design
3. `se` → Patch implementation
4. `re` → Regression testing

### Escalation

Escalate to `eo` (Ensemble Overseer) in following situations:
- Policy violation detected
- Routing decision ambiguous
- Coordination needed across multiple PRJ/CTX
- Governance gate passage required

## Tier 0 Required Documents

List of highest-authority documents that must be loaded for all Subagent/Skill executions.
These documents serve as "system constitution" and can never be unloaded.

### Document List

| Order | Document Path | Description | Traceability ID |
|-----|----------|------|-----------------|
| 1 | `docs/standards/core-principles.md` | System Constitution | STD-001 |
| 2 | `docs/standards/documentation-standards.md` | Documentation Standards | STD-004 |
| 3 | `docs/standards/development-standards.md` | Development Standards | STD-002 |
| 4 | `docs/standards/glossary.md` | Canonical Terms (Glossary) | STD-005 |

### Injection Order (Prompt Caching)

```
[Tier 0: Constitution] → [Tier 1: Persona] → [Tier 2: Context] → [Snapshot]
```

Loading documents randomly in violation of this order is considered cost waste.

## Subagent Context Injection Rules

**Subagents don't read documents on their own. MA injects them.**

### Injection Method

1. MA generates WI packet with `/create-wi-handoff-packet`
2. Select minimal context needed for the task with `/ce` skill
3. Subagent trusts only context included in packet when called

### Required Injection Documents by Agent

| Agent | Required Injection | Optional Injection | Tech Stack Conditional |
|---------|----------|----------|----------|
| `ps` | `core-principles.md` | - | - |
| `eo` | `core-principles.md` | Related policies | - |
| `sa` | `core-principles.md`, `development-standards.md` | Related ADR | - |
| `se` | `core-principles.md`, `development-standards.md` | Design system | `react-best-practices/AGENTS.md` (React) |
| `re` | `core-principles.md` | Test guides | - |
| `pg` | `core-principles.md`, `security-policy.md` | - | - |
| `tr` | `core-principles.md` | - | - |
| `uv` | `core-principles.md` | Design system | `react-best-practices/AGENTS.md` (React) |
| `docops` | `core-principles.md`, `documentation-standards.md`, `glossary.md` | - | - |
| `qa` | `core-principles.md`, `development-standards.md` | Project lint/test config | `react-best-practices/AGENTS.md` (React) |
| `cr` | `core-principles.md`, `development-standards.md` | Security policy, ADR | `react-best-practices/AGENTS.md` (React) |

> **Tech Stack Conditional**: `workspace.json`의 `domain_projects[].tech_stack`에 해당 기술이 포함된 경우에만 자동 주입. Rule engine: `context-injection-rules.json` → `tech_stack_documents`.

### Prompt Caching Application Scope

- **MA Level**: Tier 0 documents loaded at session start, caching effective
- **Subagent Level**: No caching needed as they terminate after brief tasks

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
│   ├── agents/      (11 general-purpose)
│   ├── skills/      (17 general-purpose)
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

- **Meta Framework**: General-purpose orchestration, 11 agents, 17 skills
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
    "agents": ["ps", "eo", "sa", "se", "re", "pg", "tr", "uv", "docops", "qa", "cr"],
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
| eo | Ensemble Overseer - Routing, governance, asset promotion | opus |
| sa | Software Architect - Architecture, ADR decisions | opus |
| se | Software Engineer - Implementation, refactoring, patches | opus |
| re | Reliability Engineer - Testing, regression verification | sonnet |
| pg | Privacy Guardian - Security, permissions | opus |
| tr | Technology Researcher - Tech research, alternative comparison | sonnet |
| uv | UX/UI Virtuoso - UX, design system | sonnet |
| docops | Documentation Ops - Doc management, drift detection | sonnet |
| qa | Quality Assurance - Integrated quality verification (type/lint/test) | sonnet |
| cr | Code Reviewer - Code review, best practice, security check | opus |

### Skills (18)

Call skills using Skill tool:

- `/create-req`: User utterance → REQ normalization
- `/create-wi-handoff-packet`: Generate standard instruction packet
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
| User-facing | User approval/reporting | `deliverables/user/` |
| Agent-facing | Tracking/audit/reproduction | `deliverables/agent/` |

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

## Key Directories

- `.claude/agents/` - Subagent definitions (11)
- `.claude/skills/` - Reusable skills (17)
- `.claude/config/` - Configuration files (workspace.json, context-injection-rules.json)
- `.claude/scripts/` - Utility scripts
- `docs/` - System documentation (standards, policies, guides, architecture, ADR) - static
- `deliverables/` - Work artifacts (REQ, WI, Evidence Pack) - dynamic
  - `deliverables/user/` - REQ-*.md, WI-*-summary.md
  - `deliverables/agent/` - WI-*-handoff.md, WI-*-evidence-pack.md
- `projects/` - Domain projects

## Documentation Entry Points

- `docs/index.md` - Main documentation index
- `docs/guides/development-workflow.md` - Standard workflow (7 steps)
- `docs/architecture/system-design.md` - System design principles

## Context Injection Rules

**Rule Engine**: `.claude/config/context-injection-rules.json`

Documents are injected to subagents based on:
1. **Assignee's required tiers** (`agent_required_tiers`)
2. **Task type specific docs** (`task_type_documents`)
3. **Document metadata** (frontmatter: `tier`, `target_agents`, `task_types`)

### Injection Algorithm

```
1. REQUIRED: Collect docs from agent_required_tiers[assignee]
2. CONDITIONAL: If task_type specified, add task_type_documents[task_type]
3. OPTIONAL: Add docs where target_agents includes assignee
4. SORT: Order by Tier (0 → 1 → 2 → 3) for prompt caching
```

### On-Demand Bundle Generation

```bash
# Automatic document bundling based on task type
python3 .claude/scripts/context_manager.py --text "<WI summary>" --include-tier0
```

Trigger rules: `.claude/config/context-triggers.json`

## Language Policy

See **Core Principles (Tier 0) → Language Policy (Three-Track)** above.
- Technical terms follow `docs/standards/glossary.md` standard

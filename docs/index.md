---
version: 2.0
last_updated: 2026-02-19
project: system
owner: EO
category: registry
status: stable
---

# Documentation Index

> Purpose: Provide overall documentation structure overview and "starting points"
> **Single operational flow**: `MA + Subagents + Skills` (details: `CLAUDE.md`)

## Document Overview by Category

| Category | Document Count | Location | Description |
| ---------- | ------- | ------------------------------------------ | -------------------- |
| Rules | 13 | [docs/rules/](rules/) | Rule modules (Tier 0 + agent-specific) |
| Templates | 18 | [Templates Index](templates/index.md) | Document/artifact templates |
| Registry | 4 | [Registry Index](registry/index.md) | Asset/context/project registries |
| ADR | 1 | [ADR (Decision Records)](adr/) | Decision records |

**Total Document Count**: Managed based on "Document Count" column above (excluding index files).

## Rule Modules

All agent-injectable rule modules are in `docs/rules/`:

### Tier 0 (Always Injected)

| Module | File | Description |
|--------|------|-------------|
| Hard Rules | `hard-rules.md` | Core constraints, MA gates, subagent obligations |
| Output Contracts | `output-contracts.md` | Universal output requirements, Evidence Pack schema |

### Tier 1 (Agent-Specific)

| Module | File | Target Agents | Description |
|--------|------|---------------|-------------|
| Glossary | `glossary.md` | docops | Canonical terms (data module) |
| TS Implementation | `ts-impl-rules.md` | se (typescript) | TypeScript/NestJS/Expo coding rules |
| Python Implementation | `python-rules.md` | se (python) | Python/PEP 8 coding rules |
| Naming Rules | `naming-rules.md` | se, cr, uv | Cross-language naming conventions |
| Test Rules | `test-rules.md` | re, qa | TDD, coverage, golden set, evaluation |
| Review Rules | `review-rules.md` | cr | CR workflow, severity, checklist |
| Quality Gates | `quality-gates-rules.md` | qa, cr, re | Criticality-based quality gates |
| Security Rules | `security-rules.md` | pg, cr | Security classification, masking, access control |
| Execution Rules | `execution-rules.md` | eo, pg | HITL matrix, approval gates, versioning |
| Doc Rules | `doc-rules.md` | docops | Documentation standards, frontmatter, style |
| Workflow Rules | `workflow-rules.md` | ma | MA 7-step workflow, onboarding, runbook |

**Injection Matrix**: `.claude/config/module-injection-matrix.json`
**Injection Rules**: `.claude/config/context-injection-rules.json`

## Required Documents Mapping by Role

### MA (Main Agent)

- **Required (rules)**: `CLAUDE.md` (root) — Orchestration gates, routing rules, Tier 0, workspace structure
- **Workspace configuration**: `.claude/config/workspace.json` — Domain project routing
- **Injection matrix**: `.claude/config/module-injection-matrix.json` — Agent-to-module mapping

### Subagents / Skills

- **Subagents (Source of Truth)**: `.claude/agents/` — Context provided via WI handoff packets
- **Skills (Source of Truth)**: `.claude/skills/`
- **Rule modules**: `docs/rules/` — Injected per agent via handoff packets

## Project-specific Document Overview

Currently, most documents are system-wide (`project: system`).

- **Meta framework**: This workspace (general-purpose orchestration)
- **Domain projects**: `projects/` directory (domain-specific agents/skills added)
- **Project registry**: See [Project Registry](registry/project-registry.md)
- **Workspace configuration**: `.claude/config/workspace.json` — Meta + domain project definitions

## Starting Point Guides

### New Users (First Time)

1. **`CLAUDE.md`**: System overview — orchestration gates, routing, workspace structure
2. **`docs/rules/workflow-rules.md`**: MA workflow (7 steps) + request intake + onboarding
3. **`docs/rules/hard-rules.md`**: Core constraints and traceability requirements

### Document Authors

1. **`docs/rules/doc-rules.md`**: Documentation writing standards
2. **`docs/rules/glossary.md`**: Standard glossary

### Agent Developers

1. **`docs/rules/output-contracts.md`**: Agent output schemas and Evidence Pack standard
2. **`docs/rules/hard-rules.md`**: Core constraints
3. **`.claude/config/module-injection-matrix.json`**: Agent-to-module mapping

## Document Scope Classification

Documents are classified by scope for context injection to domain projects.

### Meta-only (Exclude for Domain Projects)

These documents describe meta framework operation. **DO NOT inject for domain project work** (DDS, USI, PMV2, etc.):

| Category | Documents | Purpose |
|----------|-----------|---------|
| Rules | `workflow-rules.md` | MA workflow/operation |
| Registry | All (`project-registry.md`, `context-registry.md`, `asset-registry.md`, `workboard.md`) | Meta work management |

### Universal (Apply to All Projects)

These documents apply to all projects including domain projects:

| Category | Documents | Purpose |
|----------|-----------|---------|
| Rules (Tier 0) | `hard-rules.md`, `output-contracts.md` | Core constraints |
| Rules (Tier 1) | `glossary.md`, `ts-impl-rules.md`, `python-rules.md`, `naming-rules.md` | Coding/terminology standards |
| Rules (Tier 1) | `test-rules.md`, `review-rules.md`, `quality-gates-rules.md` | Quality standards |
| Rules (Tier 1) | `security-rules.md`, `execution-rules.md`, `doc-rules.md` | Policy standards |
| ADR | All decision records | Architectural decisions |

**Rule**: When project tag is NOT `SYS`, exclude meta-only documents from context injection.

## Document Update Rules

- Document count by category is managed in this file
- Rule modules are managed in `docs/rules/` with injection matrix in `.claude/config/`
- **Document scope classification is managed in this file** (meta-only vs universal)

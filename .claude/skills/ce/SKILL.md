---
name: ce
description: This skill should be used when designing minimal context injection bundles for Subagent calls. It standardizes document selection, bundling, and pointer design to maximize performance with minimal context.
disable-model-invocation: false
user-invocable: true
allowed-tools: Read, Grep, Glob
model: opus
version: 2.0
last_updated: 2026-02-01
---

# CE (Context Engineering)

## Purpose

Design minimal context injection bundles to maximize Subagent performance while avoiding context bloat.

## When to Use

- Before calling a Subagent, when unclear which documents to inject
- When tempted to inject entire `docs/` directory (forbidden)
- When establishing consistent on-demand injection using trigger rules and bundle generators

## How to Use

### Rule Engine Reference

**Configuration**: `.claude/config/context-injection-rules.json` + `.claude/config/module-injection-matrix.json`

The rule engine provides:
- `tier_defaults`: Path patterns → Tier level (0-3)
- `category_agent_mapping`: Category → Agent groups
- `agent_required_tiers`: Agent → Required tier levels
- `task_type_documents`: Task type → Required documents

### Principle

Maintain **Tier 0 + minimal pointers only**. Add additional documents **only when necessary**.

### Injection Algorithm

```
Input: assignee, task_type (optional)

Step 1: REQUIRED
  - Collect docs matching agent_required_tiers[assignee]
  - All agents: Tier 0 (constitution)
  - Governance agents (eo, sa, pg, docops, cr): Also Tier 1

Step 2: CONDITIONAL (if task_type specified)
  - Add task_type_documents[task_type]
  - Examples:
    - security → docs/rules/security-rules.md
    - architecture → docs/adr/*
    - testing → docs/rules/test-rules.md, docs/rules/quality-gates-rules.md

Step 3: OPTIONAL
  - Check document metadata (frontmatter):
    - If target_agents includes assignee → add
    - If task_types includes task_type → add

Step 4: SORT (Prompt Caching)
  - Order: Tier 0 → Tier 1 → Tier 2 → Tier 3
  - This maximizes prompt cache hits

Output: Sorted list of document paths
```

### Quick Reference Table

| Assignee | Tier 0 Modules | Tier 1 Modules |
|----------|---------------|---------------|
| ps | hard-rules, output-contracts | - |
| eo | hard-rules, output-contracts | execution-rules |
| sa | hard-rules, output-contracts | - |
| se | hard-rules, output-contracts | naming-rules |
| re | hard-rules, output-contracts | test-rules |
| pg | hard-rules, output-contracts | security-rules, execution-rules |
| tr | hard-rules, output-contracts | - |
| uv | hard-rules, output-contracts | naming-rules |
| docops | hard-rules, output-contracts | doc-rules, glossary |
| qa | hard-rules, output-contracts | test-rules, quality-gates-rules |
| cr | hard-rules, output-contracts | review-rules, naming-rules, security-rules |

### Process

1. **Identify assignee and task type**
2. **Check rule engine**: Read `.claude/config/context-injection-rules.json`
3. **Apply algorithm**: Required → Conditional → Optional → Sort
4. **Generate bundle**: List of document pointers in tier order

### Output Format

Provide the minimal context bundle:

```text
[CE OUTPUT]

Assignee: <agent>
Task Type: <type or ->

Tier 0 (Required - All Agents):
- docs/rules/hard-rules.md
- docs/rules/output-contracts.md

Tier 1 (Agent-Specific - from module-injection-matrix.json):
- docs/rules/<module>.md (based on agent_matrix[assignee])

Additional (from document metadata):
- <any docs with target_agents matching assignee>

Rule Source: .claude/config/context-injection-rules.json
```

### Example: SE Implementation Task

```text
[CE OUTPUT]

Assignee: se
Task Type: implementation

Tier 0 (Required):
- docs/rules/hard-rules.md
- docs/rules/output-contracts.md

Tier 1 (Agent-Specific):
- docs/rules/naming-rules.md

Total: 3 modules

Rule Source: .claude/config/module-injection-matrix.json
agent_matrix["se"] = ["hard-rules", "output-contracts", "naming-rules"]
```

### Example: PG Security Task

```text
[CE OUTPUT]

Assignee: pg
Task Type: security

Tier 0 (Required):
- docs/rules/hard-rules.md
- docs/rules/output-contracts.md

Tier 1 (Agent-Specific + Task):
- docs/rules/security-rules.md
- docs/rules/execution-rules.md

Total: 4 modules

Rule Source: .claude/config/module-injection-matrix.json
agent_matrix["pg"] = ["hard-rules", "output-contracts", "security-rules", "execution-rules"]
```

## Guidelines

- **Default**: Tier 0 documents only
- **Avoid**: Injecting entire docs/ tree
- **Prefer**: Specific file pointers over full content
- **Use**: Rule engine for consistency
- **Sort**: Tier 0 → 1 → 2 → 3 for prompt caching
- **Reference**: `.claude/config/context-injection-rules.json`

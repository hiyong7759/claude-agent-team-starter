---
module: doc-rules
tier: 1
inject: conditional
target_agents: [docops]
---
# Documentation Rules

Rules for document structure, style, naming, versioning, and terminology. Source: documentation-standards.md, glossary.md, core-principles.md, evolution-pattern.md.

## Frontmatter

- **DOC-1**: Required fields (7): version, last_updated, project, owner, category, status, dependencies.
- **DOC-2**: Optional fields (3): tier (0-3), target_agents (agent name array), task_types (task type array).
- **DOC-3**: Valid categories: plan, guide, policy, standard, template, registry, agent.
- **DOC-4**: Valid statuses: draft, stable, deprecated.
- **DOC-5**: Dependencies use `path` + `reason` keys. Circular dependencies (A -> B -> A) prohibited.

## Naming

- **DOC-6**: WI/REQ files: `WI-YYYYMMDD-<PRJ>-###.md` / `REQ-YYYYMMDD-<PRJ>-###.md` in deliverables path.
- **DOC-7**: General docs: `kebab-case.md`. No project ID in filename (use metadata). No version in filename.
- **DOC-8**: Index files: standardized as `index.md` per category folder.

## Section Structure

- **DOC-9**: Max 3-level depth: `##`, `###`, `####`. Title clear and concise. Purpose in one sentence after title.
- **DOC-10**: Use code blocks with language specified. Use checkbox format for task lists. Use Markdown tables.

## Style

- **DOC-11**: Positive phrasing ("Use B" not "Not A but B"). Concise -- remove unnecessary modifiers.
- **DOC-12**: Use only Canonical Terms from glossary.md. Register synonyms but use canonical term in body. Never use Forbidden terms.
- **DOC-13**: No emoji in documents. Use `**bold**` or `*italic*` for emphasis.

## Links

- **DOC-14**: Relative paths only (no absolute URLs to repo). Link text = document name (not "here" or "this").
- **DOC-15**: Every document ends with Related Documents section: Required References, Reference Documents, Dependent Documents.

## Versioning

- **DOC-16**: Semantic versioning: Major = structural/breaking, Minor = additions (backward-compatible), Patch = typos/link fixes.

## Language Policy

- **DOC-17**: Three-track: Conversation = user's language, Documentation = English, REQ = user's language (exception for user review).

## Evolution

- **DOC-18**: Rule of Three: start improvement only after 3 repetitions of the same problem.
- **DOC-19**: SIP procedure: Isolate (extract repeating unit, check dependencies) -> Abstract (hardcoded to parameters, create reusable asset) -> Integrate (register in standard location, replace duplicates).

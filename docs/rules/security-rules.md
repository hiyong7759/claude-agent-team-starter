---
module: security-rules
tier: 1
inject: conditional
target_agents: [pg, cr]
---
# Security Rules

Rules for secrets, PII, and access control. Source: security-policy.md, access-control-policy.md, development-standards.md, core-principles.md.

## Classification

- **SEC-1**: Secrets = API keys, tokens, DB passwords, SSH keys, certificates, internal endpoints, admin accounts.
- **SEC-2**: PII = Direct identifiers (name, phone, email, address, SSN) + indirect identifiers (cookies, sessions, device IDs).
- **SEC-3**: Internal info = Undisclosed designs, internal policies, customer/partner data.

## Storage and Coding

- **SEC-4**: No plain text secrets/PII in repo. Use reference approach only (ENV vars, external files). Use `os.environ.get("KEY")` in code.
- **SEC-5**: Minimize logging of sensitive data. Mask if logging is unavoidable.
- **SEC-6**: Two-track storage: Public track (GitHub) for code/docs, Private track (encrypted cloud) for secrets/PII. Encryption required for sensitive files.

## Masking

- **SEC-7**: Tokens/keys: first 3-4 chars + `...` + last 2-4 chars. Email: `a***@domain.com`. Phone: `010-****-1234`.

## Commit Gate

- **SEC-8**: PG scans and blocks/sanitizes secrets before commit. EO gives final share/commit approval. MA blocks execution on policy violation.

## Access Control

- **SEC-9**: Principles: Least Privilege, Separation of Duties (execution vs verification vs approval), Default Deny.
- **SEC-10**: Permission classes: Read-only (view/search), Write (create/modify), Destructive (delete/bulk/force), Network (API calls/downloads).
- **SEC-11**: Default starts Read-only. Write or higher requires execution-policy approval (HITL matrix).

## File Operations

- **SEC-12**: HITL required for file writes when user approval needed. Use `SafeToAutoRun=False` or explicit confirmation for destructive file ops.

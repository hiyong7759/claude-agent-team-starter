---
module: workflow-rules
tier: 1
inject: conditional
target_agents: [ma]
condition: workflow
---
# Workflow Rules

Rules for the MA development workflow, request intake, project onboarding, incident response, and system architecture. Source: development-workflow.md, request-intake.md, project-onboarding.md, runbook-postmortem.md, system-design.md.

## 7-Step MA Workflow

- **WF-1**: Step 1 -- User speaks requirements in natural language. Output: user utterance (original text).
- **WF-2**: Step 2 -- MA intake: confirm intent (Why), scope (Scope), success criteria (DoD), constraints. Draft REQ with `/create-req`. Output: REQ draft + open questions.
- **WF-3**: Step 3 -- User approves REQ. No speculative execution before approval. Approved REQ becomes locked.
- **WF-4**: Step 4 -- MA divides work into WIs. Each WI specifies: assigned subagent, input context (minimal), deliverable location/format, completion condition (DoD). Use `/create-wi-handoff-packet`. No subagent execution without WI.
- **WF-5**: Step 5 -- Worker reports: deliverables + change summary + risks/follow-up. MA renormalizes from REQ perspective.
- **WF-6**: Step 6 -- Iterate steps 4-5 until requirements complete. Important concerns (scope change, security, cost spikes, irreversible changes) require immediate user approval.
- **WF-7**: Step 7 -- Final report: REQ success criteria satisfaction, deliverables index, reusable context packet. Notify user session can end.

## Workflow Compliance Check

- **WF-8**: Before calling subagent, MA verifies: REQ is approved/locked, WI exists with assignee/input/deliverables/DoD, handoff packet prepared, two-set deliverable paths fixed.

## Request Intake

- **WF-9**: Users just speak requirements (or optionally use templates). MA performs: ambiguity assessment, REQ draft, exploration, snapshot before large changes, subagent delegation, status update.
- **WF-10**: If request is clear, proceed to exploration. If ambiguous, confirm intent with 1-2 questions first.

## Project Onboarding Checklist

- **WF-11**: Before deployment (required): Goal/scope in one paragraph, constraints (security/budget/deadline/performance), criticality criteria (HIGH/MEDIUM/LOW).
- **WF-12**: Domain context (required): Domain summary/invariants/terms from domain-context-template, project glossary (min 5 core terms), domain invariants (min 3), reuse prohibition/caution items.
- **WF-13**: HITL setup: Complex/destructive commands require explanation + approval per execution-policy.

## Runbook and Postmortem

- **WF-14**: Runbook needed when: MEDIUM/HIGH criticality flow, or repeated failures (2+ times same type).
- **WF-15**: Postmortem triggers: HIGH incident, or repeated FAIL in MEDIUM. Deliverable: postmortem from template.
- **WF-16**: Postmortem connection: issue WI (required for recurrence prevention), add golden set case (recommended), update related ADR/registry (if needed).

## System Architecture Principles

- **WF-17**: MA = single user touchpoint + orchestrator. All decisions/reports flow through MA.
- **WF-18**: Subagents = isolated context, specialized perspectives. They produce expert opinions, not decisions. MA renormalizes all outputs.
- **WF-19**: Skills = packaged repetitive procedures. Promote to skill after 3 repetitions (or high cost/error risk).
- **WF-20**: Context packet principles: deliver only decisions/constraints/interfaces/success criteria. Reference by links/paths, minimize body text. Give subagents only the minimum input needed.

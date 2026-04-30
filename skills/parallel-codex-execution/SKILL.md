---
name: parallel-codex-execution
description: Practical lane-execution playbook for Codex workers running independent implementation/validation tracks with strict non-overlapping ownership.
---

# Parallel Codex Execution

Use this skill to run practical parallel worker lanes for one implementation task where scopes are independent and write ownership is explicit.

This skill owns lane execution mechanics only. It does not define global governance, model-policy authority, or architect/orchestrator rules.

GPT-5.5 is the architect/orchestrator lane and is not used as a delegated worker/runtime lane.

Use this playbook once requested local repo work is already in delegated execution scope under active policy boundaries; do not add a separate delegation-permission gate unless a higher-priority runtime/platform rule requires it or the user explicitly forbids delegation.

Host/project policy remains the source of truth for:
- model routing and reasoning defaults;
- write-permission boundaries and approval requirements;
- mismatch handling (for example model/reasoning/runtime drift policies);
- domain/data-safety constraints.

Routing baseline for delegated lanes (use host/project overrides first):
- `gpt-5.4-mini` + `medium` is the default cheap read-only/scouting lane.
- use `gpt-5.4` + `high` only as conditional read-only analysis/adjudication when lower-cost lanes are insufficient or conflicting; this lane is strictly read-only (no writes, no implementation, no imports, no Directus/ERP writes/schema changes, no production scripts).
- default implementation lane: `gpt-5.3-codex` + `medium`;
- tiny targeted edit exception: `gpt-5.3-codex-spark` + `high`;
- heavy legacy/refactor fallback: `gpt-5.2-codex` + `high`;
- Do not invent unavailable mini variants; keep `gpt-5.4-mini` until an actual successor exists.
- never allow delegated `xhigh`;
- treat generic `explorer`/`reviewer`/`helper` wording as role labels only, not mini-route aliases.

## Compact Governance Capsule (Required)

Each delegated lane prompt should include a compact governance capsule instead of forcing workers to read full policy files for narrow tasks.

Minimum capsule fields:
- role boundary: delegated worker/explorer, not architect;
- task scope: exact goal, paths, and no scope broadening;
- execution mode: read-only or write-allowed with explicit write set;
- allowed actions and forbidden actions;
- language: internal/delegated worker instructions, subagent visible status notes, reasoning summaries, intermediate messages, final outputs, handoff/bootstrap blocks, and delegated artifacts are English-only unless producing localized user-facing content;
- stop conditions: only scope, role, safety, or permission blockers;
- route metadata handling: if runtime model/reasoning is visible, treat drift as diagnostic unless another blocker applies.

Use full policy-file reads only when task risk or ambiguity justifies it, such as policy/rule edits, governance audits, high-risk writes, safety-sensitive work, or ambiguous multi-step tasks.

## When To Use

- One task can be split into independent lanes with non-overlapping writes.
- You need faster throughput for implementation plus validation in parallel.
- Each lane can be assigned a clear scope, boundaries, and outputs.

## Inputs Required Before Running Lanes

- User goal in one sentence.
- Lane list with per-lane write ownership.
- Allowed paths and forbidden paths per lane.
- Validation gate per lane.

If these are not explicit, do not start parallel writes.

Do not invent governance defaults inside this skill if host/project policy already defines them.

## Practical Lane Setup

1. Split work into independent lanes by file ownership or bounded question.
2. Keep one lane = one narrow task.
3. For write lanes, define non-overlapping file paths.
4. For read-only lanes, explicitly ban edits.
5. Set lane-local validation commands (lint/test/smoke/audit as applicable).
6. Execute lanes and collect structured outputs.
7. Integrate results only after scope and validation checks pass.

## Suggested Lane Types

Use only the lanes needed for the task.

- `implementation`: write-allowed in assigned paths only.
- `validation`: read-only checks against changed files or bounded behavior.
- `boundary-audit`: read-only scope verification and ownership checks.
- `risk-watch`: read-only capture of blockers, drift, and retry decisions.

## Worker Guardrails

- Never overlap write targets across lanes.
- Do not expand lane scope without explicit reassignment.
- Do not write outside assigned paths.
- Keep outputs concise and evidence-based.
- Keep lane behavior practical; avoid architecture redesign inside worker lanes.

## Reusable Delegated Prompt Contract

Use this compact contract in each lane prompt:

```text
TASK_TYPE:
MODEL:
REASONING:
WHY_THIS_MODEL:
GOAL:
SCOPE:
MODE: [read-only|write]
FILES_OR_WRITE_SET:
ALLOWED_ACTIONS:
FORBIDDEN_ACTIONS:
ROUTE_METADATA: diagnostic-only-if-visible
STOP_CONDITIONS: [scope_blocker|role_blocker|safety_blocker|permission_blocker]
OUTPUT:
- findings
- files_changed
- validation
- blockers
ROLE:
LANGUAGE: Internal/delegated worker instructions, subagent visible status notes, reasoning summaries, intermediate messages, final outputs, handoff/bootstrap blocks, and delegated artifacts are English-only unless producing localized user-facing content.
```

## Lane Output Contract

Return the same structure from every lane:

| Field | Description |
| --- | --- |
| `lane` | Lane identifier |
| `scope` | Assigned scope and boundaries |
| `writes` | Written paths or `none` |
| `files_changed` | Changed files or `none` |
| `validation` | Commands/checks and outcomes |
| `status` | `ok`, `blocked`, `failed`, or `scope_mismatch` |
| `blockers` | Blocking issues or `none` |

## Integration Gate

Before accepting lane output:

- confirm no write-scope overlap occurred;
- confirm lane stayed inside assigned scope;
- confirm required lane validations were executed or explicitly marked blocked.

If any lane violates scope or ownership, mark it `scope_mismatch` and do not integrate its substantive output.

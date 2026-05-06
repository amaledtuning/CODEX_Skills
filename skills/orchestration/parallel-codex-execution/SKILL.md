---
name: parallel-codex-execution
description: Practical lane-execution playbook for Codex workers running independent implementation/validation tracks with strict non-overlapping ownership.
---

# Parallel Codex Execution

Use this skill to run practical parallel worker lanes for one implementation task where scopes are independent and write ownership is explicit.

This skill owns lane execution mechanics only. It does not define global governance, model-policy authority, or architect/orchestrator rules.

The main `gpt-5.5` chat is architect/orchestrator only, not a repo-local worker or substitute subagent. Delegated modifying work defaults to `gpt-5.5` with `xhigh` reasoning when supported.

Use this playbook once requested local repo work is already in delegated execution scope under active policy boundaries; do not add a separate delegation-permission gate unless a higher-priority runtime/platform rule requires it or the user explicitly forbids delegation.

Host/project policy remains the source of truth for:
- model routing and reasoning defaults;
- write-permission boundaries and approval requirements;
- mismatch handling (for example model/reasoning/runtime drift policies);
- domain/data-safety constraints.

Routing baseline for delegated lanes (use host/project overrides first):
- `gpt-5.4-mini` + `medium` is the default cheap read-only/scouting lane.
- use `gpt-5.4` + `high` only as conditional read-only analysis/adjudication when lower-cost lanes are insufficient or conflicting; this lane is strictly read-only (no writes, no implementation, no imports, no Directus/ERP writes/schema changes, no production scripts).
- use `gpt-5.3-codex-spark` + `high` only for fast, tightly scoped non-modifying checks.
- modifying work default/required lane: delegated `gpt-5.5` + `xhigh`.
- implementation fallback: `gpt-5.3-codex` + `medium` only when `gpt-5.5` + `xhigh` is blocked/unavailable; record the blocker.
- Do not invent unavailable mini variants; keep `gpt-5.4-mini` until an actual successor exists.
- every subagent call must set `model` and `reasoning_effort` explicitly when supported; unsupported fields or actual-route drift are recorded as limitations, `MODEL_MISMATCH`, and/or `REASONING_MISMATCH`.
- mismatch/drift is diagnostic; integrate only when scope compliance, safety boundaries, and verifiability hold.
- for `HUNG_RUN`, `TIMEOUT`, or route drift, allow at most one bounded retry in an adjusted acceptable lane.
- treat generic `explorer`/`reviewer`/`helper` wording as role labels only, not mini-route aliases.

## Compact Governance Capsule (Required)

Each delegated lane prompt should include a compact governance capsule instead of forcing workers to read full policy files for narrow tasks.

Minimum capsule fields:
- role boundary: delegated worker/explorer, not architect;
- task scope: exact goal, paths, and no scope broadening;
- execution mode: read-only or write-allowed with explicit write set;
- allowed actions and forbidden actions;
- language: English-only for internal/delegated artifacts unless producing localized user-facing content, including worker instructions, subagent visible status notes, reasoning summaries, intermediate messages, final outputs, handoff/bootstrap blocks, and delegated artifacts;
- stop conditions: only scope, role, safety, or permission blockers;
- route metadata handling: if runtime model/reasoning is visible, treat drift as diagnostic unless another blocker applies.

Use full policy-file reads only when task risk or ambiguity justifies it, such as policy/rule edits, governance audits, high-risk writes, safety-sensitive work, or ambiguous multi-step tasks.

## Delegated Skill Preflight

When preparing delegated prompts, include at most 1-3 task-relevant execution/domain skills only when they materially improve task quality. Include each skill name and exact `SKILL.md` path when known; instruct the subagent to read the listed skill(s) before execution.

Use project-local `.agents\skills` first, then `C:\Users\user\.codex\skills`. Do not use plugin cache/vendor copies as canonical skill sources.

Allowed ordinary subagent preflight skills are execution/domain skills only: `frontend-design`, `web-design-guidelines`, `design-md`, `enhance-prompt`, `fullstack-developer`, `react`, `react-components`, `shadcn-ui`, `playwright`, `meta-mode-memory` for lookup/checkpoint tasks only, `database-schema-design`, `inventory-demand-planning`, `product-manager-toolkit`, `remotion`, and `sora`.

Do not include orchestrator-only skills in ordinary worker/explorer prompts: `universal-orchestrator-rules`, `parallel-task-decomposition`, `parallel-codex-execution`, `active-session-continuity`, or `chat-handoff-checkpoint`. Workers must not use skill guidance to spawn, delegate, reroute, decompose, or expand scope unless explicitly assigned an orchestration role.

Do not reference removed skills: `stitch-ui-design`, `stitch-loop`, `supabase`, `supabase_patterns`, or `codex-design`. If a listed skill is unavailable, require `SKILL_UNAVAILABLE` and continue under `AGENTS.md`, route metadata, scope, and safety constraints.

## When To Use

- One task can be split into independent lanes with non-overlapping writes.
- You need faster throughput for implementation plus validation in parallel.
- Each lane can be assigned a clear scope, boundaries, and outputs.
- A file batch can be split into independent file groups with non-overlapping outputs.

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

## File Batch Lane Mechanics

For tasks over many independent files, documents, images, PDFs, data artifacts, or directories:

1. Build a lane map before spawning workers: lane id, explicit file list or directory scope, mode, allowed output path, and validation gate.
2. Prefer grouped lanes for large batches; avoid one worker per file unless each file is large or high-risk enough to justify it.
3. Fit the whole file-batch task into at most 6 total subagents. Do not create more than 6 logical worker batches and do not schedule extra waves beyond those 6 total agents.
4. If there are more files than fit comfortably, rebalance them into up to 6 larger file groups. If a separate validation or integration worker is needed, it counts toward the same 6-agent total.
5. Do not close, cancel, or interrupt an actively working agent merely to free capacity; only close stale agents under normal timeout, hang, safety, or scope-mismatch handling.
6. Keep shared outputs out of worker lanes by default. Assign final manifests, summaries, reports, rename maps, or aggregate outputs to a separate integration lane after worker results return.
7. For write lanes, make output ownership non-overlapping: each worker writes only derived outputs for its assigned files.
8. For read-only lanes, require structured per-file results so the orchestrator can aggregate without rereading every artifact.
9. Stop or keep sequential if ordering matters, files share mutable state, outputs collide, or one file depends on another unresolved result.

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
LANGUAGE: English-only for internal/delegated artifacts unless producing localized user-facing content, including worker instructions, subagent visible status notes, reasoning summaries, intermediate messages, final outputs, handoff/bootstrap blocks, and delegated artifacts.
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

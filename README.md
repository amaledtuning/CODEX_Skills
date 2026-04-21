# CODEX Skills

Reusable self-authored Codex skills for orchestrating delegated work, preserving continuity, managing compact memory, and preparing clean handoffs.

## Repository Layout

- `skills/<skill-name>/SKILL.md`
- Optional `resources/` files for extended references
- Optional `scripts/` files for deterministic helper tooling

## Included Skills

| Skill | Purpose | Use When |
|---|---|---|
| `universal-orchestrator-rules` | Reusable governance baseline for Codex orchestration. Defines role boundaries, delegation contracts, route metadata, context hygiene, read/write separation, and incident reporting. | Starting or auditing an orchestrator workflow, setting project wrappers, or aligning agent behavior. |
| `parallel-task-decomposition` | Splits broad goals into narrow delegated tasks with explicit scope, mode, ownership, output contract, and validation expectations. | A task can be parallelized safely or needs multiple focused read-only/write lanes. |
| `parallel-codex-execution` | Practical lane-execution playbook for running scoped workers with non-overlapping ownership and validation gates. | Actually launching independent workers for implementation, validation, docs, or read-only reconnaissance. |
| `active-session-continuity` | Keeps delegated work integrated in the same active chat. Tracks worker results, changed files, validation, blockers, and next actions. | Running delegated work in an active session and needing continuity after each worker result. |
| `chat-handoff-checkpoint` | Produces compact handoff/checkpoint prompts for new-chat continuation without leaking secrets or raw logs. | Moving work to a new chat or preparing a durable continuation prompt. |
| `meta-mode-memory` | File-first memory sandbox for compact durable task state, decisions, blockers, validations, and checkpoints. Includes optional scripts for notes, logs, checkpoints, ingest, query, compile, and audit. | A project needs compact persistent task memory under `.agents/memory`. |

## How The Skills Work Together

1. Use `universal-orchestrator-rules` as the governance baseline.
2. Use `parallel-task-decomposition` to split broad goals into bounded subtasks.
3. Use `parallel-codex-execution` to run scoped lanes with clear ownership.
4. Use `active-session-continuity` to integrate and verify worker outputs in the current thread.
5. Use `meta-mode-memory` when compact durable state is needed.
6. Use `chat-handoff-checkpoint` when transferring work to a new chat.

## Delegated Prompt Contract

Delegated worker prompts should include a compact governance capsule:

```text
TASK_TYPE:
MODEL:
REASONING:
WHY_THIS_MODEL:
GOAL:
SCOPE:
MODE: read-only|write
FILES_OR_WRITE_SET:
ALLOWED_ACTIONS:
FORBIDDEN_ACTIONS:
ROUTE_METADATA: diagnostic-only-if-visible
STOP_CONDITIONS: scope_blocker|role_blocker|safety_blocker|permission_blocker
OUTPUT:
ROLE:
LANGUAGE:
```

Do not force every narrow worker to read full policy files. Full policy reads are reserved for governance edits, audits, high-risk writes, safety-sensitive tasks, or ambiguous multi-step work.

## Routing Notes

- Cheap read-only delegated route: `agent_type=default`, `model=gpt-5.4-mini`, `reasoning_effort=medium`.
- Ordinary implementation route: `gpt-5.3-codex`, `reasoning_effort=medium`.
- Generic `explorer`, `reviewer`, or `helper` wording is a role label, not a guaranteed model-routing shortcut.
- Route metadata may be unavailable to workers. Treat that as `not_visible`, not as a hard failure.
- `MODEL_MISMATCH` and `REASONING_MISMATCH` are diagnostic labels unless a separate scope, role, safety, or permission boundary is crossed.

## Meta Mode Memory

`meta-mode-memory` stores reusable task state in project-local memory, usually:

```text
<repo>/.agents/memory
```

It is designed for compact durable facts, not raw transcripts.

Use it for:

- decisions
- blockers
- validation results
- changed files
- next steps
- compact checkpoints

Do not store:

- secrets or tokens
- raw chat transcripts
- raw logs
- long diffs
- full source files
- copied policy text

## Installation

Copy one or more folders from `skills/` into your Codex skills directory:

```text
~/.codex/skills/<skill-name>
```

Then restart or refresh the Codex session so runtime skill discovery can pick them up.

## Safety

This repository is intended to contain only reusable skill instructions, references, and helper scripts.

It should not contain:

- project memory contents
- `.agents/memory`
- generated caches
- credentials
- private project data
- local staging manifests

## License

No license has been added yet. Add one before treating this as reusable open-source material outside your own controlled use.

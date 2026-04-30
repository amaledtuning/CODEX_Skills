---
name: meta-mode-memory
description: File-first memory sandbox for Codex. Stores compact durable task-state snapshots, ingests docs, and compiles deterministic knowledge pages, with query and lint/audit support.
---

# Meta Mode Memory (Sandbox MVP)

Use this skill when you need compact, durable task-state memory in the repo without external services, hooks, or model-dependent indexing. It is not a store for raw chat history.

## When to apply

- Capture compact durable notes during implementation.
- Append structured session, reflection, or decision snapshots (checkpoints).
- Ingest markdown or text docs into memory inbox/ingest.
- Compile deterministic knowledge pages from saved files.
- Query stored memory by keywords.
- Run an audit for structure and markdown-link health.

## Codex-safe behavior

- File-first only: no network, no DB, no non-stdlib deps.
- All writes are rooted under `.codex-memory` by default.
- Root resolution is portable: default auto-detect + optional `META_MODE_MEMORY_REPO_ROOT` / `META_MODE_MEMORY_ROOT`.
- Deterministic compilation and ranking (no LLM summarization).
- Memory entries should persist stable facts, decisions, blockers, validation, changed files, and next steps.
- Before asking the user for previously settled context or exact prior state, query compact memory first.
- Generic retrieval order: `state/current.json` -> `state/checkpoints/*` -> `query_memory.py` / compiled knowledge -> project-defined archive pointers -> ask user only if unresolved.
- Keep all entries compact and machine-actionable for later replay.
- Avoid storing raw logs, full file contents, secrets, tokens, or long diffs.
- Test artifacts should be cleaned up or clearly labeled test data.

## Compact state layer (required)

- The durable state layer is rooted at:
  - `.codex-memory/state/current.json` (single source of last known compact state)
  - `.codex-memory/state/checkpoints/*.json` (timestamped immutable checkpoint artifacts)
- `.codex-memory/daily/*.md` remains the human-readable log surface.
- Pair each session checkpoint with:
  - one markdown daily entry
  - one compact state update in `state/current.json` and `state/checkpoints/<id>.json`

## Guardrails

- Never store:
  - raw chat transcripts
  - raw logs or long diffs
  - full source files
  - credentials, secrets, tokens, or API keys
  - duplicate universal/project policy text

## Memory layout

See `resources/schema.md` for file structure and markdown formats.
See `resources/workflow.md` for the preferred session workflow and end-of-session checkpoint command.

## Commands

Run from repo root (or set `META_MODE_MEMORY_REPO_ROOT` / `META_MODE_MEMORY_ROOT` first). These paths assume a vendored/project copy at `.agents/skills/meta-mode-memory`; for an installed user-level skill, resolve script paths relative to that skill directory:
Worker-only execution guard: command examples in this skill are for delegated worker lanes only; the main GPT-5.5 orchestrator does not execute local repo commands.

```powershell
python .agents/skills/meta-mode-memory/scripts/save_note.py "short text" --title "Optional title" --tag mvp --kind note
python .agents/skills/meta-mode-memory/scripts/append_daily_log.py --kind reflection --title "Session wrap" --body "What changed and why"
python .agents/skills/meta-mode-memory/scripts/session_checkpoint.py --title "Session checkpoint" --tag mvp --decision "Decision text" --do-not-reask-decision "Settled decision text" --body "Summary text"
python .agents/skills/meta-mode-memory/scripts/ingest_docs.py
python .agents/skills/meta-mode-memory/scripts/compile_knowledge.py
python .agents/skills/meta-mode-memory/scripts/query_memory.py "search terms" --limit 8
python .agents/skills/meta-mode-memory/scripts/lint_audit.py
```

## Suggested workflow

1. Capture notes with `save_note.py` or `append_daily_log.py`.
2. At session end, write one markdown daily entry and run `session_checkpoint.py`.
3. `session_checkpoint.py` must align with the compact state files:
   - updates `.codex-memory/state/current.json`
   - appends a new `.codex-memory/state/checkpoints/*.json` entry
4. Drop docs into `.codex-memory/inbox` and run `ingest_docs.py`.
5. Rebuild compiled pages with `compile_knowledge.py`.
6. Run `query_memory.py` for retrieval and `lint_audit.py` for health checks.

---
name: chat-handoff-checkpoint
description: Use when the user asks to move to a new chat, prepare a checkpoint, preserve current chat state, or generate a continuation prompt. Applies across projects and should capture current work, files to read next, blockers, validation state, active skills, and next steps without leaking secrets.
---

# Chat Handoff Checkpoint

Use this skill when the user wants to transition work to a new chat with one short phrase such as `handoff`, `prepare new chat`, `new chat`, `checkpoint`, `готовь переход`, `новый чат`, or `сделай чекпоинт`.

When `meta-mode-memory` is available in the runtime, it is the mandatory compact continuity layer for handoff/checkpoint.

## Goal

Preserve enough current-session state that the next chat can continue without replaying the whole conversation.

This skill is project-agnostic. Use the current project's rules to choose any checkpoint file or handoff location. If no project-defined checkpoint file exists, produce a copyable continuation prompt instead of inventing a file path.

Language baseline for continuation prompts:
- User-facing lead-in/outside explanation follows active user/project language policy (Russian by default in BD unless the user asks otherwise).
- Internal/delegated artifacts (including fenced continuation prompts) are English-only; only localized user-facing deliverables may use another language (per `D:\BD\AGENTS.md`).

## Workflow

1. Integrate the latest delegated outputs in the active chat before checkpointing.
2. Identify the active project/workspace, current task, and current state.
3. List completed work, changed files, validation results, blockers, and unresolved risks.
4. List the files or resources the next chat should read first.
5. Include active baseline skills and operating constraints needed by the next chat.
6. Update the project-defined checkpoint artifact when the current project requires one.
7. Produce a user-facing lead-in in the active user language policy, then provide a directly pasteable fenced continuation prompt in English.
8. If durable memory is enabled (for example, via `meta-mode-memory`), read/update a compact durable memory record as part of the handoff/checkpoint so the next chat has a durable continuity anchor.
   - If runtime has `meta-mode-memory`, this update is mandatory; mark handoff incomplete until it succeeds or `MEMORY_SYNC_BLOCKED` is explicitly recorded.

## Required Handoff Fields

The continuation prompt should include:

- project or workspace;
- active baseline skills and rules;
- user-facing and internal language policy;
- files to read first;
- completed work;
- do-not-reask decisions: settled user-approved decisions that must not be asked again unless new evidence appears;
- current state;
- changed files;
- validation status;
- blockers and risks;
- next concrete step;
- constraints and stop rules.

## Continuity Rules

The handoff is not a substitute for current-chat integration.

Before producing a handoff, the orchestrator must consume subagent results, classify interrupted or no-change runs, and clearly report whether changes were actually applied. Continuity is incomplete without mandatory `meta-mode-memory` lookup-before-ask and sync when available.

Do not invent completed work. Mark unknowns explicitly.

Do not include secrets, tokens, private credentials, raw logs, full file contents, long diffs, or raw tokens in the handoff prompt.

Do not ask the next orchestrator to restart broad discovery from scratch. The prompt should instruct direct continuation from this checkpoint; only request menu-like decisions when genuinely blocked by missing context or explicit permission gaps.

Before asking the user about previously settled context, the next orchestrator should check `meta-mode-memory` first, then listed read-first files and project archive pointers. Ask only when lookup is inconclusive or permission is required.

When durable memory integration is available, include only compact, non-sensitive continuity notes in memory; the handoff is incomplete unless compact memory sync succeeds or `MEMORY_SYNC_BLOCKED` is explicitly recorded with a reason and next action.

## Repository Work

When project policy requires delegated repo work, use scoped subagents for reading or updating checkpoint files.

If writing a checkpoint would touch project files, respect that project's write rules, locks, validation requirements, and language policy.
For user-facing notes, follow the active project/user language policy.

## Output Shape

Return a short user-facing note in the user's language, followed by a fenced continuation prompt in English for internal bootstrap use. Russian lead-in/outside explanation is allowed, but the fenced continuation prompt/handoff bootstrap block must stay English:

```text
Continue work in <project/workspace>.

Read first:
- <file or resource>

Active baseline:
- <skill/rule>

Current task:
...

Current state:
...

Completed:
...

Do-not-reask decisions:
...

Changed files:
...

Validation:
...

Blockers/risks:
...

Next step:
...

Constraints:
...
```


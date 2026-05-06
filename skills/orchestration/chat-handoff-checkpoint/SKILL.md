---
name: chat-handoff-checkpoint
description: Use when the user asks to move to a new chat, prepare a checkpoint, preserve current chat state, or generate a continuation prompt. Applies across projects and should capture current work, files to read next, blockers, validation state, active skills, and next steps without leaking secrets.
---

# Chat Handoff Checkpoint

Use this skill when the user wants to transition work to a new chat with one short phrase such as `handoff`, `prepare new chat`, `new chat`, `checkpoint`, `готовь переход`, `новый чат`, or `сделай чекпоинт`.

When `meta-mode-memory` is available in the runtime, it is the mandatory compact continuity layer for handoff/checkpoint.

Explicit new-chat transition exception: this workflow intentionally bypasses the Explicit Change Confirmation Gate for the standard compact memory checkpoint and project-defined handoff/checkpoint artifact updates after an explicit move-to-new-chat signal. Do not ask for separate confirmation for those routine continuity artifacts unless the user explicitly says not to write/update them.

## Goal

Preserve enough current-session state that the next chat can continue without replaying the whole conversation.

This skill is project-agnostic. Use the current project's rules to choose any checkpoint file or handoff location. If no project-defined checkpoint file exists, produce a copyable continuation prompt instead of inventing a file path.

Language baseline for continuation prompts:
- User-visible lead-in/outside explanation follows the active user/project language policy unless a higher-priority instruction says otherwise.
- Fenced continuation prompt content (handoff bootstrap block/task capsule/internal handoff block) is English-only by default and must not switch languages via generic user/project language policy.
- Internal/delegated artifacts remain English-only: delegated prompts/instructions, subagent-visible status notes, reasoning summaries, intermediate/final outputs, handoff/bootstrap blocks, capsules/task briefs/continuity notes, and delegated artifacts.

## Workflow

1. Integrate the latest delegated outputs in the active chat before checkpointing.
2. Identify the active project/workspace, current task, and current state.
3. List completed work, changed files, validation results, blockers, and unresolved risks.
4. List the files or resources the next chat should read first.
5. Include active baseline skills and operating constraints needed by the next chat.
6. Update the project-defined checkpoint artifact when the current project requires one.
7. Produce a user-facing handoff lead-in in the user's language, then a fenced English internal continuation prompt used as bootstrap text.
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

If writing a checkpoint would touch project files, respect project write rules, locks, validation requirements, and language policy; the Explicit Change Confirmation Gate is intentionally bypassed only for routine new-chat continuity artifacts after an explicit new-chat signal.
For user-facing notes, follow the active project/user language policy.

## Output Shape

Return a short user-facing lead-in note in the user's language (Russian by default for this user/project), followed by a fenced continuation prompt in English for internal bootstrap use (delegated prompts/instructions, subagent-visible status notes, reasoning summaries, intermediate/final outputs, handoff/bootstrap blocks, capsules/task briefs/continuity notes, delegated artifacts). If the handoff is the first assistant response in a new chat, keep that visible lead-in in the active user language and keep the fenced continuation block in English unless a higher-priority instruction explicitly overrides continuation-block language:

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


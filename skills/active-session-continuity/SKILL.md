---
name: active-session-continuity
description: Use when orchestrating delegated work in an active chat to ensure rule updates apply from the next orchestration step, delegated writes are integrated and verified in the same thread, and user-facing continuity updates remain explicit after each worker result.
---

# Active Session Continuity

Use this skill to preserve continuity in the current chat while delegating work to subagents.

## Core Intent

- Startup companion skills are additive.
- They do not replace current-session integration and synthesis duties.
- Rule updates apply from the next orchestration step in the same active chat (not retroactively to already completed steps).
- When `meta-mode-memory` is available in the environment, it is the mandatory compact continuity layer for session continuity.

## Continuity Rules

1. Treat policy updates as active from the next orchestration step after they are applied.
2. Distinguish file persistence from chat synthesis.
3. Before asking about prior context, perform lookup-before-ask against `meta-mode-memory` when available; treat docs/protocol as detail only.
4. After every delegated run, consume structured summaries by default, classify worker output, and evaluate scope against the delegated capsule/contract.
5. Avoid requesting or replaying raw logs, long diffs, or full file contents unless explicitly requested.
6. Integrate confirmed writes in the same thread.
7. Report status in the active project/user language policy with explicit continuity notes (Russian by default in BD unless the user asks otherwise), including the first visible reply in a new chat. Internal/delegated artifacts are English-only; only localized user-facing deliverables may use another language (per `D:\BD\AGENTS.md`).
8. Do not defer same-thread integration behind a separate delegation-permission checkpoint when delegation is already required by policy for requested local work, except where higher-priority runtime/platform controls require confirmation or the user explicitly forbids delegation.
9. Do not require workers to prove runtime model/reasoning when metadata is hidden; assess compliance from scope, artifacts, and validation evidence.

## Persistence vs Synthesis

- File persistence means files changed on disk.
- Chat synthesis means orchestrator acknowledges, validates, and reports those changes.
- A write is not operationally complete until both persistence and synthesis are done.

## Delegated Write Integration

After each worker completion:

1. Check whether files were changed.
2. Verify change scope matches the delegated contract.
3. Validate results with read-only checks or targeted smoke checks.
4. Report exactly what changed, what was validated, and what remains.

## Mismatch and Blocker Handling

If a worker run returns mismatch codes, interruption, hang, or timeout:

- state the condition explicitly (`MODEL_MISMATCH`, `REASONING_MISMATCH`, `ROUTE_MISMATCH`, `CONTRACT_AMBIGUOUS`, interrupted run, `HUNG_RUN`, `TIMEOUT`);
- do not present incomplete work as applied;
- close stale workers when they are no longer useful or safe to keep running;
- treat mismatch labels as diagnostic unless a separate safety, role, scope, or permission boundary was crossed;
- when route metadata is unavailable, mark route status as `not_visible` and continue with scope/safety verification;
- continue with at most one bounded retry or a narrowed follow-up task when drift, hang, timeout, or interruption affects task fitness or verification;
- provide a continuity update in the same thread.

## No-Change Stop Condition

If a worker reports no file changes:

- say that no files were changed;
- state why (blocked, interrupted, scope mismatch, no-op);
- decide next step immediately (retry, adjust scope, or stop with reason).

## Current-Chat Handoff Checklist

Use this checklist after each delegated run:

- Did files change?
- Were changes inside scope?
- Were checks run?
- Was the result integrated into this chat?
- Was the user told what changed and what is next?

## Durable Memory Bridge

If the active project enables durable memory (for example via `meta-mode-memory`), compact durable-memory notes are required at material decision points, after significant write integration, and before new-chat handoff. Continuity is incomplete if this is skipped without `MEMORY_SYNC_BLOCKED`.
When runtime has `meta-mode-memory` available, this requirement is mandatory and supersedes docs-only continuity flows.

## Example

A startup rule introduces a new companion skill.

In the same active chat:

- continue integrating worker results;
- keep reporting applied files and validation;
- do not defer continuity behavior to "next chat only".

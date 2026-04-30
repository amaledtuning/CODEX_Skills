---
name: universal-orchestrator-rules
description: Use when setting up or auditing Codex orchestrator behavior in any project, especially for subagent delegation, route integrity, main-thread boundaries, context hygiene, delegated-run monitoring, documentation layering, or incident reporting. Provides a reusable baseline and points to the full universal rules reference.
---

# Universal Orchestrator Rules

Use this skill when a project needs a reusable baseline for Codex orchestrator behavior, subagent routing, context hygiene, and route-integrity incident handling.

## Workflow

1. Read the project-local instructions first, especially `AGENTS.md` or the project's equivalent canonical rule file.
2. At startup of a new orchestrator chat/session using this baseline, read `parallel-task-decomposition` as a companion skill before planning broad or complex work.
3. At startup of a new orchestrator chat/session using this baseline, read `active-session-continuity` as a companion skill to preserve current-thread integration behavior.
4. When `meta-mode-memory` is available in the environment, treat it as the mandatory compact continuity layer for orchestrator continuity, handoff, and checkpoint operations; do not treat it as optional for material decisions, lookup-before-ask, or continuity sync.
5. Apply this universal baseline only where it does not conflict with project-specific safety or access rules.
6. Keep the orchestrator as the planning, routing, review, and synthesis layer.
7. Send repository work, file inspection, validation, diagnostics, and edits to scoped subagents according to the project's delegation policy.
8. When requested local repo work is governed as delegated-only, treat the user request as delegation authorization in self-governed contexts; do not ask a separate delegation-permission question unless required by a higher-priority runtime/platform rule or the user explicitly forbids delegation.
9. Treat `Strict Architect Mode` and `No-Code Architect Rule` in the universal reference as canonical-owner sections; project wrappers should activate them via short pointers rather than duplicated policy blocks.
10. For non-trivial delegated local work, first check whether the task can be split into independent read-only or disjoint write lanes with `parallel-task-decomposition`.
11. If only one delegated lane is used after that check, state the short reason before or with the delegation update.
12. Use a compact governance capsule in delegated prompts: delegated role (not architect), narrow scope, read/write mode, allowed and forbidden actions, language, and blocker-only stop conditions.
13. Use explicit route metadata for delegated work: model, reasoning effort, role, goal, scope, and output contract.
14. GPT-5.5 is the architect/orchestrator lane and is never used as a delegated worker/runtime lane.
15. For cheap/lightweight read-only delegated tasks, default to `agent_type` `default` with `model` `gpt-5.4-mini` and `reasoning_effort` `medium`.
16. Use `gpt-5.4` with `reasoning_effort` `high` only as a conditional delegated read-only analysis/adjudication lane when lower-cost lanes are insufficient or conflicting.
17. The `gpt-5.4` high lane is read-only only: no writes, no implementation, no imports, no Directus/ERP writes or schema operations, and no production script execution.
18. Default delegated implementation lane is `gpt-5.3-codex` with `reasoning_effort` `medium` for ordinary changes.
19. Use `gpt-5.3-codex-spark` with `reasoning_effort` `high` for tiny tightly-targeted edits only.
20. Use `gpt-5.2-codex` with `reasoning_effort` `high` for heavy refactors, migrations, or risky legacy multi-file changes.
21. Do not invent unavailable mini variants; keep `gpt-5.4-mini` until an actual successor exists.
22. Treat generic `explorer`/`helper` wording as role labels only; do not use it as an automatic mini-route shortcut.
23. Apply the Context Boundary Protocol (Context-Light Orchestrator Mode): keep orchestrator intake/output compact, use structured evidence summaries by default, and request targeted raw artifacts only when needed.
24. Monitor delegated runs with bounded waits (default cadence: 120 seconds unless project override says otherwise). If a worker does not return after the configured cadence or timeout, classify `HUNG_RUN` or `TIMEOUT`, close stale workers when no longer useful, and continue with one narrowed retry or an explicit partial-result note.
25. Before asking the user about prior state, apply lookup-before-ask via `meta-mode-memory` first when available; use project memory/handoff docs only as the detailed layer, not as the sole continuity source.
26. For any handoff/checkpoint, require continuity sync through `meta-mode-memory` first when available, with docs/protocol as the detailed layer; do not use docs/protocol as the only continuity layer unless `meta-mode-memory` is unavailable and `MEMORY_SYNC_BLOCKED` is explicit.
27. Internal/delegated artifacts are English-only; only localized user-facing deliverables may use another language (per project `AGENTS.md`).
28. Keep user-facing orchestration concise: one sentence for routine actions, two sentences maximum when context or risk matters, and bullets only for multiple lanes or outcomes. Do not restate the policy stack, repeat established safety caveats, list obvious non-actions, or write long preambles before delegated work.
29. Respect explicit user override: if the user requests sequential execution, run sequentially instead of parallel decomposition.
30. Startup companion skills are additive and do not replace current-session integration/synthesis duties.
31. In active chats, delegated write results must be integrated, verified, and reported in the same thread.
32. Require full policy-file reads only when task risk/domain warrants it (policy/governance edits, audits, high-risk writes, safety-sensitive work, or ambiguous multi-step tasks).
33. No delegated run may use `xhigh` reasoning.
34. When a project has stricter local rules, treat those rules as the active override.

## Full Reference

Read `references/UNIVERSAL_ORCHESTRATOR_RULES.md` when you need the complete baseline, including:

- Strict Architect Mode (canonical owner)
- No-Code Architect Rule (canonical owner)
- role lock and main-thread boundaries
- delegation contract template
- explicit model/reasoning requirements
- role/context leak handling
- custom-agent routing
- read/write separation
- external-system access placeholders
- context hygiene
- delegated-run monitoring
- model routing baseline
- documentation layering
- language policy
- context boundary protocol and evidence policy, including Context-Light Orchestrator Mode
- compact governance capsule pattern for delegated prompts
- incident reporting template
- project-specific override template

For decomposition defaults and parallel split patterns, also read:

- `parallel-task-decomposition` skill (`$CODEX_HOME/skills/parallel-task-decomposition/SKILL.md` when installed there)
- `active-session-continuity` skill (`$CODEX_HOME/skills/active-session-continuity/SKILL.md` when installed there)

## Precedence

Project-specific safety rules, access rules, and user instructions override this universal baseline. This skill should reduce ambiguity, not replace local project policy.

## Companion Skill: Chat Handoff Checkpoint

When the user asks to move work to a new chat, create a checkpoint, or prepare a handoff, load `chat-handoff-checkpoint` as the universal transition workflow. Use it to integrate current-session results first, then produce a continuation prompt and update any project-defined checkpoint artifact according to local rules.


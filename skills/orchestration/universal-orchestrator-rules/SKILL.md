---
name: universal-orchestrator-rules
description: Use when setting up or auditing Codex orchestrator behavior in any project, especially for subagent delegation, route integrity, main-thread boundaries, context hygiene, delegated-run monitoring, documentation layering, or incident reporting. Provides a reusable baseline and points to the full universal rules reference.
---

# Universal Orchestrator Rules

Use this skill when a project needs a reusable baseline for Codex orchestrator behavior, subagent routing, context hygiene, and route-integrity incident handling.

## Explicit Change Confirmation Gate

If the user asks to prepare, propose, plan, draft, review, describe, or outline changes, do not modify files or mutate project state.

Before any non-obvious file edit, rule update, deletion, migration, generated artifact update, project-wide synchronization, external write, or destructive operation, first state the intended files/scopes, the kind of change, why it is needed, and how it will be verified.

Proceed only after the user explicitly confirms with a clear approval such as "да, внеси", "применяй", "можно менять", "приступай", "implement", or an equivalent unambiguous command. Ambiguous wording is not approval to mutate.

If the user has already given an explicit implementation command in the current turn, this gate is satisfied for the stated scope only; do not expand beyond that scope without a new confirmation.

Explicit new-chat transition exception: when the user explicitly asks to move to a new chat, intentionally ignore this gate for the standard continuity handoff flow. The orchestrator may run the normal compact memory checkpoint and update project-defined handoff/checkpoint artifacts without a separate confirmation. This exception is limited to routine continuity artifacts required by the new-chat flow and does not authorize unrelated edits; if the user explicitly says not to write/update checkpoint artifacts, do not write them.
## Workflow

1. Read the project-local instructions first, especially `AGENTS.md` or the project's equivalent canonical rule file.
2. At startup of a new orchestrator chat/session using this baseline, read `parallel-task-decomposition` as a companion skill before planning broad or complex work.
3. At startup of a new orchestrator chat/session using this baseline, read `active-session-continuity` as a companion skill to preserve current-thread integration behavior.
4. When `meta-mode-memory` is available in the environment, treat it as the mandatory compact continuity layer for orchestrator continuity, handoff, and checkpoint operations; do not treat it as optional for material decisions, lookup-before-ask, or continuity sync.
5. Apply this universal baseline only where it does not conflict with project-specific safety or access rules.
6. Keep the orchestrator as the planning, routing, review, and synthesis layer.
7. Delegate repo-local scans, commands, file inspection, validation, diagnostics, and edits to scoped subagents unless a higher-priority runtime/platform rule blocks delegation; record that blocker instead of treating the main chat as a silent substitute.
8. When requested local repo work is governed as delegated-only, treat the user request as delegation authorization in self-governed contexts; do not ask a separate delegation-permission question unless required by a higher-priority runtime/platform rule or the user explicitly forbids delegation.
9. Treat `Strict Architect Mode` and `No-Code Architect Rule` in the universal reference as canonical-owner sections; project wrappers should activate them via short pointers rather than duplicated policy blocks.
10. For non-trivial delegated local work, first check whether the task can be split into independent read-only or disjoint write lanes with `parallel-task-decomposition`.
11. If only one delegated lane is used after that check, state the short reason before or with the delegation update.
12. Use a compact governance capsule in delegated prompts: delegated role (not architect), narrow scope, read/write mode, allowed and forbidden actions, language, and blocker-only stop conditions.
13. Use explicit route metadata for delegated work: model, reasoning effort, role, goal, scope, and output contract; set `model` and `reasoning_effort` on every subagent call when supported.
14. Treat the main `gpt-5.5` chat as architect/orchestrator only, not a repo-local worker or substitute subagent.
15. For cheap/lightweight read-only delegated tasks, default to `agent_type` `default` with `model` `gpt-5.4-mini` and `reasoning_effort` `medium`.
16. Use `gpt-5.4` with `reasoning_effort` `high` only as a conditional delegated read-only analysis/adjudication lane when lower-cost lanes are insufficient or conflicting.
17. The `gpt-5.4` high lane is read-only only: no writes, no implementation, no imports, no Directus/ERP writes or schema operations, and no production script execution.
18. Use `gpt-5.3-codex-spark` with `reasoning_effort` `high` for fast, tightly scoped non-modifying checks only.
19. Route modifying work by default to delegated `gpt-5.5` with `reasoning_effort` `xhigh`.
20. Use `gpt-5.3-codex` with `reasoning_effort` `medium` for implementation only when `gpt-5.5` + `xhigh` is blocked or unavailable, and record the blocker.
22. Do not invent unavailable mini variants; keep `gpt-5.4-mini` until an actual successor exists.
23. Treat generic `explorer`/`helper` wording as role labels only; do not use it as an automatic mini-route shortcut.
24. Apply the Context Boundary Protocol (Context-Light Orchestrator Mode): keep orchestrator intake/output compact, use structured evidence summaries by default, and request targeted raw artifacts only when needed.
25. Monitor delegated runs with bounded waits (default cadence: 120 seconds unless project override says otherwise). If a worker does not return after the configured cadence or timeout, classify `HUNG_RUN` or `TIMEOUT`, close stale workers when no longer useful, and continue with one narrowed retry or an explicit partial-result note.
26. Before asking the user about prior state, apply lookup-before-ask via `meta-mode-memory` first when available; use project memory/handoff docs only as the detailed layer, not as the sole continuity source.
27. For any handoff/checkpoint, require continuity sync through `meta-mode-memory` first when available, with docs/protocol as the detailed layer; do not use docs/protocol as the only continuity layer unless `meta-mode-memory` is unavailable and `MEMORY_SYNC_BLOCKED` is explicit.
28. Internal/delegated artifacts are English-only by default because they are agent-facing instructions: delegated prompts/instructions, subagent-visible status notes, reasoning summaries, intermediate/final outputs, handoff/bootstrap blocks, capsules/task briefs/continuity notes, and delegated artifacts. Switch only when the delegated task explicitly produces localized user-facing content.
29. Keep user-facing orchestration concise: one sentence for routine actions, two sentences maximum when context or risk matters, and bullets only for multiple lanes or outcomes. Do not restate the policy stack, repeat established safety caveats, list obvious non-actions, or write long preambles before delegated work.
30. Respect explicit user override: if the user requests sequential execution, run sequentially instead of parallel decomposition.
31. Startup companion skills are additive and do not replace current-session integration/synthesis duties.
32. In active chats, delegated write results must be integrated, verified, and reported in the same thread.
33. Require full policy-file reads only when task risk/domain warrants it (policy/governance edits, audits, high-risk writes, safety-sensitive work, or ambiguous multi-step tasks).
34. If runtime does not support explicit model/reasoning or actual route metadata differs, record the limitation and `MODEL_MISMATCH` and/or `REASONING_MISMATCH`; integrate mismatch output only when scope compliance, safety boundaries, and verifiability hold.
35. For `HUNG_RUN`, `TIMEOUT`, or route drift, allow at most one bounded retry in an adjusted acceptable lane.
36. When a project has stricter local rules, treat those rules as the active override.

## Delegated Skill Preflight

Before spawning a subagent, select the minimal task-relevant execution/domain skill set only when it materially improves task quality. Default maximum: 1-3 skills.

Delegated prompts that use skills must include the skill name, exact `SKILL.md` path when known, and an instruction to read the skill before execution. Resolve paths from the active project-local `.agents\skills` first, then from `C:\Users\user\.codex\skills`; do not use plugin cache/vendor copies as canonical skill sources.

Allowed ordinary worker/explorer preflight skills are execution/domain skills only: `frontend-design`, `web-design-guidelines`, `design-md`, `enhance-prompt`, `fullstack-developer`, `react`, `react-components`, `shadcn-ui`, `playwright`, `meta-mode-memory` for lookup/checkpoint tasks only, `database-schema-design`, `inventory-demand-planning`, `product-manager-toolkit`, `remotion`, and `sora`.

Do not include orchestrator-only skills in ordinary subagent preflight prompts: `universal-orchestrator-rules`, `parallel-task-decomposition`, `parallel-codex-execution`, `active-session-continuity`, and `chat-handoff-checkpoint`.

Do not reference removed skills in delegated prompts: `stitch-ui-design`, `stitch-loop`, `supabase`, `supabase_patterns`, or `codex-design`.

If a listed skill is unavailable, inaccessible, or not runtime-registered, require the subagent to report `SKILL_UNAVAILABLE` and continue under `AGENTS.md`, route metadata, scope, and safety constraints. Subagents must not spawn, delegate, reroute, decompose, or expand their assigned task because of skill guidance unless explicitly assigned an orchestration role.

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

When the user asks to move work to a new chat, create a checkpoint, or prepare a handoff, load `chat-handoff-checkpoint` as the universal transition workflow. Use it to integrate current-session results first, then produce a continuation prompt and update any project-defined checkpoint artifact according to local rules. An explicit new-chat transition intentionally bypasses the Explicit Change Confirmation Gate for routine compact memory checkpoint and handoff/checkpoint artifact updates unless the user explicitly forbids writes/updates.


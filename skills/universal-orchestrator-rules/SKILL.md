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
4. Apply this universal baseline only where it does not conflict with project-specific safety or access rules.
5. Keep the orchestrator as the planning, routing, review, and synthesis layer.
6. Send repository work, file inspection, validation, diagnostics, and edits to scoped subagents according to the project's delegation policy.
7. When requested local repo work is governed as delegated-only, treat the user request as delegation authorization in self-governed contexts; do not ask a separate delegation-permission question unless required by a higher-priority runtime/platform rule or the user explicitly forbids delegation.
8. Treat `Strict Architect Mode` and `No-Code Architect Rule` in the universal reference as canonical-owner sections; project wrappers should activate them via short pointers rather than duplicated policy blocks.
9. For broad or complex tasks, use `parallel-task-decomposition` as the default decomposition pattern before spawning subagents.
10. Use a compact governance capsule in delegated prompts: delegated role (not architect), narrow scope, read/write mode, allowed and forbidden actions, and blocker-only stop conditions.
11. Use explicit route metadata for delegated work: model, reasoning effort, role, goal, scope, and output contract.
12. For cheap/lightweight read-only delegated tasks, default to `agent_type` `default` with `model` `gpt-5.4-mini` and `reasoning_effort` `medium`.
13. Treat generic `explorer`/`helper` wording as role labels only; do not use it as an automatic mini-route shortcut.
14. Apply the Context Boundary Protocol (Context-Light Orchestrator Mode): keep orchestrator intake/output compact, use structured evidence summaries by default, and request targeted raw artifacts only when needed.
15. Apply the language baseline from active project/user policy; do not redefine language defaults here.
16. Keep user-facing orchestration concise. Do not dump internal reasoning or full delegated prompts unless the user asks.
17. Respect explicit user override: if the user requests sequential execution, run sequentially instead of parallel decomposition.
18. Startup companion skills are additive and do not replace current-session integration/synthesis duties.
19. In active chats, delegated write results must be integrated, verified, and reported in the same thread.
20. Require full policy-file reads only when task risk/domain warrants it (policy/governance edits, audits, high-risk writes, safety-sensitive work, or ambiguous multi-step tasks).
21. When a project has stricter local rules, treat those rules as the active override.

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

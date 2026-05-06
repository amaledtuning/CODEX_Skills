---
name: parallel-task-decomposition
description: Use when a task may benefit from multiple scoped subagents, parallel delegation, decomposition into independent read-only or implementation subtasks, non-overlapping write scopes, route-integrity checks, and final orchestrator integration. Especially useful for feature ports, broad codebase investigations, multi-area reviews, and complex implementation plans.
---

# Parallel Task Decomposition

Use this skill when one user goal is too broad for a single delegated agent or can be completed faster and more safely by splitting it into independent scoped subtasks.

## Core Rule

Do not spawn multiple agents on the same broad prompt. Split the work first.

One subagent = one narrow task with a clear role, scope, output, and ownership boundary.

The main `gpt-5.5` chat is architect/orchestrator only, not a repo-local worker or substitute subagent. Delegated modifying work defaults to `gpt-5.5` with `xhigh` reasoning when supported.

When the user request requires delegated local repo work under active policy boundaries, decompose and delegate by default; do not block for a separate delegation-permission question unless a higher-priority runtime/platform rule requires it or the user explicitly forbids delegation.

For non-trivial delegated local work, always perform a quick parallelization check before spawning. If the task stays in one lane, state the short reason, such as single write scope, dependency on one answer, safety boundary, or overhead exceeding value.

## When To Parallelize

Use parallel agents when:

- read-only discovery can be split by source, subsystem, document, or question;
- implementation work has non-overlapping write sets;
- one worker can implement while another prepares tests, fixtures, or documentation in separate files;
- independent reviewers can validate different risks after an implementation;
- external research and local codebase inspection can run separately.

## When Not To Parallelize

Keep work sequential when:

- the next step depends on one unresolved answer;
- multiple workers would edit the same file or shared migration;
- scope is ambiguous enough that workers would need architectural judgment;
- the task is small enough that orchestration overhead exceeds value;
- external writes, data imports, or destructive operations require a single controlled path.

## Decomposition Workflow

1. Define the user goal in one sentence.
2. Identify independent questions or file ownership areas.
3. Separate read-only work from write work.
4. Assign each subtask a non-overlapping scope.
5. If only one lane remains, record the short reason and continue without forcing artificial parallelism.
6. Pick the canonical route and explicit reasoning effort for each worker: `gpt-5.4-mini` + `medium` as default read-only, `gpt-5.4` + `high` only for conditional read-only adjudication, `gpt-5.3-codex-spark` + `high` for fast tightly scoped non-modifying checks, and delegated `gpt-5.5` + `xhigh` for modifying work. Use `gpt-5.3-codex` + `medium` for implementation only when `gpt-5.5` + `xhigh` is blocked/unavailable and the blocker is recorded.
7. Include a compact governance capsule in every delegated prompt (role/scope/mode/allowed-forbidden/language/stop conditions), and keep internal/delegated artifacts English-only: delegated prompts/instructions, subagent-visible status notes, reasoning summaries, intermediate/final outputs, handoff/bootstrap blocks, capsules/task briefs/continuity notes, and delegated artifacts.
8. Run independent read-only or disjoint write tasks in parallel.
9. Integrate results in the main orchestrator thread.
10. Resolve conflicts, choose the implementation path, and run final validation or review.

## Delegated Skill Preflight

When preparing delegated prompts, include at most 1-3 task-relevant execution/domain skills only when they materially improve task quality. Include each skill name and exact `SKILL.md` path when known; instruct the subagent to read the listed skill(s) before execution.

Use project-local `.agents\skills` first, then `C:\Users\user\.codex\skills`. Do not use plugin cache/vendor copies as canonical skill sources.

Allowed ordinary subagent preflight skills are execution/domain skills only: `frontend-design`, `web-design-guidelines`, `design-md`, `enhance-prompt`, `fullstack-developer`, `react`, `react-components`, `shadcn-ui`, `playwright`, `meta-mode-memory` for lookup/checkpoint tasks only, `database-schema-design`, `inventory-demand-planning`, `product-manager-toolkit`, `remotion`, and `sora`.

Do not include orchestrator-only skills in ordinary worker/explorer prompts: `universal-orchestrator-rules`, `parallel-task-decomposition`, `parallel-codex-execution`, `active-session-continuity`, or `chat-handoff-checkpoint`. Workers must not use skill guidance to spawn, delegate, reroute, decompose, or expand scope unless explicitly assigned an orchestration role.

Do not reference removed skills: `stitch-ui-design`, `stitch-loop`, `supabase`, `supabase_patterns`, or `codex-design`. If a listed skill is unavailable, require `SKILL_UNAVAILABLE` and continue under `AGENTS.md`, route metadata, scope, and safety constraints.

## Read-Only Patterns

Good parallel read-only splits:

- docs and rules audit;
- file tree and entrypoint discovery;
- business logic comparison;
- test coverage inspection;
- external repository feature reconnaissance;
- API/schema comparison;
- independent file, document, image, PDF, data artifact, or directory batch inspection.

Read-only workers must not edit files. Their output should include findings, evidence, risks, and proposed next actions.
Generic `explorer` and `reviewer` roles are always scoped read-only and must not act as the main orchestrator.
Generic `explorer`/`reviewer` wording is a role label only and is not a guaranteed mini-routing shortcut.
For cheap/lightweight read-only delegated tasks, follow the canonical routing baseline from `universal-orchestrator-rules` unless stricter host policy overrides.
Default read-only delegated lane: `gpt-5.4-mini` + `medium`.
Use `gpt-5.4` + `high` only for conditional read-only analysis/adjudication when lower-cost lanes are insufficient or conflicting; this lane is strictly read-only (no writes, no implementation, no imports, no Directus/ERP writes/schema changes, no production scripts).
Use `gpt-5.3-codex-spark` + `high` only for fast, tightly scoped non-modifying checks.
Modifying work default/required lane: delegated `gpt-5.5` + `xhigh`; `gpt-5.3-codex` + `medium` is an implementation fallback only when `gpt-5.5` + `xhigh` is blocked/unavailable and the blocker is recorded.
Do not invent unavailable mini variants; keep `gpt-5.4-mini` until an actual successor exists.
When project-specific read-only lanes are configured, they take precedence over generic `explorer`/`reviewer` usage.

## File Batch Parallelization Pattern

Use this pattern when one task touches many independent files, documents, images, PDFs, data artifacts, or directories.

Default approach:

- first check whether files are independent;
- split independent files into bounded worker lanes;
- fit the whole file-batch task into at most 6 total subagents;
- do not create more than 6 logical worker batches and do not schedule extra waves beyond those 6 total agents;
- rebalance files into up to 6 larger groups when needed, counting any separate validation or integration worker toward the same 6-agent total;
- never close, cancel, or interrupt an actively working agent merely to free capacity; only normal timeout, hang, safety, or scope-mismatch handling may close stale agents;
- prefer file groups over one worker per file for large batches;
- give each worker an explicit file list or directory scope;
- forbid workers from touching shared outputs unless assigned;
- handle final manifests, summaries, reports, rename maps, or aggregation in a separate integration step.

Do not parallelize when order matters, files share mutable state, outputs collide, one file depends on another unresolved result, or the batch is too small for worker overhead.

## Implementation Patterns

Parallel implementation is allowed only with disjoint write sets.

Good splits:

- worker A edits backend adapter files, worker B edits frontend component files;
- worker A creates tests, worker B updates implementation;
- worker A updates a skill, worker B updates a repo mirror document;
- worker A writes migration scaffolding, worker B writes dry-run diagnostics.

Avoid parallel implementation when two workers would touch the same file, shared config, generated lockfile, migration ordering, or global rule document.

## Delegated Contract Template

Every delegated task should include a compact contract and capsule:

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
CONSTRAINTS:
EVIDENCE_POLICY:
ESCALATION_CONDITION:
OUTPUT:
- findings
- proposed change
- files affected
- risks
- tests/validation
ROLE:
LANGUAGE: English-only for internal/delegated artifacts unless producing localized user-facing content: delegated prompts/instructions, subagent-visible status notes, reasoning summaries, intermediate/final outputs, handoff/bootstrap blocks, capsules/task briefs/continuity notes, and delegated artifacts.
```

Do not attach full policy documents to every narrow task. Include only task-specific policy references when needed.
Require full policy-file reads only for policy/rule changes, governance audits, high-risk writes, safety-sensitive work, or ambiguous multi-step tasks.

Use `fork_context=true` only when the worker genuinely needs full parent context. Prefer a minimal self-contained brief for ordinary tasks.

## Integration Rules

The orchestrator owns the final decision.

After workers return:

- compare outputs for agreement, gaps, and conflicts;
- record route/model/reasoning mismatch as diagnostic drift and assess impact on scope, safety, task fitness, and verification;
- integrate mismatch-run output only when scope compliance, safety boundaries, and verifiability hold;
- use at most one bounded retry when drift, `HUNG_RUN`, or `TIMEOUT` materially affects safety, scope compliance, task fitness, or verification confidence;
- do not merge conflicting edits blindly;
- run a final read-only audit or targeted validation when the task changes rules, configs, scripts, migrations, or multi-file behavior;
- summarize the result to the user in the user-facing language.

## Example: Feature Port

Goal: port a Claude Code feature such as MetaMode to Codex.

Possible split:

- Agent 1: external repo scout, read README and file tree, summarize user-facing feature;
- Agent 2: implementation model scout, inspect hooks, commands, settings, and scripts;
- Agent 3: Codex adaptation scout, map feature to skills, AGENTS.md, plugins, MCP, or automations;
- Agent 4: implementation worker, create the selected Codex artifact in a bounded write scope;
- Agent 5: read-only reviewer, validate behavior, rule compatibility, and missing docs.

Keep each prompt narrow. Do not ask all agents to solve the whole port independently.

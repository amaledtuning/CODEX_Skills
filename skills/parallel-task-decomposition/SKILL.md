---
name: parallel-task-decomposition
description: Use when a task may benefit from multiple scoped subagents, parallel delegation, decomposition into independent read-only or implementation subtasks, non-overlapping write scopes, route-integrity checks, and final orchestrator integration. Especially useful for feature ports, broad codebase investigations, multi-area reviews, and complex implementation plans.
---

# Parallel Task Decomposition

Use this skill when one user goal is too broad for a single delegated agent or can be completed faster and more safely by splitting it into independent scoped subtasks.

## Core Rule

Do not spawn multiple agents on the same broad prompt. Split the work first.

One subagent = one narrow task with a clear role, scope, output, and ownership boundary.

When the user request requires delegated local repo work under active policy boundaries, decompose and delegate by default; do not block for a separate delegation-permission question unless a higher-priority runtime/platform rule requires it or the user explicitly forbids delegation.

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
5. Pick the cheapest sufficient model and explicit reasoning effort for each worker.
6. Include a compact governance capsule in every delegated prompt (role/scope/mode/allowed-forbidden/stop conditions).
7. Run independent read-only or disjoint write tasks in parallel.
8. Integrate results in the main orchestrator thread.
9. Resolve conflicts, choose the implementation path, and run final validation or review.

## Read-Only Patterns

Good parallel read-only splits:

- docs and rules audit;
- file tree and entrypoint discovery;
- business logic comparison;
- test coverage inspection;
- external repository feature reconnaissance;
- API/schema comparison.

Read-only workers must not edit files. Their output should include findings, evidence, risks, and proposed next actions.
Generic `explorer` and `reviewer` roles are always scoped read-only and must not act as the main orchestrator.
Generic `explorer`/`reviewer` wording is a role label only and is not a guaranteed mini-routing shortcut.
For cheap/lightweight read-only delegated tasks, route with `agent_type` `default`, `model` `gpt-5.4-mini`, and `reasoning_effort` `medium` unless stricter host policy overrides.
For high-end delegated read-only adjudication, route with `agent_type` `default`, `model` `gpt-5.4`, and `reasoning_effort` `high` with explicit read-only scope.
When project-specific read-only lanes are configured, they take precedence over generic `explorer`/`reviewer` usage.

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
LANGUAGE:
```

Do not attach full policy documents to every narrow task. Include only task-specific policy references when needed.
Require full policy-file reads only for policy/rule changes, governance audits, high-risk writes, safety-sensitive work, or ambiguous multi-step tasks.

Use `fork_context=true` only when the worker genuinely needs full parent context. Prefer a minimal self-contained brief for ordinary tasks.

## Integration Rules

The orchestrator owns the final decision.

After workers return:

- compare outputs for agreement, gaps, and conflicts;
- record route/model/reasoning mismatch as diagnostic drift and assess impact on scope, safety, task fitness, and verification;
- retry only when drift materially affects safety, scope compliance, task fitness, or verification confidence;
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

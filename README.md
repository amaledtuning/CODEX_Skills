# CODEX Skills

Self-authored global Codex skills for design quality passes and orchestrated workflow control.

This repository intentionally publishes only custom skills from `C:\Users\user\.codex\skills`. It does not include system skills, plugin/vendor skills, framework implementation skills, or third-party imported skills.

## Repository Layout

```text
skills/
  design/<skill-dir>/
  orchestration/<skill-dir>/
```

Each skill directory keeps the normal Codex skill package shape:

- `SKILL.md` for the trigger metadata and main workflow.
- Optional `agents/openai.yaml` UI metadata.
- Optional `references/`, `resources/`, `scripts/`, or `assets/` folders when the skill needs supporting material.

## Installation

Copy the skill folders you want into your Codex skills directory, preserving each folder name:

```text
~/.codex/skills/<skill-dir>
```

Then restart or refresh Codex so runtime skill discovery can load the new metadata. Skills are procedural aids; they do not replace project rules, system instructions, repository policies, or user approvals.

## Design / UX Skills

| Skill | What it does | How it works |
| --- | --- | --- |
| `shape-visual-attention` | Makes the most important element noticed first across UI, documents, slides, posters, images, and dashboards. | Diagnoses the attention path, then adjusts hierarchy, grouping, contrast, scale, alignment, affordance, and redundant state cues. |
| `improve-readability-information-design` | Makes dense text and structured information easier to read, scan, compare, and understand. | Identifies the reading mode, then restructures headings, labels, paragraphs, tables, spacing, rhythm, and type hierarchy. |
| `reduce-cognitive-load` | Simplifies complex flows, explanations, forms, dashboards, and multi-step materials. | Maps what users must notice, understand, remember, decide, and do, then reduces load through chunking, context, defaults, recognition cues, and progressive disclosure. |
| `design-onboarding-mental-model` | Designs onboarding, first-run, tutorial, empty-state, and explainer experiences around accurate user mental models. | Compares the user's likely current model with the intended model, then teaches the core concept through sequence, examples, cause-effect feedback, and a first useful action. |
| `build-motivation-trust` | Strengthens ethical motivation, credibility, confidence, progress, social proof, and willingness to continue. | Finds trust or motivation blockers, then adds credible proof, human context, useful progress cues, reassurance, clear value, and user agency. |
| `simplify-decisions-recovery` | Clarifies choices, comparisons, defaults, pricing, validation, undo, confirmations, and recovery paths. | Locates the decision or failure point, then improves grouping, defaults, recommendation logic, comparison criteria, error prevention, and safe recovery. |
| `design-pass` | Routes broad design pass requests to the smallest useful set of design skills. | Selects 1-3 focused skills based on the medium and goal, then pairs them with execution skills only when an artifact must be produced or edited. |

## Orchestration / Workflow Skills

| Skill | What it does | How it works |
| --- | --- | --- |
| `active-session-continuity` | Keeps delegated work integrated and verifiable inside the active chat. | Tracks worker outputs, scope compliance, changed files, validation, blockers, and next actions before the orchestrator reports completion. |
| `chat-handoff-checkpoint` | Prepares compact continuation prompts and checkpoints for moving work to a new chat. | Captures current state, completed work, changed files, validation, blockers, files to read next, active constraints, and safe next steps without storing secrets or raw logs. |
| `meta-mode-memory` | Provides a file-first memory sandbox for durable compact task state. | Uses local state files and scripts to save notes, checkpoints, daily logs, ingested docs, compiled knowledge pages, keyword queries, and audits. |
| `parallel-codex-execution` | Guides independent worker lanes with strict scope and non-overlapping write ownership. | Defines compact governance capsules, route metadata, lane contracts, validation expectations, drift handling, and integration rules. |
| `parallel-task-decomposition` | Splits broad goals into narrow delegated subtasks when parallel work is safe. | Checks whether work can be divided by independent read scopes or disjoint write sets, then assigns one clear role, scope, output, and boundary per lane. |
| `universal-orchestrator-rules` | Establishes a reusable baseline for Codex orchestrator behavior and route integrity. | Points projects to role boundaries, delegation contracts, confirmation gates, context hygiene, model/reasoning metadata, monitoring, and incident reporting patterns. |

## Exclusions

This catalog deliberately excludes non-self-authored, system, plugin, framework, and third-party skills, including OpenAI `.system` skills and implementation helpers such as React, frontend, Playwright, Sora, shadcn/ui, database, inventory, product-management, and vendor Supabase/Stitch skills.

## Safety

Do not store credentials, project memory dumps, raw transcripts, generated caches, private project data, or local staging artifacts in this repository.

## License

No license has been added yet. Add one before treating this as reusable open-source material outside your own controlled use.

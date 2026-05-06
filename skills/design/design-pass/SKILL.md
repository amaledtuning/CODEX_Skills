---
name: design-pass
description: Opt-in router for design quality passes across UI, websites, presentations, PDFs, documents, images, posters, banners, infographics, decks, ads, and product materials. Use when the user explicitly invokes `$design-pass`, asks for a design pass, or wants a visual/UX/readability/attention/trust/decision-quality review without needing to remember the individual design skill names.
---

# Design Pass

Use this skill as the single entry point for design quality work. It selects the smallest useful set of design reasoning skills, then pairs them with the relevant execution skill only when output needs to be created or edited.

## Routing Rule

Choose 1-3 skills, not the whole design set. Prefer the narrowest route that matches the material and user goal.

| User intent or material | Use these design skills |
| --- | --- |
| Presentation, PDF, one-pager, deck, report | `shape-visual-attention`, `improve-readability-information-design`, `reduce-cognitive-load` |
| Image, poster, banner, ad, promo visual | `shape-visual-attention`, `build-motivation-trust` |
| Dense text, hard to read, make clearer | `improve-readability-information-design`, `reduce-cognitive-load` |
| Onboarding, tutorial, empty state, explainer | `design-onboarding-mental-model`, `reduce-cognitive-load` |
| Pricing, comparison, recommendation, choice | `simplify-decisions-recovery`, `reduce-cognitive-load` |
| Form, checkout, validation, error, recovery | `simplify-decisions-recovery`, `build-motivation-trust` |
| Make more convincing, credible, trustworthy | `build-motivation-trust`, `shape-visual-attention` |
| General visual or UX polish with no clearer clue | `shape-visual-attention`, then add one more skill only if the main problem is readability, load, onboarding, trust, or decisions |

## Workflow

1. Identify the medium and the user's requested outcome.
2. Select the route from the table; if uncertain, choose the smallest plausible route and state the assumption.
3. Read the selected skill(s) before giving design recommendations or editing the artifact.
4. Pair with execution skills only when the task requires producing or modifying an artifact: `presentations`, `documents`, `imagegen`, `frontend-design`, `react`, `shadcn-ui`, `figma`, or `spreadsheets`.
5. Return a concise pass result: selected skills, priority issues, concrete changes, and any execution follow-up.

## Boundaries

Do not auto-load every design skill. Do not use this skill for purely technical tasks with no design, visual communication, UX, readability, attention, trust, decision, or user-comprehension goal. Do not duplicate the detailed principles from the routed skills; load those skills instead.

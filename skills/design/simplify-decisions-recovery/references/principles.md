# Decision and Recovery Principles

Source anchor: paraphrased from the design book in `D:\Project Skills\Книги по дизайну\100_glavnyh_principov_dizayna_kak_uderzhat_vnimanie.pdf`, especially predictable mistakes, stress, choice overload, framing, group decisions, and decision support sections around pp. 223-257.

## Core Principles

- People make predictable mistakes, especially under stress, time pressure, fatigue, or uncertainty.
- More options can reduce decision quality. People often seek more information than they can process well.
- Clear criteria matter more than raw option count. Help users compare along dimensions that map to their goal.
- Defaults shape behavior. Use defaults to support common user goals, not to hide unwanted outcomes.
- Framing changes perception. Present tradeoffs honestly and consistently so one option is not unfairly distorted.
- Errors should be prevented before they need recovery. Use constraints, previews, validation, and reversible actions.
- Recovery should be visible and specific. Users need to know what happened, what it means, and what they can do next.
- Confirmation is useful for high-consequence actions, but annoying for low-risk reversible actions.

## Practical Checklist

- Name the decision the user is actually making.
- Reduce options by grouping, filtering, recommending, or sequencing.
- Make comparison criteria explicit and user-centered.
- Provide a recommended path only when the basis is clear.
- Explain consequences before irreversible actions.
- Prefer undo for reversible actions and confirmation for destructive or costly actions.
- Use inline validation close to the field or choice that caused the issue.
- Write error messages that include cause, consequence, and next step.
- In pricing/comparison tables, align rows so tradeoffs can be scanned.
- In decks/PDFs, lead the audience from criteria to recommendation rather than dumping options.
- In dashboards, distinguish alert, diagnosis, and action.

## Anti-Patterns

- Large undifferentiated option grids.
- Pricing tables where every plan is visually promoted.
- Defaults that benefit the product while surprising the user.
- Error messages that blame the user or give no recovery action.
- Confirmation dialogs for harmless actions and no confirmation for destructive ones.
- Framing that hides tradeoffs or manipulates risk perception.

## Output Pattern

When using this skill, produce:

1. Decision or failure point.
2. Overload or error risk.
3. Simplified option structure or comparison model.
4. Default/recommendation policy.
5. Error prevention and recovery path.
6. Medium-specific notes for UI, slide, PDF, table, dashboard, form, or decision-support visual.

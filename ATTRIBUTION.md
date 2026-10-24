# Attribution

This collection is a curated merge of two MIT-licensed skill libraries. Each merged skill names
the upstream skills it draws from. Upstream text is adapted, not copied wholesale: names,
cross-references, and conflicting guidance were reconciled.

## Sources

### mattpocock/skills

- Author: Matt Pocock
- URL: <https://github.com/mattpocock/skills>
- License: MIT (Copyright (c) 2026 Matt Pocock)

Skills carried forward: `codebase-design`, `domain-modeling`, `improve-codebase-architecture`,
`prototype`, `research`, `retro`, `triage`, `wayfinder`, `teach`, `to-questionnaire`, `wait-what`,
`wizard`, `setup-pre-commit`, `setup-ts-deep-modules`, and the setup workflow now called
`setup-project-workflow`.

Skills merged: `tdd`, `diagnosing-bugs`, `code-review`, `pr`, `grilling`, `grill-me`,
`grill-with-docs`, `to-spec`, `to-tickets`, `implement`, `implement-spec`, `handoff`,
`claude-handoff`, `writing-for-agents`, and `setup-matt-pocock-skills`.

### obra/superpowers

- Author: Jesse Vincent and contributors
- URL: <https://github.com/obra/superpowers>
- License: MIT (Copyright (c) 2025 Jesse Vincent)

Skills carried forward: `verification-before-completion`, `using-git-worktrees`,
`dispatching-parallel-agents`.

Skills merged: `test-driven-development`, `systematic-debugging`, `requesting-code-review`,
`receiving-code-review`, `brainstorming`, `writing-plans`, `executing-plans`,
`subagent-driven-development`, `finishing-a-development-branch`, and `writing-skills`.

### show-me (via mattpocock/skills)

- Author: Dex Horthy, Humanlayer
- URL: <https://github.com/humanlayer/skills>
- License: MIT

The PR-body guidance in `finishing-a-development-branch` is derived from `show-me`.

### openmodelica

The OpenModelica skill and `SyntaxCard.mo` were provided by the repository owner.

## Merged skill map

| This collection | Upstream skills |
|---|---|
| `test-driven-development` | matt `tdd`; superpowers `test-driven-development` |
| `systematic-debugging` | matt `diagnosing-bugs`; superpowers `systematic-debugging` |
| `code-review` | matt `code-review`; superpowers `requesting-code-review`, `receiving-code-review` |
| `design-dialogue` | superpowers `brainstorming`; matt `grilling`, `grill-me`, `grill-with-docs` |
| `spec-and-plan` | matt `to-spec`, `to-tickets`; superpowers `writing-plans` |
| `executing-plans` | superpowers `executing-plans`, `subagent-driven-development`; matt `implement`, `implement-spec` |
| `writing-for-agents` | superpowers `writing-skills`; matt `writing-for-agents` |
| `finishing-a-development-branch` | superpowers `finishing-a-development-branch`; matt `pr` |
| `handoff` | matt `handoff`, `claude-handoff` |

## Not carried forward

`ask-matt` (router), `chief-of-staff`, `loop-me`, `writing-beats`, `writing-fragments`,
`writing-shape`, `diagnosing-superpowers`, `using-superpowers`, `git-guardrails-claude-code`,
`migrate-to-shoehorn`, `scaffold-exercises`, and the browser-based visual companion from
`brainstorming`. Reasons are recorded in the repository history and in the merge plan.

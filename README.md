# Skills

A shared collection of agent skills for coding work: a design-to-delivery workflow, the
disciplines that keep each step honest, and a few specialised tools. Every skill is plain
Markdown with optional references and scripts, so it can be read, forked, and improved after
a session teaches us something.

The collection merges [mattpocock/skills](https://github.com/mattpocock/skills) and
[obra/superpowers](https://github.com/obra/superpowers), deduplicating overlapping skills into
single skills named for their purpose. See [ATTRIBUTION.md](ATTRIBUTION.md) for provenance.

## Install

Point OpenCode at the `skills/` directory in your `opencode.jsonc`:

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "skills": ["/absolute/path/to/skills/skills"]
}
```

Or link every skill into the global skills directory:

```sh
./scripts/link-global.sh
```

OpenCode discovers each `skills/<id>/SKILL.md` as the skill with ID `<id>`. See
[opencode.example.jsonc](opencode.example.jsonc).

## The workflow

The skills are designed to chain. A typical feature runs:

| Step | Skill | What it produces |
|---|---|---|
| 1 | [`design-dialogue`](skills/design-dialogue/SKILL.md) | Shared understanding and an approved design |
| 2 | [`spec-and-plan`](skills/spec-and-plan/SKILL.md) | A spec, a ticket graph, and a task-by-task plan |
| 3 | [`using-git-worktrees`](skills/using-git-worktrees/SKILL.md) | An isolated workspace with a clean baseline |
| 4 | [`executing-plans`](skills/executing-plans/SKILL.md) | Implemented tasks, each verified and reviewed |
| 5 | [`code-review`](skills/code-review/SKILL.md) | Standards and spec findings, acted on |
| 6 | [`finishing-a-development-branch`](skills/finishing-a-development-branch/SKILL.md) | A merge, PR, or preserved branch |
| 7 | [`retro`](skills/retro/SKILL.md) | Improvements to the environment for next time |

## All skills

Every skill below is **model-invoked** unless it is labelled _(user-invoked)_. Model-invoked
skills carry a description the agent can reach on its own; user-invoked skills are the ten listed
again under [User-invoked skills](#user-invoked-skills) and can only be called by hand.

### Design and planning

- **[design-dialogue](skills/design-dialogue/SKILL.md)** - Draw out what the user actually
  wants, then stress-test the decisions through rounds of questions before building.
- **[spec-and-plan](skills/spec-and-plan/SKILL.md)** - Turn an agreed design into a written
  spec, tracer-bullet tickets with blocking edges, and an executable plan.
- **[codebase-design](skills/codebase-design/SKILL.md)** - Shared vocabulary for deep modules,
  seams, adapters, leverage, and locality.
- **[domain-modeling](skills/domain-modeling/SKILL.md)** - Build and sharpen the project's
  glossary and ADRs as decisions crystallise.
- **[prototype](skills/prototype/SKILL.md)** - Throwaway code that answers one design question.
- **[improve-codebase-architecture](skills/improve-codebase-architecture/SKILL.md)** _(user-invoked)_ - Scan for
  deepening opportunities, report them visually, then explore the chosen one.
- **[wayfinder](skills/wayfinder/SKILL.md)** _(user-invoked)_ - Map work too large for one session as decision
  tickets on an issue tracker.
- **[research](skills/research/SKILL.md)** - Investigate a question against primary sources and
  capture a cited note.

### Implementation

- **[executing-plans](skills/executing-plans/SKILL.md)** - Execute a plan inline, with a fresh
  subagent per task, or across a parallel task graph.
- **[test-driven-development](skills/test-driven-development/SKILL.md)** - Red-green-refactor
  with pre-agreed seams, honest tests, and proof that each test can fail.
- **[systematic-debugging](skills/systematic-debugging/SKILL.md)** - Build a feedback loop,
  reproduce and minimise, rank hypotheses, then fix the root cause.
- **[verification-before-completion](skills/verification-before-completion/SKILL.md)** - Evidence
  before claims, always.
- **[dispatching-parallel-agents](skills/dispatching-parallel-agents/SKILL.md)** - One focused
  agent per independent problem domain.
- **[using-git-worktrees](skills/using-git-worktrees/SKILL.md)** - Isolated workspaces with a
  verified clean baseline.

### Review and delivery

- **[code-review](skills/code-review/SKILL.md)** - Two-axis review (Standards and Spec), plus
  how to request, receive, and act on feedback.
- **[finishing-a-development-branch](skills/finishing-a-development-branch/SKILL.md)** - Verify,
  choose merge/PR/keep, and clean up; includes the PR body shape.
- **[conventional-commits](skills/conventional-commits/SKILL.md)** - Write commit messages in
  the Conventional Commits format: type, optional scope, breaking-change marker, a required
  body, and closing footers.
- **[squash-merge-message](skills/squash-merge-message/SKILL.md)** - Write the squash commit of a
  pull request so its changelog parts serve users and its body serves developers.
- **[handoff](skills/handoff/SKILL.md)** _(user-invoked)_ - Compact a session into a handoff document or a fresh
  background agent.
- **[retro](skills/retro/SKILL.md)** _(user-invoked)_ - Turn a session's friction into environment improvements.
- **[triage](skills/triage/SKILL.md)** _(user-invoked)_ - Move issues and external PRs through triage roles into
  agent-ready briefs.

### Writing and collaboration

- **[writing-for-agents](skills/writing-for-agents/SKILL.md)** - Write skills, AGENTS.md files,
  and other documents agents consume; includes testing skills with subagents.
- **[teach](skills/teach/SKILL.md)** _(user-invoked)_ - Teach a concept in this workspace.
- **[to-questionnaire](skills/to-questionnaire/SKILL.md)** _(user-invoked)_ - Turn a decision you cannot make
  into a questionnaire for someone else.
- **[wait-what](skills/wait-what/SKILL.md)** _(user-invoked)_ - Stop and re-pitch a message that did not land.
- **[wizard](skills/wizard/SKILL.md)** - Generate an interactive bash wizard for human-only
  steps.

### Setup

- **[setup-project-workflow](skills/setup-project-workflow/SKILL.md)** _(user-invoked)_ - Configure the issue
  tracker, triage labels, and domain docs this collection assumes.
- **[setup-pre-commit](skills/setup-pre-commit/SKILL.md)** - Wire Husky, lint-staged, type
  checking, and tests into pre-commit.
- **[setup-ts-deep-modules](skills/setup-ts-deep-modules/SKILL.md)** _(user-invoked)_ - Enforce package
  boundaries in TypeScript with dependency-cruiser.

### Domain

- **[openmodelica](skills/openmodelica/SKILL.md)** - Build, check, and simulate Modelica models
  with OpenModelica's `omc`, including a syntax card of tested forms and a test-model runner.

## User-invoked skills

Ten skills are meant to be called by you, not fired autonomously by the model. Each sets
`metadata: opencode/autoinvoke: false` in its frontmatter, so OpenCode keeps its description out
of the agent's context and only your explicit invocation loads it. They still work by typing the
skill's name; they just cannot be reached by the agent. Reach for one when:

| Skill | Purpose |
|---|---|
| [`wayfinder`](skills/wayfinder/SKILL.md) | Map work too large for one session as decision tickets on the issue tracker and resolve them one at a time. |
| [`triage`](skills/triage/SKILL.md) | Move incoming issues and external PRs through triage into agent-ready briefs, or close them with a reason. |
| [`improve-codebase-architecture`](skills/improve-codebase-architecture/SKILL.md) | Scan a codebase for deepening opportunities, report them visually, then work through the chosen one. |
| [`retro`](skills/retro/SKILL.md) | Conduct a retrospective on a coding session and rank evidence-backed improvements to steering files, checks, and tooling. |
| [`handoff`](skills/handoff/SKILL.md) | Compact a session into a handoff document, or seed a fresh background agent with it. |
| [`setup-project-workflow`](skills/setup-project-workflow/SKILL.md) | Configure a repo for this collection: its issue tracker, triage labels, and domain doc layout. |
| [`setup-ts-deep-modules`](skills/setup-ts-deep-modules/SKILL.md) | Enforce TypeScript package boundaries so each package stays a deep module with a narrow entry point. |
| [`teach`](skills/teach/SKILL.md) | Teach a skill or concept in this workspace through a guided, hands-on lesson. |
| [`to-questionnaire`](skills/to-questionnaire/SKILL.md) | Turn a decision you cannot make alone into a written questionnaire for the person who can. |
| [`wait-what`](skills/wait-what/SKILL.md) | Re-pitch the last message in plain language when it did not land. |

## Improving a skill

Skills earn changes through observed failures, not enthusiasm. Read
[AGENTS.md](AGENTS.md) before editing one, and [writing-for-agents](skills/writing-for-agents/SKILL.md)
before changing a skill's shape. Run `python3 scripts/validate-skills.py` before committing.

## License

MIT. Upstream portions retain their original copyright notices; see [LICENSE](LICENSE) and
[ATTRIBUTION.md](ATTRIBUTION.md).

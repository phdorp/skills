# Writing for discovery

Part of [`writing-for-agents`](../SKILL.md). The `SKILL.md` shape, and how to name, describe, and size a skill so the agent finds it and reads the right part.

## SKILL.md structure

```markdown
---
name: writing-for-agents
description: Use when creating or editing skills, AGENTS.md or CLAUDE.md files, or any document an agent consumes.
---

# Skill Name

## Overview
What this is, and the core principle, in one or two sentences.

## When to use
Symptoms and situations. When not to use. A small flowchart only if the decision is non-obvious.

## Steps / core pattern
The actions, in order, with a completion criterion each. A before/after example for a technique.

## Quick reference
A table or bullets for scanning.

## Implementation
Short code inline; heavy reference behind a relative link.

## Common mistakes
What goes wrong and the fix.

## Related skills
IDs only, with what each supplies.
```

Keep the body under ~500 lines. Split at the point where the hierarchy demands it, not at a round number.

## Description

The description is the skill's always-loaded context pointer. It decides whether the agent loads the body at all, so it gets the pointer discipline from `SKILL.md`: the leading word front-loaded, one trigger per branch, no identity the body already carries.

- Start with "Use when…" and follow with triggering conditions and symptoms.
- Third person. It is injected into a system prompt, and a first-person description ("I can help with…") reads as conversation rather than metadata.
- Include the words a real task would contain: error strings (`ENOTEMPTY`, "hook timed out"), symptoms ("flaky", "hanging", "zombie process"), tools and file types, and the synonyms a user might type ("timeout/hang/freeze").
- Describe the problem, not one language's symptom, unless the skill is specific to that technology. "Use when tests have race conditions or pass and fail inconsistently" travels; "use when the test calls setTimeout" does not.
- Keep it under 1024 characters; aim for a few hundred.

**Never summarize the workflow.** A description that says "dispatches one subagent per task with a review between tasks" tells the agent what to do, and the body becomes documentation it skips. State the trigger; let the body carry the process. This was observed directly: a summary description produced one review where the body required two, and removing the summary from the description restored the two-stage behaviour.

```yaml
# Bad: workflow summary, agent follows it instead of the body
description: Use when executing plans — one subagent per task with code review between tasks

# Bad: process detail
description: Use for TDD — write the test first, watch it fail, write minimal code, refactor

# Good: triggers only
description: Use when executing an implementation plan with independent tasks in the current session

# Good: triggers only, including the about-to-violate case
description: Use when implementing any feature or bugfix, before writing implementation code; also when tempted to test after the fact
```

## Keywords

The agent searches descriptions and greps bodies. Seed both with the words a future task will contain:

- Error messages and exit codes.
- Symptoms in the user's vocabulary, plus the synonyms they might use.
- Commands, library and file names, config keys.
- The leading word the document is built around, repeated as a token in the body.

Keywords go where they are true. Stuffing a description with unrelated terms makes the skill fire on the wrong task, which costs more than a missed trigger.

## Naming

The directory name is the ID: lowercase kebab-case, active voice, describing what the agent does.

- `writing-for-agents`, not `agent-doc-guidelines`.
- `test-driven-development`, not `tdd-guidelines`.
- `condition-based-waiting`, not `async-test-helpers`.

Verb-first and gerund forms read as actions (`writing-for-agents`, `testing-skills`, `debugging-with-logs`); noun phrases are acceptable (`code-review`). Avoid vague names (`helpers`, `utils`) and inconsistent patterns within one collection. Names are how other documents and humans refer to the skill, so a rename is a cross-reference change across the repo.

## Token budgets

Context is shared with the system prompt, the conversation, every other skill's description, and the actual task. At startup only names and descriptions load; the body loads when the skill fires, and supporting files only when their pointer fires. Concision still matters, because once loaded every token competes with the conversation.

- Descriptions: a few hundred characters. They are paid every turn.
- `SKILL.md`: the steps and the reference every run needs. Under ~500 lines; smaller is better.
- Always-loaded instructions files (`AGENTS.md` / `CLAUDE.md`): a page, mostly pointers.
- Frequently loaded skills: under ~200 lines.

Compress by pointing, not by abbreviating. "Run `--help` for the flags" beats listing every flag that will drift. Compress examples to the minimum that still shows the shape.

```sh
wc -l skills/*/SKILL.md
```

A body that keeps growing is telling you a section wants to be disclosed, or that a branch wants its own skill.

## Cross-referencing other skills

Refer by ID, with the relationship explicit:

- **Required background**: "Understand `test-driven-development` before using this skill; it defines the cycle this one adapts."
- **Optional companion**: "See `code-review` for the review pass."
- **Relative link** when the target is a file in this repo: `[testing-skills.md](testing-skills.md)`.

Two rules:

1. **Point, do not duplicate.** If another skill owns the rule, name it and stop. A copy drifts, and inflates that rule's prominence in this document past its rank.
2. **No force-loading syntax.** An `@path` reference in some harnesses expands the file into context immediately, spending the whole budget before the material is needed. A plain relative link or an ID is read on demand.

## Anti-patterns

- **A table of contents in the description**: trigger branches are not a chapter list.
- **Skill names that describe the topic** (`async-testing`, `documentation`) rather than the action; the agent cannot tell when to fire them.
- **Keywords unrelated to the body**: wrong-task firing.
- **A body that restates the description** in its overview, paying twice for one meaning.
- **Deep link chains**: `SKILL.md` → `advanced.md` → `details.md` gets partially read.
- **History in the body**: "as of the last update…" goes stale. Put dated material in an "old patterns" section or delete it.

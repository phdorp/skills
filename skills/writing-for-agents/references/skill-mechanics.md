# Skill mechanics

The skill-specific branch of [`writing-for-agents`](../SKILL.md): what changes when the document is a skill. Frontmatter, naming, invocation, and directory layout. Everything about writing the words is in `SKILL.md`.

## Where a skill lives

A skill is a directory named for its ID, containing `SKILL.md`:

```
skills/<id>/
  SKILL.md              # required: what every run needs
  references/*.md       # optional: disclosed reference, one level deep
  scripts/*             # optional: tools executed, not read
  *.dot, *.svg          # optional: diagram sources and renders
```

This repo keeps the source in `skills/` and installs from there. OpenCode reads each `skills/<id>/SKILL.md`; point `skills` in `opencode.jsonc` at the collection, or link the directories into the global root:

- OpenCode global: `~/.config/opencode/skills/<id>/`
- Claude Code: `~/.claude/skills/<id>/`
- Cross-runtime alias: `~/.agents/skills/<id>/`

The files are identical across roots. Write paths relative to the skill directory, with forward slashes.

## Frontmatter

```yaml
---
name: writing-for-agents
description: Use when creating or editing skills, AGENTS.md or CLAUDE.md files, or any document an agent consumes.
---
```

- **ID** comes from the directory name: lowercase kebab-case (`writing-for-agents`, `test-driven-development`). No spaces, parentheses, or capitals; other references use the ID alone.
- **`name`** is the human-readable title used when displaying the skill.
- **`description`** is the pointer the agent reads before deciding to load the body. Write it for the agent: start with "Use when…", then the trigger branches, symptoms, and error strings a real task would contain. Third person. Under 1024 characters; aim shorter.
- **`metadata`** carries harness hints.

A description never summarizes the workflow. Testing this repo's imports showed the failure directly: a description saying "code review between tasks" made the agent perform one review, while the body's flowchart required two (spec compliance, then quality). Rephrasing the description to "Use when executing implementation plans with independent tasks" made the agent read the body and follow both. The summary becomes a shortcut around the body.

User-invoked skills add the invocation flag:

```yaml
---
name: retro
description: "Conduct a retrospective on a coding session."
metadata:
  opencode/autoinvoke: false
---
```

`disable-model-invocation: true` is the portable spelling of the same flag; use one or the other.

## Invocation

Two choices, trading the two loads from `SKILL.md`.

### Model-invoked

Keep a description so the agent can fire the skill autonomously and other skills can reach it. You can still type its name: model-invocation always _includes_ user reach; a description only adds agent discovery, never removes the human's.

- The description is the skill's top-level context pointer, forced to stay loaded at all times: permanent context load in exchange for discoverability.
- The pointer rules apply in full — front-load the leading word, one trigger per branch, cut identity the body already carries.
- A model-invoked skill whose content is all reference is also a home for shared reference: another skill can invoke it, so reference needed by several skills lives in one place.

Pick model-invocation only when the agent must reach the skill on its own, or another skill must.

### User-invoked

Strip the description from the agent's reach: only the human typing the skill's name can invoke it, and no other skill can.

- Zero context load.
- The description becomes human-facing: a one-line summary, trigger lists stripped.
- The cost is cognitive load: you are the index that must remember it exists.

If a skill only ever fires by hand, make it user-invoked and pay no context load. If it lives in a workflow the agent should start on its own, pay for the description.

### Shared reference between user-invoked skills

Two user-invoked skills cannot reach each other, and each is invisible to the agent until typed. When both need the same reference, put it in a plain file outside the skill system — a doc any skill or `AGENTS.md` line can point at — rather than duplicating it or promoting both skills to model-invocation.

## Splitting by invocation

The sequence cut (splitting a run of steps so later steps do not tempt a rush) lives in `SKILL.md`. The invocation cut is the skill-specific one: split off a model-invoked skill when you have a distinct leading word that should trigger it on its own, or another skill must reach it. You pay context load for the new always-loaded description, so that independent reach has to be worth it.

The usual mistake is one giant user-invoked skill that a human has to remember and then wade through. Split when the second half has its own trigger; keep it together when every invocation needs both halves.

## Router skills

When user-invoked skills multiply past what you can remember, that piled-up cognitive load is cured by a **router skill**: one user-invoked skill that names the others and when to reach for each, so the human has one skill to remember instead of many.

- The router is user-invoked, so it costs no context load.
- It can only hint, never fire the others: user-invoked skills have no description, so nothing but the human can reach them.
- Keep it a table or a short list: skill ID, the situation, the one-line outcome. The router earns its place when the list is genuinely hard to remember, not as a table of contents for its own sake.
- If the router starts accumulating rules rather than pointers, the rules belong in the skills it names.

## Supporting files

Separate a file when it is heavy reference (API docs, full syntax) or a reusable tool (script, template). Keep inline what every run needs: principles, short code patterns, the step sequence.

```
skill-with-heavy-reference/
  SKILL.md          # overview, steps, pointers
  references/
    api.md          # 600 lines of reference, read on demand
    examples.md     # worked examples
  scripts/
    validate.py     # executed, never loaded whole
```

- Link references one level deep from `SKILL.md`. A pointer chain gets partially read (`head -100`) and the agent proceeds on a preview.
- Name files for their content: `form-validation-rules.md`, not `doc2.md`. Group by domain (`reference/finance.md`, `reference/sales.md`) so only the relevant branch loads.
- Give a reference file over ~100 lines a short contents list, so a partial read still shows its scope.
- Keep one authoritative copy. A supporting file that repeats a rule from `SKILL.md` will drift.

## Scripts

Invoke bundled scripts through their interpreter in the prose — `node scripts/render-graphs.js <skill-dir>`, `bash scripts/tool.sh`, `python3 scripts/validate.py` — never as a bare path. Some harness plugin packagers strip executable bits, so a bare `scripts/tool.sh` fails with `Permission denied`.

Say which of the two the agent should do:

- **Execute** for deterministic operations: "Run `scripts/validate.py` to check the plan."
- **Read as reference** only when the logic itself is the guidance: "See `scripts/validate.py` for the rule set."

Scripts should solve their own errors and say what went wrong, rather than returning a bare stack trace for the agent to interpret. Any constant the script relies on gets a comment explaining its value; a magic number becomes a mystery the agent has to guess around.

## Diagram sources

Flowcharts follow [flowcharts.md](flowcharts.md) and [graphviz-conventions.dot](graphviz-conventions.dot). Render them with [../scripts/render-graphs.js](../scripts/render-graphs.js); commit the source `.dot` block in `SKILL.md` so the diagram stays editable.

## Checklist for a new skill

- [ ] Directory name and frontmatter ID agree; lowercase kebab-case.
- [ ] Description states triggers only, no workflow summary.
- [ ] Invocation chosen deliberately: description if the agent or another skill must reach it, no description if only by hand.
- [ ] Steps have checkable completion criteria.
- [ ] Heavy reference and tools are in their own files, linked one level deep.
- [ ] Scripts are invoked through their interpreter, with execute-vs-read stated.
- [ ] Every relative link resolves.
- [ ] A baseline run exists for the failure the skill addresses, or the skill is explicitly baseline.

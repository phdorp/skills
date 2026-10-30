---
name: writing-for-agents
description: Use when creating or editing skills, AGENTS.md or CLAUDE.md files, or any document an agent consumes.
---

# Writing for Agents

A document an agent consumes is a skill, an `AGENTS.md` / `CLAUDE.md`, or a doc reached by a pointer. The packaging differs; the writing does not. The agent runs the same _process_ every time rather than producing the same output, so the levers below make each document predictable.

- Skill-specific mechanics: [references/skill-mechanics.md](references/skill-mechanics.md)
- Testing what you wrote: [references/testing-skills.md](references/testing-skills.md)
- Anthropic's authoring guidance, adapted: [references/anthropic-best-practices.md](references/anthropic-best-practices.md)

## Context pointers

A **context pointer** is a reference held in the agent's context that names out-of-context material and encodes the condition for reaching it. A skill's description is one; a line in `AGENTS.md` naming a doc is the same object. The pointer's _wording_, not its target, decides when the agent reaches the material, and how reliably. A must-have target behind a weakly worded pointer is a variance bug: sharpen the wording first, and inline the material only if sharpening fails.

A pointer does two jobs: state what the material is, and list the **branches** that should trigger reaching it (a branch is a distinct case the document handles, so different runs take different paths through it). Every word of an always-loaded pointer costs on every turn, so it earns harder pruning than the body:

- **Front-load the leading word**: the pointer is where it does its triggering work.
- **One trigger per branch.** Synonyms that rename a single branch are one branch written twice; collapse them and keep only genuinely distinct branches.
- **Cut identity the body already carries.**

## The two loads

Every document and pointer you add spends one of two budgets:

- **Context load** is the cost of always-loaded material on the agent's window: an `AGENTS.md` line, a skill description, anything sitting in context every turn, spending tokens and attention whether or not it fires.
- **Cognitive load** is the cost on the human: which documents exist and when to reach for each. The human is the index. It is not a cost to minimise — it is the price of human agency. Spend it where human judgement matters, remove it where it does not.

Material reached only through a pointer escapes context load at the price of the pointer's own line; material with no pointer at all rides entirely on cognitive load.

## Information hierarchy

A document is built from two content types: **steps** (the ordered actions the agent performs) and **reference** (definitions, rules, facts consulted on demand). They mix freely: all steps (a recipe), all reference (a review's rules, this skill), or both. The core decision is where each piece sits on the **information hierarchy**, a ladder ranked by how immediately the agent needs the material:

1. **In-file step** is the primary tier: what the agent does, in order.
2. **In-file reference** is consulted on demand. Often a legitimately flat peer-set (every rule of a review on one rung), which is a fine arrangement, not a smell.
3. **Disclosed reference** sits in a separate file, reached by a context pointer and loaded only when the pointer fires. Its range runs from a sibling file in the same folder to fully external reference that lives anywhere and that any document can point at.

Push too little down and the top bloats; push too much and you hide material the agent needs. That tension is the whole decision.

**Progressive disclosure** is the move down the ladder, out of the main file and behind a pointer, so the top stays legible. It is not primarily a token optimisation: it is how the hierarchy is protected. Branching is the cleanest disclosure test: inline what every branch needs, and push behind a pointer what only some branches reach. When a document has steps, in-file reference that should be disclosed buries them and turns attending to them into a coin-flip — a variance lever, not just a legibility one.

**Co-location** is the within-file companion: the ladder decides _how far down_ a piece sits, co-location decides _what sits beside it_ once there. Keep a concept's definition, rules, and caveats under one heading rather than scattered, so reading one part brings its neighbours with it. The test: the document should read like documentation written for the agent. Grouped material reads that way; scattered material does not. (Distinct from duplication: that repeats one meaning in two places; scattering fragments one meaning across many.)

**Sprawl** is the failure mode: a document simply too long, even when every line is live and unique. Attention thins across the excess, and every extra line is one more to keep relevant. The cure is the ladder: disclose reference behind pointers, and split by branch or sequence so each path carries only what it needs.

## Steps and completion criteria

Every step ends on a **completion criterion**, the condition that tells the agent the work is done. Two properties make it a lever:

- **Clarity**: can the agent tell done from not-done? A vague bound ("understanding reached") invites **premature completion**: ending the step before it is genuinely done, attention slipping to _being done_. The visible steps still ahead (the **post-completion steps**) supply the pull; the criterion's clarity is the resistance. Defend in order: **sharpen the bound first** (local and cheap); only if it is irreducibly fuzzy _and_ you observe the rush, hide the later steps by splitting the sequence. Hiding only works across a real context boundary (a hand-off or a subagent dispatch; an inline call leaves the later steps in context and clears nothing).
- **Demand**: how much it requires. "Every modified model accounted for" forces thorough work where "produce a change list" does not. Demand drives **legwork**, the digging the agent does within the work, latent in the wording rather than written as its own step. It is not step-bound: "every rule applied" binds a body of flat reference just as "every step done" binds a sequence, which is how an all-reference document still carries an exhaustiveness bar.

The strongest criteria are both checkable and exhaustive.

## When to split

Splitting one document into two spends one of the two loads, so split only when the cut earns it:

- **By sequence**: split a run of steps where the post-completion steps tempt the agent to rush the one in front of it. Keeping them out of view drives more legwork on the current task. Beware the reverse: merging sequences exposes each step's later steps to what follows, inviting premature completion.
- **By invocation**: skill-specific; see [references/skill-mechanics.md](references/skill-mechanics.md).

## Leading words

A **leading word** is a compact concept already living in the model's pretraining that the agent thinks with while running the document (_lesson_, _fog of war_, _tracer bullets_). Repeated as a token, never as a sentence, it accumulates a distributed definition and anchors a whole region of behaviour in the fewest tokens by recruiting priors the model already holds. Coining your own works if you define it clearly, but a made-up word recruits no priors: you pay in definition tokens what a pretrained word gives free. Reach for an existing word first.

It anchors twice. In the body, _execution_: the agent reaches for the same behaviour every time the word appears, and inside flat reference it focuses attention on a class of thing to look for. In a pointer, _invocation_: when the same word lives in your prompts, your docs, and your codebase, the agent links that shared language to the material and reaches it more reliably.

Hunt for opportunities to refactor with leading words. A triad spelled out at three sites, a pointer spending a sentence to gesture at one idea — each is a passage begging to collapse into a single token:

- "fast, deterministic, low-overhead" → _tight_ (a _tight_ loop).
- "a loop you believe in" → _red_, turning a fuzzy gate into a binary observable state (the loop goes _red_ on the bug, or it doesn't).

You win twice: fewer tokens, and a sharper hook for the agent to hang its thinking on. Assume every document carries restatements that leading words retire. Go find them.

**Negation** is the failure mode beside this lever: steering by prohibition drags the forbidden behaviour into context and makes it _more_ available, not less. _Don't think of an elephant_, and the elephant is all there is; the negation is a weak modifier the strongly activated concept overruns, so the ban half-reads as an instruction to do the thing. Prompt the **positive**: state the target behaviour ("write one-line comments") so the banned one is never spoken. A prohibition earns its place only as a hard guardrail you cannot phrase positively; even then, pair it with the positive target so attention lands on what to do.

## Pruning

- Keep each meaning in a **single source of truth**: one authoritative place, so changing the behaviour is a one-place edit. **Duplication** (the same meaning in more than one place) costs maintenance and tokens, and inflates a meaning's prominence on the ladder past its real rank. (The accidental inverse of a leading word, which repeats a token on purpose, never the meaning.)
- The **environment** is a source of truth too (`package.json` scripts, config files, the directory layout, `--help` output), and a document that restates it is a **cache**: a copy of a lookup, earning its load only when the lookup is expensive. Cache what the agent cannot find by looking: the unwritten convention, the reason behind a choice, the gotcha no config confesses. Leave one-file, one-command lookups to the environment, where they cannot go stale.
- Check every line for **relevance**: does it still bear on what the document does? A line loses relevance by never bearing on the task (mere exposition, or a branch that should be disclosed) or by going stale as the behaviour or world it describes changes. Shorter documents are easier to keep relevant. Without a pruning discipline the default fate is **sediment**: stale layers that settle because adding feels safe and removing feels risky, until you core down through them to find what is still live.
- Hunt **no-ops** sentence by sentence: an instruction the model already obeys by default pays load to say nothing. The test — does it change behaviour versus the default? — is model-relative, not reader-relative: two people disagreeing about a no-op disagree about the default, and settle it by running the document, not by debate. When a sentence fails, delete the whole sentence rather than trim words from it. The test also grades leading words: a word too weak to beat the default (_be thorough_ when the agent is already thorough-ish) is a no-op, and the fix is a stronger word (_relentless_), not a different technique.

## What earns a skill

Create a skill when the material is a reusable technique, pattern, or reference: it was not obvious the first time, you would reach for it again across projects, and it applies beyond one repo. Skip it for a one-off solution, a standard practice already well documented elsewhere, or a project convention that belongs in that project's instructions file. A mechanical rule that a linter, test, or hook can enforce belongs in the check, not in prose.

The type decides the test: a **technique** (a method with steps), a **pattern** (a mental model), a **reference** (docs, commands), or a **discipline** (a rule the agent is tempted to skip). Only the last needs pressure testing.

## Skill mechanics in brief

A skill is a directory `skills/<id>/` holding a `SKILL.md` and optional supporting files. This repo's `skills/` directory is the source; OpenCode discovers each `skills/<id>/SKILL.md`, and the global install mirrors it at `~/.config/opencode/skills/<id>/`. Other harnesses use their own roots (`~/.claude/skills/`, `~/.agents/skills/`) for the same files. Full detail: [references/skill-mechanics.md](references/skill-mechanics.md).

**Frontmatter** carries the ID and the pointer:

```yaml
---
name: writing-for-agents
description: Use when ...
---
```

- The ID is the directory name: lowercase kebab-case, active or gerund (`writing-for-agents`, `test-driven-development`).
- `name` is the human-readable title; `description` is the pointer the agent reads.
- The description states _when_ to use the skill — trigger branches and symptoms — and never summarizes the workflow. An agent that reads a workflow summary follows the summary instead of the skill. Keyword and naming detail: [references/discovery.md](references/discovery.md).
- A user-invoked skill sets `opencode/autoinvoke: false` under `metadata` (or `disable-model-invocation: true` where harness portability matters).

**Invocation** trades the two loads:

- **Model-invoked** keeps a description, so the agent can fire it and other skills can reach it. That is permanent context load for discoverability and shared reference. Choose it when the agent must reach the skill on its own, or another skill must. It stays reachable by name.
- **User-invoked** strips the description: only the human typing the name reaches it, at zero context load and more cognitive load. Choose it for workflows you start by hand. When user-invoked skills multiply, add a **router skill**: one user-invoked skill that names the others and when to reach for each, so the human remembers one. It can only hint, never fire them.

**Layout** follows the hierarchy:

```
skills/<id>/
  SKILL.md            # steps and the reference every run needs
  references/*.md     # disclosed reference, one level deep
  scripts/*.js        # tools executed, not read
```

Keep references one level deep from `SKILL.md`; a chain of pointers gets read partially. Invoke bundled scripts through their interpreter (`node scripts/tool.js <args>`, `bash scripts/tool.sh`), never by bare path: some packagers strip executable bits, and a bare path fails there with `Permission denied`. Say whether a script is executed or read as reference.

## Testing what you wrote

A document is a claim about agent behaviour; test the claim. The cycle is TDD's, applied to prose: run the scenario without the document (RED), write the smallest document that fixes the observed failure (GREEN), then close the loopholes the next run finds (REFACTOR). Use `test-driven-development` for the cycle itself; this section covers the document-specific form.

| TDD | Document |
|---|---|
| Test case | Scenario with a subagent, one fresh context per rep |
| Failing test (RED) | Baseline run without the document; failure recorded verbatim |
| Minimal code (GREEN) | Smallest guidance addressing those specific failures |
| Passing test | Same scenario with the document: the agent now complies |
| Refactor | New rationalization found, countered, re-tested |

**Which cycle to run depends on the document:**

- **Discipline skill** — the agent knows the rule and skips it under pressure: run the full cycle with pressure scenarios combining 3+ pressures (time, sunk cost, authority, exhaustion). If you did not watch an agent fail without it, you do not know the document prevents the right failure.
- **Reference skill or plain doc** — no rule to violate: test retrieval and application instead. Can the agent find the right file and section from the description or pointer? Does it apply what it finds to a new case? Cover the common cases and look for gaps. Pressure-testing a reference doc produces theatre.
- **Imported upstream skill** — baseline until this repo observes a failure. Port it, test it on first real use, and write the reproducing test before changing the wording. A refactor that is not fixing an observed failure is not a test.

**Match the form to the failure.** The form that fixes one failure backfires on another.

| Baseline failure | Right form | Wrong form |
|---|---|---|
| Skips a rule under pressure | Prohibition + rationalization table + red flags | Soft guidance ("consider…") |
| Complies, but output has the wrong shape | Positive recipe: state what the output IS, its parts in order | A list of things not to do |
| Omits a required element | Structural slot in the template the agent fills | Prose reminder beside the template |
| Behaviour depends on a condition | Conditional keyed to an observable predicate | Unconditional rule plus exemption clauses |

**Micro-test the wording before full scenarios.** One fresh-context sample per call: the system prompt is the realistic whole (skill or prompt template, not the paragraph in isolation), and the user message tempts the failure. Always run a no-guidance control; if the control does not fail, there is nothing to fix. Use 5+ reps per variant and read every flagged match by hand — echoed templates and quoted counter-examples score as hits. Convergence across reps is the signal that the wording binds; five interpretations across five reps means tighten the form rather than add words.

Full method, pressure-scenario templates, meta-testing, and a worked campaign: [references/testing-skills.md](references/testing-skills.md). Closing loopholes in a discipline skill: [references/bulletproofing.md](references/bulletproofing.md). Flowcharts, when a decision genuinely needs one: [references/flowcharts.md](references/flowcharts.md).

## Checklist

Before publishing a document:

- [ ] The description states when to use it, with no workflow summary.
- [ ] Every branch that should reach the material appears in a pointer, once.
- [ ] Each meaning lives in one place; no line restates the environment.
- [ ] Steps name a checkable completion criterion, and the demand is explicit.
- [ ] Reference every branch needs is inline; the rest is disclosed one level deep.
- [ ] Leading words carry repeated concepts; prohibitions are replaced by positive targets.
- [ ] A baseline run exists for the failure the document addresses, or the document is marked baseline.
- [ ] Relative links resolve, and scripts run through their interpreter.

## Anti-patterns

- **Narrative example**: "In session 2025-10-03 we found…" is too specific to reuse. State the pattern.
- **Workflow summary in the description**: the agent follows the summary and skips the body.
- **Multi-language dilution**: five mediocre ports of one example. One runnable example in the language the task uses.
- **Code or commands in a flowchart**: not copy-pasteable. Put them in a code block and keep the flowchart for decisions.
- **Generic labels**: `step1`, `helper2`, `pattern4` carry no meaning. Name the thing.
- **Speculative sections**: content for a hypothetical case nobody has hit is sediment on arrival.

## Related skills

- `test-driven-development` — the RED-GREEN-REFACTOR cycle this skill borrows for documents.
- `code-review` — review the guidance in a change the way you review code: does it bind, and does it earn its lines?
- `retro` — find the friction in a session that justifies a document change, and sort it into a mechanical check or a judgement call.

---
name: design-dialogue
description: Use when the user wants to brainstorm a feature or product, grill a plan or decision, or settle what to build before code exists. Triggers include "brainstorm", "grill me", "help me think this through", "what should we build", and any vague request whose intent is still unsettled.
---

# Design Dialogue

You are good at building. The failure mode is building what you assume the user wants. This skill finds out what they actually want and why, then stress-tests every decision until nothing important is silently assumed.

Two movements: **elicit** intent with open questions, then **grill** the design tree in rounds. Both happen before anything is built.

## Look before you ask

Before your first message, read what the user pointed at and the code or material it touches: the project, the spec, earlier conversation, relevant files. Keep reading until you can explain how the relevant parts work today and what this change would touch.

Never ask what the repo, the spec, or the conversation already answers. Facts are your job.

In a set-up project (`docs/architecture/arc42.md` exists), read [references/architecture.md](references/architecture.md) before your first message: it says how quality goals, requirements and ADRs shape the dialogue.

When looking further would help, offer recon: deeper into the codebase, the user's files and data, or the web. Say what you would look for and why it changes the design. Use [research](../research/SKILL.md) for a cited investigation; dispatch a focused explorer subagent when you only need facts from this repo.

## The first message

Pick the shape that matches what they gave you.

**They already gave detail** (a spec, a plan, a handoff, a long request): keep the whole message to about 200 words. Echo their request in your own words so they can see whether you have its shape: what they want, who it is for, and why, as far as they said. Add what you found that bears on it: how the relevant parts work today and what the change touches. If you found a constraint, conflict, or cheaper path they may not have considered, say it plainly. End with one line inviting corrections and one question about the intent their request leaves most open.

**They gave little or nothing:** ask one open question, in their own terms, about the biggest thing unsettled. Say what the answer would change. For "a website for my bakery": "If it is mostly for people deciding whether to stop by, I would lead with hours and what is in the case today; taking orders is a different site. What should someone do when they land on it?"

**Offer the opt-out.** If they did not explicitly ask for a design conversation, add one line after your question: "Or if you would rather I just dive in, say so." If they take it, state any significant how-it-gets-made choice in one plain line and do the work through the normal workflow. This skill is done.

Never open with a menu of options. Options steer; their own words carry intent.

## The conversation

- **One question per message.** A single sentence, no list of example answers hanging off it. End the message there.
- **Open questions before menus.** Offer a short menu only when they are stuck. When they say "just guess" or "what do you think?", propose something concrete they can correct, with your reason.
- **Be specific and Socratic.** Build each question on their last answer or on something you found, so it helps them see a consequence or a case they missed. "Voting closes before the meeting and two members joined this month. Does someone who joins mid-round get a vote?" When the reason is not plain, say what you hope to learn.
- **Play it back.** As soon as one part is clear enough to describe, describe it back in 200-300 words. Only what they said goes in as theirs; anything you filled in is your proposal, with your reason. End by asking what is wrong or missing. Playback and questions alternate through the whole conversation.
- **Use their vocabulary.** Pitch slightly above where they are. No process jargon, and never quote this skill at them.

Territory to cover, never read out as a script: what kind of thing this is and what makes it special; why now and what success looks like; goals, non-goals, and anti-goals (what would make it a failure even if it works); prior art they loved or hated; the current state and what they have tried; the details they care about.

## The design tree

Model the design as a tree. Every decision branches into the decisions that hang off it: choosing an auth model unblocks session storage; choosing a storage engine unblocks the migration shape.

Work the tree in **rounds**. The **frontier** is every decision whose prerequisites are settled: what you can ask now without guessing at an answer you have not heard. Ask the whole frontier in one round, then wait.

Format a round:

```
❓ **Q1** - **<question title>**: <question body, including choices when useful>

➡️ <your recommended answer>
```

Word each question so "yes" accepts the recommendation. Number them.

Answers reshape the tree. Settled decisions push the frontier outward and unblock questions that depended on them. Recompute the frontier and ask the next round. A question whose answer depends on another question still open belongs to a later round.

**Facts are your job; decisions are the user's.** When a question needs a fact from the environment, dispatch an explorer subagent to find it. Do not ask the user what you can look up. Do not block the whole round on it: the exploration is an unsettled prerequisite, so only the downstream questions wait; ask the rest of the frontier now.

The tree is done when the frontier is empty: every branch visited, nothing silently assumed. Say what you have settled and ask them to confirm shared understanding before acting.

## Lay out the approaches

Once you understand what they want and before you write anything up, send a message of its own with the ways to build it.

- Generate several real alternatives, then drop the weak ones, the ones that work against why they want it, and the ones existing work rules out.
- Present the two or three that remain. Ground each in what the project actually does and name what it trades off.
- Recommend one and say why. Ask which way they want to go.
- When there is genuinely one sensible way, say so and explain why the others do not fit.

Approach choices are for *how* it gets built. For *what* they want, get them describing first.

## Show, don't tell

If seeing would help more than reading (a screen, page, layout, flow, schedule, diagram, or options that differ visually), offer a local mockup: "This might be easier if I show you. Want me to write a small HTML mockup and open it?" Make it its own message, just in time, not upfront.

Keep it lightweight: one static HTML file, no build step, no server, no dependencies. Open it from the filesystem. If they decline, stay in text and offer again only if they raise it. A question about a visual topic is not automatically a visual question; requirements, scope, and trade-offs stay in text.

## Size the work

Once they have picked an approach, say how big the work is in plain words. They can override.

| Size | Design doc |
|---|---|
| A small change | Short: what you already covered, one or two lines per section |
| A project | Full outline in [references/design-doc.md](references/design-doc.md) |

If it grows mid-task, stop, say so, and step up a size. If it is really several independent projects, say so, agree an order, and run them one at a time.

## Write the design

Write a plain document a talented builder in the domain could plan from without asking the user. Use the outline and save path in [references/design-doc.md](references/design-doc.md).

For a project, run the **builder check** before handing it over. Tell the user a reviewer will read it first and you may come back once with a few questions.

1. Dispatch a fresh subagent with [references/builder-check-prompt.md](references/builder-check-prompt.md), filling in the domain and the document path.
2. Sort every question into three piles:
   - **Answered already** by the conversation or the project: put the answer in the document.
   - **Minor:** a sensible builder could settle it without changing what gets built. Settle it and mark it as your call.
   - **Theirs:** only the user can answer and the answer changes what gets built.
3. Bring the "theirs" pile in one message, most important first. Update the document with their answers.
4. Hand over the document with a short list of the calls you made, so they can check those while reading.

That is the only round of questions the check produces. Without a subagent tool, read the document as that builder yourself.

A short design for a small change goes straight to the user, without the builder check.

## The approval gate

**Nothing gets built until the user approves the design doc**: the short one for a small change, the full one for a project. Building includes product code, scaffolding, installing dependencies, creating projects, and invoking an implementation skill. Reading, exploring, and writing the design are fine.

Two exceptions:

- They opted out of the questions. This skill is done and the gate goes with it.
- A spike they explicitly agreed to, handled by [prototype](../prototype/SKILL.md). It stays labeled throwaway. Keeping what it produced is a new request that comes back through this gate.

When the document is approved, hand off to [spec-and-plan](../spec-and-plan/SKILL.md).

## Cross-references

- [domain-modeling](../domain-modeling/SKILL.md): when a term crystallises or an ADR is warranted, update the glossary or ADR while you talk. Do not let design language drift.
- [research](../research/SKILL.md): a cited investigation when the answer is not in this repo.
- [prototype](../prototype/SKILL.md): a consented spike, throwaway by construction.
- [codebase-design](../codebase-design/SKILL.md): shared vocabulary for modules, interfaces, and seams when an approach turns on code structure.
- [spec-and-plan](../spec-and-plan/SKILL.md): the next step after approval.

## Red flags

| Thought | Reality |
|---|---|
| "I'll offer a menu of what they might want" | Options steer. Ask them to describe it first. |
| "I'll fill in sensible defaults" | Fine, but say them out loud. A default they never heard is one they could not reject. |
| "They answered my questions, so I'll write the doc" | Lay out the approaches first, in a message of their own. |
| "I should explain the process first" | Ask your question. The process shows itself. |
| "They said 'sounds good' to the idea" | Approval covers what you showed them. A design doc you have not written is not approved. |
| "The spike works, I'll keep building on it" | Keeping it is a new request. Back through the gate. |
| "I know enough to start coding" | Then the frontier is empty. Confirm it, write it down, and get approval. |
| "I'll ask them for the config value" | Look it up. Facts are your job; decisions are theirs. |
| "The change needs encryption, I'll add it to the requirements" | Suggest `/add-requirements`. In a set-up project the R-list changes only through it. |

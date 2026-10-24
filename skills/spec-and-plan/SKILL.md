---
name: Spec and Plan
description: Use when the user wants to write a spec, turn a conversation into a spec, break a spec or plan into tickets, or write an implementation plan. Triggers include "write a spec", "write a plan", "break this into tickets", "turn this into tickets", and "plan this out".
---

# Spec and Plan

Turn an agreed design into three artifacts, in order. Produce only the ones the work needs.

| Artifact | Answers | Write it when |
|---|---|---|
| **Spec** | What are we building, for whom, and how will we know it works? | Intent is agreed but not written down, the work crosses sessions, or someone else will build or review it |
| **Tickets** | In what order, in what slices, and what blocks what? | The work spans more than one sitting or more than one agent, or you need to track progress |
| **Plan** | Exactly which files, names, signatures, and tests? | A multi-step implementation is about to start |

Spec first, then tickets, then a plan per ticket or per coherent group. A spec can go straight to a plan when the work is one slice. A one-line change needs neither.

Read `docs/agents/issue-tracker.md` if it exists; it says where this repo publishes. If the repo has no tracker configuration, run [setup-project-workflow](../setup-project-workflow/SKILL.md) or use the local forms below.

## 1. Write the spec

Synthesize; do not interview. Use what is already in the conversation and the codebase. If a real gap remains, state the assumption in the spec instead of inventing an answer or restarting the dialogue.

### Explore first

Read the code the feature touches, the project's `GLOSSARY.md`, and any ADRs in the area. Use the project's vocabulary. If the conversation produced new terms, update the glossary through [domain-modeling](../domain-modeling/SKILL.md) rather than inventing synonyms in the spec.

### Sketch the seams, then confirm

Before writing, identify where the feature will be tested. Use [codebase-design](../codebase-design/SKILL.md) language.

- Prefer an existing seam to a new one.
- Use the highest seam that can prove the behaviour.
- Propose new seams at the highest point you can.
- Fewer is better; the ideal number is one.

Show the seams to the user and get agreement before writing the spec. A wrong seam invalidates the testing decisions.

### Fill the template

Use [references/spec-template.md](references/spec-template.md). The shape:

- **Problem Statement** from the user's perspective.
- **Solution** from the user's perspective.
- **User Stories**: a long numbered list, `As an <actor>, I want <feature>, so that <benefit>`. Cover every aspect, including failure, permission, and empty states.
- **Implementation Decisions**: modules, interfaces, contracts, schema, interactions. No file paths or code snippets; they go stale. Exception: a prototype snippet that encodes a decision (state machine, reducer, schema, type shape), trimmed to the decision-rich parts.
- **Testing Decisions**: what makes a good test here (external behaviour, not internals), which modules, and prior art in the repo.
- **Out of Scope** and **Further Notes**.

### Publish

- **Configured tracker**: create one issue with the spec body and apply the `ready-for-agent` triage label unless the user says otherwise. If the source was an existing issue, publish as its sub-issue or follow the tracker doc.
- **No tracker**: write `docs/specs/YYYY-MM-DD-<topic>-spec.md` and commit it.
- Never close or rewrite a parent issue as part of publishing.

## 2. Break it into tickets

Tickets are **tracer bullets**: narrow but complete vertical slices through every layer, each demoable or verifiable on its own, each sized to one fresh context window. Not a horizontal slice of one layer.

Before slicing, look for **prefactor** work that makes the change easy, and take it first. "Make the change easy, then make the easy change."

Give every ticket its **blocking edges**: the tickets that must finish before it can start. No blockers means it can start now.

### Wide refactors are the exception

A wide refactor is one mechanical change (rename a column, retype a shared symbol) whose blast radius fans across the codebase, so no vertical slice lands green. Sequence it as **expand-contract**:

1. **Expand**: add the new form beside the old. Nothing breaks.
2. **Migrate**: move call sites in batches sized by blast radius (per package, per directory). Each batch is a ticket blocked by the expand, and CI stays green because the old form still exists.
3. **Contract**: delete the old form once no caller remains, blocked by every migrate batch.

When even the batches cannot stay green alone, keep the sequence but let them share an integration branch that all block a final integrate-and-verify ticket. Green is promised only there.

### Quiz the user

Present the breakdown as a numbered list. For each ticket show title, blocked by, and what it delivers end to end. Ask:

- Is the granularity right: too coarse or too fine?
- Does each ticket depend only on tickets that genuinely gate it?
- Should any be merged or split?

Iterate until they approve.

### Publish

- **Local files**: one file per ticket at `.scratch/<feature>/issues/<NN>-<slug>.md`, numbered from `01` in dependency order. Never one combined file. Use [references/ticket-template.md](references/ticket-template.md).
- **Tracker**: one issue per ticket, created in dependency order so blockers have real IDs. Use the platform's native blocking relationship where it has one, otherwise list blockers as text. If the source was an issue, make each ticket its sub-issue. Apply `ready-for-agent` unless told otherwise.

Work the frontier: any ticket whose blockers are done.

## 3. Write the plan

Write for an engineer who has not seen this codebase or this spec. They write idiomatic code once they know the exact interface and the exact test. They cannot know what you decided: which files, which names and signatures, which values from the spec, which tests prove each task. Document those.

Save to `docs/plans/YYYY-MM-DD-<feature>.md` unless the project prefers another path, and commit it.

### Scope and file structure

If the spec covers independent subsystems, write one plan per subsystem. Each plan should produce working, testable software on its own.

Map the files before defining tasks: what is created or modified, and what each one is responsible for. Prefer focused files with one responsibility. Split by responsibility, not by technical layer. Files that change together live together. Follow established patterns; if a file you touch has grown unwieldy, include a split in the plan.

### Right-size tasks and steps

A task is the smallest unit that carries its own test cycle and is worth a fresh reviewer's gate. Fold setup, configuration, scaffolding, and documentation into the task that needs them. Split only where a reviewer could reject one task while approving its neighbour. Every task ends with an independently testable deliverable.

Each step is one action with a checkable result:

1. Write the failing test.
2. Run it and see it fail.
3. Implement the minimal code.
4. Run it and see it pass.
5. Commit.

### Fill the template

Use [references/plan-template.md](references/plan-template.md). Required parts:

- **Header**: feature name, one-sentence goal, 2-3 sentence architecture, tech stack, path to the spec.
- **Global Constraints**: project-wide requirements copied verbatim from the spec, one line each: version floors, dependency limits, naming and copy rules, platform requirements. Every task implicitly includes this section.
- **Review Focus**: the five input classes or failure modes the spec implies but no task's tests exercise, most likely to bite first, one line each. The spec says what the software must do, not everything it will meet. Silence on an input is not permission for it to break. Write the list once with the spec in front of you, then add the test that pins each line to the task that owns the code.
- **File Structure**: the map above.
- **Tasks**: exact file paths under Files (Create/Modify/Test); Interfaces with **Consumes** (exact signatures from earlier tasks) and **Produces** (exact names and types later tasks rely on); then the steps.
- **Self-review** and **execution handoff** sections below.

### What a step contains

A step is done when the implementer can write exactly one reasonable thing from it. Unambiguous, not complete.

- **Test step**: the test's name and assertions as code, with the spec's exact values.
- **Code step**: the exact signature (name, parameters, return type), the file, and the specific values the spec pins. The implementer writes the body. Include a body only for an algorithm the signature and tests do not determine, or exact copy the spec fixes.
- **Verification step**: the command and the output that means it passed.
- **Reference to another task**: point at that task's Interfaces block; do not repeat its code.

A plan longer than the code it describes has written the code instead. Lines that decide nothing ("TBD", "handle edge cases", "add appropriate validation", "write tests for the above") are the opposite failure. The self-review catches both.

### Self-review

Run this yourself; do not dispatch it.

1. **Spec coverage**: point to a task for every spec section and requirement. Add missing tasks.
2. **Step scan**: every step allows exactly one reasonable action. No step is a transcript.
3. **Type consistency**: names, signatures, and properties in later tasks match earlier ones. `clearLayers()` in Task 3 and `clearFullLayers()` in Task 7 is a bug.
4. **Review Focus**: every listed failure mode has a test in the task that owns the code. An empty section means you checked, not that you skipped.
5. **Proportion**: compare plan length to spec length. If code blocks dominate, replace bodies with signatures and test names. Fix inline and move on.

### Hand off

Link the plan and ask the user to review it and confirm it captures what they want before implementation. If they already chose an execution method, respect it; otherwise ask them to choose the mode [executing-plans](../executing-plans/SKILL.md) offers, with a one-sentence recommendation based on task coupling, task count, and the cost of a shipped mistake.

Wait for approval, then invoke [executing-plans](../executing-plans/SKILL.md). Implementation follows the plan task by task with [test-driven-development](../test-driven-development/SKILL.md).

## When to skip

- **One-line change**: no spec, no tickets, no plan. Do it and say what you did.
- **One slice, one sitting, one agent**: the spec may be enough. Skip tickets.
- **Design still unsettled**: go back to [design-dialogue](../design-dialogue/SKILL.md). Do not speculate in the spec.

## Red flags

| Thought | Reality |
|---|---|
| "I'll interview the user for the spec" | No. Synthesize the conversation. Interview is design-dialogue. |
| "I'll pick the seams while writing" | Confirm seams first. They decide the testing decisions. |
| "I'll skip tickets, the plan covers it" | Then say so. Tickets exist to expose order and blocking risk. |
| "Plans can leave the file names open" | The implementer cannot know them. Name every file. |
| "I'll describe the algorithm line by line" | Only when the signature and tests do not determine it. |
| "The plan is long, so it is thorough" | Longer than the spec means it wrote the code. |

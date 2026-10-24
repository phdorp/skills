# Design Document

A design document is what a talented builder in the domain reads to plan the work without going back to the user. Write for that person, not for a process reviewer.

## Where it goes

Default to `docs/specs/YYYY-MM-DD-<topic>-design.md` in a software repo, and commit it. Use the date the design was agreed.

The project's preference overrides the default. Check, in order:

1. A path named in `docs/agents/` configuration or the repo's `AGENTS.md`.
2. An existing `docs/specs/` or `docs/design/` convention.
3. The default above.

Outside a software repo, ask where the user keeps documents.

## Two sizes

**Short form, for a small change.** One or two lines per section. It records what the conversation already settled and goes straight to the user for approval. No builder check.

**Full form, for a project.** Every section below, written for a builder who was not in the conversation. Run the builder check before handing it over.

If the work grows while you are writing, stop, say so, and move up a size.

## Outline

### Intent and why

What this is, who it serves, and what changes for them. The why, in the user's terms. Include the trigger: why now, and what happens if nothing is built.

### Goals

What success looks like, stated so someone could tell whether it was reached. Prefer observable outcomes over activities.

### Non-goals

Things a reasonable reader might expect to be included but are not. Naming them prevents scope creep and wrong assumptions.

### Anti-goals

What would make this a failure even if it technically works: wrong audience, wrong tone, a workflow that is slower than the status quo, a dependency the user does not want.

### Constraints

Fixed points the builder cannot trade away:

- platforms, versions, languages, and frameworks already in use
- deadlines, budgets, and team size
- data, privacy, compliance, and access limits
- compatibility with existing users, files, or APIs
- decisions already made elsewhere (ADRs, contracts, house style)

Give exact values where they exist.

### Approaches

The two or three real alternatives considered, grounded in what the project actually does. For each: the shape of the solution and what it trades off. State which one the user picked and why.

Drop alternatives that were weak, worked against the intent, or were ruled out by existing work. If there was genuinely one sensible way, say so and explain why the others did not fit.

### Decisions

The parts of the how that the user decided, in the words they decided them. Include the smaller calls you made and marked as yours, each with its reason. A builder should be able to tell which decisions are fixed and which are theirs to make.

Do not include a task list. The plan comes later.

### What is left to the builder

The choices you deliberately did not make, and the boundaries within which the builder may make them. Say what would require coming back to the user.

## Writing rules

- Plain language. No process jargon, no restating of this outline as headings with no content.
- Decisions, not options. An approach section records the choice; it does not reopen it.
- Exact values over adjectives. "Postgres 16, Node 22" beats "modern stack".
- No implementation transcript. File names and signatures belong in the plan.
- Only what the user said goes in as theirs. Your inferences carry your reason.
- Short enough to read in one sitting at the size chosen.

## Checklist before handover

- [ ] Intent, goals, non-goals, and anti-goals are all present and distinguishable.
- [ ] Constraints carry exact values.
- [ ] Approaches names the alternatives, the trade-offs, the pick, and the reason.
- [ ] Decisions separate the user's calls from yours.
- [ ] "Left to the builder" is explicit, including when to come back.
- [ ] Nothing in the document depends on having been in the conversation.

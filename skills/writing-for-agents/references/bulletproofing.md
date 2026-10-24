# Bulletproofing against rationalization

Part of [`writing-for-agents`](../SKILL.md). Use it when the baseline failure is a discipline failure: the agent knows the rule and skips it under pressure.

This toolkit covers discipline failures only. For output with the wrong shape (a bloated prompt, a buried verdict, a restated spec) or an omitted element, prohibition-based bulletproofing backfires; use the forms in `SKILL.md` under "Match the form to the failure".

The psychology behind these patterns is in [persuasion-principles.md](persuasion-principles.md): authority, commitment, and social proof raise compliance in LLM conversations, and they work because the model was trained on human text in which those patterns precede or accompany compliance.

## Close every loophole explicitly

State the rule, then forbid the specific workarounds the baseline produced. A bare rule invites a negotiation; named workarounds remove the exit.

```markdown
Write code before the test? Delete it. Start over.

No exceptions:
- Don't keep it as "reference"
- Don't adapt it while writing the test
- Don't look at it
- Delete means delete
```

Every line there answers a rationalization observed in a real run. Add lines the same way: from the transcript, not from imagination.

## Address spirit-versus-letter arguments

Put the principle early, before the specific rules:

```markdown
Violating the letter of the rules is violating the spirit of the rules.
```

That single line retires a whole class of "I followed the intent" arguments, and it costs one sentence. It belongs at the top of a discipline skill, not in a footnote.

## Build the rationalization table

Every excuse an agent makes during baseline testing goes into a two-column table: the excuse in the agent's words, the reality in one line.

```markdown
| Excuse | Reality |
|---|---|
| "Too simple to test" | Simple code breaks. The test takes 30 seconds. |
| "I'll test after" | Tests that pass immediately prove nothing. |
| "Tests after achieve the same goals" | Tests-after ask "what does this do?"; tests-first ask "what should this do?" |
| "Keep it as reference" | You will adapt it. That is testing after. Delete means delete. |
```

Guidelines:

- Quote the excuse verbatim. Paraphrase blunts the counter.
- Answer the strongest version of the excuse, not a strawman.
- One row per distinct excuse. Two rows that differ only in wording are one rationalization.
- A row the agent never made is speculation; leave it out until a run produces it.

## Create a red-flags list

A red-flags list lets an agent catch itself mid-rationalization. It is a short list of the exact phrases and moves that precede a violation.

```markdown
## Red flags — stop and start over

- Code before test
- "I already manually tested it"
- "Tests after achieve the same purpose"
- "It's about spirit, not ritual"
- "This case is different because…"

All of these mean: delete the code, start over with TDD.
```

End the list with the action, not just the diagnosis. Naming the flag without naming the response leaves the agent to negotiate at the moment it is least able to.

## Put the symptom in the pointer

The description is read before the body, so it can catch the agent at the moment of temptation:

```yaml
description: Use when implementing any feature or bugfix, before writing implementation code; also when tempted to test after the fact or when manual testing feels faster.
```

Trigger branches, including the about-to-violate ones, not a summary of the rules.

## Calibrate the strength

Absolute framing ("never", "no exceptions", "every") removes the "is this an exception?" decision, and a discipline skill usually needs it. Two cautions:

- Reserve it for rules you will defend. An absolute that the agent can see is unreasonable loses authority for the whole document.
- Pair a prohibition with its positive target: say what to do, then name the banned workaround. The positive carries the behaviour; the prohibition closes the exit.

Do not escalate every sentence to uppercase. Emphasis is a budget: spend it on the one rule whose violation motivated the skill, and the rest reads normally.

## Verify the bulletproofing

1. Re-run the same pressure scenario with the updated skill.
2. Check the agent picks the right option and cites the new section.
3. Ask the meta-test question: "How could the skill have made this clearer?"
4. If a new rationalization appears, add one counter, and re-run.

The skill is bulletproof for that scenario when reps converge, the agent cites the rule, and the meta-test returns "the skill was clear". A different scenario may still break it; that is the next test, not a reason to add counters preemptively.

## Anti-patterns

- **Counter-everything**: a wall of prohibitions reads as noise and dilutes the one rule that matters.
- **Nuance clauses**: "don't X unless it matters" reopens the negotiation. Express a real exception as its own conditional on an observable predicate.
- **Exemption clauses that do not scope**: "this limit does not apply to code blocks" still suppresses code blocks. Restructure so the rule cannot reach the exempt case.
- **Vague counters**: "don't cheat" is not a counter; "don't keep it as reference" is.
- **Untested tables**: rationalization rows invented at the desk tend to answer objections no agent actually makes, while the real one goes unaddressed.
